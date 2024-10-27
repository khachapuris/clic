"""This module contains a dictionary with units used in the calculator.

The user can add new items or modify existing units. For readability,
quantity-defining functions are provided, but the units can be any
Quantity objects.
"""

from decimal import Decimal
from mathclasses import Quantity, glob_pi


def one(unit):
    """Return a quantity of type '1 unit'."""
    return Quantity(Decimal(1), {unit: 1})


def few(a, unit):
    """Return a quantity of type 'a units'."""
    return Quantity(a, {unit: 1})


def der(kg, m, s, a):
    """Return a unit derived from basic si units."""
    return Quantity(Decimal(1), {'kg': kg, 'm': m, 's': s, 'a': a})


units = dict()

prefixes = {-9: 'n', -6: 'μ', -3: 'm', -2: 'c', -1: 'd',
            0: '', 1: 'da', 2: 'h', 3: 'k', 6: 'M', 9: 'G'}


def si(unit, name, exps=None):
    """Add SI units to the units dictionary.

    Arguments:
    unit -- the unit,
    name -- the name of that unit,
    exps -- a list of numbers representing prefixes.
    """
    global units
    if not exps:
        exps = [-9, -6, -3, 0, 3, 6, 9]
    for exp in exps:
        name1 = prefixes[exp] + name
        unit1 = unit * (Decimal('10') ** exp)
        units.update({name1: unit1})


# Add SI units

si(few(Decimal('0.001'), 'kg'), 'g', [-9, -6, -3, 0, 3])  # gramm
si(few(Decimal('1000'),  'kg'), 't', [0, 3, 6, 9])        # tonne
si(one('m'), 'm', [-9, -6, -3, -2, -1, 0, 3])             # meter
si(one('s'), 's', [-9, -6, -3, 0])                        # second
si(one('A'), 'A')                                         # ampere
si(one('K'), 'K')                                         # kelvin
si(one('mol'), 'mol')                                     # mole
si(one('rad'), 'rad', [0])                                # radian

si(der(0,  0, -1,  0), 'Hz')  # herz
si(der(1,  1, -2,  0), 'N')   # newton
si(der(1, -1, -2,  0), 'Pa', [-9, -6, -3, 0, 2, 3, 6, 9])  # pascal
si(der(1,  2, -2,  0), 'J')   # joule
si(der(1,  2, -3,  0), 'W')   # watt
si(der(0,  0,  1,  1), 'C')   # couloumb
si(der(1,  2, -3, -1), 'V')   # volt
si(der(1,  2, -3, -2), 'Ω')   # ohm
si(der(0,  0, -1,  0), 'Bq', [0, 3, 6, 9])  # becquerrel
si(der(0,  2, -2,  0), 'Gy', [-6, -3, -2, 0])  # gray

si(Quantity(Decimal('0.001'), {'m': 3}), 'l', [-3, 0])    # litre
si(Quantity(Decimal('10000'), {'m': 2}), 'a', [2])        # hectare

units |= {
    'min': few(Decimal(60), 's'),
    'h': few(Decimal(3600), 's'),
    'deg': few(glob_pi / Decimal(180), 'rad')
}
