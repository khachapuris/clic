"""This module provides mathematical classes for fixed-point calculations."""

from decimal import Decimal
import decimal
from math import asin, acos, atan

from config import CONFIG


glob_pi = Decimal('3.1415926535897932384626433833')
glob_e = Decimal('2.7182818284590452353602874714')


def normalize_fraction(d):
    a = f'{round(d, 22):f}'
    if '.' in a:
        return a.rstrip('0').rstrip('.').replace(
            '.',
            CONFIG['number']['decimal_separators'][0]
        )
    return a


def decimal_to_string(x, notation='classic'):
    """Return a string representation of decimal x."""
    y = x.adjusted()
    if notation == 'classic':
        if Decimal('5e-10') < x < Decimal('5e12'):
            y = y // 3 * 3
        if Decimal('-5e-10') > x > Decimal('-5e12'):
            y = y // 3 * 3
    elif notation == 'engineering':
        y = y // 3 * 3
    elif notation == 'scientific':
        pass
    elif notation == 'normal':
        return f'{normalize_fraction(x)}'
    else:
        raise ValueError('invalid notation')
    if y == 0:
        return f'{normalize_fraction(x)}'
    a = x / Decimal(10) ** y
    if a == 1:
        return f'10^{y}'
    return f'{normalize_fraction(a)} * 10^{y}'


class Multiset:
    """The creation of the Multiset object and the related functionality."""

    def __init__(self, data):
        """The initialiser of the class.

        Arguments:
        data -- a dictionary of type {element: number_of_duplicates}.
        """
        # Skip all elements with zero duplicates
        self.data = {el: data[el] for el in data if data[el]}

    def __iter__(self):
        """Return an iterator over the multiset."""
        return self.data.__iter__()

    def __bool__(self):
        """Return True if the multiset is not empty."""
        return bool(self.data)

    def get(self, el):
        """Return the number of duplicates of element."""
        if el in self.data:
            return self.data[el]
        return 0

    def __add__(self, other):
        """Addition of multisets."""
        ans = dict()
        for el in (self.data | other.data):
            ans.update({el: self.get(el) + other.get(el)})
        return Multiset(ans)

    def __sub__(self, other):
        """Subtraction of multisets."""
        ans = dict()
        for el in (self.data | other.data):
            ans.update({el: self.get(el) - other.get(el)})
        return Multiset(ans)

    def __mul__(self, n):
        """Multiplication of multisets by a number."""
        ans = dict()
        for el in self.data:
            ans.update({el: self.get(el) * n})
        return Multiset(ans)

    def __truediv__(self, n):
        """Division of multisets by a number."""
        ans = dict()
        for el in self.data:
            ans.update({el: self.get(el) / n})
        return Multiset(ans)

    def __neg__(self):
        """Negation of multisets."""
        ans = dict()
        for el in self.data:
            ans.update({el: -self.get(el)})
        return Multiset(ans)

    def __eq__(self, other):
        return self.data == other.data


