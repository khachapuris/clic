# clic

CLIC
is an extensible command line scientific calculator written in Python.

## Description

### Math used in clic

- Infix notation & fixed point calculations
- Clean expression syntax:
    + Implicit multiplication — ~`a*b`~, `a b`
    + Function notation — ~`sin(x)^2`~, `sin^2 x`
    + Fractions — ~`(1+2)/(2+3)`~, `1+2 / 2+3`
    + Inline division — ~`1+(2/2)+3`~, `1 + 2:2 + 3`
- Vectors
- Units (all SI units added by default)
- Variable assignment
- Exponentiation, modulo division, square root implemented initially
- Trigonometric and reverse trigonometric functions

### Extensibility

- Write extensions with your own functions and operators

## Installation

1. Make sure you have Python installed
2. Install the python curses library (only for TUI, CLI works without it)
3. Use `git clone` to copy the git repository to your computer.
4. `cd` into the `clic` directory
5. Run the calculator's CLI (interactive) by executing `python src/cli.py`
6. Run the calculator's CLI (non-interactive) by executing
`python src/cli.py 'your expression here'`
6. Run the calculator's TUI by executing `python src/tui.py`

## Usage

Please see the user manual (MANUAL.md).

### How to exit

To exit the calculator's CLI, type `exit` and press Enter.

To exit the calculator's TUI, press the backslash `\`
