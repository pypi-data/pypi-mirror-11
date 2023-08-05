import numpy
import six

from chainer import cuda
from chainer import function
from chainer.utils import type_check


def _extract_gates(x):
    r = x.reshape((x.shape[0], x.shape[1] / 4, 4) + x.shape[2:])
    return (r[:, :, i] for i in six.moves.range(4))


def _sigmoid(x):
    return 1 / (1 + numpy.exp(-x))


def _grad_sigmoid(x):
    return x * (1 - x)


def _grad_tanh(x):
    return 1 - x * x

_preamble = '''
__device__ float sigmoid(float x)      { return 1 / (1 + __expf(-x)); }
__device__ float grad_sigmoid(float y) { return y * (1 - y); }
__device__ float grad_tanh(float y)    { return 1 - y * y; }

#define COMMON_ROUTINE \
    int I = i / rsize; \
    int J = i % rsize; \
    const float* x_i = x + I * 4 * rsize; \
    float aa =   tanhf(x_i[          J]); \
    float ai = sigmoid(x_i[  rsize + J]); \
    float af = sigmoid(x_i[2*rsize + J]); \
    float ao = sigmoid(x_i[3*rsize + J]);
'''


class LSTM(function.Function):

    """Long short-term memory unit with forget gate.

    It has two inputs (c, x) and two outputs (c, h), where c indicates the cell
    state. x must have four times channels compared to the number of units.

    """

    def check_type_forward(self, in_types):
        type_check.expect(in_types.size() == 2)
        c_type, x_type = in_types

        type_check.expect(
            c_type.dtype == numpy.float32,
            x_type.dtype == numpy.float32,

            c_type.ndim >= 2,
            x_type.ndim >= 2,
            c_type.ndim == x_type.ndim,

            x_type.shape[0] == c_type.shape[0],
            x_type.shape[1] == 4 * c_type.shape[1],
        )
        for i in range(2, c_type.ndim.eval()):
            type_check.expect(x_type.shape[i] == c_type.shape[i])

    def forward_cpu(self, inputs):
        c_prev, x = inputs

        a, i, f, o = _extract_gates(x)
        self.a = numpy.tanh(a)
        self.i = _sigmoid(i)
        self.f = _sigmoid(f)
        self.o = _sigmoid(o)

        self.c = self.a * self.i + self.f * c_prev
        h = self.o * numpy.tanh(self.c)
        return self.c, h

    def backward_cpu(self, inputs, grad_outputs):
        c_prev = inputs[0]
        gc, gh = grad_outputs

        gx = numpy.empty_like(inputs[1])
        ga, gi, gf, go = _extract_gates(gx)

        # Consider the case that either gradient is not given
        if gc is None:
            gc = 0
        if gh is None:
            gh = 0

        co = numpy.tanh(self.c)
        gc_prev = gh * self.o * _grad_tanh(co) + gc  # multiply f later
        ga[:] = gc_prev * self.i * _grad_tanh(self.a)
        gi[:] = gc_prev * self.a * _grad_sigmoid(self.i)
        gf[:] = gc_prev * c_prev * _grad_sigmoid(self.f)
        go[:] = gh * co * _grad_sigmoid(self.o)
        gc_prev *= self.f  # multiply f here

        return gc_prev, gx

    def forward_gpu(self, inputs):
        c_prev, x = inputs
        lsize = c_prev.shape[0] * c_prev.shape[1]
        rsize = c_prev.size // lsize

        self.c = cuda.empty_like(c_prev)
        h = cuda.empty_like(c_prev)
        cuda.elementwise(
            '''float* c, float* h, const float* c_prev, const float* x,
               int lsize, int rsize''',
            '''COMMON_ROUTINE;
               c[i] = aa * ai + af * c_prev[i];
               h[i] = ao * tanhf(c[i]);''',
            'lstm_fwd', preamble=_preamble)(self.c, h, c_prev, x, lsize, rsize)

        return self.c, h

    def backward_gpu(self, inputs, grad_outputs):
        c_prev, x = inputs
        gc, gh = grad_outputs
        lsize = c_prev.shape[0] * c_prev.shape[1]
        rsize = c_prev.size // lsize

        # Odd rule to determine whether the gradient is given or not.
        if gc is None:
            gc = self.c
        if gh is None:
            gh = self.c

        gc_prev = cuda.empty_like(c_prev)
        gx = cuda.empty_like(x)
        cuda.elementwise(
            '''
               float* gc_prev, float* gx, const float* c_prev, const float* x,
               const float* c, const float* gc, const float* gh, int lsize,
               int rsize
            ''', '''
               COMMON_ROUTINE;
               float* gx_i = gx + I * 4 * rsize;
               float& ga = gx_i[          J];
               float& gi = gx_i[  rsize + J];
               float& gf = gx_i[2*rsize + J];
               float& go = gx_i[3*rsize + J];

               float co  = tanhf(c[i]);
               // Odd rule: if gh == c [gc == c] then gh [gc] is not given,
               // since we cannot pass null pointer to the kernel through
               // PyCUDA.
               float gc1 = (gh == c ? 0 : gh[i] * ao * grad_tanh(co))
                         + (gc == c ? 0 : gc[i]);
               go        =  gh == c ? 0 : gh[i] * co * grad_sigmoid(ao);

               gc_prev[i] = gc1 * af;
               ga         = gc1 * ai        * grad_tanh(aa);
               gi         = gc1 * aa        * grad_sigmoid(ai);
               gf         = gc1 * c_prev[i] * grad_sigmoid(af);
            ''',
            'lstm_bwd', preamble=_preamble)(
                gc_prev, gx, c_prev, x, self.c, gc, gh, lsize, rsize)

        return gc_prev, gx


