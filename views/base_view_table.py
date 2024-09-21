import curses
from abc import ABC, abstractmethod


class BaseView(ABC):
    COMMAND_HEIGHT = 5
    HEADER_HEIGHT = 1
    SEPARATOR_HEIGHT = 1

    def __init__(self, stdscr, window_title=" Default Title ", data=None):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.data = data

        self.outer_height = self.stdscr.getmaxyx()[0]
        self.outer_width = self.stdscr.getmaxyx()[1] - 2
        self.inner_width = self.outer_width - 2
        self.content_height = self.outer_height - (self.COMMAND_HEIGHT + self.HEADER_HEIGHT + self.SEPARATOR_HEIGHT + 1)

        self.outer_wind = self.create_outer_window(window_title)
        self.command_wind = None
        self.header_wind = self.create_header_wind()
        self.separator_wind = self.create_separator_wind()
        self.content_pad = None

        self.sorted_content = []

    def create_outer_window(self, title):
        outer_wind = curses.newwin(self.outer_height,
                                   self.outer_width,
                                   0,
                                   1)
        outer_wind.keypad(True)
        outer_wind.box()
        outer_wind.addstr(0, (self.outer_width - len(title)) // 2, title)
        outer_wind.refresh()
        return outer_wind

    def create_command_window(self, first_line, second_line, third_line=""):
        command_wind = self.outer_wind.derwin(self.COMMAND_HEIGHT,
                                              self.inner_width,
                                              0,
                                              1)
        command_wind.addstr(2, (self.inner_width - len(first_line)) // 2, first_line)
        command_wind.addstr(3, (self.inner_width - len(second_line)) // 2, second_line)
        if third_line != "":
            command_wind.addstr(4, (self.inner_width - len(third_line)) // 2, third_line)
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
        pad_height = max(len(self.data) + 1, self.content_height)
        self.content_pad = curses.newpad(pad_height, self.inner_width)
        self.sort_data(sort_fields=['id'])
        self.fill_pad()
        self.content_pad.refresh(0, 0,
                                 self.COMMAND_HEIGHT + self.HEADER_HEIGHT + self.SEPARATOR_HEIGHT, 2,
                                 self.COMMAND_HEIGHT + self.HEADER_HEIGHT + self.SEPARATOR_HEIGHT + self.content_height
                                 - 1,
                                 self.inner_width - 1)

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

    @abstractmethod
    def sort_data(self, sort_fields=['id']):
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
    def sort_key(list_of_dict, sort_fields):
        return sorted(list_of_dict, key=lambda x: tuple([x[field] for field in sort_fields]))

    @abstractmethod
    def fill_pad(self):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_header_index(header_string):
        raise NotImplementedError

    def create_sort_menu(self, sorts_fields_list, content_headers):
        current_line_index = 0
        indexes_values = self.get_header_index(content_headers)
        strings_menu = content_headers.split(" │ ")
        indexes = {i: (indexes_values[i], strings_menu[i]) for i in range(len(indexes_values))}

        running = True

        self.header_wind.clear()
        self.header_wind.addstr(0, 1, content_headers)
        self.header_wind.addstr(
            0,
            1 + indexes[current_line_index][0],
            indexes[current_line_index][1],
            curses.A_REVERSE
        )
        self.header_wind.refresh()

        while running:
            key = self.outer_wind.getch()
            if key == curses.KEY_RIGHT:
                current_line_index = (current_line_index + 1) % len(indexes)
            elif key == curses.KEY_LEFT:
                current_line_index = (current_line_index - 1) % len(indexes)
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.sort_data(sort_fields=sorts_fields_list[current_line_index])
                self.fill_pad()
            elif key in [81, 113]:
                running = False

            self.header_wind.clear()
            self.header_wind.addstr(0, 1, content_headers)
            self.header_wind.addstr(
                0,
                1 + indexes[current_line_index][0],
                indexes[current_line_index][1],
                curses.A_REVERSE,
            )
            self.header_wind.refresh()

        self.header_wind.addstr(0, 1, content_headers)
        self.header_wind.refresh()

    @abstractmethod
    def create_general_menu(self):
        raise NotImplementedError
