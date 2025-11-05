"""Module with vector operations."""

from token import Token

from decimal import Decimal
from mathclasses import Vector, Array


def cdot(a, b):
    if isinstance(a, Vector):
        if isinstance(b, Vector):
            ans = 0
            for el1, el2 in zip(a, b):
                ans += el1 * el2
            return ans
    return a * b


def plus_or_minus(a, b=None):
    if isinstance(a, Vector) or isinstance(b, Vector):
        raise ValueError('Plus-or-minus on vectors not implemented yet')
    ans = Vector()
    if b is None:
        (a, b) = (Decimal('0'), a)
    return Vector.join(Vector.join(ans, a + b), a - b)


def minus_or_plus(a, b=None):
    if isinstance(a, Vector) or isinstance(b, Vector):
        raise ValueError('Plus-or-minus on vectors not implemented yet')
    ans = Vector()
    if b is None:
        (a, b) = (Decimal('0'), a)
    return Vector.join(Vector.join(ans, a + b), a - b)


def distance(a):
    if isinstance(a, Vector):
        return cdot(a, a) ** Decimal('0.5')
    return abs(a)


exporttokens = [
    *Token.with_alt(['±', 'plus_or_minus'], plus_or_minus, 'addition',
                    'oper', 'Plus-or-minus'),
    *Token.with_alt([' ±', ' plus_or_minus'], plus_or_minus, 'strong',
                    'func', 'Positive-or-negative'),
    Token('dist', distance, 'normal', 'func', 'Length of vector'),
    Token('[', lambda a: Array(*a), 'static', 'open', 'Open an array',
          closes=']'),
    Token(']', lambda: None, 'static', 'clos', 'Close an array', closes='['),
]

exportmappings = {
    'pm': '±',
}
