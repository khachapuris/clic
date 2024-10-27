# Welcome to clic manual!

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

1. Use commands to quit the calculator or delete variables
2. To quit type `/q`
3. To delete variable `a` type `/d a`
4. To reset all variables type `/d`

### Multiple expressions

1. To type multiple expressions on one line, use a semicolon (`a = 5; a + 2`)
2. To hide the last output, add a semicolon at the end
(`a = 5; b = 15;`, `c = 1024;`)
3. You can create comments by hiding the output of strings
(`"This is a comment";`)

## Command line interface

1. Run the CLI with `python calculator.py`
2. Type in the expression / command and press Enter
3. To exit type `/q` and press Enter

## Terminal user interface

1. Run the TUI with `python frontend.py`
2. Type in the expression
    + `/` — create fraction
    + `'` — insert square root
3. Press `Enter` to see the answer
4. Press `Enter` again to start a new expression
5. Press `\` on any step to exit

## Adding your Python functions

### Step 1: Write the function

Go to `mathfunctions.py` and write your function in Python.
It should meet the following criteria:

- If the function accepts a number as an argument, it should support decimal
values (see the decimal docs at https://docs.python.org/3/library/decimal.html)
- If the function returns a number, it should be a decimal
- If it will be an operator, the function should accept two arguments
- If it will be a function, the function should accept one argument
- NOTE: if `func(arg1, arg2, arg3)` is inputed in the calculator,
the function `func` will recieve one vector argument: `(arg1, arg2, arg3)`;
to use it in the function, iterate over it

### Step 2: Register the function

Go to `functions.py` and add a token to the list.
Use one of the following examples.

```python
# Simple function
Token('name', function, 1, 3, 1, 'func'),
# Operator with preference x
Token('name', function, 2, x, 0, 'oper'),
# Sign with preference x
Token('name', function, 1, x, 0, 'sign'),
```

### Step 3: Use the function / operator / sign

Run the calculator in any interface and use your new
function / operator / sign.

## Various examples
