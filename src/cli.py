#!/usr/bin/env python

"""This script contains a command line interface for clic calculator.

It runs the calculator with a prompt.
"""

from calculator import Calculator
from config import CONFIG
import sys


def greek_completer(text, state):
    vocab = {
        # Greek alphabet (uppercase)
        'Alpha':   'Α', 'Beta':  'Β', 'Gamma':   'Γ', 'Delta':   'Δ',
        'Epsilon': 'Ε', 'Zeta':  'Ζ', 'Eta':     'Η', 'Theta':   'Θ',
        'Iotta':   'Ι', 'Kappa': 'Κ', 'Lambda':  'Λ', 'Mu':      'Μ',
        'Nu':      'Ν', 'Xi':    'Ξ', 'Omicron': 'Ο', 'Pi':      'Π',
        'Rho':     'Ρ', 'Sigma': 'Σ', 'Tau':     'Τ', 'Upsilon': 'Υ',
        'Phi':     'Φ', 'Chi':   'Χ', 'Psi':     'Ψ', 'Omega':   'Ω',
        # Greek alphabet (lowercase)
        'alpha':   'α', 'beta':  'β', 'gamma':   'γ', 'delta':   'δ',
        'epsilon': 'ε', 'zeta':  'ζ', 'eta':     'η', 'theta':   'θ',
        'iotta':   'ι', 'kappa': 'κ', 'lambda':  'λ', 'mu':      'μ',
        'nu':      'ν', 'xi':    'ξ', 'omicron': 'ο', 'pi':      'π',
        'rho':     'ρ', 'sigma': 'σ', 'tau':     'τ', 'upsilon': 'υ',
        'phi':     'φ', 'chi':   'χ', 'psi':     'ψ', 'omega':   'ω',
        # Other
        'deg':     '°', 'sqrt':  '√', 'sigmaf':  'ς',
    }
    # With backslash
    for word in vocab:
        if text.endswith('\\' + word):
            start = '\\'.join(text.split('\\')[:-1])
            return [start + vocab[word]][state]
    # Without backslash
    for word in vocab:
        if text == word:
            return [vocab[word]][state]
    return None
    # if text in vocab:
    #     return [vocab[text], None][state]
    # return None


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


def single_prompt():
    """A nice single line one-time prompt."""
    helptext = '''
,~~~~~~~~~~~~~~~~ Basic help ~~~~~~~~~~~~~~~~,
| exit -- exit the calculator                |
| help -- display this help                  |
| list -- list available functions & units   |
| help <NAME> -- help on a specific function |
'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
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
            print(LINE_UP, end=LINE_CLEAR)
            print(f'{PROMPT}{exp} = {ans}')
        else:
            print(f'= {ans}')


def command_line_calc():
    """Calculate using command line arguments."""
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
            while True:
                single_prompt()