class Quantity:
    """The Quantity object stores physical quantities."""

    class OperationError(ArithmeticError):
        """An operation error class for quantities."""
        pass

    def __init__(self, value, units):
        """The initialiser for the class.

        Arguments:
        value -- a number representing the numeric value of a quantity,
        units -- a dictionary that matches units and their powers.
        """
        if isinstance(units, dict):
            units = Multiset(units)
        self.units = units
        self.value = value

    @classmethod
    def angle(cls, value, degree=False):
        """An initialiser for angle quantities.

        >>> Quantity.angle(5)
        Q(5, rad)
        >>> Quantity.angle(1, 'degree')
        Q(0.0175, rad)
        """
        if degree:
            return cls(value / Decimal(180) * glob_pi, {'rad': 1})
        return cls(value, {'rad': 1})

    def unit_str(self):
        """Return a string representation of the quantity's unit part."""
        ans = ''
        for unit in self.units:
            power = self.units.get(unit)
            ans += str(unit)
            if power != 1:
                ans += '^' + str(power)
            ans += '*'
        return ans[:-1]

    def getpow(self, unit):
        """Return the power in which unit is present in the quantity."""
        if unit in self.units:
            return self.units.get(unit)
        return 0

    def __mul__(self, other):
        """Multiplication of quantities."""
        if isinstance(other, Quantity):
            units = self.units + other.units
            value = self.value * other.value
            if units:
                return Quantity(value, units)
            return value
        return Quantity(self.value * other, self.units)

    def __truediv__(self, other):
        """Division of quantities."""
        if isinstance(other, Quantity):
            units = self.units - other.units
            value = self.value / other.value
            if units:
                return Quantity(value, units)
            return value
        return Quantity(self.value * other, self.units)

    def __add__(self, other):
        """Addition of quantities."""
        if isinstance(other, Quantity):
            if self.units == other.units:
                return Quantity(self.value + other.value, self.units)
        raise Quantity.OperationError('addition of different units')

    def __neg__(self):
        """Negation of quantities."""
        return Quantity(-self.value, self.units)

    def __sub__(self, other):
        """Subtraction of quantities."""
        if isinstance(other, Quantity):
            if self.units == other.units:
                return Quantity(self.value - other.value, self.units)
        raise Quantity.OperationError('subtraction of different units')

    def __rmul__(self, other):
        return Quantity(other * self.value, self.units)

    def __rtruediv__(self, other):
        return Quantity(other / self.value, -self.units)

    def __radd__(self, other):
        raise Quantity.OperationError('addition of different units')

    def __rsub__(self, other):
        raise Quantity.OperationError('subtraction of different units')

    def __round__(self, num):
        return Quantity(round(self.value, num), self.units)

    def __pow__(self, n, opt=None):
        """Exponentiation of quantities."""
        if not isinstance(n, (int, Decimal)):
            raise Quantity.OperationError('raising to a (quantity) power')
        return Quantity(self.value ** n, self.units * n)

    def __repr__(self):
        """String representation of quantities with additional info."""
        if self.value == 1:
            return f'Quantity({self.unit_str()})'
        return f'Quantity({decimal_to_string(self.value)}, {self.unit_str()})'

    def __str__(self):
        """String representation of quantities without additional info."""
        return f'{decimal_to_string(self.value)} {self.unit_str()}'

    def isangle(self, radians=Multiset({'rad': 1})):
        """Return True if the quantity is an angle."""
        return self.units == radians

    @staticmethod
    def cos(x):
        """Return the cosine of the angle."""
        if isinstance(x, Quantity):
            if not x.isangle():
                OperErr = Quantity.OperationError
                raise OperErr('trigonometry of non-angle quantities')
            x = x.value
        decimal.getcontext().prec += 2
        i, lasts, s, fact, num, sign = 0, 0, 1, 1, 1, 1
        while s != lasts:
            lasts = s
            i += 2
            fact *= i * (i-1)
            num *= x * x
            sign *= -1
            s += num / fact * sign
        decimal.getcontext().prec -= 2
        return +s

    @staticmethod
    def sin(x):
        """Return the sine of the angle."""
        if isinstance(x, Quantity):
            if not x.isangle():
                OperErr = Quantity.OperationError
                raise OperErr('trigonometry of non-angle quantities')
            x = x.value
        decimal.getcontext().prec += 2
        i, lasts, s, fact, num, sign = 1, 0, x, 1, x, 1
        while s != lasts:
            lasts = s
            i += 2
            fact *= i * (i-1)
            num *= x * x
            sign *= -1
            s += num / fact * sign
        decimal.getcontext().prec -= 2
        return +s

    @staticmethod
    def tan(x):
        """Return the tangent of the angle."""
        return Quantity.sin(x) / Quantity.cos(x)

    @staticmethod
    def cot(x):
        """Return the cotangent of the angle."""
        return Quantity.cos(x) / Quantity.sin(x)

    @staticmethod
    def arcsin(x):
        """Return an angle with given sine."""
        return Quantity.angle(Decimal(asin(x)))

    @staticmethod
    def arccos(x):
        """Return an angle with given cosine."""
        return Quantity.angle(Decimal(acos(x)))

    @staticmethod
    def arctan(x):
        """Return an angle with given tangent."""
        return Quantity.angle(Decimal(atan(x)))


class Vector:
    """The creation of the Vector object and the related functionality."""

    class OperationError(ArithmeticError):
        """An operation error class for vectors."""
        pass

    def __init__(self, *args):
        """The initialiser of the class.

        Arguments:
        *args -- elements of the vector.
        """
        self.ls = list(args)

    @staticmethod
    def join(a, b):
        """Create vectors by joining elements.

        >>> a = Vector.join(1, 2)  # (1; 2)
        >>> b = Vector.join(a, 3)  # (1; 2; 3)
        """
        if isinstance(a, Vector):
            a.ls.append(b)
            return a
        return Vector(a, b)

    def __add__(self, other):
        """Addition of vectors."""
        if isinstance(other, Vector) and len(other.ls) == len(self.ls):
            ans = Vector()
            for a, b in zip(self.ls, other.ls):
                Vector.join(ans, a + b)
            return ans
        raise Vector.OperationError('addition of different sizes')

    def __sub__(self, other):
        """Subtraction of vectors."""
        if isinstance(other, Vector) and len(other.ls) == len(self.ls):
            ans = Vector()
            for a, b in zip(self.ls, other.ls):
                Vector.join(ans, a - b)
            return ans
        raise Vector.OperationError('subtraction of different sizes')

    def __mul__(self, other):
        """Multiplication of vectors."""
        if isinstance(other, Vector):
            if len(other.ls) == len(self.ls):
                ans = 0
                for a, b in zip(self.ls, other.ls):
                    ans += a * b
                return ans
            raise Vector.OperationError('multiplication of different sizes')
        ans = Vector()
        for a in self.ls:
            Vector.join(ans, a * other)
        return ans

    def __truediv__(self, other):
        """Division of vectors."""
        if isinstance(other, Vector):
            if len(other.ls) == len(self.ls):
                ans = 0
                for a, b in zip(self.ls, other.ls):
                    ans += a / b
                return ans
            raise Vector.OperationError('division of different sizes')
        ans = Vector()
        for a in self.ls:
            Vector.join(ans, a / other)
        return ans

    def __rmul__(self, other):
        return self * other

    def __iter__(self):
        """Return an iterator over a vector."""
        return self.ls.__iter__()

    def __repr__(self):
        """String representation of vectors."""
        vector_separator = CONFIG['expression']['vector_separator'] + ' '
        return '(' + vector_separator.join([str(x) for x in self.ls]) + ')'


class UnknownName():
    """A place to keep unknown names before raising an error."""
    def __init__(self, name):
        self.name = name

    def raise_error(self, *args):
        raise ValueError(f'unknown name: {self.name}')

    __add__ = raise_error
    __sub__ = raise_error
    __mul__ = raise_error
    __div__ = raise_error
    __truediv__ = raise_error
    __radd__ = raise_error
    __rsub__ = raise_error
    __rmul__ = raise_error
    __rdiv__ = raise_error
    __rtruediv__ = raise_error
    __str__ = raise_error
