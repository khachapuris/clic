"""This module contains a list of tokens that are loaded by default."""

from decimal import Decimal
from copy import copy

from clic.mathclasses import Vector, Array
from clic.mathclasses import glob_pi, glob_e, glob_inf
from clic.config import CONFIG


imp = CONFIG['system']['implicit_mul_name']
vec = CONFIG['expression']['vector_separator']
sq_root = (lambda a: a ** Decimal('0.5'))

exporttokens = [
    [['('], lambda: None, 'static', '(', 'Opening parenthesis'],
    [[')'], lambda: None, 'static', ')', 'Closing parenthesis'],
    [['+'], lambda a, b: a + b, 'addition', 'oper', 'Addition'],
    [['-'], lambda a, b: a - b, 'addition', 'oper', 'Subtraction'],
    [['*'], lambda a, b: a * b, 'mul-tion', 'oper', 'Multiplication'],
    [[':'], lambda a, b: a / b, 'mul-tion', 'oper', 'Inline division'],
    [['^'], lambda a, b: a ** b, 'strong', 'oper', 'Exponentiation',
     'reverse'],
    [[' -'], lambda a: -a, 'strong', 'func', 'Negation'],
    [[' +'], lambda a: +a, 'strong', 'func', 'Positition'],
    [[imp], lambda a, b: a * b, 'normal', 'oper', 'Implicit multiplication',
     'reverse'],
    [[vec], Vector.join,         'light', 'oper', 'Argument separator'],
    [['/'], lambda a, b: a / b,  'light', 'oper', 'Fraction bar'],
    [['∞', 'INF'], lambda: copy(glob_inf), 'static', 'var', 'Infinity'],
    [['π', 'pi'], lambda: copy(glob_pi),   'static', 'var', 'The number pi'],
    [['e'], lambda: copy(glob_e),          'static', 'var', 'The number e'],
    [['sqrt'], sq_root,   'strong', 'func', 'Square root'],
    [['√'], sq_root,      'static', 'open', 'Square root', 'regular', "'"],
    [["'"], lambda: None, 'static', 'clos', 'Square root', 'regular', '√'],
    [['..'], Array.from_range, 'strong', 'oper', 'Create array by range'],
]

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
    'sqrt':   '√', 'sigmaf': 'ς', 'pm':      '±', 'infty':   '∞',
    # Shortcuts
    'ee': ' * 10^',
}
