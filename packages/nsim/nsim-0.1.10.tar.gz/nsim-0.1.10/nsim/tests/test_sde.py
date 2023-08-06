"""An empty file where tests should be
"""

import pytest
from nsim import sde
import numpy as np

tspan = np.arange(0.0, 1000.0, 0.005)

def test_mismatched_f():
    y0 = np.zeros(3)
    f = lambda y, t: np.array([1.0, 2.0, 3.0, 4.0])
    G = lambda y, t: np.ones((3, 3))
    with pytest.raises(sde.SDEValueError):
        y = sde.sodeint(f, G, y0, tspan)

# Testing non-deterministic software. What's the best way to do that?
# (the tests below will occasionally fail when the code is correct)

def test_integrate_1D():
    y0 = 0.0;
    f = lambda y, t: -1.0 * y
    G = lambda y, t: 0.2
    y = sde.sodeint(f, G, y0, tspan)
    assert(np.isclose(np.mean(y), 0.0, rtol=0, atol=1e-02))
    assert(np.isclose(np.var(y), 0.2*0.2/2, rtol=1e-01, atol=0))

def test_integrate_ND():
    y0 = np.zeros(3)
    def f(y, t):
        return np.array([ -1.0*y[0], 
                          y[2], 
                          -1.0*y[1] - 0.4*y[2] ])
    def G(y, t): 
        return np.diag([0.2, 0.0, 0.5])
    y = sde.sodeint(f, G, y0, tspan)
    w = np.fft.rfft(y[:, 2])
    # TODO assert spectral peak is around 1.0 radians/s
