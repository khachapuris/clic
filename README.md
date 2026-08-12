# CLIC

CLIC is a command line calculator written in Python. It offers various advanced
functions, operates with metric system units, and allows for bulk operations
and variable assignment. CLIC also comes with a built-in Greek letter and
symbol support, and is Python-extendable.

[![asciicast](https://asciinema.org/a/z3rbdHj3TR9ZqrsRCFLaJbnVC.png)](https://asciinema.org/a/z3rbdHj3TR9ZqrsRCFLaJbnVC)

## Installation

To install clic, follow these steps (the instructions are for Unix-like
systems; however, I am sure this can be done similarly on Windows):

1. Ensure you have `git` and `python3` installed
2. Clone the clic package: `git clone https://github.com/khachapuris/clic`
3. Now we will create a virtual environment and install the calculator with pip
(this avoids contradictions with the global environment):
    - stay outside of the `clic` folder
    - `mkdir clic-calculator`
    - `cd clic-calculator`
    - `python3 -m venv .venv` (creates a virtual environment)
    - `source .venv/bin/activate` (activates the virtual environment)
    - `python3 -m pip install --upgrade pip`
    - `python3 -m pip install -e <the-absolute-path>/clic` (installs clic)
4. To run the calculator, do `python3 -m clic`

To run the calculator in a single command, create a bash script somewhere in
your $PATH with the following contents:

```bash
# File called `clic` in your $PATH

# Activate the virtual environment
cd <the-absolute-path>/clic-calculator
source .venv/bin/activate

# Run the calculator with all arguments provided
if [[ -z "$@" ]]; then
    python -m clic
else
    python -m clic ''"$@"''
fi

# Close everything when finished
deactivate
```

Now just write `clic` from anywhere in your command line to start the
calculator.

## Usage

For the fun part, you can skip down to Basic calculations

### Navigation

These commands used inside clic will help you with navigation:
- `list`: presents you with a list of all functions, variables and mappings
defined in the calculator
- `help <NAME>`: shows help to any item on the list above (excluding mappings)
- `exit`, `Ctrl+C`, `Ctrl+D`: quits the calculator
- `help`: shows a basic help message

### Entering Greek letters and weird symbols

All the available special characters are listed under the mappings section of
the `list` command output. There are two ways to get such a symbol in your
prompt:

1. Type the whole name associated with the symbol (e.g. `alpha`) and press Tab
on your keyboard
2. Type backslash (`\`) followed by the beginning of the name (`\al`) and press
Tab on your keyboard

Both result in a symbol (`α`) replacing what you typed. The second method can
be specifically useful when trying to insert a symbol directly after some text,
as the first method will probably not work.

### Basic calculations

A major feature of clic is having 2 distinct ways to write division: with
a colon (`:`) and a fraction bar (`/`). These are not interchangable!
The colon works like simple inline division, while the fraction bar separates
the whole equation to form a large fraction. For example,
- `1 + 5 : 5` ($1+5:5$) returns `2`
- `1 + 5 / 5` ($\frac{1+5}{5}$) returns `1.2`
- `1 + (5/5)` ($1+\frac{5}{5}$) returns `2`

All other syntax is obvious from the examples below.
- `-3 + 12^3 + 11.56 * 6.11 - 120_000 : 2`
- `60 (km/h) : (m/s)` (converts between units)
- `5 ft + 11 km`
- `cos 2π + sin^2 120°`
- `√ 1024' + √ 3'`
- `log(2; 8)`
- `5!`
- `||-1| - |8||` (absolute value)
- `M("Al2(SO4)3")` (molar mass of compound)
- `pf 9997` (prime factorization, returns `"13 * 69"`)
- `variable = 5 + 4;` (assignes but outputs nothing)
- `variable + 1`
- `x = 9; y = 4; x^3 - 10 x y`
- `[1; 2; 6]^2` (bulk operation: returns `[1; 4; 36]`)
- `Sum [1; 4; 36]` (statistics operation: returns `41`)
- `ans` (returns the last answer, `41`)

Note that the arguments in the logarithm and bulk operations are separated by
a semicolon (`;`). This allows to use both the period (`.`) and comma (`,`) as
decimal separators. However, it can easily be changed in the configuration.

## Configuration

The configuration is stored in `.clic/config.toml` in your home folder. Here
are the default values:

```toml
global.show_debug = false

# Use one of the following number notations:
number.notation = "classic" # (engineering + scientific)
# number.notation = "engineering"
# number.notation = "scientific"
# number.notation = "normal" # (no exponent)
number.decimal_separators = ".,"
number.thousands_separators = "_"

modules.load_all = true
modules.load = []
modules.exclude = []

expression.argument_separator = ";"
expression.expression_separator = ";"
expression.reverse_expression_order = false
expression.answer_name = "ans"

view.oneline = true
view.loop = true
# Colors in ANSI color codes
view.prompt_color = "1;32"
```

### Modules

The modules section defines which parts of the calculator are loaded, and which
are left out (use it if you want to hide some functionality). The `help <NAME>`
command lets you see in which module any specific function is defined.

- Hide any module by adding it to `modules.exclude`
- Use only basic functionality by setting `modules.load_all` to `false`
- Load only a specific module(s) by both setting `modules.load_all = false`
and adding the desired module(s) to `modules.load`

### Number and expression symbols

The usage of periods `.` and commas `,` in numbers varies by area, so clic
provides a way to configure them based on your personal preferences. Each of
the following entries in the config signifies a certain role, to which you can
assign any symbol (or multiple symbols when allowed).

1. `number.decimal_separators`
    - allows one or more symbols
    - used to separate the whole part from the decimal part of a number
    - the default `.,` will make `10.0` and `10,0` both signify the number ten
    - the first character will be used in the calculator's output
2. `number.thousands_separators`
    - allows one or more symbols
    - used to visualize the thousands in large numbers
    - the default `_` will make `12_000` mean `12000`
3. `expression.argument_separator`
    - the symbol used to separate arguments of a function (`log(3; 5)`)
    and in bulk operations (`[1; 2; 5] - [1; 3; -3]`)
4. `expression.expression_separator`
    - the symbol used to separate multiple expressions written on a single
    line, usually with assignments (`x = 5; 3x`)

By default, the argument and expression separators are both set to be a
semicolon (`;`); however, each one of them can be set individually

### View

1. `view.oneline`: write the answer to the same line as the expression
2. `view.loop`: stay in interactive mode until the user explicitly quits
    (when turned off, clic quits after the first calculation is made)
3. `view.prompt_color`: the ANSI color code used for the prompt
    (green by default)

## Writing extensions

CLIC allows you to write custom functions, variables, mappings, etc. using
Python. For a quick result, see the Overview section below; if you want deep
customization, also check the Token specialization & Mapping specialization
sections.

### Overview

1. Create a Python file in `~/.clic/modules`, name it something like
    `mymodule.py` (use any name you like)
2. The calculator will search for two variables in your file;
    namely `CLIC_TOKENS` (required) and `CLIC_MAPPINGS` (optional):
    - `CLIC_TOKENS` lists all functions and variables provided by the module
    - `CLIC_MAPPINGS` lists all mappings provided by the module

Paste this example into your file:

```python
# ~/.clic/modules/mymodule.py
from decimal import Decimal


def double(x):
    """Double the given number."""

    # Always use the `Decimal` type
    return x * Decimal('2')


def sum_of_squares(args):
    """Return the sum of squares of all arguments."""

    # Check if we are provided with a list of arguments...
    if type(args).__name__ == 'ArgList':
        answer = Decimal('0')
        for arg in args:
            answer += arg ** Decimal('2')
        return answer

    return args ** Decimal('2')


def gravitational_constant(META):
    """Return the gravitational constant as a Quantity."""

    # G = 6.67430 m^3 / kg * s^2

    # META.Quantity is used to create a Quantity object
    return META.Quantity(Decimal('6.67430'), {'m': 3, 'kg': -1, 's': -2})


CLIC_TOKENS = [
    [['double'], double,        'normal func', 'Duplication'],
    [['Sqsum'], sum_of_squares, 'normal func', 'Sum of squares'],
    [['G'], gravitational_constant, 'static var', 'Gravitational constant',
     {'use_meta': True}],
]

CLIC_MAPPINGS = {
    'aleph': 'ℵ',
}
```

After you save the file, run the calculator and try out its new abilities:

```
clic: double(4.5) = 9
clic: Sqsum(1; 3; 4) = 26
clic: G = 6.6743 m^3*kg^-1*s^-2
```

`aleph<Tab>` will render the aleph character.

### Token specification

Tokens specified in `CLIC_TOKENS` can serve as functions, unary operators,
variables, normal operators, signs, opening braces, closing braces, and double
functions. Here is a thorough breakdown of how each of listing should look:

1. Name(s)
    - a list of names to be used in the calculator
    - names must be unique
    - for non-ascii names, consider providing an ascii-only alternative name
    - if the same name is used both as an unary opearator and a normal
    operator, the name for the unary token must begin with a space (` `)
    (e.g. ` -` is unary minus, `-` is normal minus)
    - if the token is a replacement for two other tokens going one after
    another, its name must have a space in between their respective names
    (e.g. `sin ^` is a token that replaces `sin` and `^` when used together)

2. Callable
    - a function or lambda statement that will be called when the token is
    executed by clic
    - callables must always return `Decimal` type and never `int` and `float`
    - the callable must accept this number of arguments (besides `META`):
        - function / unary operator: 1
        - variable: 0
        - operator: 2
        - sign: 1
        - opening brace: 1
        - closing brace: 0
        - double function: 2
    - if the token is a function, and it was called with multiple arguments
    inside clic, then the callable will receive a single iterable argument of
    type `ArgList` (e.g. `log(2; 8)` calls `log_callable(ArgList(2, 8))`)
    - when comparing against a type, do `type(obj).__name__ == '<TypeName>'`
    - when operating on `Quantity` and `Array` types, use the same operations
    as with numbers (e.g. addition, subtraction, multiplication & division)
    - to use static methods or initializers of the classes built into the
    calculator, list `META` as the last argument of the function;
        - `META.Quantity.sin`, `META.Quantity.cos`, `META.Quantity.tan`
        - `META.Quantity.arcsin`,`META.Quantity.arccos`,`META.Quantity.arctan`
        - `META.Array(*args)` creates a new array with the given elements
        - `META.Quantity(value, units)` creates a quantity
            - `value` is a Decimal value
            - `units` is a dictionary matching units (`str`) to their powers
            (`int`)

3. Preference & Kind
    - preference and kind are specified as a single string with two words
    and a space in between
    - preference ranges from `light`, `addition`, `mul-tion`, `normal` to
    `strong`, `strongest` and `static`; every next value will takes precedence
    over the ones before
    - the kind is one of the following:
        - `func`: function or unary operator
        - `var`: variable
        - `oper`: normal operator
        - `sign`: sign (placed after the operand, like `3!`)
        - `open`: opening brace
        - `clos`: closing brace
        - `doub`: double function (takes two arguments without a semicolon)
    - the most reasonable combinations are `normal func` for a function and
    `static var` for a variable

4. Help text
    - the help text will be displayed when `help` is called on the token
    - avoid specifying the kind inside the help text to avoid duplication

5. Options (optional)
    - a dictionary for token-specific configuration
    - consists of the following entries:
        - `closes` (str) used to provide the related opening or closing token
        name (required for all opening and closing braces)
        - `reverse` (bool) calculate multiple tokens of this type in a line
        in an opposite to logical direction (like `3^3^2`)
        - `array_input` (bool) extrapolate the token on arrays
        (use only if arrays are not covered in the callable)
        - `unknown_name_input` (bool) allow input of unquoted strings that
        would otherwise raise an unknown name error
        - `use_meta` (bool) use META inside the callable

### Mappings specification

`CLIC_MAPPINGS` is a dictionary that maps the keystrokes to the resulting
character(s). Providing custom mappings is useful if some of your token names
include special symbols that are not already covered in the calculator.

## Not implemented yet

These features are not implemented, but may follow in the future:

- [ ] matrices
- [ ] hyperbolic trigonometry
- [ ] currency operations
