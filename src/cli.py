#!/usr/bin/env python

"""This script contains a command line interface for clic calculator.

It runs the calculator with a prompt.
"""

from calculator import Calculator
from config import CONFIG
import sys


def overlap(a, b):
    # print(a, b)
    for i in range(0, len(a)):
        if b.startswith(a[-i-1:]):
            return i
    return 0


def greek_completer(text, state):
    vocab = {
        # Greek alphabet (uppercase)
        'Alpha':   'Α', 'Beta':  'Β', 'Gamma':   'Γ', 'Delta':   'Δ',
        'Epsilon': 'Ε', 'Zeta':  'Ζ', 'Eta':     'Η', 'Theta':   'Θ',
        'Iota':    'Ι', 'Kappa': 'Κ', 'Lambda':  'Λ', 'Mu':      'Μ',
        'Nu':      'Ν', 'Xi':    'Ξ', 'Omicron': 'Ο', 'Pi':      'Π',
        'Rho':     'Ρ', 'Sigma': 'Σ', 'Tau':     'Τ', 'Upsilon': 'Υ',
        'Phi':     'Φ', 'Chi':   'Χ', 'Psi':     'Ψ', 'Omega':   'Ω',
        # Greek alphabet (lowercase)
        'alpha':   'α', 'beta':  'β', 'gamma':   'γ', 'delta':   'δ',
        'epsilon': 'ε', 'zeta':  'ζ', 'eta':     'η', 'theta':   'θ',
        'iota':    'ι', 'kappa': 'κ', 'lambda':  'λ', 'mu':      'μ',
        'nu':      'ν', 'xi':    'ξ', 'omicron': 'ο', 'pi':      'π',
        'rho':     'ρ', 'sigma': 'σ', 'tau':     'τ', 'upsilon': 'υ',
        'phi':     'φ', 'chi':   'χ', 'psi':     'ψ', 'omega':   'ω',
        # Other
        'deg':     '°', 'sqrt':  '√', 'sigmaf':  'ς',
    }
    # With backslash
    for word in vocab:
        if overlap(text[-10:], '\\' + word):
            start = '\\'.join(text.split('\\')[:-1])
            return [start + vocab[word]][state]
    # Without backslash
    for word in vocab:
        if text == word:
            return [vocab[word]][state]
    return None


PROMPT = f'\033[{CONFIG["view"]["prompt_color"]}mclic:\033[0m '
LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'


def prompt():
    """A minimal prompt for the calculator."""
    helptext = '''
,~~~~~~~~~~~~~~~~ Basic help ~~~~~~~~~~~~~~~~,
| exit -- exit the calculator                |
| help -- display this help                  |
| list -- list available functions & units   |
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


def single_prompt(ctor=None):
    """A nice single line one-time prompt."""
    helptext = '''
,~~~~~~~~~~~~~~~~ Basic help ~~~~~~~~~~~~~~~~,
| exit -- exit the calculator                |
| help -- display this help                  |
| list -- list available functions & units   |
| help <NAME> -- help on a specific function |
'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
    if ctor is None:
        ctor = Calculator(helptext=helptext)
    try:
        if CONFIG['view']['replace_console_prompt']:
            print(LINE_UP, end=LINE_CLEAR)
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


def command_line_calc():
    """Calculate using command line arguments."""
    if sys.argv[1] == '--help':
        print('CLIC command-line calculator')
        print('Usage:  clic [--help,--version] [expression]')
        sys.exit()
    elif sys.argv[1] == '--version':
        print('clic 1')
        sys.exit()
    ctor = Calculator()
    ctor.calculate(''.join(sys.argv[1:]))
    flag, ans = ctor.get_answer()
    if flag:
        print(f'! {ans}')
    elif ctor.silent:
        pass
    else:
        print(f'= {ans}')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        command_line_calc()
    else:
        # impove standard UX
        import readline
        readline.parse_and_bind('tab: complete')
        readline.set_completer_delims('0123456789!@#$%^&*()-+=`~\'"<,.>/?:;| ')
        readline.set_completer(greek_completer)
        if CONFIG['view']['quit_after_first_input']:
            single_prompt()
        else:
            ctor = single_prompt()
            while True:
                single_prompt(ctor)
