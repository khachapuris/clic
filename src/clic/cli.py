#!/usr/bin/env python

"""This script contains a command line interface for clic calculator.

It runs the calculator with a prompt.
"""

from clic.calculator import Calculator
from clic.config import CONFIG
import sys
import argparse
import tomllib
import os


CONFIG['system']['help_text'] = '''
,~~~~~~~~~~~~~~~~ Basic help ~~~~~~~~~~~~~~~~,
| exit -- exit the calculator                |
| help -- display this help                  |
| list -- list available functions & units   |
| help <NAME> -- help on a specific function |
'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''

PROMPT = f'\001\033[{CONFIG["view"]["prompt_color"]}m\002clic:\001\033[0m\002 '
LINE_UP = '\001\033[1A\002'
LINE_CLEAR = '\001\x1b[2K\002'


def get_version():
    path_to_pyproject = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'pyproject.toml'
    )
    with open(path_to_pyproject, 'rb') as f:
        pyproject_data = tomllib.load(f)
        return pyproject_data['project']['version']


def overlap(a, b):
    # print(a, b)
    for i in range(0, len(a)):
        if b.startswith(a[-i-1:]):
            return i
    return 0


def create_completer(bindings, vocab):
    vocab = [word for word in vocab if ' ' not in word]
    bindlist = list(bindings)
    bindlist.sort(key=len, reverse=False)
    bindlist_reverse = list(bindings)
    bindlist_reverse.sort(key=len, reverse=True)

    def completer(text, state):
        # With backslash
        for word in bindlist:
            if overlap(text[-len(bindlist_reverse[0]):], '\\' + word):
                start = '\\'.join(text.split('\\')[:-1])
                return [start + bindings[word]][state]
        # Without backslash
        for word in bindlist_reverse:
            # if text == word:
            #     return [bindings[word]][state]
            if text.endswith(word):
                return text[:-len(word)] + [bindings[word]][state]
        # Variable completion
        if state == 0 and len(text) > 0:
            matches = [c for c in vocab if c.startswith(text)]
            if len(matches) == 1:
                return matches[0] + " "
        return None

    return completer


def single_prompt(ctor):
    """A nice single line one-time prompt."""
    try:
        exp = input(PROMPT)
    except (KeyboardInterrupt, EOFError):
        print()
        print(LINE_UP, end=LINE_CLEAR)
        sys.exit()
    ctor.calculate(exp)
    flag, ans = ctor.get_answer()
    if flag:
        print(f'! {ans}')
    elif ctor.silent:
        pass
    else:
        if CONFIG['view']['oneline']:
            if not CONFIG['global']['show_debug']:
                print(LINE_UP, end=LINE_CLEAR)
            print(f'{PROMPT}{exp} = {ans}')
        else:
            print(f'= {ans}')
    return ctor


def bare_prompt(ctor):
    """A prompt without any decorations."""
    try:
        exp = input()
    except KeyboardInterrupt:
        sys.exit(130)
    except EOFError:
        sys.exit(0)
    ctor.calculate(exp)
    flag, ans = ctor.get_answer()
    if flag:
        print(ans, file=sys.stderr)
    elif ctor.silent:
        pass
    else:
        if CONFIG['view']['oneline']:
            print(f'{exp} = {ans}')
        else:
            print(ans)
    return ctor


def app():
    parser = argparse.ArgumentParser(
        color=False,
        usage='%(prog)s [-h|-v] [--debug] [expression]',
        description='CLIC command line calculator',
    )
    parser.add_argument('-v', '--version', action='version',
                        version=f'%(prog)s {get_version()}')
    parser.add_argument('-b', '--bare', action='store_true',
                        help='do not prettify output')
    parser.add_argument('--debug', action='store_true',
                        help='run with debug options on')
    parser.add_argument('expression', nargs=argparse.REMAINDER,
                        help='the expression to calculate')
    args = parser.parse_args()

    CONFIG['global'].update({'show_debug': args.debug})
    prompt_function = bare_prompt if args.bare else single_prompt

    if args.expression:
        # Non-interactive
        ctor = Calculator(config=CONFIG)
        ctor.calculate(' '.join(args.expression))
        flag, ans = ctor.get_answer()
        if flag:
            print(ans, file=sys.stderr)
        elif ctor.silent:
            pass
        else:
            print(ans)
    else:
        # Interactive
        ctor = Calculator(config=CONFIG)
        # Impove standard UX
        try:
            import readline
            readline.parse_and_bind('tab: complete')
            readline.set_completer_delims(' ')
            readline.set_completer(create_completer(
                ctor.completion,
                ctor.vars | {'help': 'help', 'exit': 'exit', 'list': 'list'}
            ))
        except ImportError:
            print('WARNING: Could not import the "readline" module. \
The interface may now be missing some features like completion and history.',
                  file=sys.stderr)
        if CONFIG['view']['loop']:
            while True:
                prompt_function(ctor)
        else:
            prompt_function(ctor)


if __name__ == '__main__':
    app()
