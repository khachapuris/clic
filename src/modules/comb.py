"""Module with combiantorics and number theory math."""

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
    ans = Decimal('1')
    i = Decimal('0')
    while i < k:
        ans *= (n - i)
        i += 1
    return ans


def combinations(args=None, n=None, k=None):
    """Return the number of k-combinations on a set of n elements."""
    if args:
        n, k = tuple(args)
    return permutations(n=n, k=k) / factorial(k)


def prime_factorization(n):
    """Return the prime factorization of the number n as a list of tuples."""
    primes = []
    ls = []
    n = int(n)
    if n == 1:
        return []
    if n < 1:
        raise ValueError('prime factorization of nonpositive number')
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
            raise ValueError('prime factorization of large number')
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
    return ls


def pretty_prime_factorization(n):
    """Display the prime factorization of n in a human-readable format."""
    ls = prime_factorization(n)
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
    [['mod'], lambda a, b: a % b, 'mul-tion oper', 'Modulo'],
    [['!'], factorial, 'strong sign', 'Factorial', {'array_input': True}],
    [['nPr'], permutations, 'normal func', 'Number of permutations',
     {'array_input': True}],
    [['nCr'], combinations, 'normal func', 'Number of combinations',
     {'array_input': True}],
    [['pf'], pretty_prime_factorization, 'normal func', 'Prime factorization',
     {'array_input': True}],
]
