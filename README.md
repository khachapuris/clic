# clic

CLIC
is a clean, compact, customizable command line calculator
written in Python.


[![asciicast](https://asciinema.org/a/z3rbdHj3TR9ZqrsRCFLaJbnVC.png)](https://asciinema.org/a/z3rbdHj3TR9ZqrsRCFLaJbnVC)

## Installation

This instruction is for Linux; the same can be achieved in a
similar way on other platforms

1. Make sure you have Python installed
2. `cd` to a place where you decide to keep the source code
3. Use `git clone` to copy the git repository to your computer.
4. Create a symbolic link in your `$PATH` (remember to replace `your_place`!)
```bash
ln -s your_place/clic/cli.py ~/.local/bin/clic
```
5. Run the calculator with `clic`

## Usage

Basic arithmetics

| algebraic notation | expression in clic | answer        |
| ------------------ | ------------------ | ------------- |
| let $a=3$, $b=4$   | `a = 3; b = 4;`    |               |
| $3a + 5$           | `3a + 5`           | `14`          |
| $2\cdot3 - 6:0.3$  | `2*3 - 6:0.3`      | `-14`         |
| $\frac {5+16} {7}$ | `5+16 / 7`         | `3`           |
| $a^b - \sqrt{b+5}$ | `a^b - √(b+5)`     | `78`          |
| $sin^2{60\degree}$ | `sin^2 60°`        | `750 * 10^-3` |
| $7! - 5!$          | `7! - 5!`          | `4.92 * 10^3` |

Advanced math and exotic functions

| description         | expression in clic   | answer            |
| ------------------- | -------------------- | ----------------- |
| vectors             | `(1, 2) + (-5, 6.4)` | `(-4, 8.4)`       |
| SI units            | `m^3 + 3l`           | `1.003 m^3`       |
| prime factorization | `pf 103456`          | `"2^5 * 53 * 61"` |
| mass of compound    | `M "H2SO4"`          | `98`              |

Commands

| command       | description                                 |
| ------------- | ------------------------------------------- |
| `exit`        | exit the calculator                         |
| `help`        | view basic help                             |
| `list`        | list all variables, functions and operators |
| `help <NAME>` | show help on a specific function            |

Inserting special symbols (`<Tab>` is the `Tab` key)

| keypresses   | result |
| ------------ | ------ |
| `deg<Tab>`   | `°`    |
| `sqrt<Tab>`  | `√`    |
| `beta<Tab>`  | `β`    |

## Configuration

The configuration is stored in `.clic/config.toml` in your home
directory. This is the default config:
```toml
global.show_debug = false

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

expression.vector_separator = ","
expression.expression_separator = ";"
expression.answer_name = "ans"

view.oneline = true
view.replace_console_prompt = true
view.quit_after_first_input = true
# Colors in bash color codes
view.prompt_color = "1;32"
```

If you know Python you can write additional functions for the calculator.
For more details see MANUAL.md
