from decimal import Decimal
from token import Token


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


functions = [
    Token('!', factorial, 1, 4, 0, 'sign'),
]
