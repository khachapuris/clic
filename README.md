# clic

CLIC
is a clean syntax, compact, customizable command line calculator
written in Python.


[![asciicast](https://asciinema.org/a/z3rbdHj3TR9ZqrsRCFLaJbnVC.png)](https://asciinema.org/a/z3rbdHj3TR9ZqrsRCFLaJbnVC)

## Installation

1. Make sure you have Python installed
2. `cd` to a place where you decide to keep the source code
3. Use `git clone` to copy the git repository to your computer.
4. Create a symbolic link to `src/cli.py` in your execution path.
Here's an example for Linux:
```bash
ln -s ./clic/src/cli.py ~/.local/bin/clic
```
5. Run the calculator with `clic '<expression>'`
or `clic` (for interactive mode)

## Usage

When in interactive mode, you can enter an expression or a command.
If you use non-interactive mode, just put the same expression or command
in single quotes as an argument and press Enter.

### Expressions

The following are examples of valid expressions:

| algebraic notation  | expression in clic   | answer            |
| ------------------- | -------------------- | ----------------- |
| let $a=3$, $b=4$    | `a = 3; b = 4;`      |                   |
| $3a + 5$            | `3a + 5`             | `14`              |
| $2\cdot3 - 6:0.3$   | `2 * 3 - 6 : 0.3`    | `-14`             |
| $\frac {5+16} {7}$  | `5+16 / 7`           | `3`               |
| $a^b - \sqrt{b+5}$  | `a^b - √b+5'`        | `78`              |
| $sin^2{60\degree}$  | `sin^2 60°`          | `750 * 10^-3`     |
| $7! - 5!$           | `7! - 5!`            | `4.92 * 10^3`     |
| Vector operations   | `(1, 2) + (-5, 6.4)` | `(-4, 8.4)`       |
| SI units            | `m^3 + 3l`           | `1.003 m^3`       |
| Prime factorization | `pf 103456`          | `"2^5 * 53 * 61"` |
| Mass of compound    | `M "H2SO4"`          | `98`              |

All the functions and variables and their definitions can be found with the
`list` and `help` commands explained in the section below.

In case you are wondering how did `√` and `°` get here, check out
the ["Inserting special characters"](#inserting-special-characters) section.

### Commands

These commands will help you navigate the calculator:

| command                     | description                                 |
|-----------------------------|---------------------------------------------|
| `exit` (`Ctrl-C`, `Ctrl-D`) | exit the interactive mode                   |
| `help`                      | view basic help                             |
| `list`                      | list all functions, variables and mappings  |
| `help <NAME>`               | show help on a specific function / variable |

### Inserting special symbols

To enhance the experience, clic provides a way to enter non-ASCII characters
via completion. Use this in one of the two possible ways:

1. Type a backslash, followed by the name of the mapping & hit Tab (`\sqrt<Tab>`).
This way is less ambiguous and allows unfinished mappings (`\sq<Tab>`)

2. The same without typing a backslash. This requires you type it to the end
(`deg<Tab>`)

Your mapping text will be replaced with the corresponding symbol.
To see all available mappings, use the `list` command described above.

## Configuration

The configuration is stored in `.clic/config.toml` in your home
directory. This is the default config:
```toml
global.show_debug = false

# Use one of the following number notations:
number.notation = "classic" # (engineering + scientific)
# number.notation = "engineering"
# number.notation = "scientific"
# number.notation = "normal" # (no exponent)
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

Note, that `replace_console_prompt` will erase the last line of your console
(the one that you called clic from) and replace it with the clic prompt.
If you don't want this behavior, set it to `false`.
