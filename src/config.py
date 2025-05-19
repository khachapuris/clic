"""This modules gets the config from a TOML file."""
import tomllib
import os

path = os.path.expanduser('/home/john/.clicconfig.toml')
with open(path, 'rb') as file:
    user_config = tomllib.load(file)['global']

permanent_config = {
    'quote': '"',
    'alphabet_extra': '_',
    'assignment_operator': '=',
    'system_answer_name': '_',
    'implicit_mul_name': 'dot',
}

default_config = {
    'number': {
        'notation': 'classic',
        'decimal_separators': '.',
        'thousands_separators': '_',
    },
    'vector_separator': ',',
    'expression_separator': ';',
    'show_debug': False,
    'answer_name': 'ans',
    'modules': {
        'load_all': True,
        'load': [],
        'exclude': [],
    },
}

config = default_config | user_config | permanent_config
