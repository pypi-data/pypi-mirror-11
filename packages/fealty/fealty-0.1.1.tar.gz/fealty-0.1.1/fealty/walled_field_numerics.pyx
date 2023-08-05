import numpy as np
cimport numpy as np
cimport cython


cdef unsigned int wrap_inc(unsigned int M, unsigned int i):
    return i + 1 if i < M - 1 else 0


cdef unsigned int wrap_dec(unsigned int M, unsigned int i):
    return i - 1 if i > 0 else M - 1


@cython.cdivision(True)
@cython.boundscheck(False)
def grad_1d(np.ndarray[np.float_t, ndim=1] field,
            np.ndarray[np.float_t, ndim=2] grad,
            double dx,
            np.ndarray[np.uint8_t, ndim=1] walls):
    cdef:
        unsigned int i_x, i_inc, i_dec
        unsigned int M_x = walls.shape[0]
        np.float_t dx_double = 2.0 * dx, interval

    for i_x in range(M_x):
        if not walls[i_x]:
            i_inc = wrap_inc(M_x, i_x)
            i_dec = wrap_dec(M_x, i_x)

            interval = dx_double
            if walls[i_inc]:
                i_inc = i_x
                interval = dx
            if walls[i_dec]:
                i_dec = i_x
                interval = dx

            grad[i_x, 0] = (field[i_inc] - field[i_dec]) / interval
        else:
            grad[i_x, 0] = 0.0


@cython.cdivision(True)
@cython.boundscheck(False)
def grad_2d(np.ndarray[np.float_t, ndim=2] field,
            np.ndarray[np.float_t, ndim=3] grad,
            double dx,
            np.ndarray[np.uint8_t, ndim=2] walls):
    cdef:
        unsigned int i_x, i_y, i_inc, i_dec
        unsigned int M_x = walls.shape[0], M_y = walls.shape[1]
        np.float_t dx_double = 2.0 * dx, interval

    for i_x in range(M_x):
        for i_y in range(M_y):
            if not walls[i_x, i_y]:
                i_inc = wrap_inc(M_x, i_x)
                i_dec = wrap_dec(M_x, i_x)

                interval = dx_double
                if walls[i_inc, i_y]:
                    i_inc = i_x
                    interval = dx
                if walls[i_dec, i_y]:
                    i_dec = i_x
                    interval = dx

                grad[i_x, i_y, 0] = (field[i_inc, i_y] - field[i_dec, i_y]) / interval

                i_inc = wrap_inc(M_y, i_y)
                i_dec = wrap_dec(M_y, i_y)

                interval = dx_double
                if walls[i_x, i_inc]:
                    i_inc = i_y
                    interval = dx
                if walls[i_x, i_dec]:
                    i_dec = i_y
                    interval = dx

                grad[i_x, i_y, 1] = (field[i_x, i_inc] - field[i_x, i_dec]) / interval
            else:
                grad[i_x, i_y, 0] = 0.0
                grad[i_x, i_y, 1] = 0.0


@cython.cdivision(True)
@cython.boundscheck(False)
def grad_3d(np.ndarray[np.float_t, ndim=3] field,
            np.ndarray[np.float_t, ndim=4] grad,
            double dx,
            np.ndarray[np.uint8_t, ndim=3] walls):
    cdef:
        unsigned int i_x, i_y, i_z, i_inc, i_dec
        unsigned int M_x = walls.shape[0], M_y = walls.shape[1]
        unsigned int M_z = walls.shape[2]
        np.float_t dx_double = 2.0 * dx, interval

    for i_x in range(M_x):
        for i_y in range(M_y):
            for i_z in range(M_z):
                if not walls[i_x, i_y, i_z]:
                    i_inc = wrap_inc(M_x, i_x)
                    i_dec = wrap_dec(M_x, i_x)

                    interval = dx_double
                    if walls[i_inc, i_y, i_z]:
                        i_inc = i_x
                        interval = dx
                    if walls[i_dec, i_y, i_z]:
                        i_dec = i_x
                        interval = dx

                    grad[i_x, i_y, i_z, 0] = (field[i_inc, i_y, i_z] - field[i_dec, i_y, i_z]) / interval

                    i_inc = wrap_inc(M_y, i_y)
                    i_dec = wrap_dec(M_y, i_y)

                    interval = dx_double
                    if walls[i_x, i_inc, i_z]:
                        i_inc = i_y
                        interval = dx
                    if walls[i_x, i_dec, i_z]:
                        i_dec = i_y
                        interval = dx

                    grad[i_x, i_y, i_z, 1] = (field[i_x, i_inc, i_z] - field[i_x, i_dec, i_z]) / interval

                    i_inc = wrap_inc(M_z, i_z)
                    i_dec = wrap_dec(M_z, i_z)

                    interval = dx_double
                    if walls[i_x, i_y, i_inc]:
                        i_inc = i_z
                        interval = dx
                    if walls[i_x, i_y, i_dec]:
                        i_dec = i_z
                        interval = dx

                    grad[i_x, i_y, i_z, 2] = (field[i_x, i_y, i_inc] - field[i_x, i_y, i_dec]) / interval
                else:
                    grad[i_x, i_y, i_z, 0] = 0.0
                    grad[i_x, i_y, i_z, 1] = 0.0
                    grad[i_x, i_y, i_z, 2] = 0.0


