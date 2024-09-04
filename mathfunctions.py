from decimal import Decimal
from mathclasses import Quantity, Vector

"""This module stores mathematical functions used in the calculator.

The user can add custom functions to this file.
"""


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
