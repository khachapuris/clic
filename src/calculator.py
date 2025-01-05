#!/usr/bin/env python

"""This script contains a calculator for calculating fixed-point expressions.

The script runs the calculator with a minimal prompt and can be used for infix
notation calculations. It can also be used as a module and provides class
Calculator and function minimal_prompt. For more details please see MANUAL.md.
"""

import sys

import decimal
from decimal import Decimal
from mathclasses import Quantity, Vector
from mathclasses import decimal_to_string

from token import Token
import symbols as smbs
from functions import modules


class Calculator:
    """The Calculator object provides methods for calculating expressions."""

    class CompilationError(Exception):
        """An compilation error class for the calculator."""

    class EmptyOutputError(Exception):
        """An error to be raised for an empty output."""

    def __init__(self, predefined=None):
        """The initialiser of the class."""
        self.err = None
        self.link = smbs.sv['ans']
        self.silent = False
        self.reset_vars(predefined)

    def reset_vars(self, predefined=None):
        self.vars = {
            smbs.sv['sysans']: Decimal(0),
            'help': smbs.sv['help']
        }
        self.assign_ans(Decimal(0))
        self.assign_ans(smbs.sv['help'], link='help')
        for module in ['essential', 'default', 'custom']:
            self.load_module(module)
        if predefined:
            self.vars.update(predefined)

    def assign_ans(self, ans, link=smbs.sv['sysans']):
        """Set variable with name link to a token containing ans."""
        self.vars |= {link: Token.wrap(ans, name=link)}

    def load_module(self, module):
        """Update self.vars with tokens from module."""
        if module in modules:
            for token in modules[module]:
                self.vars.update({token.name: token})
        else:
            raise Calculator.CompilationError(f"unknown module: '{module}'")

    def split(self, string):
        """Split the given string expression."""
        ans = [[]]
        space = True
        in_string = False

        def new_word_if(divide, c):
            """Add a new word / character to ans.

            If divide is True, add a new word c to ans;
            otherwise append c to the last word.
            """
            nonlocal ans, space
            if divide:
                ans[-1].append(c)
                space = False
            else:
                ans[-1][-1] += c

        for char in string:
            if ans[-1]:
                last = ans[-1][-1][-1]
            else:
                last = ' '
            # Quote:
            if char == smbs.cc['quote']:
                # Is it an opening quote
                condition = not in_string
                new_word_if(condition, char)
                in_string = not in_string
            # Character inside a calculator string
            elif in_string:
                new_word_if(False, char)
            # Expression separator
            elif char == smbs.cc['expsep']:
                ans.append([])
            # Space
            elif char == ' ':
                space = True
            # Letter:
            elif smbs.isalphaplus(char):
                # Does it go after a non-letter / some space
                condition = not smbs.isalphaplus(last) or space
                new_word_if(condition, char)
            # Digit:
            elif smbs.isdigitplus(char):
                new_word_if(space, smbs.standard_decsep(char))
            # Symbol:
            else:
                new_word_if(True, char)
                space = True
        if in_string:
            raise ValueError('unclosed quotes')
        return ans

    def run_command(self, ls):
        """Run command according to the given list of strings.

        Returns:
        done -- the expression does not need to be calculated.
        """
        self.silent = True
        self.err = None
        # empty input
        if not ls:
            return True
        # quit the calculator
        if ls[0] == 'exit':
            sys.exit()
        # delete variable (opposite to assignment)
        elif ls[0] == 'del':
            if len(ls) == 2:
                if ls[1] == smbs.sv['sysans']:
                    self.assign_ans(Decimal(0))
                if ls[1] in list(self.vars):
                    del self.vars[ls[1]]
            return True
        # list
        elif ls[0] == 'ls':
            self.assign_ans('  '.join([str(v) for v in list(self.vars)]))
            self.silent = False
            return True
        # import module
        elif ls[0] == 'use':
            if len(ls) == 2:
                self.load_module(ls[1])
            return True
        # help
        elif ls[0] == 'help':
            if len(ls) == 1:
                self.assign_ans(self.vars['help'])
            elif len(ls) == 2 and ls[1] in self.vars:
                self.assign_ans(self.vars[ls[1]].get_help())
            else:
                self.assign_ans(f"Could not find help on '{' '.join(ls[1:])}'")
            self.silent = False
            return True
        # not a command
        self.silent = False
        return False

    def perform_assignment(self, ls):
        """Change the assignment link according to a list of strings."""
        # simple assignment (x = 1)
        if len(ls) > 2 and ls[1] == smbs.cc['assign']:
            name = ls[0]
            if not smbs.isalphaplus(name[0]) \
                    or name == smbs.sv['sysans']:
                raise Calculator.CompilationError('assignment error')
            self.link = name
            return ls[2:]
        # compound assignment (x += 1)
        if len(ls) > 2 and ls[2] == smbs.cc['assign']:
            name = ls[0]
            if name not in self.vars:
                raise Calculator.CompilationError('compound assignment error')
            self.link = name
            return ls[:2] + ls[3:]
        self.link = smbs.sv['ans']
        return ls

    def tokenize(self, ls):
        """Transform a list of strings to a list of Token objects."""
        ans = []
        for word in ls:
            if word[0] == smbs.cc['quote']:
                get = Token.give(word.strip(smbs.cc['quote']))
                ans.append(Token(word, get, 10, 0, 'str'))
            elif smbs.isdigitplus(word[0], plus='.'):
                num = Decimal(word)
                ans.append(Token(word, Token.give(num), 10, 0, 'num'))
            elif word in self.vars:
                ans.append(self.vars[word])
            else:
                raise Calculator.CompilationError(f"unknown name: '{word}'")
        return ans

    def complete_infix_notation(self, ls):
        """Add omited operators to a list of tokens."""
        last = self.vars['(']
        ans = []
        for token in ls:
            if last.name + ' ' + token.name in list(self.vars):
                ans[-1] = self.vars[last.name + ' ' + token.name]
                last = ans[-1]
                continue
            match (last.kind, token.kind):
                case ('(' | 'oper' | 'func', 'oper'):
                    alt = ' ' + token.name
                    if alt in self.vars:
                        ans += [self.vars[alt]]
                    else:
                        ans += [token]
                case ('num', 'num'):
                    ans += [token]
                case ('var' | ')' | 'num', 'var' | '(' | 'num' | 'func'):
                    ans += [self.vars[smbs.sv['implicit']], token]
                case _:
                    ans += [token]
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
        if isinstance(obj, Decimal):
            return decimal_to_string(obj)
        return str(obj)

    def calculate(self, expr):
        """Calculate expression exp and store the answer."""
        try:
            for exp in self.split(expr):
                if self.run_command(exp):
                    return None
                exp = self.perform_assignment(exp)
                exp = self.tokenize(exp)
                exp = self.complete_infix_notation(exp)
                exp = self.shunting_yard_algorithm(exp)
                exp = self.perform_operations_twice(exp)
                self.assign_ans(exp)
                self.assign_ans(exp, link=self.link)
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
            raise self.err  # DEBUG
            return (True, f'{str(self.err)}')
        ans = self.vars[smbs.sv['sysans']].calc()
        if ans is None:
            return (True, '')
        ans = self.object_to_string(ans)
        return (False, ans)


def minimal_prompt():
    """A minimal prompt for the calculator."""
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


if __name__ == '__main__':
    try:
        # readline is used to improve standard input UX
        import readline
    except ImportError:
        pass
    minimal_prompt()
