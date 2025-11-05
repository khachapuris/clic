"""Module with SI units."""

from decimal import Decimal
from mathclasses import Quantity

from token import Token


def one(unit):
    """Return a quantity of type '1 unit'."""
    return Quantity(Decimal(1), {unit: 1})


def few(a, unit):
    """Return a quantity of type 'a units'."""
    return Quantity(a, {unit: 1})


def der(kg, m, s, a):
    """Return a unit derived from basic si units."""
    return Quantity(Decimal(1), {'kg': kg, 'm': m, 's': s, 'A': a})


exporttokens = []

prefixes = {-9: 'n', -6: 'mc', -3: 'm', -2: 'c', -1: 'd',
            0: '', 1: 'da', 2: 'h', 3: 'k', 6: 'M', 9: 'G'}

verbal = {-9: 'nano', -6: 'micro', -3: 'milli', -2: 'centi', -1: 'deci',
          0: '', 1: 'deca', 2: 'hecto', 3: 'kilo', 6: 'mega', 9: 'giga'}


def si(unit, name, exps=None, ht='unit', ht_overwrite=None):
    """Add SI units to the units dictionary.

    Arguments:
    unit -- the unit,
    name -- the name of that unit,
    exps -- a list of numbers representing prefixes.
    """
    if not exps:
        exps = [-9, -6, -3, 0, 3, 6, 9]
    for exp in exps:
        name1 = prefixes[exp] + name
        unit1 = unit * (Decimal('10') ** exp)
        ht1 = 'One ' + verbal[exp] + ht
        if ht_overwrite:
            ht1 = ht_overwrite
        exporttokens.append(Token.wrap(unit1, name=name1, ht=ht1))
        # Alternative micro prefix
        if exp == -6:
            name1 = 'μ' + name
            exporttokens.append(Token.wrap(unit1, name=name1, ht=ht1))


# Add SI units

si(few(Decimal('0.001'), 'kg'), 'g', [-9, -6, -3, 0, 3],  ht='gramm')
si(few(Decimal('1000'),  'kg'), 't', [0, 3, 6, 9],        ht='tonne')
si(one('m'), 'm', [-9, -6, -3, -2, -1, 0, 3],             ht='meter')
si(one('s'), 's', [-9, -6, -3, 0],                        ht='second')
si(one('A'), 'A',                                         ht='ampere')
si(one('K'), 'K',                                         ht='kelvin')
si(one('mol'), 'mol',                                     ht='mole')
si(one('rad'), 'rad', [0],                                ht='radian')

si(der(0,  0, -1,  0), 'Hz',  ht='herz')
si(der(1,  1, -2,  0), 'N',   ht='newton')
si(der(1,  2, -2,  0), 'J',   ht='joule')
si(der(1,  2, -3,  0), 'W',   ht='watt')
si(der(0,  0,  1,  1), 'C',   ht='couloumb')
si(der(1,  2, -3, -1), 'V',   ht='volt')
si(der(1,  2, -3, -2), 'ohm', ht='ohm')
si(der(1,  2, -3, -2), 'Ω',   ht='ohm')
si(der(1, -1, -2,  0), 'Pa', [-9, -6, -3, 0, 2, 3, 6, 9], ht='pascal')
si(der(0,  0, -1,  0), 'Bq', [0, 3, 6, 9],                ht='becquerrel')
si(der(0,  2, -2,  0), 'Gy', [-6, -3, -2, 0],             ht='gray')

si(Quantity(Decimal('0.001'), {'m': 3}), 'l', [-3, 0],    ht='litre')
si(Quantity(Decimal('10000'), {'m': 2}), 'a', [2], ht_overwrite='One hectare')

# These tokens can be moved to 'time' module later
si(Quantity(Decimal('60'),    {'s': 1}), 'min', [0],      ht='minute')
si(Quantity(Decimal('3600'),  {'s': 1}), 'h',   [0],      ht='hour')
si(Quantity(Decimal('86400'), {'s': 1}), 'day', [0],      ht='day')
si(Quantity(Decimal('31557600'), {'s': 1}), 'year', [0],  ht='year')


exportmappings = {
    'ohm': 'Ω', 'micro': 'μ',
}
