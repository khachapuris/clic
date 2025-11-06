"""Module with vector operations."""

from token import Token

from decimal import Decimal
from mathclasses import Vector, Array


def plus_or_minus(a, b=None):
    if isinstance(a, Vector) or isinstance(b, Vector):
        raise ValueError('Plus-or-minus on vectors not implemented yet')
    ans = Array()
    if b is None:
        (a, b) = (Decimal('0'), a)
    return Array.join(Array.join(ans, a + b), a - b)


def minus_or_plus(a, b=None):
    if isinstance(a, Vector) or isinstance(b, Vector):
        raise ValueError('Plus-or-minus on vectors not implemented yet')
    ans = Array()
    if b is None:
        (a, b) = (Decimal('0'), a)
    return Array.join(Array.join(ans, a + b), a - b)


def distance(a):
    if isinstance(a, Vector):
        return (a * a) ** Decimal('0.5')
    return abs(a)


exporttokens = [
    *Token.with_alt(['±', 'pm'], plus_or_minus, 'addition',
                    'oper', 'Plus-or-minus'),
    *Token.with_alt([' ±', ' pm'], plus_or_minus, 'strong',
                    'func', 'Positive-or-negative'),
    Token('dist', distance, 'normal', 'func', 'Length of vector'),
    Token('[', lambda a: Array(*a), 'static', 'open', 'Array', closes=']'),
    Token(']', lambda: None, 'static', 'clos', 'Array', closes='['),
]

exportmappings = {
    'pm': '±',
}
