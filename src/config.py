"""This modules gets the config from a TOML file."""
import tomllib
import os

default_toml = '''
# Number notation options:
# - classic (engineering + scientific)
# - engineering
# - scientific
# - normal (no exponent)
number.notation = "classic"
number.decimal_separators = "."
number.thousands_separators = "_"

modules.load_all = true
modules.load = []
modules.exclude = []

vector_separator = ","
expression_separator = ";"
show_debug = false
answer_name = "ans"
'''

path0 = os.path.expanduser('~/.clic')
path = os.path.expanduser('~/.clic/config.toml')
if os.path.exists(path):
    with open(path, 'rb') as file:
        user_config = tomllib.load(file)
else:
    if not os.path.exists(path0):
        os.mkdir(path0)
    with open(path, 'w') as file:
        file.write(default_toml)
    user_config = dict()

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
