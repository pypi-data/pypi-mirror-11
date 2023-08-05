Overview
========

This module contains some tools for linear algebra.  It contains classes
to define matrices and vectors, and a number of functions for working 
on those matrices and vectors.  It is intended for mathematical and
scientific use.  It saved me a lot of time in a linear algebra class.

Classes
=======

    - vector: collection which defines a vector in Cartesian coordinates

    - matrix: two-dimensional collection stored in row-major order

Functions
==========

    - AxApproxB: solves Ax approximately equal to b; for use when the rows of matrix b are not in the column space of A

    - axpy: ax+y where a is a scalar, and x and y are vectors

    - bestfit: used to find a line of best fit from given points

    - colVec: makes a matrix with one column

    - det: returns the determinant of a square matrix.  Can return a cross product if the top row contains the unit vectors.

    - dot: returns the dot product of two vectors

    - crossProduct:  Returns a cross product

    - GaussJordan: solves AX=B, where matrices A and B are known and X is returned.  If B is not in the column-space of A, use AxApproxB.

    - identityMatrix: makes an identity matrix of a given size

    - linearCombination: returns a linear combination based on a list of scalars and a list of vectors

    - mmMult: matrix-matrix multiplication

    - mvMult: matrix-vector multiplication

    - norm: takes the norm of a vector; defaults to 2 (Euclidian norm)

    - proj: projection of one vector onto another

    - rowVec: makes a matrix with one row

    - transpose: transposes a matrix

    - unitVector: constructs a unit vector

    - v: wrapper around vector instantiation

    - zeroMatrix: makes a zero matrix of a given size

    - zeroVector: makes a zero vector of a given size

More Information
================

Help is available in the included help file.