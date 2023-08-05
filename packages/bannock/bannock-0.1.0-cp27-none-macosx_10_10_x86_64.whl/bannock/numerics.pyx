import numpy as np
from ciabatta import vector
cimport numpy as np
cimport cython
from libc.math cimport sin, cos


@cython.cdivision(True)
@cython.boundscheck(False)
def vicsek_inters(np.ndarray[np.float_t, ndim=2] v,
                  np.ndarray[int, ndim=2] inters,
                  np.ndarray[int, ndim=1] intersi):
    cdef:
        unsigned int i_1, i_i_2, i_dim
        np.ndarray[np.float_t, ndim=2] v_vic = v.copy()

    for i_1 in range(v.shape[0]):
        for i_i_2 in range(intersi[i_1]):
            for i_dim in range(v.shape[1]):
                v_vic[i_1, i_dim] += v[inters[i_1, i_i_2] - 1, i_dim]
    return vector.vector_unit_nullnull(v_vic) * vector.vector_mag(v)[:, np.newaxis]


@cython.cdivision(True)
@cython.boundscheck(False)
def vicsek_1d(np.ndarray[np.float_t, ndim=1] r,
              np.ndarray[np.int_t, ndim=1] u,
              double r_v, double L):
    cdef:
        unsigned int i_1, i_2
        np.ndarray[np.int_t, ndim=1] u_vic = np.zeros([u.shape[0]], dtype=np.int)
        double dr

    for i_1 in range(u.shape[0]):
        for i_2 in range(u.shape[0]):
            dr = abs(r[i_1] - r[i_2])
            dr = min(dr, L - dr)
            if dr < r_v:
                u_vic[i_1] += u[i_2]
        if u_vic[i_1] > 0:
            u_vic[i_1] = 1
        elif u_vic[i_1] < 0:
            u_vic[i_1] = -1
        else:
            u_vic[i_1] = 0
    return u_vic


@cython.cdivision(True)
@cython.boundscheck(False)
def rot_diff_2d(np.ndarray[np.float_t, ndim=2] v, double D, double dt):
    cdef:
        unsigned int i
        np.ndarray[np.float_t, ndim=1] th = np.random.normal(scale=np.sqrt(2.0 * D * dt), size=v.shape[0])
        np.ndarray[np.float_t, ndim=2] v_rot = np.empty((v.shape[0], v.shape[1]))
        double cos_th, sin_th

    for i in range(v.shape[0]):
        cos_th = cos(th[i])
        sin_th = sin(th[i])
        v_rot[i, 0] = cos_th * v[i, 0] - sin_th * v[i, 1]
        v_rot[i, 1] = sin_th * v[i, 0] + cos_th * v[i, 1]
    return v_rot