@cython.cdivision(True)
@cython.boundscheck(False)
def grad_i_1d(np.ndarray[np.float_t, ndim=1] field,
              np.ndarray[np.int_t, ndim=2] inds,
              np.ndarray[np.float_t, ndim=2] grad_i,
              double dx,
              np.ndarray[np.uint8_t, ndim=1] walls):
    cdef:
        unsigned int i, i_x, i_inc, i_dec
        unsigned int M_x = field.shape[0]
        double dx_double = 2.0 * dx, interval

    for i in range(inds.shape[0]):
        i_x = inds[i, 0]
        if not walls[i_x]:
            i_inc = wrap_inc(M_x, i_x)
            i_dec = wrap_dec(M_x, i_x)

            interval = dx_double
            if walls[i_inc]:
                i_inc = i_x
                interval = dx
            if walls[i_dec]:
                i_dec = i_x
                interval = dx

            grad_i[i, 0] = (field[i_inc] -  field[i_dec]) / interval
        else:
            grad_i[i, 0] = 0.0


@cython.cdivision(True)
@cython.boundscheck(False)
def grad_i_2d(np.ndarray[np.float_t, ndim=2] field,
              np.ndarray[np.int_t, ndim=2] inds,
              np.ndarray[np.float_t, ndim=2] grad_i,
              double dx,
              np.ndarray[np.uint8_t, ndim=2] walls):
    cdef:
        unsigned int i, i_x, i_y, i_inc, i_dec
        unsigned int M_x = field.shape[0], M_y = field.shape[1]
        double dx_double = 2.0 * dx, interval

    for i in range(inds.shape[0]):
        i_x, i_y = inds[i, 0], inds[i, 1]
        if not walls[i_x, i_y]:
            i_inc = wrap_inc(M_x, i_x)
            i_dec = wrap_dec(M_x, i_x)

            interval = dx_double
            if walls[i_inc, i_y]:
                i_inc = i_x
                interval = dx
            if walls[i_dec, i_y]:
                i_dec = i_x
                interval = dx

            grad_i[i, 0] = (field[i_inc, i_y] - field[i_dec, i_y]) / interval

            i_inc = wrap_inc(M_y, i_y)
            i_dec = wrap_dec(M_y, i_y)

            interval = dx_double
            if walls[i_x, i_inc]:
                i_inc = i_y
                interval = dx
            if walls[i_x, i_dec]:
                i_dec = i_y
                interval = dx

            grad_i[i, 1] = (field[i_x, i_inc] - field[i_x, i_dec]) / interval
        else:
            grad_i[i, 0] = 0.0
            grad_i[i, 1] = 0.0


@cython.cdivision(True)
@cython.boundscheck(False)
def grad_i_3d(np.ndarray[np.float_t, ndim=3] field,
              np.ndarray[np.int_t, ndim=2] inds,
              np.ndarray[np.float_t, ndim=2] grad_i,
              double dx,
              np.ndarray[np.uint8_t, ndim=3] walls):
    cdef:
        unsigned int i, i_x, i_y, i_z, i_inc, i_dec
        unsigned int M_x = field.shape[0], M_y = field.shape[1]
        unsigned int M_z = field.shape[2]
        double dx_double = 2.0 * dx, interval

    for i in range(inds.shape[0]):
        i_x, i_y, i_z = inds[i, 0], inds[i, 1], inds[i, 2]
        if not walls[i_x, i_y, i_z]:
            i_inc = wrap_inc(M_x, i_x)
            i_dec = wrap_dec(M_x, i_x)
            interval = dx_double

            if walls[i_inc, i_y, i_z]:
                i_inc = i_x
                interval = dx
            if walls[i_dec, i_y, i_z]:
                i_dec = i_x
                interval = dx

            grad_i[i, 0] = (field[i_inc, i_y, i_z] - field[i_dec, i_y, i_z]) / interval

            i_inc = wrap_inc(M_y, i_y)
            i_dec = wrap_dec(M_y, i_y)
            interval = dx_double

            if walls[i_x, i_inc, i_z]:
                i_inc = i_y
                interval = dx
            if walls[i_x, i_dec, i_z]:
                i_dec = i_y
                interval = dx

            grad_i[i, 1] = (field[i_x, i_inc, i_z] - field[i_x, i_dec, i_z]) / interval

            i_inc = wrap_inc(M_z, i_z)
            i_dec = wrap_dec(M_z, i_z)
            interval = dx_double

            if walls[i_x, i_y, i_inc]:
                i_inc = i_z
                interval = dx
            if walls[i_x, i_y, i_dec]:
                i_dec = i_z
                interval = dx

            grad_i[i, 2] = (field[i_x, i_y, i_inc] - field[i_x, i_y, i_dec]) / interval
        else:
            grad_i[i, 0] = 0.0
            grad_i[i, 1] = 0.0
            grad_i[i, 2] = 0.0


