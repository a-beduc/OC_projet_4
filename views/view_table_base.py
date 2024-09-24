import curses
from abc import ABC, abstractmethod


class ViewTableBase(ABC):
    COMMAND_HEIGHT = 5
    HEADER_HEIGHT = 1
    SEPARATOR_HEIGHT = 1

    COMMAND = []

    def __init__(self, stdscr, pad_height):
        self.stdscr = stdscr
        self.pad_height = pad_height
        curses.curs_set(0)

        self.outer_height = self.stdscr.getmaxyx()[0]
        self.outer_width = self.stdscr.getmaxyx()[1] - 2
        self.inner_width = self.outer_width - 2
        self.content_height = self.outer_height - (self.COMMAND_HEIGHT + self.HEADER_HEIGHT + self.SEPARATOR_HEIGHT + 1)

        self.outer_wind = None
        self.command_wind = None
        self.header_wind = None
        self.separator_wind = None
        self.content_pad = None
        self.content_headers = None

        self.sorted_content = []

    def create_outer_window(self, title):
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
        command_wind = self.outer_wind.derwin(self.COMMAND_HEIGHT, self.inner_width, 0, 1)
        for idx, line in enumerate(self.COMMAND):
            command_wind.addstr(idx + 2, (self.inner_width - len(line)) // 2, line)
        command_wind.refresh()
        return command_wind

    def create_header_wind(self):
        header_wind = self.outer_wind.derwin(self.HEADER_HEIGHT,
                                             self.inner_width,
                                             self.COMMAND_HEIGHT,
                                             1)
        header_wind.addstr(0, 1, self.create_content())
        header_wind.refresh()
        return header_wind

    def create_separator_wind(self):
        separator_wind = self.outer_wind.derwin(self.HEADER_HEIGHT,
                                                self.inner_width,
                                                self.HEADER_HEIGHT + self.COMMAND_HEIGHT,
                                                1)
        content_separator = self.create_separator_line(self.create_content())
        separator_wind.addstr(0, 1, content_separator)
        separator_wind.refresh()
        return separator_wind

    def create_content_pad(self):
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
    def create_separator_line(content):
        separator = " │ "
        parts = content.split(separator)
        line = ""
        for i, part in enumerate(parts):
            if i > 0:
                line += "─┼─"
            line += "─" * len(part)
        return line

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

    @abstractmethod
    def fill_pad(self, sorted_content):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_header_index(header_string):
        raise NotImplementedError

    def create_sort_menu(self, sorts_fields_list, content_headers, line_index=0):
        current_line_index = line_index
        indexes_values = self.get_header_index(content_headers)
        strings_menu = content_headers.split(" │ ")
        indexes = {i: (indexes_values[i], strings_menu[i]) for i in range(len(indexes_values))}

        running = True

        while running:
            self.header_wind.clear()
            self.header_wind.addstr(0, 1, content_headers)
            self.header_wind.addstr(
                0,
                1 + indexes[current_line_index][0],
                indexes[current_line_index][1],
                curses.A_REVERSE,
            )
            self.header_wind.refresh()

            key = self.outer_wind.getch()
            if key == curses.KEY_RIGHT:
                current_line_index = (current_line_index + 1) % len(indexes)
            elif key == curses.KEY_LEFT:
                current_line_index = (current_line_index - 1) % len(indexes)
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.header_wind.clear()
                self.header_wind.addstr(0, 1, content_headers)
                self.header_wind.refresh()
                return 'SORT', sorts_fields_list[current_line_index], current_line_index
            elif key in [81, 113]:
                self.header_wind.clear()
                self.header_wind.addstr(0, 1, content_headers)
                self.header_wind.refresh()
                running = False

    @abstractmethod
    def start_view(self):
        raise NotImplementedError
