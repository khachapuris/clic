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
        self.ctor = Calculator()

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

    def print_expression(self, y, exp):
        """Print the expression exp on line y."""
        ymax, xmax = self.scr.getmaxyx()
        top, middle, bottom = '', '', ''
        mode = 'middle'
        numer, denom = '', ''
        for char in exp:
            if char == '{':
                mode = 'top'
            elif char == '/':
                mode = 'bottom'
            elif char == '}':
                mode = 'middle'
                w = max(len(numer), len(denom))
                top += numer.center(w + 2)
                middle += ' ' + '-' * w + ' '
                bottom += denom.center(w + 2)
                numer, denom = '', ''
            elif mode == 'top':
                numer += char
            elif mode == 'middle':
                top += ' '
                middle += char
                bottom += ' '
            elif mode == 'bottom':
                denom += char
        self.scr.addstr(y - 1, 1, top)
        self.scr.addstr(y, 1, middle)
        self.scr.addstr(y + 1, 1, bottom)

    def main(self):
        self.println(0, 'some left-aligned text', 'NAME', 'smth else')
        self.println(-3, 'just text', 'help?', 'more text...')
        self.print_expression(5, '2 +{3 + 12/4}-{2/3 * 3:1}')
        self.scr.getkey()


if __name__ == '__main__':
    curses.wrapper(lambda stdscr: Display(stdscr).main())
