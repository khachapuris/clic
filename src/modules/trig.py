"""Module with trigonometric functions."""

from decimal import Decimal
from copy import deepcopy
from clic.mathclasses import Quantity, glob_pi

DEGREE = Quantity(glob_pi / Decimal(180), {'rad': 1})
RADIAN = Quantity(Decimal(1), {'rad': 1})


exporttokens = [
    [['sin'], Quantity.sin, 'normal func', 'Sine'],
    [['cos'], Quantity.cos, 'normal func', 'Cosine'],
    [['tan', 'tg'], Quantity.tan, 'normal func', 'Tangent'],
    [['arcsin'], Quantity.arcsin, 'normal func', 'Angle by sine'],
    [['arccos'], Quantity.arccos, 'normal func', 'Angle by cosine'],
    [['arctan', 'arctg'], Quantity.arctan, 'normal func', 'Angle by tangent'],
    [['sin ^'], lambda a, b: Quantity.sin(b) ** a, 'normal doub', ''],
    [['cos ^'], lambda a, b: Quantity.cos(b) ** a, 'normal doub', ''],
    [['tan ^', 'tg ^'], lambda a, b: Quantity.tan(b) ** a, 'normal doub', ''],
    [['°', 'deg'], lambda: deepcopy(DEGREE), 'static var', 'Degree'],
    [['rad'], lambda: deepcopy(RADIAN),      'static var', 'Radian'],
]

exportmappings = {
    'deg': '°',
}
