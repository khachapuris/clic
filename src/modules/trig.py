"""Module with trigonometric functions."""

from decimal import Decimal


# Use the META variable to get Quantity functions
sin = (lambda a, META: META.Quantity.sin(a))
cos = (lambda a, META: META.Quantity.cos(a))
tan = (lambda a, META: META.Quantity.tan(a))
arcsin = (lambda a, META: META.Quantity.arcsin(a))
arccos = (lambda a, META: META.Quantity.arccos(a))
arctan = (lambda a, META: META.Quantity.arctan(a))


def sin_exp(a, b, META):
    """Exponentiation shorthand for the sine function."""
    if a > Decimal('0'):
        return META.Quantity.sin(b) ** a
    if a == Decimal('-1'):
        return META.Quantity.arcsin(b)
    raise ValueError('raising function to negative exponent')


def cos_exp(a, b, META):
    """Exponentiation shorthand for the cosine function."""
    if a > Decimal('0'):
        return META.Quantity.cos(b) ** a
    if a == Decimal('-1'):
        return META.Quantity.arccos(b)
    raise ValueError('raising function to negative exponent')


def tan_exp(a, b, META):
    """Exponentiation shorthand for the tangent function."""
    if a > Decimal('0'):
        return META.Quantity.tan(b) ** a
    if a == Decimal('-1'):
        return META.Quantity.arctan(b)
    raise ValueError('raising function to negative exponent')


def degree(META):
    """Return a quantity representing one degree."""
    return META.Quantity(META.glob_pi / Decimal(180), {'rad': 1})


def radian(META):
    """Return a quantity representing one radian."""
    return META.Quantity(Decimal(1), {'rad': 1})


CLIC_TOKENS = [
    [['tan', 'tg'], tan, 'normal func', 'Tangent', {'use_meta': True}],
    [['sin'], sin,       'normal func', 'Sine',    {'use_meta': True}],
    [['cos'], cos,       'normal func', 'Cosine',  {'use_meta': True}],
    [['arctan',
      'arctg'], arctan, 'normal func', 'Angle by tangent', {'use_meta': True}],
    [['arcsin'], arcsin, 'normal func', 'Angle by sine',   {'use_meta': True}],
    [['arccos'], arccos, 'normal func', 'Angle by cosine', {'use_meta': True}],
    [['tan ^',
      'tg ^'], tan_exp,          'normal doub', '', {'use_meta': True}],
    [['sin ^'], sin_exp,         'normal doub', '', {'use_meta': True}],
    [['cos ^'], cos_exp,         'normal doub', '', {'use_meta': True}],
    [['°', 'deg'], degree, 'static var', 'Degree', {'use_meta': True}],
    [['rad'], radian,      'static var', 'Radian', {'use_meta': True}],
]

CLIC_MAPPINGS = {
    'deg': '°',
}
