# Readme

`Engineering Numerical Methods` is a collection of numerical methods aimed at solving the most common problems that can be encounterd in engineering applications.

The whole content is presented in form of **wiki**, with multiple markdown files fully linked together.

Practical examples are also provided to ease the comprehension of the presented methods and provide an insight of practical application.

Map of Contents:

- [CoolProp Utilities](./doc/doc_coolprop_utils.md)
- [Decorators](./doc/doc_decorators.md)
- [Numerical Convergence](./doc/doc_numerical_convergence.md)
- [Table Printout](./doc/doc_table_printout.md)
- [Utilities](./doc/doc_utils.md)


## TODO

- [ ] `img` folder containing all the images to be linked in the `md` files
- [ ] identify and add license
- [ ] `py` script for index/links generation
- [ ] `#a` curves intersection to `utilities`
- [ ] `#a` into `Table Printout`, markdown table printout
- [ ] `#a` `decorators` documentation
- [x] `#a` `CoolProp` plot `ph` diagram given a list of multiple `(T, p, x)` points
- [x] `#a` `CoolProp` toolbox (with reference to version number of the module)

## Development Guidelines

- all the notes to be reported in `.md` files only
- method comparative based on execution **timing** 
- implement `wiki` (i.e. internal linking in all files)
  - master file connected to al the ones contained in subfolders
  - each file connected to its parent and children (if present)
- folder structure to be defined while going ahead with the implementation
- use `LaTeX` for formula

# Other Topics

Other topics to be investigated:

- secant method (root finding)
- Ridder's method
- finite difference model
- partial differential equations
- multidimensional boundary value problems

--- 

# Snippets

Linking:

- `<a href="path/here"> Display Text </a>` : <a href="./DataManipulation/data_manipulation.md">Data Manipulation</a>
- `[Display Text](path/here)` : [Data Manipulation](./DataManipulation/data_manipulation.md)\

---

# Resources

## `pdf` Books

All the `pdf` here mentioned can be retrieved from the main `LIBRARY`:

- `[book] Modeling and Simulation in Python.pdf`
- `[book] numerical methods for computational science and engineering.pdf`
- `[book] Numerical Methods in Engineering with Python 3.pdf`