import curses
from curses.textpad import Textbox
from base_view_table import BaseView


class TournamentView(BaseView):
    COMMAND_HEIGHT = 6
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

    def __init__(self, stdscr, data):
        super().__init__(stdscr, window_title=" List of Tournaments ", data=data)
        self.command_wind = self.create_command_window("[↓][↑] Move, [s] Sort menu, [q] Quit",
                                                       "[n] New Tournament, [l] Load Tournament",
                                                       "Sort: [←][→] Move, [Enter] Sort, [q] Back/Quit")
        self.content_headers = self.create_content()
        self.create_content_pad()

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

    def create_general_menu(self):
        running = True
        pad_start_line = 0

        while running:
            key = self.outer_wind.getch()

            if key == curses.KEY_DOWN:
                if pad_start_line < len(self.data) - self.content_height:
                    pad_start_line += 1
            elif key == curses.KEY_UP:
                if pad_start_line > 0:
                    pad_start_line -= 1

            elif key in [83, 115]:  # 'S' or 's'
                self.create_sort_menu(self.SORTS_FIELDS, self.content_headers)

            elif key in [81, 113]:  # 'Q' or 'q'
                return "quit"

            elif key in [78, 110]:  # 'N' or 'n'
                return "new_tournament"

            elif key in [76, 108]:  # 'L' or 'l'
                input_value = self.create_load_tournament_wind()
                curses.curs_set(0)
                self.refresh_main_view()
                if type(input_value) is int:
                    self.create_error_message()
                    self.refresh_main_view()
                else:
                    pass

            self.content_pad.refresh(pad_start_line, 0,
                                     self.COMMAND_HEIGHT + self.HEADER_HEIGHT + self.SEPARATOR_HEIGHT,
                                     2,
                                     self.COMMAND_HEIGHT + self.HEADER_HEIGHT + self.SEPARATOR_HEIGHT +
                                     self.content_height - 1,
                                     self.inner_width - 1)

    def sort_data(self, sort_fields=['id']):
        data_list = []
        for key, value in self.data.items():
            id_num = int(key.split("_")[1])
            date_start_list = value['date_start'].split('-')
            date_start_num = int(''.join(date_start_list))
            date_end_list = value['date_end'].split('-')
            date_end_num = int(''.join(date_end_list))
            data_list.append({
                'id': id_num,
                'name': value['name'],
                'place': value['place'],
                'date_start': date_start_num,
                'date_end': date_end_num,
                'participants': value['participants'],
                'rounds': value['rounds'],
                'complete': value['complete']
            })
        self.sorted_content = self.sort_key(data_list, sort_fields)

    def fill_pad(self):
        self.content_pad.clear()
        for i, data in enumerate(self.sorted_content):
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
        return box.gather()

    def refresh_main_view(self):
        self.command_wind.clear()
        self.command_wind.refresh()
        self.outer_wind = self.create_outer_window(" List of Tournaments ")
        self.command_wind = self.create_command_window(
            "[↓][↑] Move, [s] Sort menu, [q] Quit",
            "[n] New Tournament, [l] Load Tournament",
            "Sort: [←][→] Move, [Enter] Sort, [q] Back/Quit"
        )
        self.header_wind.clear()
        self.header_wind.refresh()
        self.header_wind = self.create_header_wind()
        self.separator_wind.clear()
        self.separator_wind.refresh()
        self.separator_wind = self.create_separator_wind()
        self.content_pad.refresh(0, 0,
                                 self.COMMAND_HEIGHT + self.HEADER_HEIGHT + self.SEPARATOR_HEIGHT, 2,
                                 self.COMMAND_HEIGHT + self.HEADER_HEIGHT + self.SEPARATOR_HEIGHT +
                                 self.content_height - 1,
                                 self.inner_width - 1)

    def create_error_message(self):
        clearing_space_height = 5
        clearing_space_width = 22
        clearing_wind = self.outer_wind.derwin(clearing_space_height, clearing_space_width,
                                               (self.outer_height - clearing_space_height) // 2,
                                               (self.outer_width - clearing_space_width) // 2)
        clearing_wind.clear()
        clearing_wind.refresh()

        error_window = clearing_wind.derwin(clearing_space_height - 2, clearing_space_width - 2, 1, 1)
        error_window.clear()
        error_window.box()
        text = " ERROR "
        width_error = error_window.getmaxyx()[1]
        error_window.addstr(0, (width_error - len(text)) // 2, text)
        text_2 = "ID is not valid"
        error_window.addstr(1, (width_error - len(text_2)) // 2, text_2)
        error_window.refresh()
        self.outer_wind.getch()


def main(stdscr):
    data = {
        "t_1": {
            "name": "Tournament test",
            "place": "Testland",
            "date_start": "2020-12-04",
            "date_end": "2020-12-05",
            "participants": 6,
            "rounds": 4,
            "complete": True
        },
        "t_2": {
            "name": "Tcsdfdsfourfefement test",
            "place": "Tesfsfsfnd fdsf sdfs",
            "date_start": "2020-12-04",
            "date_end": "2021-01-05",
            "participants": 12,
            "rounds": 8,
            "complete": False
        }
    }
    view = TournamentView(stdscr, data)
    view.create_general_menu()


if __name__ == '__main__':
    curses.wrapper(main)
