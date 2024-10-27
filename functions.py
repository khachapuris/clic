"""This module contains a list of functions/operators for the calculator.

To register custom functions add corresponding tokens to the list.
"""

from token import Token

from decimal import Decimal
from mathclasses import Quantity, Vector
import mathfunctions as mf

import symbols as smbs


functions = [
    # Essential tokens
    Token('+', lambda a, b: a + b,  2, 1, 0, 'oper', 'Addition'),
    Token('-', lambda a, b: a - b,  2, 1, 0, 'oper', 'Subtraction'),
    Token('*', lambda a, b: a * b,  2, 2, 0, 'oper', 'Multiplication'),
    Token(':', lambda a, b: a / b,  2, 2, 0, 'oper', 'Inline division'),
    Token('^', lambda a, b: a ** b, 2, 4, 1, 'oper', 'Exponentiation'),
    Token(' -', lambda a: -a,       1, 4, 1, 'func', 'Negation'),
    Token(' +', lambda a: +a,       1, 4, 1, 'func', 'Positition'),
    Token(smbs.sv['implicit'], lambda a, b: a * b, 2, 3, 1, 'oper',
          'Implicit multiplication'),

    # Default tokens
    Token('!', mf.factorial,         1, 4, 0, 'sign', 'Factorial'),
    Token(',', Vector.join,          2, 0, 0, 'oper', 'Comma'),
    Token('/', lambda a, b: a / b,   2, 0, 0, 'oper', 'Fraction bar'),
    Token('mod', lambda a, b: a % b, 2, 2, 0, 'oper', 'Modulo'),
    Token('sin',    Quantity.sin,    1, 3, 1, 'func', 'Sine'),
    Token('cos',    Quantity.cos,    1, 3, 1, 'func', 'Cosine'),
    Token('tan',    Quantity.tan,    1, 3, 1, 'func', 'tangent'),
    Token('arcsin', Quantity.arcsin, 1, 3, 1, 'func', 'Angle by sine'),
    Token('arccos', Quantity.arccos, 1, 3, 1, 'func', 'Angle by cosine'),
    Token('arctan', Quantity.arctan, 1, 3, 1, 'func', 'Angle by tangent'),
    Token('sin ^', lambda a, b: Quantity.sin(a) ** b, 2, 3, 1, 'func'),
    Token('cos ^', lambda a, b: Quantity.cos(a) ** b, 2, 3, 1, 'func'),
    Token('tan ^', lambda a, b: Quantity.tan(a) ** b, 2, 3, 1, 'func'),
    Token('sqrt', lambda a: a ** Decimal('0.5'),      1, 4, 1, 'func',
          'Square root'),

    # Place your custom tokens here
]


links = {
    # Alternative names for tokens
    ('√', 'sqrt'),
    ('tg', 'tan'),
    ('arctg', 'arctan'),
}
