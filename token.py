"""This module provides a class for calculator tokens.

The tokens represent data stored in the expression, for example
numbers, variables, operators, and functions. To view / modify
the list of tokens used in the calculator see functions.py.
"""

import copy


class Token:
    """Token objects are data storage and data transformation elements."""

    def __init__(self, name, calc, arg_num, pref, ltor, kind='', helptext=''):
        """The initialiser of the class.

        Arguments:
        calc -- the token's function,
        arg_num -- number of arguments of calc,
        pref -- the token's preference,
        ltor -- a truthy value, if tokens with the same pref
          should be calculated left-to-right, falsy otherwise,
        kind -- the kind of the token (optional),
        name -- the name of the token (optional).
        """
        self.name = name
        self.calc = calc
        self.arg_num = arg_num
        self.pref = pref
        self.ltor = ltor
        self.kind = kind
        self.help = helptext

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

    def get_help(self):
        if self.kind == 'func':
            return f'{self.help} function'
        if self.kind == 'oper':
            return f'{self.help} operator'
        if self.kind == 'sign':
            return f'{self.help} sign'

    def __repr__(self):
        """String representation of tokens."""
        if self.name:
            return self.name
        if self.arg_num == 0:
            return str(self.calc())
        if self.kind:
            return self.kind
        return '<?>'
