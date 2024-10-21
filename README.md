# clic

CLIC
is a customizable command line scientific calculator written in Python.

## Description

### One calculator — two interfaces

CLIC provides two different interfaces.
Though the expression rules remains the same,
each interface has its own features.

- Command line interface
    + Use this for a set of related calculations
    + Inline expression editing
    + Variable assignment and vectors become very useful
    + Calculating multiple expressions at once steps in
- Terminal user interface
    + Use this when substituting variables in a formula, for example
    + Fullscreen editing of one expression
    + **Horizontal fraction bars** are an essential feature of clic TUI
    + Autoscrolling of expressions that are bigger than the terminal window

### Math used in clic

- Infix notation & fixed point calculations
- Math notation makes the expressions look clean:
    + Implicit multiplication — ~`a*b`~, `a b`
    + Function notation — ~`sin(x)^2`~, `sin^2 x`
    + Inline division vs fractions — ~`(1+2)/(2+3)`~, `1+2 / 2+3`
- Advanced math objects — vectors, units, angles
- Variable assignment
- Exponentiation, modulo division, square roots implemented initially
- Trigonometric and reverse trigonometric functions

### Editing the default setup

- Edit default functions & operators
- Use your own Python functions in the calculator
- Add your own and edit default units
- Change stuff like decimal separators throughout the whole application

## Installation

1. Make sure you have Python installed
2. Install the python curses library (only for TUI, CLI works without it)
3. Use `git clone` to copy the git repository to your computer.
4. `cd` into the `clic` directory
5. Run the calculator's CLI by executing `python calculator.py`
6. Run the calculator's TUI by executing `python frontend.py`

## Usage

Here you can see some basic usage examples. For more information
please see the documentation (the documentation is not written yet).

### Expression rules

- Operators & parenthesis: `85.64 * (2^3 + 11^-1) : 0.01`
- Units: `10 m * 11 s`
- Vectors: `(1, 2) + (-3, 4)`
- Variable assignment: `variable_name1 = 11 + 12`
- Compound variable assignment: `variable_name1 += 1`
- A semicolon at the end hides the output: `c = 1024;`
- Trigonometric functions: `sin 30deg`, `sin(0.2 + 0.3)`
- Trigonometric function exponentiation: `cos^2 x`

### Command line interface

When you run the CLI, a prompt will appear on the screen.

Type in the expression and press Enter.

When you finish calculating, type `/q` and press Enter.

### Terminal user interface

When you run the TUI, the calculator will take the whole terminal window.

Type in the expression. You can use the following shortcuts:

- Press `/` to create a fraction
- Press `'` to insert a square root
- Press `Enter` to see the answer

When you are finished, press `\` to exit
