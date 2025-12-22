"""Module with statistics functions."""

from token import Token

from decimal import Decimal
from mathclasses import Vector, Array


def plus_or_minus(a, b=None):
    if isinstance(a, Vector) or isinstance(b, Vector):
        raise ValueError('Plus-or-minus on vectors not implemented yet')
    ans = Array()
    if b is None:
        (a, b) = (Decimal('0'), a)
    if b >= 0:
        return Array.join(Array.join(ans, a - b), a + b)
    return Array.join(Array.join(ans, a + b), a - b)


def distance(a):
    if isinstance(a, Vector):
        return (a * a) ** Decimal('0.5')
    return abs(a)


def mean(a):
    if isinstance(a, Array):
        return sum(a) / len(a)
    return 0


def array_sort(a):
    if isinstance(a, Array):
        return Array(*sorted(list(a)))
    raise TypeError('Cannot sort anything but arrays')


def median(array):
    if isinstance(array, Array):
        ls = sorted(list(array))
        a = len(array)
        if a % 2 == 0:
            return (ls[a // 2 - 1] + ls[a // 2]) / 2
        else:
            return ls[a // 2]
    return 0


def variance(array):
    return mean((mean(array) - array) ** 2)


def deviation(array):
    return variance(array) ** Decimal('0.5')


exporttokens = [
    *Token.with_alt(['±', 'pm'], plus_or_minus, 'addition',
                    'oper', 'Plus-or-minus'),
    *Token.with_alt([' ±', ' pm'], plus_or_minus, 'strong',
                    'func', 'Positive-or-negative'),
    Token('dist', distance, 'normal', 'func', 'Length of vector'),
    Token('SUM', lambda a: sum(a), 'normal', 'func', 'Sum of array elements'),
    Token('LEN', lambda a: len(a), 'normal', 'func', '# of array elements'),
    Token('SORT', array_sort, 'normal', 'func', 'Sorted version of array'),
    Token('MEAN', mean, 'normal', 'func', 'Mean of array'),
    Token('MEDIAN', median, 'normal', 'func', 'Median of array'),
    Token('VARIANCE', variance, 'normal', 'func', 'Variance of data in array'),
    Token('DEVIATION', deviation, 'normal', 'func', 'Standard deviation'),
    Token('[', lambda a: Array(*a), 'static', 'open', 'Array', closes=']'),
    Token(']', lambda: None, 'static', 'clos', 'Array', closes='['),
]

exportmappings = {
    'pm': '±',
}
