from copy import deepcopy
import os

def _to_str(headers:list[any], records:list[list[any]]) -> tuple[list[str], list[list[str]]]:
    """
    Convert the content of the provided lists to string.
    Input lists are copied to avoid issues due to list mutability.
    - headers: list[any], list of the table headers
    - records: list[list[any]], list of the records (i.e. table content)
    Returns:
    - h_str: list[str]: 
    - r_str: list[list[str]]
    """
    h_str, r_str = deepcopy(headers), deepcopy(records)
    h_str = [str(h) for h in headers]
    r_str = [[str(r) for r in rec] for rec in records]
    return h_str, r_str

def _check_consistency(headers:list[any], records:list[list[any]]) -> bool:
    """
    The size consistency of headers and all the records is checked.
    - headers: list[any], list of the table headers
    - records: list[list[any]], list of the records (i.e. table content)
    Returns:
    - ValueError: an error is raised when the input are not consistent
    - bool: a True is returned if the consistency is checked
    """
    for i, rec in enumerate(records):
        if len(rec) != len(headers):
            raise ValueError(f"Headers and Records {i} are not the same length: {len(headers)} != {len(rec)}")
    return True

def _calc_max_width_horiz(headers:list[str], records:list[list[str]], spaces:int=2, width:int=None) -> list[int]:
    """
    Calculate the maximum column width by considering additional spacing and compares it with a user defined value. The maximum spacing between the calculated and the user defined is used. Horizontal layout.
    - headers: list[any], list of the table headers
    - records: list[list[any]], list of the records (i.e. table content)     
    - spaces : int, default=2, additional spacing to the width measured
    - widt   : int, default=None, user defined width
    Return
    - col_len: list[int], the width of each column
    """
    headers, records = _to_str(headers, records)
    col_len = [width if width is not None else 0 for _ in headers] # initialize with width if not None else 0
    for i, h in enumerate(headers):
        l = len(h)
        col_len[i] = l if l > col_len[i] else col_len[i]
    for rec in records:
        for i, r in enumerate(rec):
            l = len(r)
            col_len[i] = l if l > col_len[i] else col_len[i]
    col_len = [l + spaces for l in col_len] # adding two spaces
    return col_len

def _calc_max_width_vert(headers:list[any], records:list[list[any]], spaces:int=None, width:int=None) -> list[int]:
    """
    Calculate the maximum column width by considering additional spacing and compares it with a user defined value. The maximum spacing between the calculated and the user defined is used. Vertical layout.
    - headers: list[any], list of the table headers
    - records: list[list[any]], list of the records (i.e. table content)     
    - spaces : int, default=2, additional spacing to the width measured
    - widt   : int, default=None, user defined width
    Return
    - col_len: list[int], the width of each column
    """    
    headers, records = _to_str(headers, records)
    spaces = spaces if spaces else 2
    col_len = [width if width is not None else 0 for _ in range(len(records) + 1)] # initialize with width if not None else 0
    for h in headers:
        col_len[0] = len(h) if len(h) > col_len[0] else col_len[0]
    for i, rec in enumerate(records):
        for r in rec:
            col_len[i+1] = len(r) if len(r) > col_len[i+1] else col_len[i+1]
    col_len = [l + spaces for l in col_len] # adding two spaces
    return col_len

def _build_table_horiz(headers:list[str], records:list[list[str]], settings:dict) -> str:
    """
    Build the table as string, horizontal layout:
    - headers: list[str], list of the table headers
    - records: list[list[str]], list of the records (i.e. table content)    
    - settings: dict, settings dictionary
    Returns:
    - s: str, the table
    """
    col_len = _calc_max_width_horiz(headers, records, spaces=settings["spaces"], width=settings["width"])
    sep = settings["separator"]
    template = sep
    for i in range(len(headers)):
        if i == 0:
            template += "{:<%d}%s" % (col_len[i], sep)
        else:
            template += "{:^%d}%s" % (col_len[i], sep) 
    template += "\n"
    rows = [headers]
    if settings["markdown"]:
        rows += [["---" for _ in range(len(headers))]]
    rows += records
    s = ""
    for row in rows:
        s += template.format(*row)
    return s

def _build_table_vert(headers:list[str], records:list[list[str]], settings:dict) -> str:
    """
    Build the table as string, vertical layout:
    - headers: list[str], list of the table headers
    - records: list[list[str]], list of the records (i.e. table content)    
    - settings: dict, settings dictionary
    Returns:
    - s: str, the table formatted as string   
    """
    col_len = _calc_max_width_vert(headers, records, spaces=settings["spaces"], width=settings["width"])
    sep = settings["separator"]
    template = sep
    for i in range(len(records) + 1):
        if i == 0:
            template += "{:<%d}%s" % (col_len[i], sep)
        else:
            template += "{:^%d}%s" % (col_len[i], sep) 
    template += "\n"

    rows = [[h] for h in headers]
    for rec in records:
        for i, r in enumerate(rec):
            rows[i].append(r)
    if settings["markdown"]:
        rows.insert(1, ["---" for _ in range(len(rows[0]))])

    s = ""
    for row in rows:
        s += template.format(*row)
    return s

