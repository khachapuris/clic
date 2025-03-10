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


def prime_factorization(n):
    """Return the prime factorisation of n."""
    primes = []
    ls = []
    n = int(n)
    if n == 1:
        return []
    if n < 1:
        raise ValueError('nonpositive number pf')
    x = 1
    power = 0
    while n % 2 == 0:
        n //= 2
        power += 1
    if power > 0:
        ls.append((2, power))
    while n > 1:
        x += 2
        power = 0
        is_prime = True
        if x > 10000000:
            raise ValueError('large number pf')
        for a in primes:
            if a * a > x:
                is_prime = True
                break
            if x % a == 0:
                is_prime = False
                break
        if not is_prime:
            continue
        primes.append(x)
        while n % x == 0:
            n //= x
            power += 1
        if power != 0:
            ls.append((x, power))
        if x * x > n and n != 1:
            ls.append((n, 1))
            break
    ans = ''
    if ls == []:
        return '1'
    for el in ls[:-1]:
        if el[1] == 1:
            ans += str(el[0]) + ' * '
        else:
            ans += str(el[0]) + '^' + str(el[1]) + ' * '
    el = ls[-1]
    if el[1] == 1:
        ans += str(el[0])
    else:
        ans += str(el[0]) + '^' + str(el[1])
    return ans


exporttokens = [
    Token('!', factorial,    4, 0, 'sign', 'Factorial'),
    Token('perm', permutations, 3, 1, 'func', 'Number of permutations'),
    Token('comb', combinations, 3, 1, 'func', 'Number of combinations'),
    Token('mod', lambda a, b: a % b, 2, 0, 'oper', 'Modulo'),
    Token('pf', prime_factorization, 3, 1, 'func', 'Prime factorization'),
]
