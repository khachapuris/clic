from calculator import Calculator
import symbols as smbs

import curses
import curses.ascii as cascii
import sys


class Display:
    """The Display class is used for displaing the calculator."""

    def __init__(self, stdscr):
        """The initialiser for the class.

        Arguments:
        stdscr -- the terminal screen.
        """
        self.scr = stdscr
        self.pad = curses.newpad(3, 500)
        helptext = "Welcome to clic! Press '\\' to exit, please see README.md"
        self.ctor = Calculator({'help': helptext})
        self.exp = ''
        self.cursor = 0
        self.showans = False
        self.update_mask_bars(self.exp)

    def format_exp(self):
        """Return the expression with clic fraction syntax."""
        smb_str = '(/)'
        smb_num = 0
        ans = ''
        for char in self.exp:
            if char == '\\':
                ans += smb_str[smb_num]
                smb_num = (smb_num + 1) % 3
                continue
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
        s, r = Display.divide(xmax - len(center) - 2, 2)
        left_gap = ' ' * (s - len(left))
        right_gap = ' ' * (s - len(right) + r)
        string = ' ' + left + left_gap + center + right_gap + right + ' '
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
        if self.showans:
            y, x, printable = self.mask[-1]
            self.pad.addstr(y, x, ' = ' + self.ctor.get_answer()[1])
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

    def process_input(self, key):
        c = self.cursor

        def printable(i):
            if i >= len(self.exp):
                return 9
            return self.mask[i][2]

        if key == 'KEY_BACKSPACE':
            if self.showans:
                self.showans = False
            elif self.cursor:
                if printable(c-1) + printable(c) + printable(c+1) == 0:
                    self.exp = self.exp[:c-1] + self.exp[c+2:]
                elif printable(c-1):
                    self.exp = self.exp[:c-1] + self.exp[c:]
                self.cursor -= 1
        elif key == 'KEY_LEFT':
            if self.cursor:
                self.cursor -= 1
        elif key == 'KEY_RIGHT':
            if self.cursor < len(self.exp):
                self.cursor += 1
        elif key == '/':
            self.exp = self.exp[:c] + '\\\\\\' + self.exp[c:]
            self.cursor += 1
        elif key == '\n':
            if not printable(c):
                self.cursor += 1
            elif not printable(c + 1):
                self.cursor += 2
            elif self.showans:
                self.exp = ''
                self.cursor = 0
                self.showans = False
            else:
                self.showans = True
                self.ctor.calculate(self.format_exp())
        elif key == '\\':
            sys.exit()
        elif len(key) == 1:
            self.exp = self.exp[:c] + key + self.exp[c:]
            self.cursor += 1

    def main(self):
        while True:
            self.update_mask_bars(self.exp)
            self.println(0, center='clic')
            self.println(-2, left=self.ctor.vars['help'])
            self.update_pad(self.exp)
            self.print_exp(5, 2, 2)
            inp = self.scr.getkey()
            self.process_input(inp)


if __name__ == '__main__':
    curses.wrapper(lambda stdscr: Display(stdscr).main())
