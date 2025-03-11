# DOC - Utilities

- [DOC - Utilities](#doc---utilities)
  - [Printout](#printout)
    - [`print_table`](#print_table)
    - [`print_dictionary_tree`](#print_dictionary_tree)

---

## Printout

Functions for a fast good-loking data printout.

### `print_table`

Given a list of elements they are printed in a table format with the number of columns and spacing defined by the user.

The table is returned as string.

Arguments:

```text
    - values: list, values to be printed
    - cols: int,  number of columns
    - col_width: int, default=20, width (digits) of each column
    - title: str, default="", title of the table
```

### `print_dictionary_tree`

Recursive function to print the whole tree of keys belonging to a dictionary.

```text
    - d: dict, dictionary
    - t: int, tabs to be added to the nested dictionary keys
```
---

[<< Home](../readme.md)


