"""Module with trigonometric functions."""

from token import Token

from decimal import Decimal
from mathclasses import Quantity, glob_pi


exporttokens = [
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
]
