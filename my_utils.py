"""
    Project: Countries_CSV-to-HTML-and-LaTeX-formats
    Purpose: Academical
    Description: Contains auxiliary methods

    Author: João Rodrigues
    Student No.: 16928

    Course: LESI
    Subject: Languages Processing
    College: IPCA
    Academic year: 2021/2022
"""

def slurp(filename):
    """Reads a file and returns it content as string"""

    try:
        with open(filename, "rt") as fh:
            contents = fh.read()
        return contents
    # Case file doesn't exists
    except FileNotFoundError:
        print("File was not found! Please check filename or directory.")
        exit(1)


def split_columns_values(file_string):
    """Splits a csv file string in 2 (Header and content)

        Header: 1st line, which contains columns' names
        Values: Remaining lines, which contains values

        Both variables are returned as a tuple
    """

    # Position of \n - where it ends 1st line
    newline_position = file_string.find('\n')

    # 1st line ends on \n character
    header = file_string[:newline_position]
    values = file_string[newline_position + 1:]
    return header, values

