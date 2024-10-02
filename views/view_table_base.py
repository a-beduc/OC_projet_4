import curses
from abc import ABC, abstractmethod


class ViewTableBase(ABC):
    """
    Abstract class that implement most of the methods used in view_table_players and view_table_tournament,
    for displaying and managing tables in the terminal using curses.

    Constants to be defined in child classes:
        COMMAND: A list of command instructions to be displayed.
        SORTS_FIELDS: A list of fields used to sort content in the table.
    """
    COMMAND_HEIGHT = 5
    HEADER_HEIGHT = 1
    SEPARATOR_HEIGHT = 1

    # Need to be implemented in child class
    COMMAND = []

    # Need to be implemented in child class
    SORTS_FIELDS = []

    def __init__(self, stdscr, pad_height):
        """ Initializes the table view with the given terminal screen and pad height (lines of datas). """
        self.stdscr = stdscr
        self.pad_height = pad_height
        curses.curs_set(0)

        self.outer_height = self.stdscr.getmaxyx()[0]
        self.outer_width = self.stdscr.getmaxyx()[1] - 2
        self.inner_width = self.outer_width - 2
        self.content_height = self.outer_height - (self.COMMAND_HEIGHT + self.HEADER_HEIGHT + self.SEPARATOR_HEIGHT + 1)

        # Attributes storing the window and pad objects of the view
        self.outer_wind = None
        self.command_wind = None
        self.header_wind = None
        self.separator_wind = None
        self.content_pad = None
        self.content_headers = None

        # Attributes used in the sort menu
        self.sorted_content = []
        self.current_sort_index = 0
        self.line_headers = None
        self.indexes = None
        self.SORT_KEY_ACTIONS = {
            curses.KEY_RIGHT: self.sort_move_right,
            curses.KEY_LEFT: self.sort_move_left,
            curses.KEY_ENTER: self.sort_select_option,
            10: self.sort_select_option,    # ASCII number for [Enter] key
            13: self.sort_select_option,    # ASCII number for [Enter] key
            ord('Q'): self.sort_quit,
            ord('q'): self.sort_quit
        }

        # Attributes used in the main menu
        self.pad_line = 0
        self.TABLE_KEY_ACTION = {
            curses.KEY_DOWN: self.move_down,
            curses.KEY_UP: self.move_up,
            ord('S'): self.sort_menu,
            ord('s'): self.sort_menu,
            ord('Q'): self.quit,
            ord('q'): self.quit,
        }

    def initialize(self, title):
        """ Initializes all the windows and pads needed for the table view. """
        self.outer_wind = self.create_outer_window(f" {title} ")
        self.command_wind = self.create_command_window()
        self.header_wind = self.create_header_wind()
        self.separator_wind = self.create_separator_wind()
        self.content_pad = self.create_content_pad()
        self.content_headers = self.create_content()

    def create_outer_window(self, title):
        """ Creates and returns the outer window for the table with a border and a title. """
        outer_wind = curses.newwin(self.outer_height,
                                   self.outer_width,
                                   0,
                                   1)
        outer_wind.clear()
        outer_wind.keypad(True)
        outer_wind.box()
        outer_wind.addstr(0, (self.outer_width - len(title)) // 2, title)
        outer_wind.refresh()
        return outer_wind

    def create_command_window(self):
        """ Create, update and returns the command window at the top of the screen. """
        command_wind = self.outer_wind.derwin(self.COMMAND_HEIGHT, self.inner_width, 0, 1)
        for idx, line in enumerate(self.COMMAND):
            command_wind.addstr(idx + 2, (self.inner_width - len(line)) // 2, line)
        command_wind.refresh()
        return command_wind

    def create_header_wind(self):
        """ Create, update and returns the headers of the column of the table. """
        header_wind = self.outer_wind.derwin(self.HEADER_HEIGHT,
                                             self.inner_width,
                                             self.COMMAND_HEIGHT,
                                             1)
        header_wind.addstr(0, 1, self.create_content())
        header_wind.refresh()
        return header_wind

    def create_separator_wind(self):
        """ Create and return a line of separation between headers and the pad that contains the content. """
        separator_wind = self.outer_wind.derwin(self.HEADER_HEIGHT,
                                                self.inner_width,
                                                self.HEADER_HEIGHT + self.COMMAND_HEIGHT,
                                                1)
        content_separator = self.update_separator_line(self.create_content())
        separator_wind.addstr(0, 1, content_separator)
        separator_wind.refresh()
        return separator_wind

    @staticmethod
    def update_separator_line(content):
        separator = " │ "
        parts = content.split(separator)
        line = ""
        for i, part in enumerate(parts):
            if i > 0:
                line += "─┼─"
            line += "─" * len(part)
        return line

    def create_content_pad(self):
        """ Create and returns a pad that will hold the table's content rows. """
        content_pad = curses.newpad(self.pad_height, self.inner_width)
        content_pad.refresh(0, 0,
                            self.COMMAND_HEIGHT + self.HEADER_HEIGHT + self.SEPARATOR_HEIGHT, 2,
                            self.COMMAND_HEIGHT + self.HEADER_HEIGHT + self.SEPARATOR_HEIGHT + self.content_height
                            - 1,
                            self.inner_width - 1)
        return content_pad

    @abstractmethod
    def create_content(self, data=None):
        raise NotImplementedError

    @staticmethod
    def reformat_id(software_id):
        length_id_target = 4
        return f"#{str(software_id).zfill(length_id_target)}"

    @staticmethod
    def reformat_name(name, target_length):
        if len(name) < target_length:
            return name.ljust(target_length)
        else:
            return name[:target_length - 1] + "."

    @staticmethod
    def reformat_date(date_number):
        str_date_number = str(date_number)
        return '-'.join([str_date_number[0:4], str_date_number[4:6], str_date_number[6:8]])

    @staticmethod
    @abstractmethod
    def get_header_index(header_string):
        raise NotImplementedError

    def sort_move_right(self):
        self.current_sort_index = (self.current_sort_index + 1) % len(self.indexes)

    def sort_move_left(self):
        self.current_sort_index = (self.current_sort_index - 1) % len(self.indexes)

    def sort_select_option(self):
        """ Selects the currently highlighted sort option and returns associated sort field """
        self.header_wind.clear()
        self.header_wind.addstr(0, 1, self.content_headers)
        self.header_wind.refresh()
        return 'SORT', self.SORTS_FIELDS[self.current_sort_index]

    def sort_quit(self):
        self.header_wind.clear()
        self.header_wind.addstr(0, 1, self.line_headers)
        self.header_wind.refresh()
        return 'QUIT'

    def initialize_sort_menu(self, line_headers):
        """
        Initializes the sort menu with the available sort fields and headers.

        Args:
            line_headers: The headers of the table displayed in the sort menu.
        """
        self.line_headers = line_headers
        indexes_values = self.get_header_index(line_headers)
        strings_menu = line_headers.split(" │ ")
        self.indexes = {i: (indexes_values[i], strings_menu[i]) for i in range(len(indexes_values))}

    def highlight_sort_line(self):
        self.header_wind.addstr(0, 1, self.line_headers)
        self.header_wind.addstr(
            0,
            1 + self.indexes[self.current_sort_index][0],
            self.indexes[self.current_sort_index][1],
            curses.A_REVERSE,
        )
        self.header_wind.refresh()

    def create_sort_menu(self, line_headers):
        """ Creates and displays the sort menu, allowing the user to select a field to sort by. """
        self.initialize_sort_menu(line_headers)

        while True:
            self.highlight_sort_line()
            key = self.outer_wind.getch()
            action = self.SORT_KEY_ACTIONS.get(key)
            if action:
                result = action()
                if result:
                    return result

    def move_up(self):
        """ Scroll the content pad up one line. """
        if self.pad_line > 0:
            self.pad_line -= 1

    def move_down(self):
        """ Scroll the content pad down one line. """
        if self.pad_line < self.pad_height - self.content_height:
            self.pad_line += 1

    @staticmethod
    def quit():
        return 'BACK'

    def sort_menu(self):
        """ Start the sort menu and returns the selected sort action. """
        action = self.create_sort_menu(self.content_headers)
        if action is not None:
            return action

    def update_pad(self):
        """ Updates and refreshes the content pad to display the current lines based on the current scroll position. """
        self.content_pad.refresh(self.pad_line, 0,
                                 self.COMMAND_HEIGHT + self.HEADER_HEIGHT + self.SEPARATOR_HEIGHT,
                                 2,
                                 self.COMMAND_HEIGHT + self.HEADER_HEIGHT + self.SEPARATOR_HEIGHT +
                                 self.content_height - 1,
                                 self.inner_width - 1)

    def start_view(self):
        """
        Starts the main loop for displaying and interacting with the table view.
        Handles user input for scrolling and sorting.
        """
        while True:
            self.update_pad()
            key = self.outer_wind.getch()
            action = self.TABLE_KEY_ACTION.get(key)
            if action:
                result = action()
                if result:
                    return result

    def fill_pad(self, sorted_content):
        """ Fills the content pad with sorted content rows. """
        self.content_pad.clear()
        for i, data in enumerate(sorted_content):
            line = self.create_content(data)
            self.content_pad.addstr(i, 1, line)
        self.content_pad.refresh(0, 0,
                                 self.COMMAND_HEIGHT + self.HEADER_HEIGHT + self.SEPARATOR_HEIGHT, 2,
                                 self.COMMAND_HEIGHT + self.HEADER_HEIGHT + self.SEPARATOR_HEIGHT +
                                 self.content_height - 1,
                                 self.inner_width - 1)
