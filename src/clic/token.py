"""This module provides a class for calculator tokens.

The tokens represent data stored in the expression, for example
numbers, variables, operators, and functions. To view / modify
the list of tokens used in the calculator see functions.py.
"""

import copy
import clic.mathclasses as mathclasses
from clic.mathclasses import (
    allow_unknown_name,
    generalize_array_input,
)


def define_meta(function):
    """A wrapper to provide functions in distant modules with math classes."""

    def wrapper(*args, **kwargs):
        return function(*args, **kwargs, META=mathclasses)

    return wrapper


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

    def __init__(self, name, calc, pref, kind, ht='', reverse=False,
                 closes=None, array_input=False, unknown_name_input=False,
                 use_meta=False):
        """The initialiser of the class.

        Arguments:
        name -- the name of the token,
        calc -- the token's function,
        pref -- the token's preference,
        kind -- the kind of the token,
        ht -- the help text for the token (optional),
        reverse -- whether a row of identical tokens should be calculated
          in reverse order (optional),
        closes -- the closing/opening pair of the token (optional),
        array_input -- whether to explicitly manage array calculations,
        unknown_name_input -- whether to allow unknown names to be used
          instead of text input (optional).
        """
        self.name = name
        if array_input:
            calc = generalize_array_input(calc)
        if unknown_name_input:
            calc = allow_unknown_name(calc)
        if use_meta:
            calc = define_meta(calc)
        self.calc = calc
        if kind in ('func', 'sign', 'open'):
            self.arg_num = 1
        elif kind in ('oper', 'doub'):
            self.arg_num = 2
        else:
            self.arg_num = 0
        if kind in ('func', 'doub'):
            self.ltor = 0 if reverse else 1
        else:
            self.ltor = 1 if reverse else 0
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
    def with_alt(names, calc, pref, kind, ht='', reverse=False, closes=None):
        """Create a token with alternative names (as a tuple)."""
        return (
            Token(name, calc, pref, kind, ht, reverse, closes)
            for name in names
        )

    @staticmethod
    def from_config(names, calc, kind, ht='', options={}):
        """Create a tuple of tokens using configuration setup."""
        pref, kind = kind.split(' ')
        return (
            Token(name, calc, pref, kind, ht, **options)
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
            if self.name.startswith(' '):
                line1 = f'UNARY{self.name}  --  {self.ht} {kind_name}'
            else:
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

    def __str__(self):
        """String representation of tokens."""
        if self.name:
            return self.name
        if self.arg_num == 0:
            return str(self.calc())
        if self.kind:
            return self.kind
        return '<?>'

    def __repr__(self):
        return str(self)
