"""Module with units that are not a part of SI."""

from decimal import Decimal
from copy import deepcopy
from clic.mathclasses import Quantity


# Helper functions

def one(unit):
    """Return a quantity of type '1 unit'."""
    return Quantity(Decimal(1), {unit: 1})


def few(a, unit):
    """Return a quantity of type 'a units'."""
    return Quantity(a, {unit: 1})


def der(kg, m, s, a):
    """Return a unit derived from basic si units."""
    return Quantity(Decimal(1), {'kg': kg, 'm': m, 's': s, 'A': a})


# Temperature functions

def absolute_fahrenheit(fahrenheits):
    """Convert absolute temperature from degrees Fahrenheit to Kelvins."""
    kelvins = (fahrenheits + Decimal('459.67')) * Decimal('5') / Decimal('9')
    return Quantity(kelvins, units={'K': 1})


def absolute_celcius(celcius):
    """Convert absolute temperature from degrees Celcius to Kelvins."""
    kelvins = celcius + Decimal('273.15')
    return Quantity(kelvins, units={'K': 1})


def delta_fahrenheit(fahrenheits):
    """Convert temperature change from degrees Fahrenheit to Kelvins."""
    kelvins = fahrenheits * Decimal('5') / Decimal('9')
    return Quantity(kelvins, units={'K': 1})


def delta_celcius(celcius):
    """Convert temperature change from degrees Celcius to Kelvins."""
    return Quantity(celcius, units={'K': 1})


def to_absolute_fahrenheit(kelvins):
    """Convert absolute temperature from Kelvins to degrees Fahrenheit."""
    if isinstance(kelvins, Quantity):
        if kelvins.getpow('K') != 1:
            raise ValueError('Kelvins required for conversion')
        kelvins = kelvins.value
    fahrenheits = kelvins * Decimal('9') / Decimal('5') - Decimal('459.67')
    return fahrenheits


def to_absolute_celcius(kelvins):
    """Convert absolute temperature from Kelvins to degrees Celcius."""
    if isinstance(kelvins, Quantity):
        if kelvins.getpow('K') != 1:
            raise ValueError('Kelvins required for conversion')
        kelvins = kelvins.value
    celcius = kelvins - Decimal('273.15')
    return celcius


def to_delta_fahrenheit(kelvins):
    """Convert temperature change from Kelvins to degrees Fahrenheit."""
    if isinstance(kelvins, Quantity):
        if kelvins.getpow('K') != 1:
            raise ValueError('Kelvins required for conversion')
        kelvins = kelvins.value
    fahrenheits = kelvins * Decimal('9') / Decimal('5')
    return fahrenheits


def to_delta_celcius(kelvins):
    """Convert temperature change from Kelvins to degrees Celcius."""
    if isinstance(kelvins, Quantity):
        if kelvins.getpow('K') != 1:
            raise ValueError('Kelvins required for conversion')
        kelvins = kelvins.value
    return kelvins


# US customary units

inch = few(Decimal("0.0254"), "m")
foot = few(Decimal("0.3048"), "m")
yard = few(Decimal("0.9144"), "m")
mile = few(Decimal("1609.344"), "m")
pound = few(Decimal("0.45359237"), "kg")


exporttokens = [
    [['degF'], absolute_fahrenheit, 'strong sign',
     'Absolute temperature in degrees Fahrenheit'],
    [['degC'], absolute_celcius, 'strong sign',
     'Absolute temperature in degrees Celcius'],
    [['Fdeg'], delta_fahrenheit, 'strong sign',
     'Temperature change in degrees Fahrenheit'],
    [['Cdeg'], delta_celcius, 'strong sign',
     'Temperature change in degrees Celcius'],
    [['to_degF'], to_absolute_fahrenheit, 'light sign',
     'To absolute temperature in degrees Fahrenheit'],
    [['to_degC'], to_absolute_celcius, 'light sign',
     'To absolute temperature in degrees Celcius'],
    [['to_Fdeg'], to_delta_fahrenheit, 'light sign',
     'To temperature change in degrees Fahrenheit'],
    [['to_Cdeg'], to_delta_celcius, 'light sign',
     'To temperature change in degrees Celcius'],
    [['in'], lambda: deepcopy(inch), 'static var', 'One inch'],
    [['ft'], lambda: deepcopy(foot), 'static var', 'One foot'],
    [['yd'], lambda: deepcopy(yard), 'static var', 'One yard'],
    [['mi'], lambda: deepcopy(mile), 'static var', 'One mile'],
    [['lb'], lambda: deepcopy(pound), 'static var', 'One pound'],
]
