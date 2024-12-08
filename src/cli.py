#!/usr/bin/env python

"""This script contains a command line interface for clic calculator.

It runs the calculator with a prompt.
"""

from calculator import Calculator
import symbols as smbs


def prompt():
    """A minimal prompt for the calculator."""
    helptext = 'Basic help:\n'
    helptext += smbs.cc['command'] + 'exit -- exit the calculator,\n'
    helptext += smbs.cc['command'] + 'ls f -- list available functions,\n'
    helptext += smbs.cc['command'] + 'ls u -- list available units,\n'
    helptext += smbs.cc['command'] + 'help <FUNCTION> -- help on a function.\n'
    ctor = Calculator({'help': helptext})
    print(',~~~~~~~~~~~~~~~~~~~~~~~~~~~~~,')
    print('| Welcome to clic calculator! |')
    print("| Type 'help' for basic help, |")
    print('|    please see MANUAL.md     |')
    print("'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'")
    while True:
        exp = input('\033[1;32mclic:\033[0m ')
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
