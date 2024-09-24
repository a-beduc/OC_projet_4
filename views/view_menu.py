import curses


class ViewMenu:
    ASCII_ART = [
        "                                                                        ()    ",
        "                                                                        /\\    ",
        "  (\\=,                                                                 //\\\\   ",
        " //  .\\                                                               (    ) ",
        "(( \\_  \\      ___  _  _  ____  ____  ____     __   ____  ____          )__(  ",
        " ))  `\\_)    / __)/ )( \\(  __)/ ___)/ ___)   / _\\ (  _ \\(  _ \\        /____\\ ",
        " (/     \\    ( (__ ) __ ( ) _) \\___ \\\\___ \\  /    \\ ) __/ ) __/         |  |   ",
        " | _.-'|     \\___)\\_)(_/(____)(____/(____/  \\_/\\_/(__)  (__)           |  |  ",
        ")___(   ____  __   _  _  ____  __ _   __   _  _  ____  __ _  ____   /____\\",
        "(=====) (_  _)/  \\ / )( \\(  _ \\(  ( \\ / _\\ ( \\/ )(  __)(  ( \\(_  _) (======)",
        "}====={   )( (  O )) \\/ ( )   //    //    \\/ \\/ \\ ) _) /    /  )(   }======{",
        "(_______) (__) \\__/ \\____/(__\\_)\\_)__)\\_/\\_/\\_)(_/(____)\\_)__) (__) (________)"
    ]

    MIN_TERMINAL_HEIGHT = 24
    MIN_TERMINAL_WIDTH = 80

    MAIN_MENU = {
        ' Tournaments ': (0, 'TOURNAMENT_MENU'),
        ' Players ': (1, 'PLAYER_MENU'),
        ' Exit ': (2, 'EXIT')
    }

    TOURNAMENT_MENU = {
        ' New Tournament ': (0, 'NEW_TOURNAMENT'),
        ' List Tournaments ': (1, 'VIEW_TOURNAMENT'),
        ' Back ': (2, 'MAIN_MENU')
    }

    PLAYER_MENU = {
        ' New Player ': (0, 'NEW_PLAYER'),
        ' List Players ': (1, 'VIEW_PLAYER'),
        ' Back ': (2, 'MAIN_MENU')
    }

    def __init__(self, stdscr):
        curses.curs_set(0)
        self.stdscr = stdscr
        self.terminal_h, self.terminal_w = stdscr.getmaxyx()
        self.outer_wind = None
        self.base_wind = None
        self.ascii_wind = None
        self.menu_wind = None
        self.menus = {
            'MAIN_MENU': self.MAIN_MENU,
            'TOURNAMENT_MENU': self.TOURNAMENT_MENU,
            'PLAYER_MENU': self.PLAYER_MENU
        }
        self.current_menu = None

    def initialize(self):
        self.outer_wind = curses.newwin(self.terminal_h, self.terminal_w, 0, 0)
        self.outer_wind.clear()
        self.outer_wind.refresh()
        self.base_wind = self.create_base_wind()
        self.ascii_wind = self.create_ascii_wind()
        self.menu_wind = self.create_menu_wind()
        self.current_menu = self.MAIN_MENU

    def create_base_wind(self):
        self.stdscr.clear()
        base_wind = curses.newwin(self.MIN_TERMINAL_HEIGHT,
                                  self.MIN_TERMINAL_WIDTH,
                                  (self.terminal_h - self.MIN_TERMINAL_HEIGHT) // 2,
                                  (self.terminal_w - self.MIN_TERMINAL_WIDTH) // 2)
        base_wind.refresh()
        return base_wind

    def print_ascii_art(self, window):
        for idx, line in enumerate(self.ASCII_ART):
            x = (self.MIN_TERMINAL_WIDTH - len(line)) // 2
            window.addstr(idx + 1, x, line)
        window.refresh()

    def create_ascii_wind(self):
        h, w = (len(self.ASCII_ART) + 2, self.base_wind.getmaxyx()[1])
        ascii_wind = self.base_wind.derwin(h, w, 0, 0)
        self.print_ascii_art(ascii_wind)
        ascii_wind.refresh()
        return ascii_wind

    def create_menu_wind(self):
        h, w = (len(self.MAIN_MENU) + 2, self.base_wind.getmaxyx()[1])
        menu_wind = self.base_wind.derwin(h, w, self.ascii_wind.getmaxyx()[0] + 1, 0)
        menu_wind.keypad(True)
        menu_wind.refresh()
        return menu_wind

    def print_menu(self, menu_dict, selected_index):
        self.menu_wind.clear()
        menu_items = sorted(menu_dict.items(), key=lambda item: item[1][0])
        menu_start_y = 0
        menu_width = self.menu_wind.getmaxyx()[1]
        for line, (idx, _) in menu_items:
            x = (menu_width - len(line)) // 2
            y = menu_start_y + idx
            if idx == selected_index:
                self.menu_wind.addstr(y, x, line, curses.A_REVERSE)
            else:
                self.menu_wind.addstr(y, x, line)
        self.menu_wind.refresh()

    def start_menu(self):
        running = True
        current_line_index = 0
        while running:
            self.print_menu(self.current_menu, current_line_index)
            key = self.menu_wind.getch()
            if key == curses.KEY_UP:
                current_line_index = (current_line_index - 1) % len(self.current_menu)
            elif key == curses.KEY_DOWN:
                current_line_index = (current_line_index + 1) % len(self.current_menu)
            elif key == curses.KEY_ENTER or key in [10, 13]:
                menu_items = sorted(self.current_menu.items(), key=lambda item: item[1][0])
                selected_item = menu_items[current_line_index][1][1]
                if selected_item in self.menus.keys():
                    self.current_menu = self.menus[selected_item]
                    current_line_index = 0
                else:
                    return selected_item


def main(stdscr):
    menu = ViewMenu(stdscr)
    menu.start_menu()


if __name__ == '__main__':
    curses.wrapper(main)

