#!/usr/bin/env python

from decimal import Decimal
import decimal
from math import asin, acos, atan
import functions

import copy

glob_pi = Decimal('3.1415926535897932384626433833')


class Quantity:
    """The Quantity object stores phisical quantities."""

    class OperationError(ArithmeticError):
        """An operation error class for quantities."""
        pass

    def __init__(self, value, units):
        """The initialiser for the class.

        Arguments:
        value -- a number representing the numeric value of a quantity,
        units -- a dictionary that matches units and their powers.
        """
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
        for u in list(self.units):
            power = self.units[u]
            ans += str(u)
            if power != 1:
                ans += '^' + str(power)
            ans += '*'
        return ans[:-1]

    def getpow(self, unit):
        """Return the power in which unit is present in the quantity."""
        if unit in self.units:
            return self.units[unit]
        return 0

    def __mul__(self, other):
        """Multiplication of quantities."""
        if isinstance(other, Quantity):
            units = {}
            for u in list(self.units | other.units):
                power = self.getpow(u) + other.getpow(u)
                if power != 0:
                    units[u] = power
            value = self.value * other.value
            if units:
                return Quantity(value, units)
            return value
        return Quantity(self.value * other, self.units)

    def __truediv__(self, other):
        """Division of quantities."""
        if isinstance(other, Quantity):
            units = {}
            for u in list(self.units | other.units):
                power = self.getpow(u) - other.getpow(u)
                if power != 0:
                    units[u] = power
            value = self.value * other.value
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
        """Negatition of quantities."""
        return Quantity(-self.value, self.units)

    def __sub__(self, other):
        """Subtraction of quantities."""
        if isinstance(other, Quantity):
            if self.units == other.units:
                return Quantity(self.value - other.value, self.units)
        raise Quantity.OperationError('subtraction of different units')

    def __rmul__(self, other):
        return self * other

    def __rtruediv__(self, other):
        return other * Quantity(Decimal(1), {}) / self

    def __radd__(self, other):
        raise Quantity.OperationError('addition of different units')

    def __rsub__(self, other):
        raise Quantity.OperationError('subtraction of different units')

    def __round__(self, num):
        return Quantity(round(self.value, num), self.units)

    def __pow__(self, other, opt=None):
        """Exponentiation of quantities."""
        if isinstance(other, (int, Decimal)):
            raise Quantity.OperationError('raising to a (quantity) power')
        units = {a: self.units[a] * other for a in list(self.units)}
        return Quantity(self.value ** other, units)

    def __repr__(self):
        """String representation of quantities with additional info."""
        if self.value == 1:
            return f'Quantity({self.unit_str()})'
        return f'Quantity({str(self.value)}, {self.unit_str()})'

    def __str__(self):
        """String representation of quantities without additional info."""
        return f'{str(self.value)} {self.unit_str()}'

    def isangle(self):
        """Return True if the quantity is an angle."""
        return self.units == {'rad': 1}

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
        """Return the tangene of the angle."""
        return Quantity.sin(x) / Quantity.cos(x)

    @staticmethod
    def cot(x):
        """Return the cotangene of the angle."""
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
        """Return an angle with given tangene."""
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
        return '(' + '; '.join([str(x) for x in self.ls]) + ')'


class Token:
    """Token objects are data storage and data transformation elements."""

    def __init__(self, calc, arg_num, pref, ltor, kind='', name=''):
        """The initialiser of the class.

        Arguments:
        calc -- the token's function,
        arg_num -- number of arguments of calc,
        pref -- the token's preference,
        ltor -- a truthy value, if tokens with the same pref
          should be calculated left-to-right, falsy otherwise,
        kind -- the kind of the token (optional),
        name -- the name of the token (optional).
        """
        self.name = name
        self.calc = calc
        self.arg_num = arg_num
        self.pref = pref
        self.ltor = ltor
        self.kind = kind
        self.name = name

    @staticmethod
    def give(obj):
        """Return a function that returns obj.

        >>> f = Token.give(1024)
        >>> f()
        1024
        """
        def func():
            return copy.copy(obj)
        return func

    def __repr__(self):
        """String representation of tokens."""
        if self.name:
            return self.name
        if self.arg_num == 0:
            return str(self.calc())
        if self.kind:
            return self.kind
        return '<?>'


