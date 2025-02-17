"""This module contains a list of tokens that are loaded by default.

To register custom functions add corresponding tokens to the list.
"""

from token import Token

from decimal import Decimal
from mathclasses import Quantity, Vector
from mathclasses import glob_pi, glob_e


implicit_multiplication_name = '_implicit_'


exporttokens = {
    # These tokens are loaded by default
    Token('(', lambda: None, 10, 0, '(', 'Opening parhethesis'),
    Token(')', lambda: None, 10, 0, ')', 'Closing parenthesis'),
    Token('+', lambda a, b: a + b,  1, 0, 'oper', 'Addition'),
    Token('-', lambda a, b: a - b,  1, 0, 'oper', 'Subtraction'),
    Token('*', lambda a, b: a * b,  2, 0, 'oper', 'Multiplication'),
    Token(':', lambda a, b: a / b,  2, 0, 'oper', 'Inline division'),
    Token('^', lambda a, b: a ** b, 4, 1, 'oper', 'Exponentiation'),
    Token(' -', lambda a: -a,       4, 1, 'func', 'Negation'),
    Token(' +', lambda a: +a,       4, 1, 'func', 'Positition'),
    Token(implicit_multiplication_name, lambda a, b: a * b, 3, 1, 'oper',
          'Implicit multiplication'),
    Token(',', Vector.join,         0, 0, 'oper', 'Argument separator'),
    Token('/', lambda a, b: a / b,  0, 0, 'oper', 'Fraction bar'),
    Token('sqrt', lambda a: a ** Decimal('0.5'), 4, 1, 'func',
          'Square root'),
    Token.wrap(glob_pi, name='pi', ht='The number pi'),
    Token.wrap(glob_e,  name='e',  ht='The number e'),
    # Alternative names
    Token.wrap(glob_pi, name='π',  ht='The number pi'),
    Token('√', lambda a: a ** Decimal('0.5'), 4, 1, 'func',
          'Square root'),
    # Settings
    Token.wrap(0, name='_debug_', ht='Show debug messages setting'),
    Token.wrap('classic', name='_notation_', ht='Number notation setting'),
}
