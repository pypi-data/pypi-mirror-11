"""
.. module:: rbf_surfaces
   :synopsis: RBF interpolation surfaces
.. moduleauthor:: David Bindel <bindel@cornell.edu>

:Module: rbf_surfaces
:Author: David Bindel <bindel@cornell.edu>
"""


import numpy as np
import scipy.linalg as la
from rbf_base import SimpleRBFSystem
from rbf_base import SimpleRBFSurface


class LinearRBFSystem(SimpleRBFSystem):
    """Linear RBF system"""

    dpoly = 1

    def phi(self, r):
        return r

    def dphi_div_r(self, r):
        return (r*0 + 1)/r


class CubicRBFSystem(SimpleRBFSystem):
    """Cubic RBF system"""

    dpoly = 2

    def phi(self, r):
        return r ** 3

    def dphi_div_r(self, r):
        return 3 * r


class ThinPlateRBFSystem(SimpleRBFSystem):
    """Thin plate RBF system"""

    dpoly = 2
    eps = np.finfo(np.double).tiny

    def phi(self, r):
        return r * r * np.log(r+self.eps)

    def dphi_div_r(self, r):
        return 2 * np.log(r+self.eps) + 1


class LinearRBFSurface(SimpleRBFSurface):
    RBFSystem = LinearRBFSystem


class CubicRBFSurface(SimpleRBFSurface):
    RBFSystem = CubicRBFSystem


class TPSSurface(SimpleRBFSurface):
    RBFSystem = ThinPlateRBFSystem


def toyf(x):
    if len(x.shape) == 1:
        return np.cos(2*x[0] + np.cos(3*x[1]))
    else:
        return np.cos(2*x[:, 0] + np.cos(3*x[:, 1]))


def fd_grad(f, x, h=1e-6):
    df = np.zeros(x.shape)
    xp = x.copy()
    for j in range(x.shape[0]):
        xp[j] = x[j]+h
        fp = f(xp)
        xp[j] = x[j]-h
        fm = f(xp)
        xp[j] = x[j]
        df[j] = (fp-fm)/2/h
    return df


def test_evals(RBFSurface=CubicRBFSurface):
    npts = 5
    x = np.random.random((npts, 2))
    fx = toyf(x)
    s = RBFSurface(x, fx)
    sx = s.eval(x)
    relerr = la.norm(sx-fx)/la.norm(fx)
    assert relerr < 1e-8, "Surface inconsistency: {0:.1e}".format(relerr)


def test_surface(RBFSurface=CubicRBFSurface):
    npts = 5
    x = np.random.random((npts, 2))
    y = np.random.random((2,))
    s = RBFSurface(x, toyf(x))
    dg = s.deriv(y)
    dg_fd = fd_grad(s.eval, y)
    relerr = la.norm(dg-dg_fd)/la.norm(dg)
    assert relerr < 1e-8, "Surface inconsistency: {0:.1e}".format(relerr)


def test_seminorm(RBFSurface=CubicRBFSurface):
    npts = 5
    y = np.random.random((2,))
    x0 = np.random.random((npts, 2))
    x1 = np.zeros((npts+1, 2))
    x1[:-1, :] = x0
    x1[-1, :] = y
    s0 = RBFSurface(x0, toyf(x0))
    s1 = RBFSurface(x1, toyf(x1))
    gref = s1.seminorm()-s0.seminorm()
    g = s0.dseminorm(y, s1.fx[-1])[0]
    relerr = np.abs(g-gref)/gref
    assert relerr < 1e-8, "Seminorm inconsistency: {0:.1e}".format(relerr)


def test_seminorm1(RBFSurface=CubicRBFSurface):
    npts = 5
    x = np.random.random((npts, 2))
    y = np.random.random((2,))
    s = RBFSurface(x, toyf(x))
    g, dg = s.dseminorm(y, toyf(y))
    ns0 = s.seminorm()
    s.add_points(y, toyf(y))
    ns1 = s.seminorm()
    gref = ns1-ns0
    relerr = np.abs(g-gref)/gref
    assert relerr < 1e-8, "Seminorm inconsistency: {0:.1e}".format(relerr)


def test_gutmann(RBFSurface=CubicRBFSurface):
    npts = 5
    tau = -1
    x = np.random.random((npts, 2))
    y = np.random.random((2,))
    s = RBFSurface(x, toyf(x))
    g, dg = s.dseminorm(y, tau)
    dg_fd = fd_grad(lambda y: s.dseminorm(y, tau)[0], y)
    relerr = la.norm(dg-dg_fd)/la.norm(dg)
    assert relerr < 1e-8, "Gutmann merit inconsistency: {0:.1e}".format(relerr)
    h, dh = s.diseminorm(y, tau)
    dh_fd = fd_grad(lambda y: s.diseminorm(y, tau)[0], y)
    relerr = la.norm(dh-dh_fd)/la.norm(dh)
    assert relerr < 1e-8, "Gutmann merit inconsistency: {0:.1e}".format(relerr)


if __name__ == "__main__":
    classes = [CubicRBFSurface, TPSSurface, LinearRBFSurface]
    for c in classes:
        test_evals(c)
        test_surface(c)
        test_seminorm(c)
        test_seminorm1(c)
        test_gutmann(c)
