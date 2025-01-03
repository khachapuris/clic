"""This module stores mathematical functions used in the calculator.

The user can add custom functions to this file. Note that the functions
should support Decimal input and return Decimals to be used in the calculator
(see the decimal docs at https://docs.python.org/3/library/decimal.html).
To register created functions go to functions.py.
"""

from decimal import Decimal
from mathclasses import Quantity, Vector


def factorial(x):
    """Return the factorial of x."""
    ans = 1
    i = 2
    while i <= x:
        ans *= i
        i += 1
    return Decimal(ans)


def permutations(n, k):
    """Return the number of k-permutations on a set of n elements."""
    ans = 1
    i = 0
    while i < k:
        ans *= (n - i)
        i += 1
    return Decimal(ans)


def combinations(n, k):
    """Return the number of k-combinations on a set of n elements."""
    return permutations(n, k) / factorial(n, k)
