"""This module defines logarithms."""

from clic.token import Token

from clic.mathclasses import Vector


def logarithm(args):
    if type(args).__name__ == 'Vector':
        args = list(args)
        return args[1].log10() / args[0].log10()
    return args.log10()


exporttokens = [
    Token('log', logarithm, 'normal', 'func', 'Logarithm'),
    Token('ln', lambda a: a.ln(), 'normal', 'func', 'Natural logarithm'),
]
