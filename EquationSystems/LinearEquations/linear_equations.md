# Linear Equation Systems

> Solve the simulatneous equation $A\cdot x=b$.

Solution of `n` linear algebraic equations in `n` unknowns.

Equation sets arising from physical problems are often very large: the exploitation of some matrix properties (e.g. sparseness) allows to reduce the storage requirements and the run-time.

> `LAPACK` (Linear Algebra PACKage) is a collection of routines for the solution of large sets of equations.

$A\cdot x=b$ matrix form of a linear equation system.

$A|b$ is the *augmented coefficient matrix*.

One of the most important topics in engineering application is the solution of system composed by *n* linear algebraic equations, since they are recurrent in a lot of applications. 

A linear equation system can be represented as follows:

$$\begin{matrix} 
A_{11}x_1+A_{12}x_2+\cdots+A_{1n}x_n=b_1 \\
A_{21}x_1+A_{22}x_2+\cdots+A_{2n}x_n=b_2 \\
\vdots\\ 
A_{n1}x_1+A_{n2}x_2+\cdots+A_{nn}x_n=b_n \\
\end{matrix}$$

that can be represented by the simplified notation:

$$A\cdot x=b$$

Since physical problems often lead to very large equation sets, the computational resources consumed could be vry large. In order to reduce both the memory and time cost, some special properties of the coefficient matrix (e.g. sparseness, symmetry, banding).

## Matrix Determinant

In mathematics, the determinant is a scalar value that is a function of the entries of a square matrix. It characterizes some properties of the matrix and the linear map represented by the matrix. In particular, the determinant is nonzero if and only if the matrix is invertible and the linear map represented by the matrix is an isomorphism. The determinant of a product of matrices is the product of their determinants (the preceding property is a corollary of this one). The determinant of a matrix $A$ is denoted $det(A)$, $det A$, or $|A|$.

### Solution Uniqueness

If the coefficient matrix determinant is *nonsingular* (i.e. $|A|\neq0$). The rows and columns of such a matrix are *linearly independent* (i.e. no row nor column is a linear combination of other rows or column).

### Conditioning

The matrix is almost singular (i.e. $|A|$ is very small) when the *determinant* is much smaller than the *norm* (i.e. $\parallel A \parallel$) of the matrix.

**Euclidan Norm**

$$\parallel A \parallel_e = $$

**Row-Sum Norm** (or **infinity norm**)

$$\parallel A \parallel_\infty = $$

The *matrix condition number* is a formal measure of conditioning

$$cond(A)=\parallel A \parallel \parallel A^{-1} \parallel$$

# References

- <a href="https://en.wikipedia.org/wiki/System_of_linear_equations">WikiPedia: System of Linear Equations</a>
- <a href="https://en.wikipedia.org/wiki/Determinant">WikiPedia: Matrix Determinant</a>
- <a href="https://netlib.org/lapack/">LAPACK Linear Algebra Solver</a>
- <a href="https://docs.scipy.org/doc/scipy/reference/linalg.lapack.html">`scipy` Low Level LAPACK Functions</a>




---
<p align="center"><a href="../../readme.md">Home</a> | <a href="../equation_systems.md">Equation Systems</a></p>