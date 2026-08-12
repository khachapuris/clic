"""This modules gets the config from a TOML file."""
import tomllib
import os
import shutil

default_config_path = os.path.abspath(
    str(os.path.dirname(__file__)) + '/../defaultconfig.toml'
)
with open(default_config_path, 'rb') as file:
    default_config = tomllib.load(file)

path0 = os.path.expanduser('~/.clic')
path = os.path.expanduser('~/.clic/config.toml')
if os.path.exists(path):
    with open(path, 'rb') as file:
        user_config = tomllib.load(file)
else:
    if not os.path.exists(path0):
        os.mkdir(path0)
    shutil.copy(default_config_path, path)
    user_config = dict()

system_config = {
    'quote': '"',
    'assignment_oper': '=',
    'alphabet_extra': '_μΔ°',
    'opening_braces': '([{',
    'closing_braces': '}])',
    'help_text': "Welcome to clic calculator! For the docs, see README.md"
}

CONFIG = dict()
for key in default_config:
    if key in user_config:
        CONFIG.update({
            key: default_config[key] | user_config[key]
        })
    else:
        CONFIG.update({
            key: default_config[key]
        })
CONFIG.update({
    'system': system_config,
})