def _import_settings(settings:dict) -> dict:
    """
    Handling of settings for table printout. Default values are provided when not
    available and non-allowed values are corrected.
    - settings:dict, parameters that defines the table built
        - "positioning": str, default="horiz"
            - "horiz": horizontal table positioning, i.e. records to rows
            - "vert" : vertical table positioning, i.e. records to columns
        - "spaces"    : int, default=2, additional chars to cell width
        - "width"     : int, default=None, user-defined columng width
        - "markdown"  : bool, table styled for markdown rendering 
        - "separator" : str, separator character between two columns
        - "export"    : bool, default=False, file export flag
        - "folder"    : str, default="", folder of the exported file
        - "filename"  : str, default="table.txt"
        - "printout"  : bool, default=False, flag for the table printout
    Returns:
    - settings: dict, settings dictionary copied from the input one and properly modified
    """
    settings = deepcopy(settings)
    settings["positioning"] = settings.get("positioning")
    settings["positioning"] = settings["positioning"] if settings["positioning"] in ["horiz", "vert"] else "horiz"
    settings["spaces"] = settings.get("spaces")
    settings["spaces"] = 2 if settings["spaces"] is None else settings["spaces"]
    settings["width"] = settings.get("width")
    settings["markdown"] = settings.get("markdown", False)
    settings["separator"] = settings.get("separator", '')
    settings["separator"] = ' ' if settings["separator"] is None else settings["separator"]
    settings["separator"] = '|' if settings["markdown"] else settings["separator"]
    settings["export"] = settings.get("export", False)
    settings["folder"] = settings.get("folder", "")
    settings["filename"] = settings.get("filename", "table.txt")
    settings["printout"] = settings.get("printout", False)

    return settings

def build_table(headers:list[any], records:list[list[any]], settings:dict) -> str:
    """
    - headers: list[any], list of the table headers
    - records: list[list[any]], list of the records (i.e. table content)
    - settings: dict, settings dictionary        
    Return:
    - table: str, the table formatted as string
    """
    _check_consistency(headers, records)
    settings = _import_settings(settings)
    headers, records = _to_str(headers, records)
    if settings['positioning'] == "vert":
        table = _build_table_vert(headers, records, settings)
    elif settings["positioning"] == "horiz":
        table = _build_table_horiz(headers, records, settings)
    return table

def print_table_vert(headers:list[any], records:list[list[any]], settings:dict={}):
    """
    Print vertical layout table:
    - headers: list[any], list of the table headers
    - records: list[list[any]], list of the records (i.e. table content)
    - settings: dict, default={}, settings dictionary
    Returns:
    - None
    """
    settings = _import_settings(settings)
    settings["positioning"] = "vert"
    print(build_table(headers, records, settings))

def print_table_horiz(headers:list[any], records:list[list[any]], settings:dict={}):
    """
    Print horizontal layout table:
    - headers: list[any], list of the table headers
    - records: list[list[any]], list of the records (i.e. table content)
    - settings: dict, default={}, settings dictionary
    Returns:
    - None
    """    
    settings = _import_settings(settings)
    settings["positioning"] = "horiz"
    print(build_table(headers, records, settings))

class TablePrintout:
    def __init__(self, headers:list[any], records:list[list[any]], settings:dict):
        """
        - headers: list[any], table headers
        - records: list[list[any]], table content
        - settings:dict, parameters that defines the table built
            - "positioning": str, default="horiz"
                - "horiz": horizontal table positioning, i.e. records to rows
                - "vert" : vertical table positioning, i.e. records to columns
            - "spaces"    : int, default=2, additional chars to cell width
            - "width"     : int, default=None, user-defined columng width
            - "markdown"  : bool, table styled for markdown rendering 
            - "separator" : str, separator character between two columns
            - "export"    : bool, default=False, file export flag
            - "folder"    : str, default="", folder of the exported file
            - "filename"  : str, default="table.txt"
            - "printout"  : bool, default=False, flag for the table printout
        """
        self.settings = _import_settings(settings)
        self.headers, self.records = _to_str(headers, records)
        self.build_table()
        if self.settings["printout"] is True:
            self.print_table()
        if self.settings["export"] is True:
            self.export()

    def build_table(self):
        self.table = build_table(self.headers, self.records, self.settings)

    def print_table(self, settings={}):
        if len(settings) != 0:
            self.settings = _import_settings(settings)
            self.table = self.build_table(self.headers, self.records, settings)
        print(self.table)

    def export(self, settings={}):
        if len(settings) != 0:
            self.settings = _import_settings(settings)
            self.table = self.build_table(self.headers, self.records, settings)
        filepath = os.path.join(self.settings["folder"], self.settings["filename"])
        print(f"Exporting {filepath} ... ", end='')
        with open(filepath, "w") as f:
            f.write(self.table)
        print("done!")
        