def lstm(c_prev, x):
    """Long Short-Term Memory units as an activation function.

    This function implements LSTM units with forget gates. Let the previous
    cell state :math:`c_{\\text{prev}}` and the incoming signal :math:`x`.

    First, the incoming signal :math:`x` is split into four arrays
    :math:`a, i, f, o` of the same shapes along the second axis.
    It means that :math:`x` 's second axis must have 4 times the length of
    :math:`c_{\\text{prev}}`.

    The splitted input signals are corresponding to:

        - :math:`a` : sources of cell input
        - :math:`i` : sources of input gate
        - :math:`f` : sources of forget gate
        - :math:`o` : sources of output gate

    Second, it computes outputs as:

    .. math::

        c &= \\tanh(a) \\text{sigmoid}(i)
           + c_{\\text{prev}} \\text{sigmoid}(f), \\\\
        h &= \\tanh(c) \\text{sigmoid}(o).

    These are returned as a tuple of two variables.

    Args:
        c_prev (~chainer.Variable): Variable that holds the previous cell
            state. The cell state should be a zero array or the output of the
            previous call of LSTM.
        x (~chainer.Variable): Variable that holds the incoming signal. It must
            have the second dimension four times of that of the cell state,

    Returns:
        tuple: Two :class:`~chainer.Variable` objects ``c`` and ``h``. ``c`` is
            the updated cell state. ``h`` indicates the outgoing signal.

    See the original paper proposing LSTM with forget gates:
    `Long Short-Term Memory in Recurrent Neural Networks \
    <http://www.felixgers.de/papers/phd.pdf>`_.

    .. admonition:: Example

        Assuming ``y`` is the current input signal, ``c`` is the previous cell
        state, and ``h`` is the previous output signal from an ``lstm``
        function. Each of ``y``, ``c`` and ``h`` has ``n_units`` channels.
        Most typical preparation of ``x`` is:

        >>> model = FunctionSet(w=F.Linear(n_units, 4 * n_units),
        ...                     v=F.Linear(n_units, 4 * n_units),
        ...                     ...)
        >>> x = model.w(y) + model.v(h)
        >>> c, h = F.lstm(c, x)

        It corresponds to calculate the input sources :math:`a, i, f, o` from
        the current input ``y`` and the previous output ``h``. Different
        parameters are used for different kind of input sources.

    """
    return LSTM()(c_prev, x)
