"""
Utility functions for working with columns for writing data to csv / Excel spreadsheets.

"""

from collections import namedtuple


Column = namedtuple('Column', ['name', 'number', 'find_value'])
Column.__doc__ = \
    """
    A `Column` is a tuple with `name`, `number`, and `find_value` coordinates.
    
    `find_value` functions should have two parameters: the first is some data
    of variable type to be associated with the row, and the second is the row
    number.

    Coordinates:
        name (str): the name of the column which will appear as its header
        number (int): the number of the column (starting at 1)
        find_value (Callable): a callable function associated with the column
    """
    
def getColumnByName(columns, name):
    """
    Return the first element in the list of Column tuples `columns` whose name
    coordinate is `name`.
    
    Parameters:
        columns (List[Column]): a list of Column tuples
        name (str): the name of the column to find
        
    Returns:
        a Column tuple with name coordinate `name`
    """
    return next(column for column in columns if column.name == name)

def sortColumnsByNumber(columns):
    """
    Sort the list of columns `columns` by number coordinate.
n    
    Parameters:
        columns (List[Column]): a list of Column tuples
    """
    columns.sort(key=lambda column: column.number)
    
def wrapColumnFunction(columns, name, wrapper, *, sort=True):
    """
    Wraps the `find_value` function of the column in `columns` with name 
    coordinate `name` with the function `wrapper`, which will be passed 
    the result of the `find_value` function.
    
    Parameters:
        columns (List[Column]): a list of Column tuples
        name (str): the name of the column whose `find_value` to wrap
        wrapper (Callable): the function passed the result of `find_value`
        sort (bool): whether to sort the modified column list by col. number
    """
    column = getColumnByName(columns, name)
    function = lambda data, row: wrapper(column.find_value(data, row))
    columns.remove(column)
    columns.append(Column(column.name, column.number, function))
    if sort: sortColumnsByNumber(columns)
    
def replaceColumnFunction(columns, name, function, *, sort=True):
    """
    Replaces the `find_value` function of the column in `columns` with name 
    coordinate `name` with the function `function`.
    
    Parameters:
        columns (List[Column]): a list of Column tuples
        name (str): the name of the column whose `find_value` to replace
        function (Callable): the new `find_value` coordinate
        sort (bool): whether to sort the modified column list by col. number
    """
    column = next(column for column in columns if column.name == name)
    columns.remove(column)
    columns.append(Column(column.name, column.number, function))
    if sort: sortColumnsByNumber(columns)
    
