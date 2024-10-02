import curses


class ViewMenu:
    """
    Class responsible for displaying and interacting with a menu in the terminal using the curses module.
    The menu uses the default size of a terminal on a Mac (24 lines and 80 columns).
    """

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
        """
        Initialize the ViewMenu class.
        :param stdscr: Screen object initialized by curses.wrapper()
        """
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

        self.current_menu = self.MAIN_MENU
        self.current_line_index = 0

        self.KEY_ACTIONS = {
            curses.KEY_UP: self.move_up,
            curses.KEY_DOWN: self.move_down,
            curses.KEY_ENTER: self.select_option,
            10: self.select_option,
            13: self.select_option
        }

    def initialize(self):
        """
        Initialize and create all the windows required for the menu display.
        """
        self.outer_wind = curses.newwin(self.terminal_h, self.terminal_w, 0, 0)
        self.outer_wind.clear()
        self.outer_wind.refresh()
        self.base_wind = self.create_base_wind()
        self.ascii_wind = self.create_ascii_wind()
        self.menu_wind = self.create_menu_wind()

    def create_base_wind(self):
        """
        Create the base window which will contain the ASCII art and the menu.
        :return: The created base window.
        """
        self.stdscr.clear()
        base_wind = curses.newwin(self.MIN_TERMINAL_HEIGHT,
                                  self.MIN_TERMINAL_WIDTH,
                                  (self.terminal_h - self.MIN_TERMINAL_HEIGHT) // 2,
                                  (self.terminal_w - self.MIN_TERMINAL_WIDTH) // 2)
        base_wind.refresh()
        return base_wind

    def print_ascii_art(self, window):
        """
        Print the ASCII art into the given window.
        :param window: The window where the ASCII art will be printed.
        """
        for idx, line in enumerate(self.ASCII_ART):
            x = (self.MIN_TERMINAL_WIDTH - len(line)) // 2
            window.addstr(idx + 1, x, line)
        window.refresh()

    def create_ascii_wind(self):
        """
        Create a window for the ASCII art.
        :return: The created ASCII art window.
        """
        h, w = (len(self.ASCII_ART) + 2, self.base_wind.getmaxyx()[1])
        ascii_wind = self.base_wind.derwin(h, w, 0, 0)
        self.print_ascii_art(ascii_wind)
        ascii_wind.refresh()
        return ascii_wind

    def create_menu_wind(self):
        """
        Create a window for displaying the menu options.
        :return: The created menu window.
        """
        h, w = (len(self.MAIN_MENU) + 2, self.base_wind.getmaxyx()[1])
        menu_wind = self.base_wind.derwin(h, w, self.ascii_wind.getmaxyx()[0] + 1, 0)
        menu_wind.keypad(True)
        menu_wind.refresh()
        return menu_wind

    def print_menu(self):
        """
        Display the menu options in the menu window, with the selected option highlighted.
        """
        self.menu_wind.clear()
        # ' Tournaments ': (0, 'TOURNAMENT_MENU') --> (' Tournaments ': (0, 'TOURNAMENT_MENU')) where 0 = sort_key
        menu_items = sorted(self.current_menu.items(), key=lambda item: item[1][0])
        menu_width = self.menu_wind.getmaxyx()[1]

        for line, (idx, _) in menu_items:
            x = (menu_width - len(line)) // 2
            if idx == self.current_line_index:
                self.menu_wind.addstr(idx, x, line, curses.A_REVERSE)
            else:
                self.menu_wind.addstr(idx, x, line)
        self.menu_wind.refresh()

    def move_up(self):
        self.current_line_index = (self.current_line_index - 1) % len(self.current_menu)

    def move_down(self):
        self.current_line_index = (self.current_line_index + 1) % len(self.current_menu)

    def select_option(self):
        """
        Select the currently highlighted menu item and return the corresponding action.
        :return: The action associated with the selected menu item.
        """
        # ' Tournaments ': (0, 'TOURNAMENT_MENU') --> (' Tournaments ': (0, 'TOURNAMENT_MENU')) where 0 = sort_key
        menu_items = sorted(self.current_menu.items(), key=lambda item: item[1][0])
        selected_item = menu_items[self.current_line_index][1][1]
        if selected_item in self.menus.keys():
            self.current_menu = self.menus[selected_item]
            self.current_line_index = 0
        else:
            return selected_item

    def start_menu(self):
        """
        Start the main loop for the menu interaction.
        :return: The action associated with the selected menu item.
        """
        while True:
            self.print_menu()
            key = self.menu_wind.getch()
            action = self.KEY_ACTIONS.get(key)
            if action:
                result = action()
                if result:
                    return result
