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


def derived(units):
    """Return a unit derived from units."""
    return Quantity(Decimal(1), units)


units = dict()

prefixes = {-9: 'n', -6: 'μ', -3: 'm', -2: 'c', -1: 'd',
            0: '', 1: 'da', 2: 'h', 3: 'k', 6: 'M', 9: 'G'}


def add_si(unit, name, exps=[-9, -6, -3, 0, 3, 6, 9]):
    """Add SI units to the units dictionary.

    Arguments:
    unit -- the unit,
    name -- the name of that unit,
    exps -- a list of numbers representing prefixes.
    """
    global units
    for exp in exps:
        name1 = prefixes[exp] + name
        unit1 = unit * (Decimal('10') ** exp)
        units.update({name1: unit1})


gramm = few(Decimal('0.001'), 'kg')
tonne = few(Decimal('1000'), 'kg')

add_si(gramm, 'g', [3, 0, -3, -6, -9])
add_si(tonne, 't', [9, 6, 3, 0])
add_si(one('m'), 'm', [3, 0, -1, -2, -3, -6, -9])
add_si(one('s'), 's', [0, -3, -6, -9])
add_si(one('A'), 'A')
add_si(one('K'), 'K')
add_si(one('mol'), 'mol')

litre = Quantity(Decimal('0.001'), {'m': 3})
herz = derived({'s': -1})
newton = derived({'kg': 1, 'm': 1, 's': -2})
pascal = derived({'kg': 1, 'm': -1, 's': -2})
joule = derived({'kg': 1, 'm': 2, 's': -2})
watt = derived({'kg': 1, 'm': 2, 's': -3})
coulomb = derived({'s': 1, 'A': 1})
volt = derived({'kg': 1, 'm': 2, 's': -3, 'A': -1})
ohm = derived({'kg': 1, 'm': 2, 's': -3, 'A': -2})
becquerrel = derived({'s': -1})
gray = derived({'m': 2, 's': -1})

add_si(litre, 'l', [0, -3])
add_si(herz, 'Hz')
add_si(newton, 'N')
add_si(pascal, 'Pa', [9, 6, 3, 2, 0, -3, -6, -9])
add_si(joule, 'J')
add_si(watt, 'W')
add_si(coulomb, 'C')
add_si(volt, 'V')
add_si(ohm, 'Ω')
add_si(becquerrel, 'Bq')
add_si(gray, 'Gy')

units |= {
    'min': few(Decimal(60), 's'),
    'h': few(Decimal(3600), 's'),
    'rad': one('rad'),
    'deg': few(glob_pi / Decimal(180), 'rad')
}
