# Welcome to the clic manual!

## Expressions

### Numbers

1. Numbers store fixed-point decimal numbers.
2. The decimal separator is a period (`.`) by default (`435.68`).
3. Numbers support all basic operators

### Vectors

1. Vectors store a sequence of math objects.
2. To type in a vector, use two parenthesis and separate
the items with commas (`(1, 9, 13.5)`).
3. Vectors support:
    + Addition, subtraction
    + Multiplication by a scalar
    + Vector product

### Quantities

1. Quantities store a number multiplied by a unit
2. To type in a quantity type in a number followed by a unit
(`3 km`) or just a unit (`mA`).
3. Quantities support all basic operators
(NOTE: some operations on quantities are invalid, such as `3m + 4s`)
4. All SI units are implemented; to see the list, type `/l u`

### Angles

1. Angles are a subset of quantities
2. To type in an angle type in a number followed by an angle unit
(`3 deg`, `5 rad`).
3. Angles support all basic operators and trigonometric functions

### Strings

1. Strings store text
2. To type in a string, use double quotes (`"string"`)
3. Strings can be used as arguments to some functions or as comments

### Variables

1. Variables store math objects and can be accessed by their name
2. To define a variable, use the equals sign (`a = 100`)
3. To change a variable, you can use the compound assignment
(`a += 10`, `a *= 0.1`) or just reassign it
4. To get the value of a variable, use its name (`a`)
5. To delete variable `a`, type `/d a`
6. To see the list of all variables, type `/l`

### Functions

1. Functions use prefix notation
2. To type in a function
    + with one argument, write the function name
    followed by the argument (`sin x`)
    + with ambigous argument, write the function name
    followed by the argument in parenthesis (`sin(x + y)`)
    + with more than one argument, write the function name with the
    arguments in parenthesis, separated with commas (`function_name(10, 11)`)
3. Trigonometric function exponentiation: `sin^2 30deg`
4. NOTE: negation is considered a function (`-4`)
5. To see the list of all functions, operators and signs, type `/l f`

### Operators

1. Operators use infix notation
2. To use an operator, put it between the operands
(`5.6 + 7.4`)
3. NOTE: operators can be text (`20 mod 3`)

### Signs

1. Signs use postfix notation
2. To use a sign, put it after the operand (`5!`)

### Implicit multiplication

1. Implicit multiplication is a hidden operator
2. To use implicit multiplication, put a variable/opening parenthesis/function
after a number/variable/closing parenthesis (`10 x`, `2 sqrt 2`, `(5+1)(5-1)`).

### Commands

Commands tell the calculator to do special tasks

1. To exit type `exit`
2. To list all functions, units
and variables type `list`
5. To see the basic help type `help`
6. To see help on a function, operator or sign
with name `name` type `help name`

### Multiple expressions

1. To type multiple expressions on one line, use a semicolon (`a = 5; a + 2`)
2. To hide the last output, add a semicolon at the end
(`a = 5; b = 15;`, `c = 1024;`)
3. You can create comments by hiding the output of strings
(`"This is a comment";`)

### Settings

To alter a setting, use assignment: `_setting_name_ = <setting_value>`

Here is a list of all settings with their available values:

1. `_debug_`: show debug messages and error tracebacks
    + `0`(default) -> off
    + `1` -> on
2. `_notation_`: number representation mode
    + `"classic"`(default) -> use engineering notation between `10^-9` and `10^9`,
otherwise use scientific notation
    + `"engineering"` -> express numbers like `x * 10^(3y)`
    + `"scientific"` -> express numbers like `x * 10^y`
    + `"normal"` -> express numbers without any exponent

## Command line interface

1. Run the CLI with `python src/cli.py`
2. Type in the expression / command and press Enter
3. To exit type `exit` and press Enter

### Special character insertion

CLIC offers a Julia REPL like method of entering special characters.
To input a special character, type:

1. Small greek letter -> `\` + it's name in lowercase
2. Capital greek letter -> `\` + it's name capitalised
3. Final sigma -> `\sigmaf`
4. Degree sign -> `\deg`
5. Square root sign -> `\sqrt`

Press tab, and what you typed is replaced with the symbol.

### Example

Get the number of molecules of a hydrocarbon with
8 single bonds and 2 double bonds.

```
% "1st number in the vector is the amount of carbon";
% "2nd number in the vector is the amount of hydrogen";
%
% methane = (1, 4);
%
% single = (1,  2);
% double = (1,  0);
% triple = (1, -2);
%
% methane + 8 single + 2 double
= (11, 20)
%
% exit
```

Answer: 11 carbon atoms and 20 hydrogen atoms.

## Terminal user interface

1. Run the TUI with `python src/tui.py`
2. Type in the expression
    + `/` — create fraction
    + `'v` — insert square root
    + `'o` — insert degree symbol
    + `'p` — insert pi
    + `'w` — insert ohm symbol
    + `'m` — insert micro symbol
3. Press `Enter` to see the answer
4. Press `Enter` again to start a new expression
5. Press `\` on any step to exit

### Example

Substitute values in a formula

$\tau = \frac{ c m (t_2 - t_1) \cdot R}{\eta \cdot U^2}$

and get the answer in minutes.

```
 4.2*10^3 J * 0.5 kg * 80 K * 160 Ω
 ────────────────────────────────── : min = 11.57024793388429752066115702
       kg*K * 0.8 * (220 V)^2
```

Answer: 11.6 min.

## Writing an extension

For examples, see files from the `modules` directory.

### Step 1: Write functions

Go to `src/modules` and add a file `my_module.py`, where `my_module`
is the name of your module. There write your function(s) in Python.
Every function should meet the following requirements:

- If the function accepts a number as an argument, it should support decimal
values (see the decimal docs at https://docs.python.org/3/library/decimal.html)
- If the function returns a number, it should be a decimal
- If the function will be an operator, it should accept two arguments
- If the function will be a function, it should accept one argument
- NOTE: if `func(arg1, arg2, arg3)` is entered in the calculator,
the function `func` will recieve one vector argument: `(arg1, arg2, arg3)`;
to use it in the function, iterate over it

### Step 2: Register functions

Define a list called `exporttokens` in your module.
Each element of that list should be a `Token`:

```python
from token import Token

# Here are your function definitions...

exporttokens = [
    # If you want a simple function, insert this
    Token('example_name_a', example_function_a, 3, 1, 'func', 'Help text'),
    # If you want an operator with preference x, insert this
    Token('example_name_b', example_function_b, x, 0, 'oper', 'Help text'),
    # If you want a sign with preference x, insert this
    Token('example_name_c', example_function_c, x, 0, 'sign', 'Help text'),
    # Create and register as much functions as you want
]
```
Note that the help text is optional.
Don't forget to save the file!

### Step 3: Use functions / operators / signs

Run the calculator in any interface.
Use your functions, operators and/or signs by their name (marked in the
code snippet above as `example_name_...`).
