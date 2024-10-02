from views.view_table_base import ViewTableBase


class ViewTablePlayers(ViewTableBase):
    """
    A class for displaying and managing a table of players using the curses
    library.
    Inherits from ViewTableBase and implements specific behavior for player
    data.

    Constants:
        COMMAND (list): Instructions for navigating the table and sort menu.
        SORTS_FIELDS (list): Fields by which the player table can be sorted.
    """

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

    def create_content(self, data=None):
        """
        Creates the table content for players as string lines, either
        displaying headers or data rows.
        If data is None, create headers
        """
        separator = " │ "
        software_id_header = "#ID  "
        last_name = "Last Name"
        first_name = "First Name"
        birth_date_header = "Birth Date"
        chess_id_header = "ChessID "

        fixed_length = (len(software_id_header) + len(birth_date_header)
                        + len(chess_id_header) + (4 * len(separator)))
        name_length = (self.inner_width - fixed_length - 2) // 2

        if data is None:
            first_name_header = self.reformat_name(first_name, name_length)
            last_name_header = self.reformat_name(last_name, name_length)
            return separator.join([software_id_header, last_name_header,
                                   first_name_header, birth_date_header,
                                   chess_id_header])
        else:
            software_id = self.reformat_id(data['id'])
            last_name = self.reformat_name(data['last_name'], name_length)
            first_name = self.reformat_name(data['first_name'], name_length)
            birth_date = self.reformat_date(data['date_of_birth'])
            chess_id = data['chess_id']
            return separator.join([software_id, last_name, first_name,
                                   birth_date, chess_id])

    @staticmethod
    def get_header_index(header_string):
        """
        Calculates the index positions of each column in the header string.
        """
        parts = header_string.split("│")
        idx_id = 0
        idx_last_name = 2 + len(parts[0])
        idx_first_name = 1 + idx_last_name + len(parts[1])
        idx_date = 1 + idx_first_name + len(parts[2])
        idx_chess = 1 + idx_date + len(parts[3])
        return idx_id, idx_last_name, idx_first_name, idx_date, idx_chess
