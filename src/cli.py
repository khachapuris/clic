#!/usr/bin/env python

"""This script contains a command line interface for clic calculator.

It runs the calculator with a prompt.
"""

from calculator import Calculator
import sys


PROMPT = '\033[1;32mclic:\033[0m '


def prompt():
    """A minimal prompt for the calculator."""
    helptext = '''
,~~~~~~~~~~~~~~~~ Basic help ~~~~~~~~~~~~~~~~,
| exit -- exit the calculator                |
| ls f -- list available functions           |
| ls u -- list available units               |
| help <NAME> -- help on a specific function |
'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
    ctor = Calculator(helptext=helptext)
    print(',~~~~~~~~~~~~~~~~~~~~~~~~~~~~~,')
    print('| Welcome to clic calculator! |')
    print("| Type 'help' for basic help, |")
    print('|    please see MANUAL.md     |')
    print("'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'")
    while True:
        try:
            exp = input(PROMPT)
        except (KeyboardInterrupt, EOFError):
            print('exit')
            sys.exit()
        ctor.calculate(exp)
        flag, ans = ctor.get_answer()
        if flag:
            print(f'! {ans}')
        elif ctor.silent:
            continue
        else:
            print(f'= {ans}')
        print()


if __name__ == '__main__':
    try:
        # readline is used to improve standard input UX
        import readline
    except ImportError:
        pass
    prompt()
