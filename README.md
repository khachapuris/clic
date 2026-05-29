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
    - `mkdir clic-calculator`
    - `cd clic-calculator`
    - `python3 -m venv .venv` (creates a virtual environment)
    - `source .venv/bin/activate` (activates the virtual environment)
    - `python3 -m pip install --upgrade pip`
    - `python3 -m pip install -e <the-path-from-step-2>/clic` (installs clic)
4. To run the calculator, do `python3 -m clic`

To run the calculator in a single command, create a bash script somewhere in
your $PATH with the following contents:

```bash
# File called `clic` in your $PATH

# Activate the virtual environment
cd <the-actual-path>/clic-calculator
source .venv/bin/activate
python3 -m clic $@  # Run the calculator with all arguments provided

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

One important thing is that clic has 2 different division operators: a colon
(`:`) and a fraction bar (`/`). The order of operations with them is very
different! As opposed to the colon, the fraction bar is calculated last
(imagine that the whole thing is a large fraction). For example,
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
- `M("Al2(SO4)3")` (molar mass of compound)
- `pf 9997` (prime factorization, returns `"13 * 69"`)
- `variable = 5 + 4;` (assignes and outputs nothing)
- `variable + 1`
- `x = 9; y = 4; x^3 - 10 x y`
- `[1; 2; 6]^2` (bulk operation: returns `[1; 4; 36]`)
- `SUM [1; 4; 36]` (statistics operation: returns `41`)
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

expression.vector_separator = ";"
expression.expression_separator = ";"
expression.reverse_expression_order = false
expression.answer_name = "ans"

view.oneline = true
view.replace_console_prompt = false
view.quit_after_first_input = false
# Colors in bash color codes
view.prompt_color = "1;32"
```

### Modules

The modules section defines which parts of the calculator are loaded, and which
are left out (use it if you want to hide some functionality). The `help <NAME>`
command lets you see in which module is a specific function defined.

- Hide any module by adding it to `modules.exclude`
- Use only basic functionality by setting `modules.load_all` to `false`
- Load only a specific module(s) by both setting `modules.load_all = false`
and adding the desired module(s) to `modules.load`

### Number and expression symbols

The usage of periods `.` and commas `,` in numbers varies by area, so I thought
it would be make sense if one could choose what to use for themselves. Each of
the following entries in the config signifies a certain role, to which you can
assign any symbol (or multiple symbols when allowed).

1. `number.decimal_separators`
    - allows one or more symbols
    - used to separate the whole part from the decimal part of a number
    - the default `.,` will make `10.0` and `10,0` both signify the number ten
2. `number.thousands_separators`
    - allows one or more symbols
    - used to visualize the thousands in large numbers
    - the default `_` will make `12_000` mean `12000`
3. `expression.vector_separator`
    - the symbol used to separate arguments of a function (`log(3; 5)`)
    and in bulk operations (`[1; 2; 5] - [1; 3; -3]`)
4. `expression.expression_separator`
    - the symbol used to separate multiple expressions written on a single
    line, usually with assignments (`x = 5; 3x`)

By default, the vector and expression separators are both set to be a semicolon
(`;`); however, each one of them can be set individually

### View

You can experiment with `view` entries to find what fits you best. In short,
they will hide certain parts of the prompt to make the experience more compact.

## Writing extensions

You can examine the default modules (`src/modules` folder) and try to build a
simple module on your own. Then, put it into the same folder and try it out.

(TODO: add more info to this section)

### Not implemented yet

These features are not yet implemented:

- [ ] matrices
- [ ] hyperbolic trigonometry
- [ ] currency operations
