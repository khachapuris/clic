#!/usr/bin/env python

"""This script contains a calculator for calculating fixed-point expressions.

The script runs the calculator with a minimal prompt and can be used for
infix notation calculations. It can also be used as a module and provides
class Calculator. For more details please see README.md.
"""

import sys

import decimal
from decimal import Decimal
from mathclasses import Quantity, Vector

from token import Token
from functions import functions as glob_func_list
from units import units as glob_units


glob_syntax_list = [
    Token('(', lambda: None, 0, 10, 0, '('),
    Token(')', lambda: None, 0, 10, 0, ')'),
]

glob_funcs = {}
for func in glob_func_list:
    glob_funcs.update({func.name: func})

glob_syntax = {}
for syntax in glob_syntax_list:
    glob_syntax.update({syntax.name: syntax})

glob_smbs = {
    'alpha':  '_',   # characters that behave like alphabetical
    'decseps': '.',  # desimal separator characters
    'quote':  '"',   # start / end of a calculator string
    'expsep': ';',   # expression separator
}


def isalphaplus(c):
    return c.isalpha() or c in glob_smbs["alpha"]


def isdigitplus(c):
    return c.isdigit() or c in glob_smbs["decsep"]


def standard_decsep(c):
    if c in glob_smbs["decsep"]:
        return '.'
    return c


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
        self.vars = {'_': Decimal(0), 'help': helptext} | glob_units

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
        replace = {'{': '(', '}': ')'}
        ans = [[]]
        space = True
        in_string = False

        def add(ch, divide):
            nonlocal ans, space
            if divide:
                ans[-1].append(ch)
                space = False
            else:
                ans[-1][-1] += ch

        for char in string:
            if ans[-1]:
                last = ans[-1][-1][-1]
            else:
                last = ' '
            # Quote:
            if char == glob_smbs["quote"]:
                # Opening quote
                add(char, not in_string)
                in_string = not in_string
            # Character inside a calculator string
            elif in_string:
                add(char, False)
            # Expression separator
            elif char == glob_smbs["expsep"]:
                ans.append([])
            # Space
            elif char == ' ':
                space = True
            # Letter:
            elif isalphaplus(char):
                # Letter after not letter / letter after space
                add(char, not isalphaplus(last) or space)
            # Digit:
            elif isdigitplus(char):
                # Digit with a space before it
                add(standard_decsep(char), space)
            # Symbol:
            else:
                # Symbol from the replace dictionary
                if char in replace:
                    char = replace[char]
                add(char, True)
                space = True
        if in_string:
            raise ValueError('unclosed quotes')
        return ans[0]

    def perform_assignment(self, ls):
        """Change the assignment link according to a list of strings."""
        self.err = None
        # simple assignment (x = 1)
        if len(ls) > 2 and ls[1] == '=':
            if not ls[0][0].isalpha() or ls[0] in (glob_funcs | glob_units):
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
            elif word[0] == glob_smbs["quote"]:
                get = Token.give(word.strip(glob_smbs["quote"]))
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
            if last.name + ' ' + token.name in list(glob_funcs):
                ans[-1] = glob_funcs[last.name + ' ' + token.name]
                last = ans[-1]
                continue
            match (last.kind, token.name):
                case ('(' | 'oper' | 'func', '+'):
                    pass
                case ('(' | 'oper' | 'func', '-'):
                    ans.append(glob_funcs['_neg_'])
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
        if flag:
            print(f'! {ans}')
        elif ctor.silent:
            continue
        else:
            print(f'= {ans}')
        # print()