glob_funcs = {
    '!': Token(functions.factorial, 1, 4, 0, 'sign', '<FTR>'),
    ';': Token(Vector.join,         2, 0, 0, 'oper', '<SEM>'),
    '+': Token(lambda a, b: a + b,  2, 1, 0, 'oper', '<ADD>'),
    '-': Token(lambda a, b: a - b,  2, 1, 0, 'oper', '<SUB>'),
    '*': Token(lambda a, b: a * b,  2, 2, 0, 'oper', '<MUL>'),
    ':': Token(lambda a, b: a / b,  2, 2, 0, 'oper', '<DIV>'),
    '/': Token(lambda a, b: a / b,  2, 0, 0, 'oper', '<BAR>'),
    '^': Token(lambda a, b: a ** b, 2, 3, 1, 'oper', '<POW>'),
    'mod': Token(lambda a, b: a % b,   2, 2, 0, 'oper', '<MOD>'),
    '_neg_': Token(lambda a: -a,       1, 3, 1, 'oper', '<NEG>'),
    '_dot_': Token(lambda a, b: a * b, 2, 3, 1, 'oper', '<DOT>'),
    'sin': Token(lambda a: Quantity.sin(a), 1, 3, 1, 'trig', '<sin>'),
    'cos': Token(lambda a: Quantity.cos(a), 1, 3, 1, 'trig', '<cos>'),
    'tan': Token(lambda a: Quantity.tan(a), 1, 3, 1, 'trig', '<tan>'),
    'arcsin': Token(lambda a: Quantity.arcsin(a), 1, 3, 1, 'func', '<arcsin>'),
    'arccos': Token(lambda a: Quantity.arccos(a), 1, 3, 1, 'func', '<arccos>'),
    'arctan': Token(lambda a: Quantity.arctan(a), 1, 3, 1, 'func', '<arctan>'),
}

glob_syntax = {
    '(': Token(lambda: None, 0, 10, 0, "'('", "'('"),
    ')': Token(lambda: None, 0, 10, 0, "')'", "')'"),
    '=': Token(lambda: None, 0, 10, 0, "'='", "'='"),
}

glob_trigpow = {
    'sin': Token(lambda a, b: Quantity.sin(a) ** b, 1, 3, 1, 'func', '<sin^>'),
    'cos': Token(lambda a, b: Quantity.cos(a) ** b, 1, 3, 1, 'func', '<cos^>'),
    'tan': Token(lambda a, b: Quantity.tan(a) ** b, 1, 3, 1, 'func', '<tan^>'),
}

si_units = {
    'rad': Quantity(Decimal(1), {'rad': 1}),
    'm': Quantity(Decimal(1), {'m': 1}),
    's': Quantity(Decimal(1), {'s': 1}),
    'kg': Quantity(Decimal(1), {'kg': 1}),
}


