"""This module defines logarithms."""


def logarithm(args):
    if type(args).__name__ == 'ArgList':
        args = list(args)
        return args[1].log10() / args[0].log10()
    return args.log10()


def log_exp(a, b):
    """Exponentiation shorthand for the log function."""
    if a > 0:
        return logarithm(b) ** a
    raise ValueError('raising function to negative exponent')


def ln_exp(a, b):
    """Exponentiation shorthand for the ln function."""
    if a > 0:
        return b.ln() ** a
    raise ValueError('raising function to negative exponent')


CLIC_TOKENS = [
    [['log'], logarithm, 'normal func', 'Logarithm'],
    [['log ^'], log_exp, 'normal doub', 'Logarithm'],
    [['ln'], lambda a: a.ln(), 'normal func', ''],
    [['ln ^'], ln_exp,         'normal doub', ''],
]
