"""Module with trigonometric functions."""

from token import Token

from decimal import Decimal
from mathclasses import Quantity, glob_pi


exporttokens = [
    # Default tokens
    Token('sin',    Quantity.sin,    'normal', 'func', 'Sine'),
    Token('cos',    Quantity.cos,    'normal', 'func', 'Cosine'),
    Token('tan',    Quantity.tan,    'normal', 'func', 'Tangent'),
    Token('arcsin', Quantity.arcsin, 'normal', 'func', 'Angle by sine'),
    Token('arccos', Quantity.arccos, 'normal', 'func', 'Angle by cosine'),
    Token('arctan', Quantity.arctan, 'normal', 'func', 'Angle by tangent'),
    Token('sin ^', lambda a, b: Quantity.sin(b) ** a, 'normal', 'doub'),
    Token('cos ^', lambda a, b: Quantity.cos(b) ** a, 'normal', 'doub'),
    Token('tan ^', lambda a, b: Quantity.tan(b) ** a, 'normal', 'doub'),
    Token.wrap(Quantity(glob_pi / Decimal(180), {'rad': 1}), name='deg',
               ht='Degree'),
    Token.wrap(Quantity(Decimal(1), {'rad': 1}), name='rad', ht='Radian'),
    # Alternative names
    Token('tg',    Quantity.tan,     'normal', 'func', 'Tangent'),
    Token('arctg', Quantity.arctan,  'normal', 'func', 'Angle by tangent'),
    Token('tg ^', lambda a, b: Quantity.tan(b) ** a, 'normal', 'doub'),
    Token.wrap(Quantity(glob_pi / Decimal(180), {'rad': 1}), name='°',
               ht='Degree'),
]
