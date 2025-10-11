"""Module with trigonometric functions."""

from token import Token

from decimal import Decimal
from mathclasses import Quantity, glob_pi


exporttokens = [
    Token('sin',    Quantity.sin,    'normal', 'func', 'Sine'),
    Token('cos',    Quantity.cos,    'normal', 'func', 'Cosine'),
    *Token.with_alt(['tan', 'tg'],
                    Quantity.tan,    'normal', 'func', 'Tangent'),
    Token('arcsin', Quantity.arcsin, 'normal', 'func', 'Angle by sine'),
    Token('arccos', Quantity.arccos, 'normal', 'func', 'Angle by cosine'),
    *Token.with_alt(['arctan', 'arctg'],
                    Quantity.arctan, 'normal', 'func', 'Angle by tangent'),
    Token('sin ^', lambda a, b: Quantity.sin(b) ** a, 'normal', 'doub'),
    Token('cos ^', lambda a, b: Quantity.cos(b) ** a, 'normal', 'doub'),
    *Token.with_alt(['tan ^', 'tg ^'],
                    lambda a, b: Quantity.tan(b) ** a, 'normal', 'doub'),
    *Token.wrap_with_alt(Quantity(glob_pi / Decimal(180), {'rad': 1}),
                         names=['°', 'deg'], ht='Degree'),
    Token.wrap(Quantity(Decimal(1), {'rad': 1}), name='rad', ht='Radian'),
]

exportmappings = {
    'deg': '°',
}
