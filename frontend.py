from calculator import Calculator
import curses


class Display:
    """The Display class is used for displaing the calculator."""

    def __init__(self, stdscr):
        """The initialiser for the class.

        Arguments:
        stdscr -- the terminal screen.
        """
        self.scr = stdscr
        self.pad = curses.newpad(3, 500)
        self.ctor = Calculator()
        self.exp = '1 +{3^2 + 4^2/5^2}*{2/3}'
        self.cursor = 4

    @staticmethod
    def divide(a, b):
        """Return the results of remainder division of a by b."""
        return a // b, a % b

    def println(self, y, left, center, right):
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

    def mask(self, exp):
        """Return the positions of characters in exp."""
        mask = []
        bars = []
        # "part" is a numerator / denomenator / text between fractions
        a = 0  # length of the current part
        b = 0  # length of the previous part
        x = 0  # x coordinate of the start of current part

        for char in exp:

            # Start a fraction:
            if char == '{':
                # add the coordinates of each character of current part
                mask += [(1, x + i) for i in range(a + 1)]
                # move on to the left
                x += a + 1
                # start a new part
                a, b = 0, a

            # Move from the numerator to the denomenator:
            elif char == '/':
                # start a new part
                a, b = 0, a

            # Finish current fraction:
            elif char == '}':
                w = max(a, b)  # the width of the whole fraction
                # add the coordinates of each character of the fraction
                mask += [(0, x + (w - b) // 2 + i) for i in range(b + 1)]
                mask += [(2, x + (w - a) // 2 + i) for i in range(a + 1)]
                bars += [(x, w)]
                # move on to the left
                x += w + 1
                # start a new part
                a, b = 0, a

            # Add a character to current part
            else:
                a += 1

        # Finish the last part
        mask += [(1, x + i) for i in range(a)]
        return mask, bars

    def update_pad(self, exp, mask, bars):
        """Update the expression pad.

        Arguments:
        exp -- the expression string,
        mask -- list of character positions in exp.
        """
        self.pad.clear()
        for i in range(len(exp)):
            y, x = mask[i]
            char = exp[i]
            if char not in '{/}':
                self.pad.addstr(y, x, char)
        for i in range(len(bars)):
            bar = bars[i]
            self.pad.addstr(1, bar[0], '─' * bar[1])

    def print_expression(self, y, left, right):
        """Print the expression on the screen.

        Arguments:
        y -- the y coordinate of the expression's top line,
          (if negative, counts from the bottom of the screen),
        left -- width of the margin to the left of the expression,
        right -- width of the margin to the right of the expression.
        """
        ymax, xmax = self.scr.getmaxyx()
        y %= ymax  # support negative values of y
        mask, bars = self.mask(self.exp)
        self.update_pad(self.exp, mask, bars)
        self.scr.refresh()
        y1, x1 = mask[self.cursor]
        screen_width = xmax - left - right
        if x1 > screen_width:
            padstart = x1 - screen_width + 1
            self.pad.refresh(0, padstart, y, left, y + 2, xmax - right - 1)
            self.scr.move(y + y1, xmax - right - 1)
        else:
            self.pad.refresh(0, 0, y, left, y + 2, xmax - right - 1)
            self.scr.move(y + y1, x1 + left)

    def main(self):
        self.println(0, 'some left-aligned text', 'NAME', 'smth else')
        self.println(-3, 'just text', 'help?', 'more text...')
        self.print_expression(5, 2, 2)
        self.scr.getkey()


if __name__ == '__main__':
    curses.wrapper(lambda stdscr: Display(stdscr).main())
