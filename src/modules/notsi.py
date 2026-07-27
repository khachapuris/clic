"""Module with units that are not a part of SI."""

from decimal import Decimal


# Helper functions

def lazy_quantity(*args, **kwargs):
    """Return a function that will create a new quantity when called."""

    def give_quantity(META):
        quantity = META.Quantity(*args, **kwargs)
        return quantity

    return give_quantity


# Temperature functions

def absolute_fahrenheit(fahrenheits, META):
    """Convert absolute temperature from degrees Fahrenheit to Kelvins."""
    kelvins = (fahrenheits + Decimal('459.67')) * Decimal('5') / Decimal('9')
    return META.Quantity(kelvins, units={'K': 1})


def absolute_celcius(celcius, META):
    """Convert absolute temperature from degrees Celcius to Kelvins."""
    kelvins = celcius + Decimal('273.15')
    return META.Quantity(kelvins, units={'K': 1})


def delta_fahrenheit(fahrenheits, META):
    """Convert temperature change from degrees Fahrenheit to Kelvins."""
    kelvins = fahrenheits * Decimal('5') / Decimal('9')
    return META.Quantity(kelvins, units={'K': 1})


def delta_celcius(celcius, META):
    """Convert temperature change from degrees Celcius to Kelvins."""
    return META.Quantity(celcius, units={'K': 1})


def to_absolute_fahrenheit(kelvins):
    """Convert absolute temperature from Kelvins to degrees Fahrenheit."""
    if type(kelvins).__name__ == 'Quantity':
        if kelvins.getpow('K') != 1:
            raise ValueError('Kelvins required for conversion')
        kelvins = kelvins.value
    fahrenheits = kelvins * Decimal('9') / Decimal('5') - Decimal('459.67')
    return fahrenheits


def to_absolute_celcius(kelvins):
    """Convert absolute temperature from Kelvins to degrees Celcius."""
    if type(kelvins).__name__ == 'Quantity':
        if kelvins.getpow('K') != 1:
            raise ValueError('Kelvins required for conversion')
        kelvins = kelvins.value
    celcius = kelvins - Decimal('273.15')
    return celcius


def to_delta_fahrenheit(kelvins):
    """Convert temperature change from Kelvins to degrees Fahrenheit."""
    if type(kelvins).__name__ == 'Quantity':
        if kelvins.getpow('K') != 1:
            raise ValueError('Kelvins required for conversion')
        kelvins = kelvins.value
    fahrenheits = kelvins * Decimal('9') / Decimal('5')
    return fahrenheits


def to_delta_celcius(kelvins):
    """Convert temperature change from Kelvins to degrees Celcius."""
    if type(kelvins).__name__ == 'Quantity':
        if kelvins.getpow('K') != 1:
            raise ValueError('Kelvins required for conversion')
        kelvins = kelvins.value
    return kelvins


# US customary units

inch = lazy_quantity(Decimal("0.0254"), units={'m': 1})
foot = lazy_quantity(Decimal("0.3048"), units={'m': 1})
yard = lazy_quantity(Decimal("0.9144"), units={'m': 1})
mile = lazy_quantity(Decimal("1609.344"), units={'m': 1})
pound = lazy_quantity(Decimal("0.45359237"), units={'kg': 1})


exporttokens = [
    [['degF'], absolute_fahrenheit, 'strong sign',
     'Absolute temperature in degrees Fahrenheit', {'use_meta': True}],
    [['degC'], absolute_celcius, 'strong sign',
     'Absolute temperature in degrees Celcius', {'use_meta': True}],
    [['Fdeg'], delta_fahrenheit, 'strong sign',
     'Temperature change in degrees Fahrenheit', {'use_meta': True}],
    [['Cdeg'], delta_celcius, 'strong sign',
     'Temperature change in degrees Celcius', {'use_meta': True}],
    [['to_degF'], to_absolute_fahrenheit, 'light sign',
     'To absolute temperature in degrees Fahrenheit'],
    [['to_degC'], to_absolute_celcius, 'light sign',
     'To absolute temperature in degrees Celcius'],
    [['to_Fdeg'], to_delta_fahrenheit, 'light sign',
     'To temperature change in degrees Fahrenheit'],
    [['to_Cdeg'], to_delta_celcius, 'light sign',
     'To temperature change in degrees Celcius'],
    [['in'], inch, 'static var', 'One inch', {'use_meta': True}],
    [['ft'], foot, 'static var', 'One foot', {'use_meta': True}],
    [['yd'], yard, 'static var', 'One yard', {'use_meta': True}],
    [['mi'], mile, 'static var', 'One mile', {'use_meta': True}],
    [['lb'], pound, 'static var', 'One pound', {'use_meta': True}],
]
