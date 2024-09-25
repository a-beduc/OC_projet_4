import curses


class ViewTournament:
    COMMAND_BASE = [
        '[t] Tournament Menu',
        '[p] Player Menu',
        '[q] Quit'
    ]

    COMMAND_PLAYERS = [
        '[↓][↑] Navigate',
        '[p] Sort Name',
        '[s] Sort Score',
        '[q] Back to Menu'
    ]

    COMMAND_TOURNAMENT = [
        '[↓][↑] Navigate',
        '[Enter] Select',
        '[q] Back to Menu'
    ]

    COMMAND_ROUND = [
        '[↓][↑] Navigate',
        '[Enter] Select',
        '[q] Back to Tournament'
    ]

    COMMAND_MATCH = [
        '[←] Win Left',
        '[→] Win Right',
        '[=] Draw',
        '[r] Reset',
        '[q] Quit'
    ]

    SORT_FIELDS = [
        ['last_name', 'first_name', 'score'],
        ['score', 'last_name', 'first_name']
    ]

    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.outer_wind_height, self.outer_wind_width = stdscr.getmaxyx()[0], stdscr.getmaxyx()[1] - 2
        self.left_wind_width = (self.outer_wind_width - 3) * 2 // 3
        self.right_wind_width = self.outer_wind_width - self.left_wind_width - 2
        self.bottom_wind_height = self.outer_wind_height - 10
        self.commands = {
            'command_base': self.COMMAND_BASE,
            'command_player': self.COMMAND_PLAYERS,
            'command_tournament': self.COMMAND_TOURNAMENT,
            'command_round': self.COMMAND_ROUND,
            'command_match': self.COMMAND_MATCH
        }

        self.players = None
        self.outer_wind = None
        self.info_wind = None
        self.command_wind = None
        self.tournament_wind = None
        self.player_wind = None
        self.player_pad = None

    def initialize(self, name_score):
        self.players = name_score
        self.outer_wind = self.create_outer_wind()
        self.info_wind = self.create_information_wind()
        self.command_wind = self.create_command_wind()
        self.tournament_wind = self.create_tournament_wind()
        self.player_wind = self.create_player_wind()
        self.player_pad = self.create_player_pad()
        self.update_player_pad(self.players)

    def create_outer_wind(self, title="{{default_title}}"):
        outer_wind = curses.newwin(self.outer_wind_height, self.outer_wind_width, 0, 0)
        outer_wind.box()
        box_title = f" {title} "
        outer_wind.addstr(0, (self.outer_wind_width - len(box_title)) // 2, box_title)
        outer_wind.keypad(True)
        outer_wind.refresh()
        return outer_wind

    def create_information_wind(self,
                                name="{{default_name}}",
                                place="{{default_place}}",
                                date_start="{{default_date_start}}",
                                date_end="{{default_date_end}}",
                                description="{{default_description}}"):
        info_wind = self.outer_wind.derwin(8, self.left_wind_width, 1, 1)
        info_wind.box()
        info_wind.addstr(0, 2, ' Information ')
        info_wind.addstr(1, 2, f"Name : {name}")
        info_wind.addstr(2, 2, f"Place : {place} ")
        info_wind.addstr(3, 2, f"Date Start : {date_start}")
        info_wind.addstr(4, 2, f"Date End : {date_end}")
        line_1 = f"Description : {description}"
        line_2 = ""
        if len(line_1) > self.left_wind_width:
            line_2 = line_1[self.left_wind_width - 4:]
            line_1 = line_1[:self.left_wind_width - 4]
        if len(line_2) > self.left_wind_width:
            line_2 = line_2[:self.left_wind_width - 7] + "..."
        info_wind.addstr(5, 2, line_1)
        info_wind.addstr(6, 2, line_2)
        info_wind.refresh()
        return info_wind

    def create_command_wind(self, command_key='command_base'):
        command_wind = self.outer_wind.derwin(8, self.right_wind_width, 1, self.left_wind_width + 1)
        command_wind.clear()
        command_wind.box()
        command_wind.addstr(0, 2, ' Commands ')
        for i in range(len(self.commands[command_key])):
            command_wind.addstr(i + 1, 2, self.commands[command_key][i])
        command_wind.refresh()
        return command_wind

    def create_tournament_wind(self):
        bottom_left_wind = self.outer_wind.derwin(self.bottom_wind_height, self.left_wind_width, 9, 1)
        bottom_left_wind.box()
        bottom_left_wind.addstr(0, 2, ' Tournament ')
        bottom_left_wind.refresh()
        return bottom_left_wind

    @staticmethod
    def reformat_name(player_name, target_length):
        name = ", ".join(player_name)
        if len(name) < target_length:
            player_string = name.ljust(target_length)
        else:
            player_string = name[:target_length - 1] + "."
        return player_string

    def reformat_name_score(self, player_name_score):
        separator = ' | '
        target_length = self.right_wind_width - 6 - len(separator) - len('Score')
        player_string = self.reformat_name([player_name_score['last_name'], player_name_score['first_name']],
                                           target_length)
        score_string = str(player_name_score['score']).ljust(len('Score'))
        return separator.join([player_string, score_string])

    def create_player_pad(self):
        pad_height = len(self.players) + 1
        player_pad = curses.newpad(pad_height, self.right_wind_width - 6)
        player_pad.refresh(0, 0,
                           13, self.left_wind_width + 4,
                           self.outer_wind_height - 3, self.outer_wind_width - 3)
        return player_pad

    def update_player_pad(self, list_tuple_player_score):
        for idx, player_score in enumerate(list_tuple_player_score):
            line = self.reformat_name_score(player_score)
            self.player_pad.addstr(idx, 0, line)
        self.player_pad.refresh(0, 0,
                                13, self.left_wind_width + 4,
                                self.outer_wind_height - 3, self.outer_wind_width - 3)

    def create_player_wind(self):
        player_wind = self.outer_wind.derwin(self.bottom_wind_height, self.right_wind_width,
                                             9, self.left_wind_width + 1)
        player_wind.box()
        player_wind.addstr(0, 2, ' Player ')
        text_menu = self.reformat_name_score({'last_name': 'Last Name',
                                              'first_name': 'First Name',
                                              'score': 'Score'})
        player_wind.addstr(2, 3, text_menu)
        player_wind.refresh()
        return player_wind

    def start_view(self, memory_key=None):
        running = True
        while running:
            if memory_key is not None:
                key = memory_key
                memory_key = None
            else:
                key = self.outer_wind.getch()
            if key in [84, 116]:  # 'T'  or 't'
                self.tournament_wind.addstr(0, 2, ' Tournament ', curses.A_REVERSE)
                self.tournament_wind.refresh()
                self.command_wind = self.create_command_wind('command_tournament')
                self.outer_wind.getch()
                self.tournament_wind.addstr(0, 2, ' Tournament ')
                self.tournament_wind.refresh()
                self.command_wind = self.create_command_wind()
            elif key in [80, 112]:  # 'P' or 'p'
                self.player_wind.addstr(0, 2, ' Player ', curses.A_REVERSE)
                self.player_wind.refresh()
                self.command_wind = self.create_command_wind('command_player')
                action = self.start_player_menu()
                self.player_wind.addstr(0, 2, ' Player ')
                self.player_wind.refresh()
                self.command_wind = self.create_command_wind()
                if action is not None:
                    return action
            elif key in [81, 113]:  # 'Q' or 'q'
                return 'EXIT'

    def start_player_menu(self):
        pad_start_line = 0
        while True:
            self.player_pad.refresh(pad_start_line, 0,
                                    13, self.left_wind_width + 4,
                                    self.outer_wind_height - 3, self.outer_wind_width - 3)
            key = self.outer_wind.getch()
            if key == curses.KEY_DOWN:
                if pad_start_line < len(self.players) - (self.bottom_wind_height - 5):
                    pad_start_line += 1
            elif key == curses.KEY_UP:
                if pad_start_line > 0:
                    pad_start_line -= 1
            elif key in [81, 113]:  # 'Q' or 'q'
                return
            elif key in [83, 115]:  # 'S' or 's'
                return 'SORT', self.SORT_FIELDS[1], True
            elif key in [80, 112]:  # 'P' or 'p'
                return 'SORT', self.SORT_FIELDS[0], False

    @staticmethod
    def get_header_index(header_string):
        parts = header_string.split('|')
        idx_name = 0
        idx_score = 2 + len(parts[0])
        return idx_name, idx_score

    def start_sort_menu(self):
        current_line_index = 0
        header_string = self.reformat_name_score(('Last Name', 'First Name', 'Score'))
        indexes_values = self.get_header_index(header_string)
        strings_menu = header_string.split(' | ')
        indexes = {i: (indexes_values[i], strings_menu[i]) for i in range(len(indexes_values))}

        running = True

        while running:
            self.player_wind.addstr(2, 3, header_string)
            self.player_wind.addstr(2, 3 + indexes[current_line_index][0], indexes[current_line_index][1],
                                    curses.A_REVERSE)
            self.player_wind.refresh()

            key = self.player_wind.getch()
            if key == curses.KEY_RIGHT:
                current_line_index = (current_line_index + 1) % len(indexes)
            elif key == curses.KEY_LEFT:
                current_line_index = (current_line_index - 1) % len(indexes)
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if current_line_index == 0:
                    return 'SORT', 'NAME'
                elif current_line_index == 1:
                    return 'SORT', 'SCORE'


def main(stdscr):
    ViewTournament(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
