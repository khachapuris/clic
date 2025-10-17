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
from mathclasses import UnknownName

from token import Token
from setup import exporttokens as default_tokens
from setup import exportmappings as default_mappings

from config import CONFIG

import importlib
import os
import os.path as os_path

# The default help text
HELP_TEXT = "This is clic calculator. \
Type 'exit' to quit, please see MANUAL.md"

QUOTE = CONFIG['system']['quote']
ASSIGNMENT_OPERATOR = CONFIG['system']['assignment_operator']


class Calculator:
    """The Calculator object provides methods for calculating expressions."""

    class CompilationError(Exception):
        """An compilation error class for the calculator."""

    class EmptyOutputError(Exception):
        """An error to be raised for an empty output."""

    def __init__(self, helptext=HELP_TEXT):
        """The initialiser of the class."""
        self.err = None
        self.link = CONFIG['expression']['answer_name']
        self.silent = False
        self.reset_vars()
        self.update_modules()
        self.helptext = helptext

    def reset_vars(self):
        """Reset all variables."""
        self.vars = dict()
        self.assign_ans(Decimal(0))
        for token in default_tokens:
            self.vars.update({token.name: token})
        self.completion = default_mappings

    def update_modules(self):
        """Update the list of all modules."""
        load_all = CONFIG['modules']['load_all']
        path_to_modules = os_path.join(os_path.dirname(__file__), 'modules')
        for filename in os.listdir(path_to_modules):
            # Directories
            if not os_path.isfile(os_path.join(path_to_modules, filename)):
                continue
            # Not python files
            if not filename.endswith('.py') or filename == '__init__.py':
                continue
            module = filename[:-3]
            # Ignored modules
            if load_all and module in CONFIG['modules']['exclude']:
                continue
            if not load_all and module not in CONFIG['modules']['load']:
                continue
            try:
                exporttokens = getattr(
                    importlib.import_module(f'modules.{module}'),
                    'exporttokens',
                )
            except AttributeError:
                raise Calculator.CompilationError(
                    f"invalid module: '{module}'",
                )
            try:
                exportmappings = getattr(
                    importlib.import_module(f'modules.{module}'),
                    'exportmappings',
                )
                self.completion.update(exportmappings)
            except AttributeError:
                pass
            for token in exporttokens:
                self.vars.update({token.name: token})

    def assign_ans(self, ans, link=CONFIG['system']['answer_name']):
        """Set variable with name link to a token containing ans."""
        self.vars |= {link: Token.wrap(ans, name=link)}

    def isalphaplus(self, x):
        """Return whether x is alphabetical / semi-alphabetical or not."""
        return (x.isalpha() and x.isascii()) \
            or x in CONFIG['system']['alphabet_extra']

    def split(self, string):
        """Split the given string expression."""
        ans = [[]]
        space = True
        in_string = False
        in_name = False
        parenthesis_level = 0
        braces_level = 0

        def new_word_if(divide, c):
            """Add a new word / character to ans.

            If divide is True, add a new word c to ans;
            otherwise append c to the last word.
            """
            nonlocal space
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
            if char == QUOTE:
                # Is it an opening quote
                condition = not in_string
                new_word_if(condition, char)
                in_string = not in_string
            # Character inside a calculator string
            elif in_string:
                new_word_if(False, char)
            # Space
            elif char == ' ':
                space = True
                in_name = False
            # Expression separator
            elif char == CONFIG['expression']['expression_separator'] \
                    and braces_level == 0:
                ans.append([])
            # Decimal separator:
            elif char in CONFIG['number']['decimal_separators']:
                new_word_if(space, '.')
            # Thousands separator:
            elif char in CONFIG['number']['thousands_separators']:
                new_word_if(space, '' if last.isdigit() else char)
            # Letter:
            elif self.isalphaplus(char):
                new_word_if(not in_name, char)
                in_name = True
            # Digit:
            elif char.isdigit():
                new_word_if(space, char)
            # Symbol:
            else:
                # Count open braces (for correct expression splitting)
                if char in CONFIG['system']['opening_braces']:
                    braces_level += 1
                if char in CONFIG['system']['closing_braces']:
                    braces_level -= 1
                # Watch out for unmatched parentheses
                if char == '(':
                    parenthesis_level += 1
                if char == ')':
                    parenthesis_level -= 1
                    if parenthesis_level < 0:
                        raise ValueError('unmatched paretheses')
                new_word_if(True, char)
                space = True
                in_name = False
        if parenthesis_level != 0:
            raise ValueError('unmatched paretheses')
        if in_string:
            raise ValueError('unclosed quote')
        if CONFIG['global']['show_debug']:
            print('splitted:          ', ans)
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
        # list all variables
        elif ls[0] == 'list':
            self.assign_ans('  '.join([str(v) for v in list(self.vars)]))
            self.silent = False
            return True
        # help
        elif ls[0] == 'help':
            if len(ls) == 1:
                self.assign_ans(self.helptext)
                self.silent = False
                return True
            if len(ls) == 2 and ls[1].strip(QUOTE) in self.vars:
                self.assign_ans(
                    self.vars[ls[1].strip(QUOTE)].get_help()
                )
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
        if len(ls) > 2 and ls[1] == ASSIGNMENT_OPERATOR:
            name = ls[0]
            if name in self.vars and self.vars[name].kind != 'var':
                raise Calculator.CompilationError('assignment error')
            self.link = name
            return ls[2:]
        # compound assignment (x += 1)
        if len(ls) > 2 and ls[2] == ASSIGNMENT_OPERATOR:
            name = ls[0]
            if name not in self.vars:
                raise Calculator.CompilationError('compound assignment error')
            self.link = name
            return ls[:2] + ls[3:]
        self.link = CONFIG['expression']['answer_name']
        return ls

    def tokenize(self, ls):
        """Transform a list of strings to a list of Token objects."""
        ans = []
        for word in ls:
            if word[0] == QUOTE:
                get = Token.give(word.strip(QUOTE))
                ans.append(Token(word, get, 'static', 'str'))
            # # HACK: Create a standard for opening & closing operators
            # elif word[0] == '√':
            #     ans.append(self.vars[word])
            #     ans.append(self.vars['('])
            # elif word == "'":
            #     ans.append(self.vars[')'])
            elif word[0].isdigit() or word[0] == '.':
                num = Decimal(word)
                ans.append(Token(word, Token.give(num), 'static', 'num'))
            elif word in self.vars:
                ans.append(self.vars[word])
            else:
                ans.append(Token.wrap(
                    UnknownName(word),
                    name=f'<?{word}?>'
                ))
                # raise Calculator.CompilationError(f"unknown name: '{word}'")
        if CONFIG['global']['show_debug']:
            print('tokenized:         ', ans)
        return ans

    def complete_infix_notation(self, ls):
        """Add omited operators to a list of tokens."""
        last = self.vars['(']
        ans = []
        pairs = []
        for token in ls:
            if last.name + ' ' + token.name in list(self.vars):
                ans[-1] = self.vars[last.name + ' ' + token.name]
                last = ans[-1]
                continue
            match (last.kind, token.kind):
                case ('var' | ')' | 'num' | 'clos', 'open'):
                    pairs += token.name
                    ans += [
                        self.vars[CONFIG['system']['implicit_mul_name']],
                        token,
                        self.vars['(']
                    ]
                case (_, 'open'):
                    pairs += token.name
                    ans += [
                        token,
                        self.vars['(']
                    ]
                case (_, 'clos'):
                    if not pairs:
                        raise Calculator.CompilationError(
                            f"unclosed '{token.name}'"
                        )
                    elif token.closes == pairs[-1]:
                        pairs.pop()
                    else:
                        raise Calculator.CompilationError(
                            f"unclosed '{token.closes}'"
                        )
                    ans += [
                        self.vars[')']
                    ]
                case ('(' | 'oper' | 'func', 'oper'):
                    alt = ' ' + token.name
                    if alt in self.vars:
                        ans += [self.vars[alt]]
                    else:
                        ans += [token]
                case ('num', 'num'):
                    ans += [token]
                case (
                    'var' | ')' | 'num' | 'clos',
                    'var' | '(' | 'num' | 'func'
                ):
                    ans += [
                        self.vars[CONFIG['system']['implicit_mul_name']],
                        token
                    ]
                case _:
                    ans += [token]
            last = ans[-1]
        if CONFIG['global']['show_debug']:
            print('completed:         ', ans)
        if pairs:
            raise Calculator.CompilationError(f"unclosed '{pairs[-1]}'")
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
        ans = output + oper_stack[::-1]
        if CONFIG['global']['show_debug']:
            print('postfix notation:  ', ans)
        return ans

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
            ans = new
        else:
            ans = type_test(a, i)
        if CONFIG['global']['show_debug']:
            print('answer:            ', ans)
            print()
        return ans

    def object_to_string(self, obj):
        """Represent obj as a string."""
        if obj is None:
            return ''
        if isinstance(obj, UnknownName):
            obj.raise_error()
        if isinstance(obj, str):
            return f'"{obj}"'
        if isinstance(obj, Decimal):
            notation = CONFIG['number']['notation']
            return decimal_to_string(obj, notation=notation)
        return str(obj)

    def calculate(self, expr):
        """Calculate expression exp and store the answer."""
        try:
            for exp in self.split(expr):
                if self.run_command(exp):
                    continue
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
            if CONFIG['global']['show_debug']:
                raise self.err
            return (True, f'{str(self.err)}')
        ans = self.vars[CONFIG['system']['answer_name']].calc()
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
