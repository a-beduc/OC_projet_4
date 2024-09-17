import curses


menu = [' Tournaments ', ' Players     ', ' Exit        ']
ascii_art = [
    "                                                                            ",
    "                                                                        ()    ",
    "                                                                        /\\    ",
    "  (\\=,                                                                 //\\\\   ",
    "//  .\\                                                               (    )  ",
    "(( \\_  \\      ___  _  _  ____  ____  ____     __   ____  ____          )__(   ",
    "))  `\\_)    / __)/ )( \\(  __)/ ___)/ ___)   / _\\ (  _ \\(  _ \\        /____\\  ",
    "(/     \\    ( (__ ) __ ( ) _) \\___ \\\\___ \\  /    \\ ) __/ ) __/         |  |    ",
    "| _.-'|     \\___)\\_)(_/(____)(____/(____/  \\_/\\_/(__)  (__)           |  |   ",
    ")___(   ____  __   _  _  ____  __ _   __   _  _  ____  __ _  ____   /____\\",
    "(=====) (_  _)/  \\ / )( \\(  _ \\(  ( \\ / _\\ ( \\/ )(  __)(  ( \\(_  _) (======)",
    "}====={   )( (  O )) \\/ ( )   //    //    \\/ \\/ \\ ) _) /    /  )(   }======{",
    "(_______) (__) \\__/ \\____/(__\\_)\\_)__)\\_/\\_/\\_)(_/(____)\\_)__) (__) (________)"
]


def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    for idx, line in enumerate(ascii_art):
        x = w//2 - len(line)//2
        stdscr.addstr(idx, x, line)

    menu_start_y = len(ascii_art) + 2

    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = menu_start_y + idx
        if idx == selected_row_idx:
            stdscr.addstr(y, x, row, curses.A_REVERSE)
        else:
            stdscr.addstr(y, x, row)

    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    current_row_idx = 0

    print_menu(stdscr, current_row_idx)

    while 1:
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP:
            if current_row_idx > 0:
                current_row_idx -= 1
            else:
                current_row_idx = len(menu) - 1
        elif key == curses.KEY_DOWN:
            if current_row_idx < len(menu) - 1:
                current_row_idx += 1
            else:
                current_row_idx = 0
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.clear()
            stdscr.addstr(0, 0, "You pressed{}!".format(menu[current_row_idx]))
            stdscr.refresh()
            stdscr.getch()
            if current_row_idx == len(menu) - 1:
                break
        elif key == 27:
            break

        print_menu(stdscr, current_row_idx)

        stdscr.refresh()


if __name__ == '__main__':
    curses.wrapper(main)







