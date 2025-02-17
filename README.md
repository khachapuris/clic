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
2. Use `git clone` to copy the git repository to your computer.
3. `cd` into the `clic` directory
4. Run the calculator (interactive) by executing `python src/cli.py`
5. Run the calculator (non-interactive) by executing
`python src/cli.py 'your expression here'`

## Usage

Please see the user manual (MANUAL.md).

### How to exit

To exit the calculator's CLI, type `exit` and press Enter.
