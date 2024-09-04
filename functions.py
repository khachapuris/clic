from token import Token

from decimal import Decimal
from mathclasses import Quantity, Vector
import mathfunctions as mf

"""This module contains a list of functions/operators for the calculator.

To register custom functions add corresponding tokens to the list.
"""


functions = [
    # these are the default tokens
    Token(',', Vector.join,         2, 0, 0, 'oper'),
    Token('+', lambda a, b: a + b,  2, 1, 0, 'oper'),
    Token('-', lambda a, b: a - b,  2, 1, 0, 'oper'),
    Token('*', lambda a, b: a * b,  2, 2, 0, 'oper'),
    Token(':', lambda a, b: a / b,  2, 2, 0, 'oper'),
    Token('/', lambda a, b: a / b,  2, 0, 0, 'oper'),
    Token('^', lambda a, b: a ** b, 2, 3, 1, 'oper'),
    Token('mod', lambda a, b: a % b,   2, 2, 0, 'oper'),
    Token('_neg_', lambda a: -a,       1, 3, 1, 'oper'),
    Token('_dot_', lambda a, b: a * b, 2, 3, 1, 'oper'),
    Token('sin',    Quantity.sin,    1, 3, 1, 'func'),
    Token('cos',    Quantity.cos,    1, 3, 1, 'func'),
    Token('tan',    Quantity.tan,    1, 3, 1, 'func'),
    Token('arcsin', Quantity.arcsin, 1, 3, 1, 'func'),
    Token('arccos', Quantity.arccos, 1, 3, 1, 'func'),
    Token('arctan', Quantity.arctan, 1, 3, 1, 'func'),
    Token('sin ^', lambda a, b: Quantity.sin(a) ** b, 2, 3, 1, 'func'),
    Token('cos ^', lambda a, b: Quantity.sin(a) ** b, 2, 3, 1, 'func'),
    Token('tan ^', lambda a, b: Quantity.sin(a) ** b, 2, 3, 1, 'func'),

    # place your custom tokens here
    Token('!', mf.factorial, 1, 4, 0, 'sign'),
]
