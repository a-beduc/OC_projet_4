import curses


class PlayerView:
    def __init__(self, stdscr, data):
        self.stdscr = stdscr
        self.data = data

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
        self.content_pad = None
        self.content_headers = self.create_content(self.inner_width)
        self.sorted_players = []

        self.init_windows()

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

    def create_content(self, variable_length, player_data=None):
        separator = " │ "
        software_id_header = "#ID  "
        last_name = "Last Name"
        first_name = "First Name"
        birth_date_header = "Birth Date"
        chess_id_header = "ChessID"

        fixed_length = len(software_id_header) + len(birth_date_header) + len(chess_id_header) + (4 * len(separator))
        name_length = (variable_length - fixed_length - 2) // 2

        if not player_data:
            first_name_header = self.reformat_name(first_name, name_length)
            last_name_header = self.reformat_name(last_name, name_length)

            return separator.join([software_id_header, last_name_header, first_name_header,
                                   birth_date_header, chess_id_header])

        else:
            software_id = self.reformat_id(player_data['id'])
            last_name = self.reformat_name(player_data['last_name'], name_length)
            first_name = self.reformat_name(player_data['first_name'], name_length)
            birth_date = self.reformat_date(player_data['date_of_birth'])
            chess_id = player_data['chess_id']

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
                if current_line_index == 0:
                    self.sort_data(sort_fields=['id'])
                    self.fill_pad()
                elif current_line_index == 1:
                    self.sort_data(sort_fields=['last_name', 'first_name', 'id'])
                    self.fill_pad()
                elif current_line_index == 2:
                    self.sort_data(sort_fields=['first_name', 'id'])
                    self.fill_pad()
                elif current_line_index == 3:
                    self.sort_data(sort_fields=['date_of_birth', 'id'])
                    self.fill_pad()
                elif current_line_index == 4:
                    self.sort_data(sort_fields=['chess_id', 'id'])
                    self.fill_pad()
                else:
                    pass
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
        pad_start_line = 0

        while running:
            key = self.outer_wind.getch()
            if key in [81, 113]:
                running = False
            elif key in [83, 115]:
                self.create_sort_menu()
            elif key == curses.KEY_DOWN:
                if pad_start_line < len(self.data) - self.content_height:
                    pad_start_line += 1
            elif key == curses.KEY_UP:
                if pad_start_line > 0:
                    pad_start_line -= 1
            else:
                pass

            # self.header_wind.refresh()
            # self.command_wind.refresh()
            # self.separator_wind.refresh()
            self.content_pad.refresh(pad_start_line, 0,
                                     self.command_height + self.header_height + self.separator_height,
                                     2,
                                     self.command_height + self.header_height + self.separator_height +
                                     self.content_height - 1,
                                     self.inner_width - 1)
            # self.outer_wind.refresh()
        exit()

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
        commands_general = "[↓][↑] Move, [s] Sort menu, [q] Quit"
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

        pad_height = max(len(self.data) + 1, self.content_height)
        self.content_pad = curses.newpad(pad_height, self.inner_width)

        rows = self.content_pad.getmaxyx()[0]
        for i in range(rows):
            blank_line = self.create_separator_line(self.content_headers, blank=True)
            self.content_pad.addstr(i, 1, blank_line)
        self.sort_data(sort_fields=['id'])
        self.fill_pad()
        self.content_pad.refresh(0, 0,
                                 self.command_height + self.header_height + self.separator_height, 2,
                                 self.command_height + self.header_height + self.separator_height + self.content_height
                                 - 1,
                                 self.inner_width - 1)

    def sort_data(self, sort_fields=['id']):
        data_list = []
        for key, value in self.data.items():
            id_num = int(key.split('_')[1])
            date_of_birth_list = value['date_of_birth'].split('-')
            date_of_birth_num = int(''.join(date_of_birth_list))
            data_list.append({
                'id': id_num,
                'last_name': value['last_name'],
                'first_name': value['first_name'],
                'date_of_birth': date_of_birth_num,
                'chess_id': value['chess_id'],
            })
        self.sorted_players = self.sort_key(data_list, sort_fields)

    @staticmethod
    def sort_key(list_of_dict, sort_fields):
        return sorted(list_of_dict, key=lambda x: tuple(x[field] for field in sort_fields))

    def fill_pad(self):
        i = 0
        for player_data in self.sorted_players:
            line = self.create_content(self.inner_width, player_data)
            self.content_pad.addstr(i, 1, line)
            i += 1
        self.content_pad.refresh(0, 0,
                                 self.command_height + self.header_height + self.separator_height, 2,
                                 self.command_height + self.header_height + self.separator_height + self.content_height
                                 - 1,
                                 self.inner_width - 1)


def main(stdscr):
    data = {"p_1": {
        "last_name": "Dupont",
        "first_name": "Jean",
        "date_of_birth": "1990-05-14",
        "chess_id": "AA00001"
    },
        "p_2": {
            "last_name": "Martin",
            "first_name": "Marie",
            "date_of_birth": "1988-09-23",
            "chess_id": "AA00002"
        },
        "p_3": {
            "last_name": "Durand",
            "first_name": "Paul",
            "date_of_birth": "1992-11-10",
            "chess_id": "AA00003"
        },
        "p_4": {
            "last_name": "Bernard",
            "first_name": "Lucie",
            "date_of_birth": "1995-03-08",
            "chess_id": "AA00004"
        },
        "p_5": {
            "last_name": "Dupont",
            "first_name": "Oc\u00e9ane",
            "date_of_birth": "1992-11-10",
            "chess_id": "AA00005"
        },
        "p_6": {
            "last_name": "Carlsen",
            "first_name": "Magnus",
            "date_of_birth": "1990-11-30",
            "chess_id": "AA00010"
        },
        "p_8965": {
            "last_name": "nametestloooooooooooooooooooooooooooooooooooooooooooooooooong",
            "first_name": "",
            "date_of_birth": "1963-12-03",
            "chess_id": "AA00010"
        }
    }
    view = PlayerView(stdscr, data)
    view.create_general_menu()


if __name__ == "__main__":
    curses.wrapper(main)
