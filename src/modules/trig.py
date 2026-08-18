"""Module with trigonometric functions."""

from decimal import Decimal


# Use the META variable to get Quantity functions
sin = (lambda a, META: META.Quantity.sin(a))
cos = (lambda a, META: META.Quantity.cos(a))
tan = (lambda a, META: META.Quantity.tan(a))
csc = (lambda a, META: META.Quantity.csc(a))
sec = (lambda a, META: META.Quantity.sec(a))
cot = (lambda a, META: META.Quantity.cot(a))
arcsin = (lambda a, META: META.Quantity.arcsin(a))
arccos = (lambda a, META: META.Quantity.arccos(a))
arctan = (lambda a, META: META.Quantity.arctan(a))
arccsc = (lambda a, META: META.Quantity.arccsc(a))
arcsec = (lambda a, META: META.Quantity.arcsec(a))
arccot = (lambda a, META: META.Quantity.arccot(a))


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


def csc_exp(a, b, META):
    """Exponentiation shorthand for the sine function."""
    if a > Decimal('0'):
        return META.Quantity.csc(b) ** a
    if a == Decimal('-1'):
        return META.Quantity.arccsc(b)
    raise ValueError('raising function to negative exponent')


def sec_exp(a, b, META):
    """Exponentiation shorthand for the cosine function."""
    if a > Decimal('0'):
        return META.Quantity.sec(b) ** a
    if a == Decimal('-1'):
        return META.Quantity.arcsec(b)
    raise ValueError('raising function to negative exponent')


def cot_exp(a, b, META):
    """Exponentiation shorthand for the tangent function."""
    if a > Decimal('0'):
        return META.Quantity.cot(b) ** a
    if a == Decimal('-1'):
        return META.Quantity.arccot(b)
    raise ValueError('raising function to negative exponent')


def degree(META):
    """Return a quantity representing one degree."""
    return META.Quantity(META.glob_pi / Decimal(180), {'rad': 1})


def radian(META):
    """Return a quantity representing one radian."""
    return META.Quantity(Decimal(1), {'rad': 1})


flag = {'use_meta': True, 'array_input': True}


CLIC_TOKENS = [
    [['sin'], sin,          'normal func', 'Sine',      flag],
    [['cos'], cos,          'normal func', 'Cosine',    flag],
    [['tan', 'tg'], tan,    'normal func', 'Tangent',   flag],
    [['csc', 'cosec'], csc, 'normal func', 'Cosecant',  flag],
    [['sec'], sec,          'normal func', 'Secant',    flag],
    [['cot', 'ctg'], cot,   'normal func', 'Cotangent', flag],
    [['arcsin'], arcsin, 'normal func', 'Angle by sine',   flag],
    [['arccos'], arccos, 'normal func', 'Angle by cosine', flag],
    [['arctan', 'arctg'], arctan,    'normal func', 'Angle by tangent',  flag],
    [['arccsc', 'arccosec'], arccsc, 'normal func', 'Angle by cosecant', flag],
    [['arcsec'], arcsec,             'normal func', 'Angle by secant',   flag],
    [['arccot', 'arcctg'], arccot,   'normal func', 'Angle by tangent',  flag],
    [['sin ^'], sin_exp,            'normal doub', '', flag],
    [['cos ^'], cos_exp,            'normal doub', '', flag],
    [['tan ^', 'tg ^'], tan_exp,    'normal doub', '', flag],
    [['csc ^', 'cosec ^'], csc_exp, 'normal doub', '', flag],
    [['sec ^'], sec_exp,            'normal doub', '', flag],
    [['cot ^', 'ctg ^'], cot_exp,   'normal doub', '', flag],
    [['°', 'deg'], degree, 'static var', 'Degree', flag],
    [['rad'], radian,      'static var', 'Radian', flag],
]

CLIC_MAPPINGS = {
    'deg': '°',
}
