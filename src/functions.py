'''This module contains a dictionary with modules. Each module
contains a list of functions/operators for the calculator.
Modules can be loaded from the calculator with the 'load' command;
the default module is loaded by default.

To register custom functions add corresponding tokens to the desired module.
'''

import importlib
import os
import os.path as os_path
from os import listdir
from os.path import isfile, join

from token import Token

from decimal import Decimal
from mathclasses import Quantity, Vector
from mathclasses import glob_pi, glob_e
import mathfunctions as mf

import symbols as smbs


modules = {
    'default': [
        # These tokens are loaded by default
        Token('(', lambda: None, 10, 0, '(', 'Opening parhethesis'),
        Token(')', lambda: None, 10, 0, ')', 'Closing parenthesis'),
        Token('+', lambda a, b: a + b,  1, 0, 'oper', 'Addition'),
        Token('-', lambda a, b: a - b,  1, 0, 'oper', 'Subtraction'),
        Token('*', lambda a, b: a * b,  2, 0, 'oper', 'Multiplication'),
        Token(':', lambda a, b: a / b,  2, 0, 'oper', 'Inline division'),
        Token('^', lambda a, b: a ** b, 4, 1, 'oper', 'Exponentiation'),
        Token(' -', lambda a: -a,       4, 1, 'func', 'Negation'),
        Token(' +', lambda a: +a,       4, 1, 'func', 'Positition'),
        Token(smbs.sv['implicit'], lambda a, b: a * b, 3, 1, 'oper',
              'Implicit multiplication'),
        Token(',', Vector.join,         0, 0, 'oper', 'Argument separator'),
        Token('/', lambda a, b: a / b,  0, 0, 'oper', 'Fraction bar'),
        Token('sqrt', lambda a: a ** Decimal('0.5'), 4, 1, 'func',
              'Square root'),
        Token.wrap(glob_pi, name='pi', ht='The number pi'),
        Token.wrap(glob_e,  name='e',  ht='The number e'),
        # Alternative names
        Token.wrap(glob_pi, name='π',  ht='The number pi'),
        Token('√', lambda a: a ** Decimal('0.5'), 4, 1, 'func',
              'Square root'),

        # Place your custom tokens here
    ],
}


# Import all modules from the 'modules' directory
onlyfiles = []
my_path = os_path.join(os_path.dirname(__file__), 'modules')
for filename in os.listdir(my_path):
    if os_path.isfile(os_path.join(my_path, filename)):
        if filename.endswith('.py') and filename != '__init__.py':
            onlyfiles.append(filename[:-3])

for filename in onlyfiles:
    exporttokens = getattr(importlib.import_module(f'modules.{filename}'), 'exporttokens')
    modules.update({filename: exporttokens})
