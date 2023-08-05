"""
A class hierarchy relating to fields of all kinds.
"""
from __future__ import print_function, division
import numpy as np
from ciabatta import lattice, field_numerics, walled_field_numerics
from ciabatta.meta import make_repr_str


class Space(object):

    def __init__(self, L, dim):
        self.L = L
        self.dim = dim

    @property
    def L_half(self):
        return self.L / 2.0

    @property
    def A(self):
        return self.L ** self.dim

    def iterate(self, *args, **kwargs):
        pass

    def __repr__(self):
        fs = [('L', self.L), ('dim', self.dim)]
        return make_repr_str(self, fs)


class Field(Space):

    def __init__(self, L, dim, dx):
        Space.__init__(self, L, dim)
        self.M = int(round(self.L / dx))

    @property
    def dx(self):
        return self.L / self.M

    @property
    def A_i(self):
        return self.M ** self.dim

    @property
    def dA(self):
        return self.dx ** self.dim

    def density_field(self, r):
        return density(r, self.L, self.dx)

    def r_to_i(self, r):
        return lattice.r_to_i(r, self.L, self.dx)

    def i_to_r(self, i):
        return lattice.i_to_r(i, self.L, self.dx)

    def __repr__(self):
        fs = [('L', self.L), ('dim', self.dim), ('dx', self.dx)]
        return make_repr_str(self, fs)


class Scalar(Field):

    def __init__(self, L, dim, dx, a_0=0.0):
        Field.__init__(self, L, dim, dx)
        self.a = np.ones(self.dim * (self.M,), dtype=np.float) * a_0

    def grad(self):
        return _grad(self.a, self.dx)

    def grad_i(self, r):
        return _grad_i(self.a, self.r_to_i(r), self.dx)

    def laplacian(self):
        return _laplace(self.a, self.dx)

    def __repr__(self):
        fs = [('L', self.L), ('dim', self.dim), ('dx', self.dx),
              ('a_0', self.a_0)]
        return make_repr_str(self, fs)


class Diffusing(Scalar):

    def __init__(self, L, dim, dx, D, dt, a_0=0.0):
        Scalar.__init__(self, L, dim, dx, a_0=a_0)
        self.D = D
        self.dt = dt

        if self.D > self.dx ** 2 / (2.0 * self.dim * self.dt):
            raise Exception('Unstable diffusion constant')

    def iterate(self):
        self.a += self.D * self.laplacian() * self.dt

    def __repr__(self):
        fs = [('L', self.L), ('dim', self.dim), ('dx', self.dx),
              ('D', self.D), ('dt', self.dt), ('a_0', self.a_0)]
        return make_repr_str(self, fs)


class WalledScalar(Scalar):

    def __init__(self, L, dim, dx, walls, a_0=0.0):
        Scalar.__init__(self, L, dim, dx, a_0=a_0)
        self.walls = walls
        # Make field zero-valued where obstructed
        self.a *= np.logical_not(self.walls)

    def grad(self):
        return _walled_grad(self.a, self.dx, self.walls)

    def grad_i(self, r):
        return _walled_grad_i(self.a, self.r_to_i(r), self.dx,
                              self.walls)

    def laplacian(self):
        return _walled_laplace(self.a, self.dx, self.walls)

    def __repr__(self):
        fs = [('L', self.L), ('dim', self.dim), ('dx', self.dx),
              ('walls', self.walls), ('a_0', self.a_0)]
        return make_repr_str(self, fs)


# Note, inheritance order matters to get walled grad & laplacian call
# (see diamond problem on wikipedia and how python handles it)
class WalledDiffusing(WalledScalar, Diffusing):

    def __init__(self, L, dim, dx, walls, D, dt, a_0=0.0):
        Diffusing.__init__(self, L, dim, dx, D, dt, a_0=a_0)
        WalledScalar.__init__(self, L, dim, dx, walls, a_0=a_0)

    def __repr__(self):
        fs = [('L', self.L), ('dim', self.dim), ('dx', self.dx),
              ('walls', self.walls), ('D', self.D), ('dt', self.dt),
              ('a_0', self.a_0)]
        return make_repr_str(self, fs)


