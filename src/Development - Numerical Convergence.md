# Development - Numerical Convergence

A this [GitHub link](https://github.com/isax785/engineering-numerical-methods/blob/develop/dev/dev_numerical-convergence.ipynb) the Jupyter notebook dedicated to the development of a **numerical convergence method**.

The convergence function is within the same repo (folder `obj`).

I currently use Jupyter notebooks with the `autoreload` function for the development of numerical models and routines that are part of or will be integrated into other modules.

Here the aim was to implement the functions `nc_function_args` and `nc_function_dict` allowing to reach the convergence of routines (i.e. class methods, functions) that are compliant with a well defined interface (i.e. arguments, dictionaries).

This implementation is functional for running the solving methods of the numerical models, i.e. the performance calculation of the refrigeration systems. But it can be applied to any method that needs a numerical solution because it cannot be solved analytically.

