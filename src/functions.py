"""This module contains a dictionary with modules. Each module
contains a list of functions/operators for the calculator.
Modules can be loaded from the calculator with the 'load' command;
the default module is loaded by default.

To register custom functions add corresponding tokens to the desired module.
"""

from token import Token

from decimal import Decimal
from mathclasses import Quantity, Vector
from mathclasses import glob_pi, glob_e
import mathfunctions as mf

import symbols as smbs

from si import units as si_units


modules = {
    'default': [
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
        Token(smbs.sv['implicit'], lambda a, b: a * b, 3, 1, 'oper',
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

        # Place your custom tokens here
    ],
    'trig': [
        # Default tokens
        Token('sin',    Quantity.sin,    3, 1, 'func', 'Sine'),
        Token('cos',    Quantity.cos,    3, 1, 'func', 'Cosine'),
        Token('tan',    Quantity.tan,    3, 1, 'func', 'Tangent'),
        Token('arcsin', Quantity.arcsin, 3, 1, 'func', 'Angle by sine'),
        Token('arccos', Quantity.arccos, 3, 1, 'func', 'Angle by cosine'),
        Token('arctan', Quantity.arctan, 3, 1, 'func', 'Angle by tangent'),
        Token('sin ^', lambda a, b: Quantity.sin(b) ** a, 3, 1, 'doub'),
        Token('cos ^', lambda a, b: Quantity.cos(b) ** a, 3, 1, 'doub'),
        Token('tan ^', lambda a, b: Quantity.tan(b) ** a, 3, 1, 'doub'),
        Token.wrap(Quantity(glob_pi / Decimal(180), {'rad': 1}), name='deg',
                   ht='Degree'),
        Token.wrap(Quantity(Decimal(1), {'rad': 1}), name='rad', ht='Radian'),
        # Alternative names
        Token('tg',    Quantity.tan,     3, 1, 'func', 'Tangent'),
        Token('arctg', Quantity.arctan,  3, 1, 'func', 'Angle by tangent'),
        Token.wrap(Quantity(glob_pi / Decimal(180), {'rad': 1}), name='°',
                   ht='Degree'),
    ],
    'comb': [
        Token('!', mf.factorial,    4, 0, 'sign', 'Factorial'),
        Token('P', mf.permutations, 3, 1, 'func', 'Number of permutations'),
        Token('C', mf.combinations, 3, 1, 'func', 'Number of combinations'),
    ],
    'numthe': [
        Token('mod', lambda a, b: a % b, 2, 0, 'oper', 'Modulo'),
    ],
    'chem': [
        Token('M', mf.mass, 3, 1, 'func', 'Molar mass of compound'),
    ],
    'si': si_units,
}


links = {
    # Alternative names for tokens
    ('tg', 'tan'),
    ('arctg', 'arctan'),
}