def density(r, L, dx):
    assert r.ndim == 2
    M = int(round(L / dx))
    dx = L / M
    inds = lattice.r_to_i(r, L, dx)
    f = np.zeros(r.shape[1] * (M,), dtype=np.int)
    if f.ndim == 1:
        field_numerics.density_1d(inds, f)
    elif f.ndim == 2:
        field_numerics.density_2d(inds, f)
    elif f.ndim == 3:
        field_numerics.density_3d(inds, f)
    else:
        raise Exception('Density calc not implemented in this dimension')
    return f / dx ** r.shape[1]


def _laplace(field, dx):
    assert dx > 0.0
    laplace = np.empty_like(field)
    if field.ndim == 1:
        field_numerics.laplace_1d(field, laplace, dx)
    elif field.ndim == 2:
        field_numerics.laplace_2d(field, laplace, dx)
    elif field.ndim == 3:
        field_numerics.laplace_3d(field, laplace, dx)
    else:
        raise Exception('Laplacian not implemented in this dimension')
    return laplace


def _grad_i(field, inds, dx):
    assert dx > 0.0
    assert inds.ndim == 2
    assert field.ndim == inds.shape[1]
    grad_i = np.empty(inds.shape, dtype=field.dtype)
    if field.ndim == 1:
        field_numerics.grad_i_1d(field, inds, grad_i, dx)
    elif field.ndim == 2:
        field_numerics.grad_i_2d(field, inds, grad_i, dx)
    elif field.ndim == 3:
        field_numerics.grad_i_3d(field, grad_i, dx)
    else:
        raise Exception("Grad_i not implemented in this dimension")
    return grad_i


def _grad(field, dx):
    assert dx > 0.0
    grad = np.empty(field.shape + (field.ndim,), dtype=field.dtype)
    if field.ndim == 1:
        field_numerics.grad_1d(field, grad, dx)
    elif field.ndim == 2:
        field_numerics.grad_2d(field, grad, dx)
    elif field.ndim == 3:
        field_numerics.grad_3d(field, grad, dx)
    else:
        raise Exception('Grad not implemented in this dimension')
    return grad


def _div(field, dx):
    assert dx > 0.0
    div = np.empty(field.shape[:-1], dtype=field.dtype)
    if field.ndim == 2:
        field_numerics.div_1d(field, div, dx)
    elif field.ndim == 3:
        field_numerics.div_2d(field, div, dx)
    elif field.ndim == 4:
        field_numerics.div_3d(field, div, dx)
    else:
        raise Exception('Divergence not implemented in this dimension')
    return div


def _walled_grad(field, dx, walls):
    assert field.shape == walls.shape
    assert dx > 0.0
    grad = np.empty(field.shape + (field.ndim,), dtype=field.dtype)
    if field.ndim == 1:
        walled_field_numerics.grad_1d(field, grad, dx, walls)
    elif field.ndim == 2:
        walled_field_numerics.grad_2d(field, grad, dx, walls)
    elif field.ndim == 3:
        walled_field_numerics.grad_3d(field, grad, dx, walls)
    else:
        raise Exception("Walled grad not implemented in this dimension")
    return grad


def _walled_grad_i(field, inds, dx, walls):
    assert field.shape == walls.shape
    assert dx > 0.0
    assert inds.ndim == 2
    assert field.ndim == inds.shape[1]
    grad_i = np.empty(inds.shape, dtype=field.dtype)
    if field.ndim == 1:
        walled_field_numerics.grad_i_1d(field, inds, grad_i, dx, walls)
    elif field.ndim == 2:
        walled_field_numerics.grad_i_2d(field, inds, grad_i, dx, walls)
    elif field.ndim == 3:
        walled_field_numerics.grad_i_3d(field, inds, grad_i, dx, walls)
    else:
        raise Exception("Walled Grad_i not implemented in this dimension")
    return grad_i


def _walled_laplace(field, dx, walls):
    assert field.shape == walls.shape
    assert dx > 0.0
    laplace = np.empty_like(field)
    if field.ndim == 1:
        walled_field_numerics.laplace_1d(field, laplace, dx, walls)
    elif field.ndim == 2:
        walled_field_numerics.laplace_2d(field, laplace, dx, walls)
    elif field.ndim == 3:
        walled_field_numerics.laplace_3d(field, laplace, dx, walls)
    else:
        raise Exception('Laplacian not implemented in this dimension')
    return laplace
