#!/usr/bin/env python

"""This script provides a fixed-point decimal Calculator."""

import sys

import decimal
from decimal import Decimal

from mathclasses import Quantity, Vector
from token import Token

# Try to import functions.functions, default to an empty list
custom_func_list = []
try:
    from functions import functions as custom_func_list
    ls = custom_func_list
    if isinstance(ls, list):
        for (x, i) in zip(ls, range(len(ls))):
            if not isinstance(x, Token):
                print(f'WARNING: functions.functions[{i}] is not a Token')
                custom_func_list = []
    else:
        print('WARNING: functions.functions is not a list')
        custom_func_list = []
except ImportError:
    print('WARNING: functions.functions was not found')
except Exception:
    print('WARNING: functions.py module contains an error. Tip: run functions.py to see the traceback')


glob_func_list = [
    Token(',', Vector.join,         2, 0, 0, 'oper'),
    Token('+', lambda a, b: a + b,  2, 1, 0, 'oper'),
    Token('-', lambda a, b: a - b,  2, 1, 0, 'oper'),
    Token('*', lambda a, b: a * b,  2, 2, 0, 'oper'),
    Token(':', lambda a, b: a / b,  2, 2, 0, 'oper'),
    Token('/', lambda a, b: a / b,  2, 0, 0, 'oper'),
    Token('^', lambda a, b: a ** b, 2, 3, 1, 'oper'),
    Token('mod', lambda a, b: a % b,   2, 2, 0, 'oper'),
    Token('_neg_', lambda a: -a,       1, 3, 1, 'oper'),
    Token('_dot_', lambda a, b: a * b, 2, 3, 1, 'oper'),
    Token('sin',    Quantity.sin,    1, 3, 1, 'trig'),
    Token('cos',    Quantity.cos,    1, 3, 1, 'trig'),
    Token('tan',    Quantity.tan,    1, 3, 1, 'trig'),
    Token('arcsin', Quantity.arcsin, 1, 3, 1, 'func'),
    Token('arccos', Quantity.arccos, 1, 3, 1, 'func'),
    Token('arctan', Quantity.arctan, 1, 3, 1, 'func'),
]

glob_syntax_list = [
    Token('(', lambda: None, 0, 10, 0, '('),
    Token(')', lambda: None, 0, 10, 0, ')'),
]

glob_funcs = {}
for func in glob_func_list + custom_func_list:
    glob_funcs.update({func.name: func})

glob_syntax = {}
for syntax in glob_syntax_list:
    glob_syntax.update({syntax.name: syntax})

glob_trigpow = {
    'sin': Token('sin^', lambda a, b: Quantity.sin(a) ** b, 2, 3, 1, 'func'),
    'cos': Token('cos^', lambda a, b: Quantity.cos(a) ** b, 2, 3, 1, 'func'),
    'tan': Token('tan^', lambda a, b: Quantity.tan(a) ** b, 2, 3, 1, 'func'),
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

    class EmptyOutputError(Exception):
        """An error to be raised for an empty output."""

    def __init__(self):
        """The initialiser of the class."""
        self.err = None
        self.link = 'ans'
        self.silent = False
        self.reset_vars()

    def reset_vars(self):
        helptext = 'This is clic calculator. :q -- quit, please see README.md'
        self.vars = {'_': Decimal(0), 'help': helptext} | si_units

    def run_command(self, string):
        """Run command according to the given string expression.

        Arguments:
        string -- the string expression.

        Returns:
        done -- was the command run or not.
        """
        if not string:
            return True
        if not string.startswith(':'):
            return False
        ls = string.split()
        # quit the calculator
        if ls[0] == ':q':
            sys.exit()
        # delete variable (opposite to assignment)
        elif ls[0] == ':d':
            if len(ls) > 1:
                if ls[1] == '_':
                    self.vars['_'] = Decimal(0)
                if ls[1] in list(self.vars):
                    del self.vars[ls[1]]
            return True
        Calculator.CompilationError(f"unknown command: '{ls[0]}'")

    def split(self, string):
        """Split the given string expression."""
        changes = {'⋅': '*', '×': '*',
                   '÷': ':', '{': '(', '}': ')'}
        # characters that behave like alphabetical
        alpha = '_'
        # desimal separator characters
        decseps = '.'
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
                ans.append(Token(word, get, 0, 10, 0, 'str'))
            elif word.isdigit() or '.' in word:
                num = Decimal(word)
                ans.append(Token(word, Token.give(num), 0, 10, 0, 'num'))
            elif word in glob_funcs:
                ans.append(glob_funcs[word])
            elif word in self.vars:
                get = Token.give(self.vars[word])
                ans.append(Token(word, get, 0, 10, 0, 'var'))
            else:
                raise Calculator.CompilationError(f"unknown name: '{word}'")
        return ans

    def complete_infix_notation(self, ls):
        """Add ommited operators to a list of tokens."""
        last = glob_syntax['(']
        ans = []
        for token in ls:
            match (last.kind, token.name):
                case ('(' | 'oper' | 'func' | 'trig', '+'):
                    pass
                case ('(' | 'oper' | 'func' | 'trig', '-'):
                    ans.append(glob_funcs['_neg_'])
                case ('trig', '^'):
                    ans[-1] = glob_trigpow[last.name]
                case _:
                    match last.kind, token.kind:
                        case ('var', 'var' | '(' | 'num'):
                            ans.append(glob_funcs['_dot_'])
                        case ('var' | ')' | 'num', 'var'):
                            ans.append(glob_funcs['_dot_'])
                        case (')', '('):
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
            if token.name == '(':
                oper_stack.append(token)
            elif token.name == ')':
                while oper_stack[-1].name != '(':
                    output.append(oper_stack.pop())
                oper_stack.pop()
            elif token.ltor:
                while oper_stack and oper_stack[-1].name != '(' \
                        and token.pref < oper_stack[-1].pref:
                    output.append(oper_stack.pop())
                oper_stack.append(token)
            else:
                while oper_stack and oper_stack[-1].name != '(' \
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

    def calculate(self, expr):
        """Calculate expression exp and store the answer."""
        for exp in expr.split(';'):
            try:
                self.silent = False
                done = self.run_command(exp)
                if done:
                    self.silent = True
                    return None
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

        Returns:
        flag -- is the output an error,
        output -- the error / answer (as a string).
        """
        if self.err:
            raise self.err
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
        if flag:
            print(f'! {ans}')
        elif ctor.silent:
            continue
        else:
            print(f'= {ans}')
        # print()
