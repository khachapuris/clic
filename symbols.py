"""This module provides character related functions and dictionaries."""

# calculator characters
cc = {
    'alpha':  '_',   # characters that behave like alphabetical
    'decseps': '.',  # desimal separator characters
    'quote':  '"',   # start / end of a calculator string
    'expsep': ';',   # expression separator
    'command': '/',  # start of a command
    'assign': '=',   # assignment operator
}

# system variables
sv = {
    'ans': 'ans',
    'sysans': '_',
    'implicit': '_dot_'
}


def isalphaplus(x):
    """Return whether x is alphabetical / semi-alphabetical or not."""
    return x.isalpha() or x in cc['alpha']


def isdigitplus(x):
    """Return whether x is a digit / decimal separator or not."""
    return x.isdigit() or x in cc['decseps']


def standard_decsep(x):
    """If x is a decsep, return a period; otherwise return x."""
    if x in cc['decseps']:
        return '.'
    return x
