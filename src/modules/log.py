"""This module defines logarithms."""


def logarithm(args):
    if type(args).__name__ == 'ArgList':
        args = list(args)
        return args[1].log10() / args[0].log10()
    return args.log10()


exporttokens = [
    [['log'], logarithm, 'normal func', 'Logarithm'],
    [['ln'], lambda a: a.ln(), 'normal func', 'Natural logarithm'],
]