@cython.cdivision(True)
@cython.boundscheck(False)
def laplace_1d(np.ndarray[np.float_t, ndim=1] field,
               np.ndarray[np.float_t, ndim=1] laplace,
               double dx,
               np.ndarray[np.uint8_t, ndim=1] walls):
    cdef:
        unsigned int i_x
        unsigned int i_inc, i_dec
        unsigned int M_x = walls.shape[0]
        np.float_t dx_sq = dx * dx, diff

    for i_x in range(M_x):
        if not walls[i_x]:
            diff = 0.0

            i_inc = wrap_inc(M_x, i_x)
            i_dec = wrap_dec(M_x, i_x)
            if not walls[i_inc]:
                diff += field[i_inc] - field[i_x]
            if not walls[i_dec]:
                diff += field[i_dec] - field[i_x]

            laplace[i_x] = diff / dx_sq
        else:
            laplace[i_x] = 0.0


@cython.cdivision(True)
@cython.boundscheck(False)
def laplace_2d(np.ndarray[np.float_t, ndim=2] field,
               np.ndarray[np.float_t, ndim=2] laplace,
               double dx,
               np.ndarray[np.uint8_t, ndim=2] walls):
    cdef:
        unsigned int i_x, i_y
        unsigned int i_inc, i_dec
        unsigned int M_x = walls.shape[0], M_y = walls.shape[1]
        np.float_t dx_sq = dx * dx, diff

    for i_x in range(M_x):
        for i_y in range(M_y):
            if not walls[i_x, i_y]:
                diff = 0.0

                i_inc = wrap_inc(M_x, i_x)
                i_dec = wrap_dec(M_x, i_x)
                if not walls[i_inc, i_y]:
                    diff += field[i_inc, i_y] - field[i_x, i_y]
                if not walls[i_dec, i_y]:
                    diff += field[i_dec, i_y] - field[i_x, i_y]

                i_inc = wrap_inc(M_y, i_y)
                i_dec = wrap_dec(M_y, i_y)
                if not walls[i_x, i_inc]:
                    diff += field[i_x, i_inc] - field[i_x, i_y]
                if not walls[i_x, i_dec]:
                    diff += field[i_x, i_dec] - field[i_x, i_y]

                laplace[i_x, i_y] = diff / dx_sq
            else:
                laplace[i_x, i_y] = 0.0


@cython.cdivision(True)
@cython.boundscheck(False)
def laplace_3d(np.ndarray[np.float_t, ndim=3] field,
               np.ndarray[np.float_t, ndim=3] laplace,
               double dx,
               np.ndarray[np.uint8_t, ndim=3] walls):
    cdef:
        unsigned int i_x, i_y, i_z
        unsigned int i_inc, i_dec
        unsigned int M_x = walls.shape[0], M_y = walls.shape[1]
        unsigned int M_z = walls.shape[2]
        np.float_t dx_sq = dx * dx, diff

    for i_x in range(M_x):
        for i_y in range(M_y):
            for i_z in range(M_z):
                if not walls[i_x, i_y, i_z]:
                    diff = 0.0

                    i_inc = wrap_inc(M_x, i_x)
                    i_dec = wrap_dec(M_x, i_x)
                    if not walls[i_inc, i_y, i_z]:
                        diff += field[i_inc, i_y, i_z] - field[i_x, i_y, i_z]
                    if not walls[i_dec, i_y, i_z]:
                        diff += field[i_dec, i_y, i_z] - field[i_x, i_y, i_z]

                    i_inc = wrap_inc(M_y, i_y)
                    i_dec = wrap_dec(M_y, i_y)
                    if not walls[i_x, i_inc, i_z]:
                        diff += field[i_x, i_inc, i_z] - field[i_x, i_y, i_z]
                    if not walls[i_x, i_dec, i_z]:
                        diff += field[i_x, i_dec, i_z] - field[i_x, i_y, i_z]

                    i_inc = wrap_inc(M_z, i_z)
                    i_dec = wrap_dec(M_z, i_z)
                    if not walls[i_x, i_y, i_inc]:
                        diff += field[i_x, i_y, i_inc] - field[i_x, i_y, i_z]
                    if not walls[i_x, i_y, i_dec]:
                        diff += field[i_x, i_y, i_dec] - field[i_x, i_y, i_z]

                    laplace[i_x, i_y, i_z] = diff / dx_sq

                else:
                    laplace[i_x, i_y, i_z] = 0.0
