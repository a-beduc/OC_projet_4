import curses
from views.view_table_base import ViewTableBase


class ViewTablePlayers(ViewTableBase):
    COMMAND = [
        "[↓][↑] Move, [s] Sort menu, [q] Quit",
        "Sort: [←][→] Move, [Enter] Sort, [q] Back/Quit"
    ]

    SORTS_FIELDS = [
            ['id'],
            ['last_name', 'first_name', 'id'],
            ['first_name', 'id'],
            ['date_of_birth', 'id'],
            ['chess_id', 'id']
        ]

    def __init__(self, stdscr, pad_height):
        super().__init__(stdscr, pad_height)

    def initialize(self):
        self.outer_wind = self.create_outer_window(" List of Players ")
        self.command_wind = self.create_command_window()
        self.header_wind = self.create_header_wind()
        self.separator_wind = self.create_separator_wind()
        self.content_pad = self.create_content_pad()
        self.content_headers = self.create_content()

    def create_content(self, data=None):
        separator = " │ "
        software_id_header = "#ID  "
        last_name = "Last Name"
        first_name = "First Name"
        birth_date_header = "Birth Date"
        chess_id_header = "ChessID"

        fixed_length = len(software_id_header) + len(birth_date_header) + len(chess_id_header) + (4 * len(separator))
        name_length = (self.inner_width - fixed_length - 2) // 2

        if data is None:
            first_name_header = self.reformat_name(first_name, name_length)
            last_name_header = self.reformat_name(last_name, name_length)
            return separator.join([software_id_header, last_name_header, first_name_header,
                                   birth_date_header, chess_id_header])
        else:
            software_id = self.reformat_id(data['id'])
            last_name = self.reformat_name(data['last_name'], name_length)
            first_name = self.reformat_name(data['first_name'], name_length)
            birth_date = self.reformat_date(data['date_of_birth'])
            chess_id = data['chess_id']
            return separator.join([software_id, last_name, first_name, birth_date, chess_id])

    @staticmethod
    def get_header_index(header_string):
        parts = header_string.split("│")
        idx_id = 0
        idx_last_name = 2 + len(parts[0])
        idx_first_name = 1 + idx_last_name + len(parts[1])
        idx_date = 1 + idx_first_name + len(parts[2])
        idx_chess = 1 + idx_date + len(parts[3])
        return idx_id, idx_last_name, idx_first_name, idx_date, idx_chess

    def start_view(self, line_index=0):
        running = True
        pad_start_line = 0
        while running:
            self.content_pad.refresh(pad_start_line, 0,
                                     self.COMMAND_HEIGHT + self.HEADER_HEIGHT + self.SEPARATOR_HEIGHT,
                                     2,
                                     self.COMMAND_HEIGHT + self.HEADER_HEIGHT + self.SEPARATOR_HEIGHT +
                                     self.content_height - 1,
                                     self.inner_width - 1)
            key = self.outer_wind.getch()
            if key in [81, 113]:
                return 'BACK'
            elif key in [83, 115]:
                action = self.create_sort_menu(self.SORTS_FIELDS, self.content_headers, line_index)
                if action is not None:
                    return action
            elif key == curses.KEY_DOWN:
                if pad_start_line < self.pad_height - self.content_height:
                    pad_start_line += 1
            elif key == curses.KEY_UP:
                if pad_start_line > 0:
                    pad_start_line -= 1

    def fill_pad(self, sorted_content):
        self.content_pad.clear()
        for i, data in enumerate(sorted_content):
            line = self.create_content(data)
            self.content_pad.addstr(i, 1, line)
        self.content_pad.refresh(0, 0,
                                 self.COMMAND_HEIGHT + self.HEADER_HEIGHT + self.SEPARATOR_HEIGHT, 2,
                                 self.COMMAND_HEIGHT + self.HEADER_HEIGHT + self.SEPARATOR_HEIGHT +
                                 self.content_height - 1,
                                 self.inner_width - 1)
