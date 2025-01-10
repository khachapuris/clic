#!/usr/bin/env python

"""This script contains a command line interface for clic calculator.

It runs the calculator with a prompt.
"""

from calculator import Calculator
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
    for word in vocab:
        if text.endswith('\\' + word):
            start = '\\'.join(text.split('\\')[:-1])
            return [start + vocab[word]][state]
    return None
    # if text in vocab:
    #     return [vocab[text], None][state]
    # return None


PROMPT = '\033[1;32mclic:\033[0m '


def prompt():
    """A minimal prompt for the calculator."""
    helptext = '''
,~~~~~~~~~~~~~~~~ Basic help ~~~~~~~~~~~~~~~~,
| exit -- exit the calculator                |
| help -- display this help                  |
| list -- list available functions & units   |
| load -- list available modules             |
| help <NAME> -- help on a specific function |
| load <NAME> -- load module                 |
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
        prompt()
