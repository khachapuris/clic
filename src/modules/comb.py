"""Module with combiantorics and number theory math."""

from token import Token
from decimal import Decimal


def factorial(x):
    """Return the factorial of x."""
    ans = 1
    i = 2
    while i <= x:
        ans *= i
        i += 1
    return Decimal(ans)


def permutations(args=None, n=None, k=None):
    """Return the number of k-permutations on a set of n elements."""
    if args:
        n, k = tuple(args)
    ans = 1
    i = 0
    while i < k:
        ans *= (n - i)
        i += 1
    return Decimal(ans)


def combinations(args=None, n=None, k=None):
    """Return the number of k-combinations on a set of n elements."""
    if args:
        n, k = tuple(args)
    return permutations(n=n, k=k) / factorial(k)


exporttokens = [
    Token('!', factorial,    4, 0, 'sign', 'Factorial'),
    Token('P', permutations, 3, 1, 'func', 'Number of permutations'),
    Token('C', combinations, 3, 1, 'func', 'Number of combinations'),
    Token('mod', lambda a, b: a % b, 2, 0, 'oper', 'Modulo'),
]
