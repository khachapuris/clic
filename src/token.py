"""This module provides a class for calculator tokens.

The tokens represent data stored in the expression, for example
numbers, variables, operators, and functions. To view / modify
the list of tokens used in the calculator see functions.py.
"""

import copy
from decimal import Decimal
from mathclasses import Quantity, Vector


class Token:
    """Token objects are data storage and data transformation elements."""

    def __init__(self, name, calc, pref, ltor, kind, ht=''):
        """The initialiser of the class.

        Arguments:
        name -- the name of the token (optional),
        calc -- the token's function,
        arg_num -- number of arguments of calc,
        pref -- the token's preference,
        ltor -- a truthy value, if tokens with the same pref
          should be calculated left-to-right, falsy otherwise,
        kind -- the kind of the token,
        ht -- the help text for the token (optional).
        """
        self.name = name
        self.calc = calc
        if kind in ('func', 'sign'):
            self.arg_num = 1
        elif kind in ('oper', 'doub'):
            self.arg_num = 2
        else:
            self.arg_num = 0
        self.pref = pref
        self.ltor = ltor
        self.kind = kind
        self.ht = ht

    @staticmethod
    def give(obj):
        """Return a function that returns obj.

        >>> f = Token.give(1024)
        >>> f()
        1024
        """
        def func():
            return copy.copy(obj)
        return func

    @staticmethod
    def wrap(obj, name='', ht=''):
        """Return a token that wraps obj."""
        kind = ''
        if isinstance(obj, str):
            kind = 'str'
        elif isinstance(obj, Decimal):
            kind = 'num'
        elif isinstance(obj, Quantity):
            kind = 'unit'
        elif isinstance(obj, Vector):
            kind = 'vec'
        return Token(name, Token.give(obj), 10, 0, kind, ht)

    def get_help(self):
        if self.kind == 'func':
            return f'{self.ht} function'
        if self.kind == 'oper':
            return f'{self.ht} operator'
        if self.kind == 'sign':
            return f'{self.ht} sign'
        return f'{self.ht}'

    def __repr__(self):
        """String representation of tokens."""
        if self.name:
            return self.name
        if self.arg_num == 0:
            return str(self.calc())
        if self.kind:
            return self.kind
        return '<?>'
