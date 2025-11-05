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

    pref_verbose = {
        'light': 0,
        'addition': 1,
        'mul-tion': 2,
        'normal': 3,
        'strong': 4,
        'strongest': 5,
        'static': 10,
    }

    ltor_verbose = {
        'ltor': 1,
        'rtol': 0,
    }

    def __init__(self, name, calc, pref, kind, ht='', order='regular',
                 closes=None):
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
        if kind in ('func', 'sign', 'open'):
            self.arg_num = 1
        elif kind in ('oper', 'doub'):
            self.arg_num = 2
        else:
            self.arg_num = 0
        if kind in ('func', 'doub'):
            self.ltor = 1 if order == 'regular' else 0
        else:
            self.ltor = 0 if order == 'regular' else 1
        if isinstance(pref, str):
            self.pref = Token.pref_verbose[pref]
        else:
            self.pref = pref
        self.kind = kind
        self.ht = ht
        self.closes = closes
        self.module = None

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
    def wrap(obj, name='', ht='Variable'):
        """Return a token that wraps obj."""
        return Token(name, Token.give(obj), 'static', 'var', ht)

    @staticmethod
    def with_alt(names, calc, pref, kind, ht='', order='regular'):
        """Create a token with alternative names (as a tuple)."""
        return (
            Token(name, calc, pref, kind, ht, order)
            for name in names
        )

    @staticmethod
    def wrap_with_alt(obj, names, ht='Variable', alt=''):
        """Create a token with wrap and alternative names (as a tuple)."""
        return (
            Token.wrap(obj, name, ht)
            for name in names
        )

    def get_help(self):
        kind_name = ''
        line1 = ''
        # Match self.kind
        if self.kind == 'func':
            kind_name = 'function'
        if self.kind == 'oper':
            kind_name = 'operator'
        if self.kind == 'sign':
            kind_name = 'sign'
        if self.kind == 'open':
            line1 = f'{self.name} ... {self.closes}   --  {self.ht} notation'
        if self.kind == 'clos':
            line1 = f'{self.closes} ... {self.name}  --  {self.ht} notation'
        # The default first line
        if not line1:
            line1 = f'{self.name}  --  {self.ht} {kind_name}'
        # The module
        if self.module is None:
            line2 = 'Part of the default setup'
        else:
            line2 = f'Part of the {self.module} module'
        return f'''
| {line1}
| {line2}
'''

    def __repr__(self):
        """String representation of tokens."""
        if self.name:
            return self.name
        if self.arg_num == 0:
            return str(self.calc())
        if self.kind:
            return self.kind
        return '<?>'
