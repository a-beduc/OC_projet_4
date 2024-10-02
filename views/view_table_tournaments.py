import curses
from curses.textpad import Textbox
from views.view_table_base import ViewTableBase


class ViewTableTournaments(ViewTableBase):
    """
    A class for displaying and managing a table of tournaments using the curses library.
    Inherits from ViewTableBase and implements specific behavior for tournament data.

    Constants:
        COMMAND (list): Instructions for navigating the table, creating new tournaments, and loading existing ones.
        SORTS_FIELDS (list): Fields by which the tournament table can be sorted.
    """

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
        tournament_key_action = {
            ord('N'): self.new_tournament,
            ord('n'): self.new_tournament,
            ord('L'): self.load_tournament,
            ord('l'): self.load_tournament
        }
        self.TABLE_KEY_ACTION.update(tournament_key_action)

    def create_content(self, data=None):
        """
        Creates the table content for tournament as string lines, either displaying headers or data rows.
        If data is None, create headers
        """
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
        """ Reformats a number to ensure it is at least two characters long."""
        string_number = str(number)
        if len(string_number) == 1:
            return f" {number}"
        else:
            return f"{number}"

    @staticmethod
    def get_header_index(header_string):
        """ Calculates the index positions of each column in the header string. """
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

    @staticmethod
    def new_tournament():
        return "NEW_TOURNAMENT"

    def load_tournament(self):
        action = self.create_load_tournament_wind()
        curses.curs_set(0)
        if action is not None:
            return 'LOAD_TOURNAMENT', action

    def create_load_tournament_wind(self):
        """ Creates a window to prompt the user to enter the ID of a tournament to load. """
        clearing_space_height, clearing_space_width = (7, 26)
        clearing_wind = self.outer_wind.derwin(clearing_space_height, clearing_space_width,
                                               (self.outer_height - clearing_space_height) // 2,
                                               (self.outer_width - clearing_space_width) // 2)
        clearing_wind.clear()
        clearing_wind.refresh()

        load_tournament_height, load_tournament_width = (clearing_space_height - 2, clearing_space_width - 2)
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
