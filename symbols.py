"""This module provides character related functions."""

# calculator character classes
ccc = {
    'alpha':  '_',   # characters that behave like alphabetical
    'decseps': '.',  # desimal separator characters
    'quote':  '"',   # start / end of a calculator string
    'expsep': ';',   # expression separator
    'command': '/',  # start of a command
    'assign': '=',   # assignment operator
}

# system variable names
svn = {
    'sysans': '_',
    'implicit': '_dot_'
}


def isalphaplus(x):
    """Return whether x is alphabetical / semi-alphabetical or not."""
    return x.isalpha() or x in ccc['alpha']


def isdigitplus(x):
    """Return whether x is a digit / decimal separator or not."""
    return x.isdigit() or x in ccc['decseps']


def standard_decsep(x):
    """If x is a decsep, return a period; otherwise return x."""
    if x in ccc['decseps']:
        return '.'
    return x
