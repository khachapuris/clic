"""Module with SI units."""

from decimal import Decimal

D = Decimal


def lazy_quantity(*args, **kwargs):
    """Return a function that will create a new quantity when called."""

    def give_quantity(META):
        quantity = META.Quantity(*args, **kwargs)
        return quantity

    return give_quantity


CLIC_TOKENS = []

prefixes = {-9: 'n', -6: 'mc', -3: 'm', -2: 'c', -1: 'd',
            0: '', 1: 'da', 2: 'h', 3: 'k', 6: 'M', 9: 'G'}

verbal = {-9: 'nano', -6: 'micro', -3: 'milli', -2: 'centi', -1: 'deci',
          0: '', 1: 'deca', 2: 'hecto', 3: 'kilo', 6: 'mega', 9: 'giga'}


def si(ht, numerical, units, names, exps=None, ht_overwrite=None):
    """Append SI units to the exporttokens list of the module.

    Arguments:
    numerical -- the numerical part of the quantity,
    units -- the units part of the quantity,
    name -- the name of that unit for the calculator,
    exps -- a list of numbers representing prefixes,
    ht -- the name of the unit for the helptext (optional),
    ht_overwrite -- a custom overwrite of the helptext (optional).
    """
    if isinstance(units, tuple):
        units = dict(zip(('kg', 'm', 's', 'A'), units))
    if not exps:
        exps = [-9, -6, -3, 0, 3, 6, 9]
    for exp in exps:
        new_names = [prefixes[exp] + name for name in names]
        new_numerical = numerical * (Decimal('10') ** exp)
        new_ht = 'One ' + verbal[exp] + ht
        if ht_overwrite:
            new_ht = ht_overwrite
        CLIC_TOKENS.append([
            new_names,
            lazy_quantity(new_numerical, units=units),
            'static var',
            new_ht,
            {'use_meta': True}
        ])
        # Alternative micro prefix
        if exp == -6:
            new_names = ['μ' + name for name in names]
            CLIC_TOKENS.append([
                new_names,
                lazy_quantity(new_numerical, units=units),
                'static var',
                new_ht,
                {'use_meta': True}
            ])


# Add SI units

si('gramm',  D('0.001'), {'kg': 1},  ['g'], [-9, -6, -3, 0, 3])
si('tonne',  D('1000'),  {'kg': 1},  ['t'], [0, 3, 6, 9])
si('meter',  D('1'), {'m': 1},   ['m'], [-9, -6, -3, -2, -1, 0, 3])
si('second', D('1'), {'s': 1},   ['s'], [-9, -6, -3, 0])
si('ampere', D('1'), {'A': 1},   ['A'])
si('kelvin', D('1'), {'K': 1},   ['K'])
si('mole',   D('1'), {'mol': 1}, ['mol'])
si('radian', D('1'), {'rad': 1}, ['rad'], [0])

si('herz',       D('1'), (0,  0, -1,  0), ['Hz'])
si('newton',     D('1'), (1,  1, -2,  0), ['N'])
si('joule',      D('1'), (1,  2, -2,  0), ['J'])
si('watt',       D('1'), (1,  2, -3,  0), ['W'])
si('couloumb',   D('1'), (0,  0,  1,  1), ['C'])
si('volt',       D('1'), (1,  2, -3, -1), ['V'])
si('ohm',        D('1'), (1,  2, -3, -2), ['ohm'])
si('ohm',        D('1'), (1,  2, -3, -2), ['Ω'])
si('pascal',     D('1'), (1, -1, -2,  0), ['Pa'], [-9, -6, -3, 0, 2, 3, 6, 9])
si('becquerrel', D('1'), (0,  0, -1,  0), ['Bq'], [0, 3, 6, 9])
si('gray',       D('1'), (0,  2, -2,  0), ['Gy'], [-6, -3, -2, 0])

si('litre', D('0.001'), {'m': 3}, ['l', 'L'], [-3, 0])
si('hectare', D('10000'), {'m': 2}, ['a'], [2], ht_overwrite='One hectare')

# These tokens can be moved to 'time' module later
si('minute', D('60'),       {'s': 1}, ['min'],  [0])
si('hour',   D('3600'),     {'s': 1}, ['h'],    [0])
si('hour',   D('3600'),     {'s': 1}, ['hr'],   [0])
si('day',    D('86400'),    {'s': 1}, ['day'],  [0])
si('year',   D('31557600'), {'s': 1}, ['year'], [0])

CLIC_MAPPINGS = {
    'ohm': 'Ω', 'micro': 'μ',
}
