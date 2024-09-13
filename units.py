"""This module contains a dictionary with units used in the calculator.

The user can add new items or modify existing units. For readability,
quantity-defining functions are provided, but the units can be any
Quantity objects.
"""

from decimal import Decimal
from mathclasses import Quantity, glob_pi


def one(unit):
    return Quantity(Decimal(1), {unit: 1})


def q(a, unit):
    return Quantity(a, {unit: 1})


units = {
    'rad': one('rad'), 'm': one('m'), 's': one('s'), 'kg': one('kg'),
    'deg': q(glob_pi / Decimal(180), 'rad'),
}
