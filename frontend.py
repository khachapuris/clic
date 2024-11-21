#!/usr/bin/env python

"""This script contains a TUI for clic calculator.

The script runs the calculator on a full screen.
It can be used as a module and provides class Display.
The only required python library is curses.
"""

from calculator import Calculator
import symbols as smbs
import tuisymbols as smbs2

import curses
import sys


class Display:
    """The Display class is used for displaying the calculator."""

    def __init__(self, stdscr):
        """The initialiser for the class.

        Arguments:
        stdscr -- the terminal screen.
        """
        self.scr = stdscr
        self.pad = curses.newpad(3, 500)
        helptext = "Welcome to clic! Press '\\' to exit, please see README.md"
        title = 'clic'
        self.ctor = Calculator({'_help': helptext, '_title': title})
        self.insert = False
        self.reset_expression()
        self.update_mask_bars(self.exp)

    def reset_expression(self):
        """Initialize the expression."""
        self.exp = ''
        self.cursor = 0
        self.showans = False

    def format_exp(self):
        """Return the expression with clic fraction syntax."""
        smb_str = '(/)'
        smb_num = 0
        ans = ''
        for char in self.exp:
            if char == '\\':
                ans += smb_str[smb_num]
                smb_num = (smb_num + 1) % 3
            elif char in smbs2.sub:
                ans += f' {smbs2.sub[char]} '
            else:
                ans += char
        return ans

    @staticmethod
    def divide(a, b):
        """Return the results of remainder division of a by b."""
        return a // b, a % b

    def println(self, y, left='', center='', right=''):
        """Print a line on the screen.

        Arguments:
        y -- the y coordinate of the line
          (if negative, counts from the bottom of the screen),
        left, center, right -- text to be aligned respectively.
        """
        ymax, xmax = self.scr.getmaxyx()
        y %= ymax  # support negative values of y
        if center:
            s, r = Display.divide(xmax - len(center) - 2, 2)
            left_gap = ' ' * (s - len(left))
            right_gap = ' ' * (s - len(right) + r)
            string = ' ' + left + left_gap + center + right_gap + right + ' '
        else:
            gap = ' ' * (xmax - len(left) - len(right) - 2)
            string = ' ' + left + gap + right + ' '
        self.scr.addstr(y, 0, string, curses.A_REVERSE)

    def add_part(self, line, start, length):
        """Add character positions to the mask.

        Arguments:
        line -- the y coordinate of the part,
        start -- x coordinate of the part start,
        length -- the length of the part.
        """
        # Ordinary characters
        self.mask += [(line, start + i, 1) for i in range(length)]
        # Control character
        self.mask += [(line, start + length, 0)]

    def update_mask_bars(self, exp):
        """Update the mask and bars according to exp."""
        self.mask = []
        self.bars = []
        # "part" is an expression fragment placed on the same level
        parts = [-1, -1, -1]
        x = 0  # x coordinate of current part start
        curr_part = 1

        for char in exp:
            # Increment current part length
            parts[curr_part] += 1
            # Print out the fraction
            if char == '\\' and curr_part == 2:
                # Print middle part before fraction
                self.add_part(1, x, parts[1])
                x += parts[1] + 1
                # Print fraction
                w = max(parts[0], parts[2])  # the width of the whole fraction
                self.add_part(0, x + (w - parts[0]) // 2, parts[0])
                self.add_part(2, x + (w - parts[2]) // 2, parts[2])
                if w == 0:  # empty fractions
                    w = 1
                self.bars += [(x, w)]
                # Initialize parameters
                x += w + 1
                parts = [-1, -1, -1]
            # Skip to next part
            if char == '\\':
                curr_part = (curr_part - 1) % 3
        # Add the last part
        self.add_part(1, x, sum(parts) + 3)
        x += sum(parts) + 3

    def update_pad(self, exp):
        """Update the expression pad.

        Arguments:
        exp -- the expression string,
        mask -- list of character positions in exp.
        """
        self.pad.clear()
        for i in range(len(exp)):
            y, x, printable = self.mask[i]
            char = exp[i]
            if printable:
                self.pad.addstr(y, x, char)
            # self.pad.addstr(y, x, char)  # DEBUG
        for i in range(len(self.bars)):
            bar = self.bars[i]
            self.pad.addstr(1, bar[0], '─' * bar[1])

    def print_exp(self, y, left, right):
        """Print the expression on the screen.

        Arguments:
        y -- the y coordinate of the expression's top line,
          (if negative, counts from the bottom of the screen),
        left -- width of the margin to the left of the expression,
        right -- width of the margin to the right of the expression.
        """
        ymax, xmax = self.scr.getmaxyx()
        y %= ymax  # support negative values of y
        self.scr.refresh()
        y1, x1, printable = self.mask[self.cursor]
        if self.showans:
            y1, x1, printable = self.mask[-1]
        screen_width = xmax - left - right
        if x1 > screen_width:
            padstart = x1 - screen_width + 1
            self.pad.refresh(0, padstart, y, left, y + 2, xmax - right - 1)
            self.scr.move(y + y1, xmax - right - 1)
        else:
            self.pad.refresh(0, 0, y, left, y + 2, xmax - right - 1)
            self.scr.move(y + y1, x1 + left)
        if self.showans:
            curses.curs_set(0)
        else:
            curses.curs_set(2)

    def calculate(self):
        """Calculate the current expression and switch to show answer mode."""
        self.showans = True
        self.ctor.calculate(self.format_exp())
        if self.ctor.silent:
            self.reset_expression()

    def process_input(self, key):
        """Change the expression / state of the calculator according to key."""
        c = self.cursor
        notstart = self.cursor > 0
        notend = self.cursor < len(self.exp)

        def is_printable(i):
            """Check whether exp[i] is printable.

            Return:
            0 -- hidden,
            1 -- printable,
            9 -- does not exist.
            """
            if i >= len(self.exp):
                return 9
            return self.mask[i][2]

        def replace(x, w, text):
            """Replace a fragment of the expression with some text.

            Arguments:
            x -- start of fragment relative to cursor,
            w -- size of fragment,
            text -- the text to replace the fragment with.
            """
            self.exp = self.exp[:c+x] + text + self.exp[c+x+w:]
            if len(text) == 0:
                self.cursor += x
            else:
                self.cursor += 1

        if key == 'KEY_RESIZE':
            self.scr.clear()
        elif key == '\\':
            sys.exit()
        elif self.showans:
            if key == 'KEY_BACKSPACE':
                self.showans = False
            elif key == '\n':
                self.reset_expression()
        elif key == 'KEY_BACKSPACE' and notstart:
            # Delete empty fractions from numerator
            if is_printable(c-1) + is_printable(c) + is_printable(c+1) == 0:
                replace(-1, 3, '')
            # Delete printable characters
            elif is_printable(c-1):
                replace(-1, 1, '')
            # Omit non-printable characters
            else:
                self.cursor -= 1
        elif key == '\n':
            # Exit an empty expression with Enter
            if not self.exp:
                sys.exit()
            # Move to next part from the end of the current part
            if not is_printable(c):
                self.cursor += 1
            elif not is_printable(c + 1):
                self.cursor += 2
            # Calculate expression
            else:
                self.calculate()
        elif key == 'KEY_DC' and notend:
            replace(0, 1, '')
        elif key == 'KEY_LEFT' and notstart:
            self.cursor -= 1
        elif key == 'KEY_RIGHT' and notend:
            self.cursor += 1
        elif self.insert:
            if key in smbs2.ins:
                replace(0, 0, smbs2.ins[key])
            self.insert = False
        elif key == '/':
            if self.mask[c][0] == 1:
                if self.exp[c-1] == ' ':
                    replace(-1, 1, '')
                    replace(0, 0, '\\\\\\')
                else:
                    replace(0, 0, '\\\\\\')
            else:
                replace(0, 0, '/')
        elif key == "'":
            self.insert = True
        elif len(key) == 1 and key.isascii() and key.isprintable():
            replace(0, 0, key)

    def main(self):
        while True:
            exp = self.exp
            if self.showans:
                exp += ' = ' + self.ctor.get_answer()[1]
            self.update_mask_bars(exp)
            self.println(0, center=self.ctor.vars['_title'])
            self.println(-2, left=self.ctor.vars['_help'])
            self.update_pad(exp)
            self.print_exp(5, 2, 2)
            inp = self.scr.getkey()
            self.process_input(inp)


if __name__ == '__main__':
    curses.wrapper(lambda stdscr: Display(stdscr).main())
