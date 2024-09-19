import curses


class PlayerView:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.outer_height = self.stdscr.getmaxyx()[0]
        self.outer_width = self.stdscr.getmaxyx()[1] - 2
        self.inner_width = self.outer_width - 2
        self.command_height = 5
        self.header_height = 1
        self.separator_height = 1
        self.content_height = self.outer_height - (self.command_height + self.header_height + self.separator_height + 1)
        self.outer_wind = None
        self.command_wind = None
        self.header_wind = None
        self.separator_wind = None
        self.content_wind = None
        self.content_headers = self.create_content(self.inner_width)
        self.init_windows()

    @staticmethod
    def reformat_id(software_id):
        length_id_target = 4
        software_id = software_id.split("_")[1] if "_" in software_id else software_id
        return f"#{software_id.zfill(length_id_target)}"

    @staticmethod
    def reformat_name(name, target_length):
        if len(name) < target_length:
            return name.ljust(target_length)
        else:
            return name[:target_length - 1] + "."

    def create_content(self,
                       variable_length,
                       software_id="#ID  ",
                       last_name="Last Name",
                       first_name="First Name",
                       birth_date="Birth Date",
                       chess_id="ChessID"):
        separator = " │ "

        software_id = self.reformat_id(software_id) if "_" in software_id else "#ID  "

        fixed_length = len(software_id) + len(birth_date) + len(chess_id) + (4 * len(separator))
        name_length = (variable_length - fixed_length - 2) // 2

        first_name = self.reformat_name(first_name, name_length)
        last_name = self.reformat_name(last_name, name_length)

        return separator.join([software_id, last_name, first_name, birth_date, chess_id])

    @staticmethod
    def create_separator_line(content, blank=False):
        separator = " │ "
        parts = content.split(separator)
        line = ""
        for i, part in enumerate(parts):
            if not blank:
                if i > 0:
                    line += "─┼─"
                line += "─" * len(part)
            else:
                if i > 0:
                    line += " │ "
                line += " " * len(part)
        return line

    @staticmethod
    def get_header_index(header_string):
        parts = header_string.split("│")
        id_software = 0
        id_last_name = 2 + len(parts[0])
        id_first_name = 1 + id_last_name + len(parts[1])
        id_date = 1 + id_first_name + len(parts[2])
        id_chess = 1 + id_date + len(parts[3])
        return id_software, id_last_name, id_first_name, id_date, id_chess

    def create_sort_menu(self):
        current_line_index = 0
        indexes_values = self.get_header_index(self.content_headers)
        strings_menu = self.content_headers.split(" │ ")
        indexes = {i: (indexes_values[i], strings_menu[i]) for i in range(len(indexes_values))}

        running = True

        self.header_wind.clear()
        self.header_wind.addstr(0, 1, self.content_headers)
        self.header_wind.addstr(
            0,
            1 + indexes[current_line_index][0],
            indexes[current_line_index][1],
            curses.A_REVERSE,
        )
        self.header_wind.refresh()

        while running:
            key = self.outer_wind.getch()
            if key == curses.KEY_RIGHT:
                current_line_index = (current_line_index + 1) % len(indexes)
            elif key == curses.KEY_LEFT:
                current_line_index = (current_line_index - 1) % len(indexes)
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.command_wind.clear()
                self.command_wind.addstr(2, 0, "You pressed [Enter]")
                self.command_wind.refresh()
            elif key in [81, 113]:
                running = False

            self.header_wind.clear()
            self.header_wind.addstr(0, 1, self.content_headers)
            self.header_wind.addstr(
                0,
                1 + indexes[current_line_index][0],
                indexes[current_line_index][1],
                curses.A_REVERSE,
            )
            self.header_wind.refresh()

        self.header_wind.addstr(0, 1, self.content_headers)
        self.header_wind.refresh()

    def create_general_menu(self):
        running = True
        while running:
            key = self.outer_wind.getch()
            if key in [81, 113]:
                running = False
            elif key in [83, 115]:
                self.create_sort_menu()
            elif key in [80, 112]:
                self.command_wind.clear()
                self.command_wind.addstr(2, 0, "You pressed 'p' or 'P'")
                self.command_wind.refresh()
            else:
                pass

            self.header_wind.refresh()
            self.command_wind.refresh()
            self.separator_wind.refresh()
            self.content_wind.refresh()
            self.outer_wind.refresh()
        exit()

    @staticmethod
    def create_header_menu():
        pass

    def init_windows(self):
        curses.curs_set(0)

        self.outer_wind = curses.newwin(self.outer_height,
                                        self.outer_width,
                                        0,
                                        1)
        self.outer_wind.keypad(True)
        self.outer_wind.box()
        title = " List of Players "
        self.outer_wind.addstr(0, (self.outer_width - len(title)) // 2, title)
        self.outer_wind.refresh()

        self.command_wind = self.outer_wind.derwin(self.command_height,
                                                   self.inner_width,
                                                   0,
                                                   1)
        commands_general = "[p] + [↓][↑] Move, [s] Sort menu, [q] Quit"
        commands_sort = "Sort: [←][→] Move, [Enter] Sort, [q] Back/Quit"
        self.command_wind.addstr(2, (self.inner_width - len(commands_general)) // 2, commands_general)
        self.command_wind.addstr(3, (self.inner_width - len(commands_sort)) // 2, commands_sort)
        self.command_wind.refresh()

        self.header_wind = self.outer_wind.derwin(self.header_height,
                                                  self.inner_width,
                                                  self.command_height,
                                                  1)
        self.header_wind.addstr(0, 1, self.content_headers)
        self.header_wind.refresh()

        self.separator_wind = self.outer_wind.derwin(self.header_height,
                                                     self.inner_width,
                                                     self.header_height + self.command_height,
                                                     1)
        content_separator = self.create_separator_line(self.content_headers)
        self.separator_wind.addstr(0, 1, content_separator)
        self.separator_wind.refresh()

        self.content_wind = self.outer_wind.derwin(self.content_height,
                                                   self.inner_width,
                                                   self.command_height + self.header_height + self.separator_height,
                                                   1)
        rows = self.content_wind.getmaxyx()[0]
        for i in range(rows):
            blank_line = self.create_separator_line(self.content_headers, blank=True)
            self.content_wind.addstr(i, 1, blank_line)
        self.content_wind.refresh()


def main(stdscr):
    view = PlayerView(stdscr)
    view.create_general_menu()


if __name__ == "__main__":
    curses.wrapper(main)