class Calculator:
    """The Calculator object provides methods for calculating expressions."""

    class CompilationError(Exception):
        """An compilation error class for the calculator."""

    def __init__(self):
        """The initialiser of the class."""
        self.vars = {'_': Decimal(0)} | si_units
        self.err = None
        self.link = 'ans'

    def split(self, string):
        """Split the given string expression."""
        changes = {'⋅': '*', '×': '*',
                   '÷': ':', '{': '(', '}': ')'}
        # characters that behave like alphabetical
        alpha = '_'
        # desimal separator characters
        decseps = '.,'
        # start / end of a calculator string
        quote = '"'
        ans = []
        space = True
        in_string = False
        for char in string:
            # calculator string is a token
            if in_string:
                ans[-1] += char
                # end of a calculator string
                if char == quote:
                    in_string = not in_string
            # start of a calculator string
            elif char == quote:
                ans.append(char)
                in_string = not in_string
            # [space] separates tokens
            elif char == ' ':
                space = True
            elif space:
                ans.append(char)
                # [letters, digits] after [space] start new tokens
                if char.isalnum() or char in (decseps + alpha):
                    space = False
            # [digits] connect tokens
            elif char.isdigit():
                ans[-1] += char
            # [letters after letters] connect tokens
            elif char.isalpha() or char in alpha:
                if ans[-1][-1].isalpha() or ans[-1][-1] in alpha:
                    ans[-1] += char
                else:
                    ans.append(char)
            # [decsep after digit] connects tokens
            elif char in decseps and ans[-1].isdigit():
                ans[-1] += '.'
            # [other symbols] make separate tokens
            else:
                # replace chars from 'changes' dict
                if char in changes:
                    char = changes[char]
                ans.append(char)
                space = True
        if in_string:
            raise ValueError('unclosed quotes')
        return ans

    def perform_assignment(self, ls):
        """Change the assignment link according to a list of strings."""
        self.err = None
        # simple assignment (x = 1)
        if len(ls) > 2 and ls[1] == '=':
            if not ls[0][0].isalpha() or ls[0] in (glob_funcs | si_units):
                raise Calculator.CompilationError('assignment error')
            self.link = ls[0]
            return ls[2:]
        self.link = 'ans'
        # compound assignment (x += 1)
        if len(ls) > 2 and ls[2] == '=':
            if not ls[0] in self.vars:
                raise Calculator.CompilationError('compound assignment error')
            self.link = ls[0]
            return ls[:2] + ls[3:]
        return ls

    def tokenize(self, ls):
        """Transform a list of strings to a list of Token objects."""
        ans = []
        for word in ls:
            if word[0] in glob_syntax:
                ans.append(glob_syntax[word])
            elif word[0] == '"':
                get = Token.give(word.strip('"'))
                ans.append(Token(get, 0, 10, 0, kind='str'))
            elif word.isdigit() or '.' in word:
                num = Decimal(word)
                ans.append(Token(Token.give(num), 0, 10, 0, kind='num'))
            elif word in glob_funcs:
                ans.append(glob_funcs[word])
            elif word in self.vars:
                get = Token.give(self.vars[word])
                ans.append(Token(get, 0, 10, 0, kind='var', name=word))
            else:
                raise Calculator.CompilationError(f"unknown name: '{word}'")
        return ans

    def complete_infix_notation(self, ls):
        """Add ommited operators to a list of tokens."""
        last = glob_syntax['(']
        ans = []
        for token in ls:
            match (last.kind, token.name):
                case ("'('" | 'oper' | 'func' | 'trig', '<ADD>'):
                    pass
                case ("'('" | 'oper' | 'func' | 'trig', '<SUB>'):
                    ans.append(glob_funcs['_neg_'])
                case ('trig', '<POW>'):
                    ans[-1] = glob_trigpow(last.name)
                case _:
                    match last.kind, token.kind:
                        case ('var', 'var' | "'('" | 'num'):
                            ans.append(glob_funcs['_dot_'])
                        case ('var' | "')'" | 'num', 'var'):
                            ans.append(glob_funcs['_dot_'])
                        case ("')'", "'('"):
                            ans.append(glob_funcs['_dot_'])
                    ans.append(token)
            if ans:
                last = ans[-1]
        return ans

    def shunting_yard_algorithm(self, ls):
        """Transform infix notation to postfix notation."""
        oper_stack = []
        output = []
        for token in ls:
            if token.name == "'('":
                oper_stack.append(token)
            elif token.name == "')'":
                while oper_stack[-1].name != "'('":
                    output.append(oper_stack.pop())
                oper_stack.pop()
            elif token.ltor:
                while oper_stack and oper_stack[-1].name != "'('" \
                        and token.pref < oper_stack[-1].pref:
                    output.append(oper_stack.pop())
                oper_stack.append(token)
            else:
                while oper_stack and oper_stack[-1].name != "'('" \
                        and token.pref <= oper_stack[-1].pref:
                    output.append(oper_stack.pop())
                oper_stack.append(token)
        return output + oper_stack[::-1]

    def perform_operations(self, ls):
        """Perform postfix notation operations."""
        data_stack = []
        for token in ls:
            if len(data_stack) < token.arg_num:
                raise Calculator.CompilationError('compilation error')
            args = []
            for _ in range(token.arg_num):
                args.insert(0, data_stack.pop())
            ans = token.calc(*args)
            # TODO: make all answers lists
            if isinstance(ans, list):
                data_stack += ans
            else:
                data_stack.append(ans)
        return data_stack

    def require_one_answer(self, stack):
        """Return the only element of a stack or raise an error."""
        if len(stack) == 1:
            return stack[0]
        raise Calculator.CompilationError('compilation error')

    def perform_operations_twice(self, ls):
        """Run perform_operations and test the answer."""
        def test(a1, i1):
            if a1 == 0 or Decimal(0.5) < i1 / a1 < 2:
                return a1
            return Decimal(0)

        def type_test(a1, i1):
            if isinstance(a1, str):
                return a1
            if isinstance(a1, Quantity):
                return Quantity(test(a1.value, i1.value), a1.units)
            return test(a1, i1)

        a = self.perform_operations(ls)
        a = self.require_one_answer(a)
        decimal.getcontext().prec -= 5
        i = self.perform_operations(ls)
        i = self.require_one_answer(i)
        decimal.getcontext().prec += 5
        if isinstance(a, Vector):
            new = Vector()
            for a2, i2 in zip(a, i):
                Vector.join(new, type_test(a2, i2))
            return new
        return type_test(a, i)

    def object_to_string(self, obj):
        """Represent obj as a string."""
        if obj is None:
            return ''
        if isinstance(obj, str):
            return f'"{obj}"'
        return str(obj)

    def calculate(self, exp):
        """Calculate expression exp and store the answer."""
        try:
            exp = self.split(exp)
            exp = self.perform_assignment(exp)
            exp = self.tokenize(exp)
            exp = self.complete_infix_notation(exp)
            exp = self.shunting_yard_algorithm(exp)
            exp = self.perform_operations_twice(exp)
            self.vars |= {'_': exp}
            self.vars |= {self.link: exp}
            self.err = None
        except Exception as err:
            self.err = err

    def get_answer(self):
        """Return the answer of the current expression.

        Output is a tuple:
        flag -- is the output an error,
        output -- the error / answer (as a string).
        """
        if self.err:
            # raise self.err
            return (True, f'{str(self.err)}')
        ans = self.vars['_']
        if ans is None:
            return (True, '')
        ans = self.object_to_string(ans)
        return (False, ans)


if __name__ == '__main__':
    ctor = Calculator()
    while True:
        exp = input('% ')
        ctor.calculate(exp)
        flag, ans = ctor.get_answer()
        if ans is None or exp == '':
            break
        if flag:
            print(f'! {ans}')
        else:
            print(f'= {ans}')
        print()
