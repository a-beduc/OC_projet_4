import curses
from controllers.controller_menu import ControllerMenu


def main(stdscr):
    menu = ControllerMenu(stdscr)
    menu.start()


if __name__ == '__main__':
    curses.wrapper(main)
