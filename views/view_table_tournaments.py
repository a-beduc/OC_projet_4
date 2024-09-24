import curses
from curses.textpad import Textbox
from views.view_table_base import ViewTableBase


class ViewTableTournaments(ViewTableBase):
    COMMAND_HEIGHT = 6

    COMMAND = [
        "[↓][↑] Move, [s] Sort menu, [q] Quit",
        "[n] New Tournament, [l] Load Tournament",
        "Sort: [←][→] Move, [Enter] Sort, [q] Back/Quit"
    ]

    SORTS_FIELDS = [
        ['id'],
        ['name', 'id'],
        ['place', 'id'],
        ['date_start', 'id'],
        ['date_end', 'id'],
        ['participants', 'id'],
        ['rounds', 'id'],
        ['complete', 'id']
    ]

    def __init__(self, stdscr, pad_height):
        super().__init__(stdscr, pad_height)

    def initialize(self):
        self.outer_wind = self.create_outer_window(" List of Tournaments ")
        self.command_wind = self.create_command_window()
        self.header_wind = self.create_header_wind()
        self.separator_wind = self.create_separator_wind()
        self.content_pad = self.create_content_pad()
        self.content_headers = self.create_content()

    def create_content(self, data=None):
        separator = " │ "
        software_id_header = "#ID  "
        name = "Name"
        place = "Place"
        date_start_header = "Date Start"
        date_end_header = "Date End  "
        number_participants_header = "P "
        number_rounds_header = "R "
        completed_header = "C "

        fixed_length = (len(software_id_header) + len(date_start_header) + len(date_end_header)
                        + len(number_participants_header) + len(number_rounds_header) + len(completed_header)
                        + (7 * len(separator)))
        name_length = (self.inner_width - fixed_length - 2) // 2

        if data is None:
            name_header = self.reformat_name(name, name_length)
            place_header = self.reformat_name(place, name_length)
            return separator.join([software_id_header, name_header, place_header, date_start_header, date_end_header,
                                   number_participants_header, number_rounds_header, completed_header])
        else:
            software_id = self.reformat_id(data['id'])
            name = self.reformat_name(data['name'], name_length)
            place = self.reformat_name(data['place'], name_length)
            date_start = self.reformat_date(data['date_start'])
            date_end = self.reformat_date(data['date_end'])
            number_participants = self.reformat_number(data['participants'])
            number_rounds = self.reformat_number(data['rounds'])
            complete = "o " if data['complete'] else "  "
            return separator.join([software_id, name, place, date_start, date_end, number_participants, number_rounds,
                                   complete])

    @staticmethod
    def reformat_number(number):
        string_number = str(number)
        if len(string_number) == 1:
            return f" {number}"
        else:
            return f"{number}"

    @staticmethod
    def get_header_index(header_string):
        parts = header_string.split("│")
        idx_id = 0
        idx_name = 2 + len(parts[0])
        idx_place = 1 + idx_name + len(parts[1])
        idx_date_start = 1 + idx_place + len(parts[2])
        idx_date_end = 1 + idx_date_start + len(parts[3])
        idx_participants = 1 + idx_date_end + len(parts[4])
        idx_rounds = 1 + idx_participants + len(parts[5])
        idx_complete = 1 + idx_rounds + len(parts[6])
        return idx_id, idx_name, idx_place, idx_date_start, idx_date_end, idx_participants, idx_rounds, idx_complete

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
            if key in [81, 113]:  # 'Q' or 'q'
                return 'BACK'
            elif key in [83, 115]:  # 'S' or 's'
                action = self.create_sort_menu(self.SORTS_FIELDS, self.content_headers, line_index)
                if action is not None:
                    return action
            elif key == curses.KEY_DOWN:
                if pad_start_line < self.pad_height - self.content_height:
                    pad_start_line += 1
            elif key == curses.KEY_UP:
                if pad_start_line > 0:
                    pad_start_line -= 1
            elif key in [78, 110]:  # 'N' or 'n'
                return "NEW_TOURNAMENT"
            elif key in [76, 108]:  # 'L' or 'l'
                action = self.create_load_tournament_wind()
                curses.curs_set(0)
                if action is not None:
                    return 'LOAD_TOURNAMENT', action

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

    def create_load_tournament_wind(self):
        clearing_space_height = 7
        clearing_space_width = 26
        clearing_wind = self.outer_wind.derwin(clearing_space_height, clearing_space_width,
                                               (self.outer_height - clearing_space_height) // 2,
                                               (self.outer_width - clearing_space_width) // 2)
        clearing_wind.clear()
        clearing_wind.refresh()

        load_tournament_height = clearing_space_height - 2
        load_tournament_width = clearing_space_width - 2
        load_tournament_wind = clearing_wind.derwin(load_tournament_height, load_tournament_width,
                                                    1,
                                                    1)
        load_tournament_wind.clear()
        load_tournament_wind.box()
        load_title = " Load Tournament "
        load_tournament_wind.addstr(0, (load_tournament_width - len(load_title)) // 2, load_title)
        load_text = "ID : "
        middle_width_of_tournament_wind = load_tournament_wind.getmaxyx()[1] // 2
        load_tournament_wind.addstr(2, middle_width_of_tournament_wind - len(load_text), load_text)
        load_tournament_wind.refresh()
        input_win = load_tournament_wind.derwin(1, 5, 2, middle_width_of_tournament_wind)
        input_win.refresh()
        box = Textbox(input_win)
        curses.curs_set(1)
        box.edit()
        user_input = box.gather().lstrip('0').strip()
        clearing_wind.clear()
        clearing_wind.refresh()
        return user_input
