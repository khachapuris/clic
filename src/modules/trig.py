"""Module with trigonometric functions."""

from decimal import Decimal


# Use the META variable to get Quantity functions
degree = (lambda META: META.Quantity(META.glob_pi / Decimal(180), {'rad': 1}))
radian = (lambda META: META.Quantity(Decimal(1), {'rad': 1}))
sin = (lambda a, META: META.Quantity.sin(a))
cos = (lambda a, META: META.Quantity.cos(a))
tan = (lambda a, META: META.Quantity.tan(a))
arcsin = (lambda a, META: META.Quantity.arcsin(a))
arccos = (lambda a, META: META.Quantity.arccos(a))
arctan = (lambda a, META: META.Quantity.arctan(a))


def sin_exp(a, b, META):
    return META.Quantity.sin(b) ** a


def cos_exp(a, b, META):
    return META.Quantity.cos(b) ** a


def tan_exp(a, b, META):
    return META.Quantity.tan(b) ** a


exporttokens = [
    [['sin'], sin,       'normal func', 'Sine', {'use_meta': True}],
    [['cos'], cos,       'normal func', 'Cosine', {'use_meta': True}],
    [['tan', 'tg'], tan, 'normal func', 'Tangent', {'use_meta': True}],
    [['arcsin'], arcsin, 'normal func', 'Angle by sine', {'use_meta': True}],
    [['arccos'], arccos, 'normal func', 'Angle by cosine', {'use_meta': True}],
    [['arctan',
      'arctg'], arctan, 'normal func', 'Angle by tangent', {'use_meta': True}],
    [['sin ^'], sin_exp,         'normal doub', '', {'use_meta': True}],
    [['cos ^'], cos_exp,         'normal doub', '', {'use_meta': True}],
    [['tan ^', 'tg ^'], tan_exp, 'normal doub', '', {'use_meta': True}],
    [['°', 'deg'], degree, 'static var', 'Degree', {'use_meta': True}],
    [['rad'], radian,      'static var', 'Radian', {'use_meta': True}],
]

exportmappings = {
    'deg': '°',
}
