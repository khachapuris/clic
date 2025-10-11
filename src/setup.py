"""This module contains a list of tokens that are loaded by default.

To register custom functions add corresponding tokens to the list.
"""

from token import Token

from decimal import Decimal
from mathclasses import Vector
from mathclasses import glob_pi, glob_e
from config import CONFIG


imp = CONFIG['system']['implicit_mul_name']
vec = CONFIG['expression']['vector_separator']
sq_root = (lambda a: a ** Decimal('0.5'))


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
    Token('sqrt', sq_root, 'strong', 'func', 'Square root'),
    *Token.wrap_with_alt(glob_pi, names=['π', 'pi'], ht='The number pi'),
    Token.wrap(glob_e,  name='e',  ht='The number e'),
    Token('√', sq_root,      'static', 'open', 'Square root', closes="'"),
    Token("'", lambda: None, 'static', 'clos', 'Square root', closes='√'),
}

exportmappings = {
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
    # Function-specific
    'sqrt':  '√', 'sigmaf':  'ς', 'pm':      '±',
}
