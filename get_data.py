#!/usr/bin/python

import csv
import time
#I stole this from sorelle's 207
"""
This library contains some functions you may find useful when working with the
given data.  Feel free to modify this to be more general and/or to point to 
other data you're looking at.  Or feel free not to use these at all if you don't
 find them useful.
"""

"""
Takes a filename and returns the given csv as a list of dictionaries where each
dictionary maps from the name of the feature as given by the header row to its
value for that data item.
"""
def get_data_list_of_dicts(filename):
    list = []
    with open(filename) as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            list.append(row)
    return list

"""
Takes a filename and returns a list containing the first row (the header row) as
a list.
"""
def get_headers(filename):
    with open(filename) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
    return headers

"""
Takes a list of dictionaries (in the form given by get_data_list_of_dicts above),
and a header list (as given by get_headers) and writes it to the given filename.
"""
def write_data_dicts(filename, headers, rows_list_of_dicts):
    with open(filename,'w') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(rows_list_of_dicts)

"""
Takes a list of lists, i.e., a list containing each row with each row represented
as a list, a list of the header row, and a filename and writes the data to the
filename as a csv.
"""
def write_data(filename, headers, rows_list_of_lists):
    with open(filename,'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows_list_of_lists)

"""
Takes a list of dictionaries (in the form given by get_data_list_of_dicts above)
and a column_name (one of the values from get_headers above) and returns the
values in that column as a list.
"""
def get_data_slice(column_name, list_of_dicts):
    list = []
    for dict in list_of_dicts:
        list.append(dict[column_name])
    return list

"""
Date conversion (useful for the lab2 power consumption data).
"""
def date_convert(date_string):
    date = time.strptime(date_string, "%d/%m/%Y %H:%M:%S")
    return time.mktime(date)

# make doctest work:
def _test():
    import doctest
    result = doctest.testmod()
    if result[0] == 0:
        print("Wahoo! Passed all", result[1], __file__.split('/')[-1], "tests!")
    else:
       print("Rats!")

if __name__ == "__main__": _test()


