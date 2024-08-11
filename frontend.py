from calculator import Calculator
import curses


class Display:
    """The class used for displaing calculator info on the screen."""

    def __init__(self, stdscr):
        """The initialiser for the class.

        Arguments:
        stdscr -- the terminal screen.
        """
        self.scr = stdscr
        self.ctor = Calculator()

    def main(self):
        self.scr.getkey()


if __name__ == '__main__':
    curses.wrapper(lambda stdscr: Display(stdscr).main())
