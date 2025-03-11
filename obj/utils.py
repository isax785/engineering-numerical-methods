def print_table(values:list, cols:int, col_width:int=20, title:str="") -> str:
    """
    Given a list of elements they are printed in a table format
    with the number of columns and spacing defined by the user.
    - values: list, values to be printed
    - cols: int,  number of columns
    - col_width: int, default=20, width (digits) of each column
    - title: str, default="", title of the table
    """
    s = title + "\n"
    for i, mod in enumerate(values):
        if i % cols == 0 and i > 0:
            s += '\n'
        s += f"{mod:<{col_width}}\t"
    print(s)
    return s

def print_dictionary_tree(d, tab:int=0):
    """
    Recursive function to print the whole tree of keys
    belonging to a dictionary.
    - d: dict, dictionary
    - t: int, tabs to be added to the nested dictionary keys
    """
    for k in d:
        if isinstance(d[k], dict):
            print('\t'*tab, k, '->')
            print_dictionary_tree(d[k], tab=tab+1)
        else:
            print('\t'*tab, k)