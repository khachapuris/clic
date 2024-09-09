"""This module provides character related functions."""

classes = {
    'alpha':  '_',   # characters that behave like alphabetical
    'decseps': '.',  # desimal separator characters
    'quote':  '"',   # start / end of a calculator string
    'expsep': ';',   # expression separator
    'command': '/',  # start of a command
    'assign': '=',   # assignment operator
}


def isalphaplus(c):
    """Return whether c is alphabetical / semi-alphabetical or not."""
    return c.isalpha() or c in classes['alpha']


def isdigitplus(c):
    """Return whether c is a digit / decimal separator or not."""
    return c.isdigit() or c in classes['decseps']


def standard_decsep(c):
    """If c is a decsep, return a period; otherwise return c."""
    if c in classes['decseps']:
        return '.'
    return c
