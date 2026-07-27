"""Module with statistics functions."""

from decimal import Decimal
from math import prod
import math


def plus_or_minus(a, b=None, META=None):
    if type(a).__name__ == 'Vector' or type(b).__name__ == 'Vector':
        raise ValueError('Plus-or-minus on vectors not implemented yet')
    ans = META.Array()
    if b is None:
        (a, b) = (Decimal('0'), a)
    if b >= 0:
        return META.Array.join(META.Array.join(ans, a - b), a + b)
    return META.Array.join(META.Array.join(ans, a + b), a - b)


def create_array(a, META):
    return META.Array(*a)


def push(array, element):
    if type(array).__name__ == 'Array':
        Array = type(array)
        ans = Array()
        for el in array:
            Array.join(ans, el)
        Array.join(ans, element)
        return ans


def distance(a):
    if type(a).__name__ == 'Array':
        return (a.dot_product(a)) ** Decimal('0.5')
    return abs(a)


def mean(a):
    if type(a).__name__ == 'Array':
        return sum(a) / len(a)
    return 0


def array_sort(a):
    if type(a).__name__ == 'Array':
        return type(a)(*sorted(list(a)))
    raise TypeError('Cannot sort anything but arrays')


def median(array):
    if type(array).__name__ == 'Array':
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


def normalcdf_phi(x):
    return (
        Decimal('1') + Decimal(math.erf(x / 2 ** Decimal('0.5')))
    ) / Decimal('2')


def normalcdf(array):
    """Find the cumulative distribution for the standard normal distr."""
    minx, maxx = tuple(array)
    return abs(normalcdf_phi(maxx) - normalcdf_phi(minx))


exporttokens = [
    [['±', 'pm'], plus_or_minus, 'addition oper', 'Plus-or-minus',
     {'use_meta': True}],
    [[' ±', ' pm'], plus_or_minus, 'strong func', 'Positive-or-negative',
     {'use_meta': True}],
    [['Σ', 'SUM'], sum,   'mul-tion func', 'Sum of array elements'],
    [['Π', 'PROD'], prod, 'mul-tion func', 'Product of array elements'],
    [['←', 'leftarrow'], push, 'mul-tion oper', 'Push element to array'],
    [['dist'], distance,        'normal func', 'Length of vector'],
    [['LEN'], lambda a: len(a), 'normal func', 'Number of array elements'],
    [['SORT'], array_sort,      'normal func', 'Sorted version of array'],
    [['MIN'], min,              'normal func', 'Minimal value of array'],
    [['MAX'], max,              'normal func', 'Maximum value of array'],
    [['MEAN'], mean,            'normal func', 'Mean of array'],
    [['MEDIAN'], median,        'normal func', 'Median of array'],
    [['VARIANCE'], variance,    'normal func', 'Variance of data in array'],
    [['DEVIATION'], deviation,  'normal func', 'Standard deviation'],
    [['normalcdf'], normalcdf,  'normal func', 'Cumulative distribution'],
    [['['], create_array, 'static open', 'Array', {'closes': ']',
                                                   'use_meta': True}],
    [[']'], lambda: None, 'static clos', 'Array', {'closes': '['}],
]

exportmappings = {
    'pm': '±',
    'leftarrow': '←',
}
