#!/usr/bin/env python

"""This script contains a command line interface for clic calculator.

It runs the calculator with a prompt.
"""

from calculator import Calculator
import readline


def greek_completer(text, state):
    vocab = {
        # Greek alphabet
        'alpha':   'α', 'beta':  'β', 'gamma':   'γ', 'delta':   'δ',
        'epsilon': 'ε', 'zeta':  'ζ', 'eta':     'η', 'theta':   'θ',
        'iotta':   'ι', 'kappa': 'κ', 'lambda':  'λ', 'mu':      'μ',
        'nu':      'ν', 'xi':    'ξ', 'omicron': 'ο', 'pi':      'π',
        'rho':     'ρ', 'sigma': 'σ', 'tau':     'τ', 'upsilon': 'υ',
        'phi':     'φ', 'chi':   'χ', 'psi':     'ψ', 'omega':   'ω',
        # Other
        'deg': '°',
    }
    if text in vocab:
        return [vocab[text], None][state]
    return None


def prompt():
    """A minimal prompt for the calculator."""
    helptext = '''
,~~~~~~~~~~~~~~~~ Basic help ~~~~~~~~~~~~~~~~,
| exit -- exit the calculator                |
| ls f -- list available functions           |
| ls u -- list available units               |
| help <NAME> -- help on a specific function |
'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
    ctor = Calculator({
        'help': helptext,
        '_prompt': '\033[1;32mclic:\033[0m ',
    })
    print(',~~~~~~~~~~~~~~~~~~~~~~~~~~~~~,')
    print('| Welcome to clic calculator! |')
    print("| Type 'help' for basic help, |")
    print('|    please see MANUAL.md     |')
    print("'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'")
    while True:
        exp = input(ctor.vars['_prompt'])
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
    readline.parse_and_bind('tab: complete')
    readline.set_completer_delims('0123456789!@#$%^&*()-+=`~\'"<,.>/?:;\\| ')
    readline.set_completer(greek_completer)
    prompt()
