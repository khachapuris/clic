"""This module contains a list of tokens that are loaded by default.

To register custom functions add corresponding tokens to the list.
"""

from token import Token

from decimal import Decimal
from mathclasses import Vector
from mathclasses import glob_pi, glob_e
from config import config as CONFIG


imp = CONFIG['implicit_mul_name']
vec = CONFIG['vector_separator']
square_root = (lambda a: a ** Decimal('0.5'))


exporttokens = {
    # These tokens are loaded by default
    Token('(', lambda: None, 'static', '(', 'Opening parhethesis'),
    Token(')', lambda: None, 'static', ')', 'Closing parenthesis'),
    Token('+', lambda a, b: a + b,  'addition', 'oper', 'Addition'),
    Token('-', lambda a, b: a - b,  'addition', 'oper', 'Subtraction'),
    Token('*', lambda a, b: a * b,  'mul-tion', 'oper', 'Multiplication'),
    Token(':', lambda a, b: a / b,  'mul-tion', 'oper', 'Inline division'),
    Token('^', lambda a, b: a ** b, 'strong', 'oper', 'Exponentiation',
          order='reverse'),
    Token(' -', lambda a: -a,      'strong', 'func', 'Negation'),
    Token(' +', lambda a: +a,      'strong', 'func', 'Positition'),
    Token(imp, lambda a, b: a * b, 'normal', 'oper', 'Implicit multiplication',
          order='reverse'),
    Token(vec, Vector.join,        'light', 'oper', 'Argument separator'),
    Token('/', lambda a, b: a / b, 'light', 'oper', 'Fraction bar'),
    Token('sqrt', square_root,     'strong', 'func', 'Square root'),
    Token.wrap(glob_pi, name='pi', ht='The number pi'),
    Token.wrap(glob_e,  name='e',  ht='The number e'),
    # Alternative names
    Token.wrap(glob_pi, name='π',  ht='The number pi'),
    Token('√', square_root,        'strong', 'func',
          'Square root'),
}
