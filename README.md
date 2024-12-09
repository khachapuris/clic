# clic

CLIC
is a customisable command line scientific calculator written in Python.

## Description

### Two interfaces

CLIC provides two different interfaces.
Though the expression syntax remains the same,
each interface has its own features.

- Command line interface
    + Use this for a set of related calculations
    + Inline expression editing
    + Variable assignment and vectors become very useful
    + Calculate multiple expressions in one line
- Terminal user interface
    + Use this when substituting values in a formula, for example
    + Fullscreen editing of one expression
    + **Horizontal fraction bars**
    + Special characters for pi, square root, etc.
    + Autoscrolling of expressions that are bigger than the terminal window

### Math used in clic

- Infix notation & fixed point calculations
- Clean expression syntax:
    + Implicit multiplication — ~`a*b`~, `a b`
    + Function notation — ~`sin(x)^2`~, `sin^2 x`
    + Inline division vs fractions — ~`(1+2)/(2+3)`~, `1+2 / 2+3`
- Vectors
- Units (all SI units added by default)
- Variable assignment
- Exponentiation, modulo division, square root implemented initially
- Trigonometric and reverse trigonometric functions

### Editing the default setup

- Edit default functions & operators
- Use your own Python functions in the calculator
- Change stuff like decimal separators throughout the whole application

## Installation

1. Make sure you have Python installed
2. Install the python curses library (only for TUI, CLI works without it)
3. Use `git clone` to copy the git repository to your computer.
4. `cd` into the `clic` directory
5. Run the calculator's CLI by executing `python src/cli.py`
6. Run the calculator's TUI by executing `python src/tui.py`

## Usage

Please see the user manual (MANUAL.md).

### How to exit

To exit the calculator's CLI, type `exit` and press Enter.

To exit the calculator's TUI, press the backslash `\`
