import curses
from curses.textpad import Textbox


class ViewTournament:
    COMMAND_NOT_STARTED = [
        '[↓][↑] Navigate',
        '[a] Add Player',
        '[p] Player Menu',
        '[b] Begin Tournament',
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
        '[r] Select Round',
        '[p] Player Menu',
        '[q] Quit'
    ]

    COMMAND_ROUND = [
        '[↓][↑] Navigate',
        '[m] Select Match',
        '[c] Complete Round',
        '[q] Quit'
    ]

    COMMAND_FINISHED_ROUND = [
        '[↓][↑] Navigate',
        '[q] Quit'
    ]

    COMMAND_MATCH = [
        '[←] Win Left',
        '[→] Win Right',
        '[d] Draw',
        '[r] Reset',
        '[Enter] Confirm',
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
            'command_not_started': self.COMMAND_NOT_STARTED,
            'command_player': self.COMMAND_PLAYERS,
            'command_tournament': self.COMMAND_TOURNAMENT,
            'command_round': self.COMMAND_ROUND,
            'command_finished_round': self.COMMAND_FINISHED_ROUND,
            'command_match': self.COMMAND_MATCH
        }

        self.outer_wind = None
        self.info_wind = None
        self.command_wind = None
        self.content_wind = None
        self.content_pad_players = None
        self.content_pad_tournament = None
        self.content_pad_round = None
        self.match_wind = None
        self.player_wind = None
        self.player_pad = None

    def draw_static_elements(self,
                             name="{{default_name}}",
                             place="{{default_place}}",
                             date_start="{{default_date_start}}",
                             date_end="{{default_date_end}}",
                             description="{{default_description}}"):
        self.outer_wind = self.create_outer_wind(name)
        self.info_wind = self.create_information_wind(name, place, date_start, date_end, description)
        self.command_wind = self.create_command_wind()
        self.content_wind = self.create_content_wind()
        self.player_wind = self.create_ranking_wind()

    def initialize_unstarted(self, list_available_players, list_participants_score):
        self.update_command_wind('command_not_started')
        self.update_ranking_pad(list_participants_score)
        self.update_content_wind_players()
        self.update_content_pad_players(list_available_players)
        self.update_ranking_pad(list_participants_score)

    def initialize_started(self, list_participants_score, list_rounds):
        self.update_command_wind()
        self.update_ranking_pad(list_participants_score)
        self.update_content_wind_tournament()
        self.update_content_pad_tournament(list_rounds)

    def create_outer_wind(self, title="{{default_title}}"):
        outer_wind = curses.newwin(self.outer_wind_height, self.outer_wind_width, 0, 1)
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

    def create_command_wind(self):
        command_wind = self.outer_wind.derwin(8, self.right_wind_width, 1, self.left_wind_width + 1)
        command_wind.clear()
        command_wind.refresh()
        return command_wind

    def create_ranking_wind(self):
        ranking_wind = self.outer_wind.derwin(self.bottom_wind_height, self.right_wind_width,
                                              9, self.left_wind_width + 1)
        ranking_wind.box()
        ranking_wind.addstr(0, 2, ' Ranking ')
        text_menu = self.reformat_name_score({'last_name': 'Last Name',
                                              'first_name': 'First Name',
                                              'score': 'Score'})
        ranking_wind.addstr(2, 2, text_menu)
        ranking_wind.refresh()
        return ranking_wind

    def create_content_wind(self):
        bottom_left_wind = self.outer_wind.derwin(self.bottom_wind_height, self.left_wind_width, 9, 1)
        bottom_left_wind.box()
        bottom_left_wind.refresh()
        return bottom_left_wind

    def create_form_wind(self, form_type):
        data_map = {
            'add_player': [' Add Player ', 'ID : '],
            'select_round': [' Select Round ', 'ID : '],
            'select_match': [' Select Match ', 'ID : ']
        }
        form_add_player_wind = self.content_wind.derwin(3, len(data_map[form_type][0]) + 6,
                                                        (self.content_wind.getmaxyx()[0] - 3) // 2,
                                                        (self.content_wind.getmaxyx()[1] - len(data_map[form_type][0])
                                                         - 6) // 2)
        form_width = form_add_player_wind.getmaxyx()[1] // 2
        form_add_player_wind.clear()
        form_add_player_wind.box()
        form_add_player_wind.addstr(0, 2, data_map[form_type][0])
        form_add_player_wind.addstr(1, form_width - len(data_map[form_type][1]), data_map[form_type][1])
        input_win = form_add_player_wind.derwin(1, 5, 1, form_width)
        form_add_player_wind.refresh()
        input_win.refresh()
        box = Textbox(input_win)
        curses.curs_set(1)
        box.edit()
        curses.curs_set(0)
        user_input = box.gather().strip()
        return user_input

    def create_match_wind(self, match_data):
        content_wind_h, content_wind_w = self.content_wind.getmaxyx()
        self.match_wind = self.content_wind.derwin(6, content_wind_w - 8,
                                              (content_wind_h - 6) // 2, 2)
        self.match_wind.clear()
        self.match_wind.box()
        self.match_wind.addstr(0, 2, f" Match n°{match_data['match_id']} ")
        target_length = self.match_wind.getmaxyx()[1] - 8
        match_string = self.reformat_name_vs_name(match_data['left'], match_data['right'], target_length)
        self.match_wind.addstr(2, 3, match_string)
        self.match_wind.addstr(3, (target_length + 8 - len(match_data['status']))//2, match_data['status'])
        self.match_wind.refresh()

    def update_command_wind(self, command_key='command_tournament'):
        self.command_wind.clear()
        self.command_wind.box()
        self.command_wind.addstr(0, 2, ' Commands ')
        for i in range(len(self.commands[command_key])):
            self.command_wind.addstr(i + 1, 2, self.commands[command_key][i])
        self.command_wind.refresh()

    def update_ranking_pad(self, list_tuple_player_score=None):
        if not list_tuple_player_score:
            new_pad_height = 1
        else:
            new_pad_height = len(list_tuple_player_score) + 1
        self.player_pad = curses.newpad(new_pad_height, self.right_wind_width - 6)

        if list_tuple_player_score:
            for idx, player_score in enumerate(list_tuple_player_score):
                line = self.reformat_name_score(player_score)
                self.player_pad.addstr(idx, 0, line)

        self.player_pad.refresh(0, 0,
                                13, self.left_wind_width + 4,
                                self.outer_wind_height - 3, self.outer_wind_width - 3)

    def update_content_wind_players(self):
        self.content_wind.clear()
        self.content_wind.box()
        self.content_wind.addstr(0, 2, ' Available players ')
        headers = self.reformat_id_player_name({'id': ' #ID',
                                                'last_name': 'Last Name',
                                                'first_name': 'First Name'})
        self.content_wind.addstr(2, 2, headers)
        self.content_wind.refresh()

    def update_content_pad_players(self, list_dict_id_player):
        pad_height = len(list_dict_id_player) + 1
        self.content_pad_players = curses.newpad(pad_height, self.left_wind_width - 6)
        if self.content_pad_tournament:
            self.content_pad_tournament.clear()
        for idx, id_player in enumerate(list_dict_id_player):
            line = self.reformat_id_player_name(id_player)
            self.content_pad_players.addstr(idx, 0, line)
        self.content_pad_players.refresh(0, 0,
                                         13, 4,
                                         self.outer_wind_height - 3, self.left_wind_width - 3)

    def update_content_wind_tournament(self):
        self.content_wind.clear()
        self.content_wind.box()
        self.content_wind.addstr(0, 2, ' Rounds ')
        headers = self.reformat_id_round_status({'id': ' #ID',
                                                 'round_name': 'Rounds',
                                                 'round_status': 'Status'})
        self.content_wind.addstr(2, 2, headers)
        self.content_wind.refresh()

    def update_content_pad_tournament(self, list_dict_rounds):
        pad_height = len(list_dict_rounds) + 1
        self.content_pad_tournament = curses.newpad(pad_height, self.left_wind_width - 6)
        self.content_pad_tournament.clear()
        for idx, id_round_status in enumerate(list_dict_rounds):
            line = self.reformat_id_round_status(id_round_status)
            self.content_pad_tournament.addstr(idx, 0, line)
        self.content_pad_tournament.refresh(0, 0,
                                            13, 4,
                                            self.outer_wind_height - 3, self.left_wind_width - 3)

    def update_content_wind_round(self, round_name):
        self.content_wind.clear()
        self.content_wind.box()
        self.content_wind.addstr(0, 2, f" {round_name} ")
        headers = self.reformat_id_match_status({'id': ' #ID',
                                                 'left': {'last_name': 'Last name', 'first_name': 'First name'},
                                                 'right': {'last_name': 'Last name', 'first_name': 'First name'},
                                                 'match_status': 'Status'})
        self.content_wind.addstr(2, 2, headers)
        self.content_wind.refresh()

    def update_content_pad_round(self, round_match_data):
        pad_height = len(round_match_data) + 1
        self.content_pad_round = curses.newpad(pad_height, self.left_wind_width - 6)
        self.content_pad_round.clear()
        for idx, match_data in enumerate(round_match_data):
            line = self.reformat_id_match_status(match_data)
            self.content_pad_round.addstr(idx, 0, line)
        self.content_pad_tournament.refresh(0, 0,
                                            13, 4,
                                            self.outer_wind_height - 3, self.left_wind_width - 3)

    @staticmethod
    def reformat_name(player_name, target_length, direction='left'):
        name = ", ".join(player_name)
        if len(name) < target_length:
            if direction == 'left':
                return name.ljust(target_length)
            elif direction == 'right':
                return name.rjust(target_length)
        else:
            return name[:target_length - 1] + "."

    @staticmethod
    def reformat_name_round(round_name, target_length):
        if len(round_name) < target_length:
            return round_name.ljust(target_length)
        else:
            return round_name[:target_length - 1] + '.'

    def reformat_name_score(self, player_name_score):
        separator = ' | '
        target_length = self.right_wind_width - 6 - len(separator) - len('Score')
        player_string = self.reformat_name([player_name_score['last_name'], player_name_score['first_name']],
                                           target_length)
        score_string = str(player_name_score['score']).ljust(len('Score'))
        return separator.join([player_string, score_string])

    def reformat_id_player_name(self, id_player_name):
        separator = ' | '
        target_length = self.left_wind_width - 6 - len(separator) - len('#000')
        player_string = self.reformat_name([id_player_name['last_name'], id_player_name['first_name']],
                                           target_length)
        id_string = str(id_player_name['id']).rjust(len('#000'))
        return separator.join([id_string, player_string])

    def reformat_id_round_status(self, id_round_status):
        separator = ' | '
        target_length = self.left_wind_width - 6 - 2 * len(separator) - len('#000') - len('not started')
        round_string = self.reformat_name_round(id_round_status['round_name'], target_length)
        id_string = str(id_round_status['id']).rjust(len('#000')) if id_round_status['id'] is not None else 'null'
        status_string = str(id_round_status['round_status']).ljust(len('not started'))
        return separator.join([id_string, round_string, status_string])

    def reformat_name_vs_name(self, player_left, player_right, target_length):
        match_string_left = self.reformat_name([player_left['last_name'], player_left['first_name']],
                                               target_length // 2, 'right')
        match_string_right = self.reformat_name([player_right['last_name'], player_right['first_name']],
                                                target_length // 2)
        return ' vs '.join([match_string_left, match_string_right])

    def reformat_id_match_status(self, id_match_status):
        separator = ' | '
        target_length = self.left_wind_width - 6 - 2 * len(separator) - len('#000') - len('pending...') - len(" vs ")
        match_string = self.reformat_name_vs_name(id_match_status['left'], id_match_status['right'], target_length)
        id_string = str(id_match_status['id']).rjust(len('#000'))
        status_string = str(id_match_status['match_status']).ljust(len('pending...'))
        return separator.join([id_string, match_string, status_string])

    def start_new_view(self, memory_key=None):
        pad_start_line = 0
        while True:
            self.content_pad_players.refresh(pad_start_line, 0,
                                             13, 4,
                                             self.outer_wind_height - 3, self.left_wind_width - 3)
            if memory_key is not None:
                key = memory_key
                memory_key = None
            else:
                key = self.outer_wind.getch()
            if key in [81, 113]:  # 'Q' or 'q'
                return 'EXIT'
            elif key == curses.KEY_DOWN:
                if pad_start_line < self.content_pad_players.getmaxyx()[0] - (self.bottom_wind_height - 5):
                    pad_start_line += 1
            elif key == curses.KEY_UP:
                if pad_start_line > 0:
                    pad_start_line -= 1
            elif key in [65, 97]:  # 'A' or 'a'
                action = self.create_form_wind('add_player')
                if action is not None or '':
                    return 'ADD_PLAYER', action
            elif key in [66, 98]:  # 'B' or 'b'
                return 'START_TOURNAMENT'
            elif key in [80, 112]:  # 'P' or 'p'
                action = self.start_ranking_menu()
                self.player_wind.addstr(0, 2, ' Player ')
                self.player_wind.refresh()
                self.update_command_wind('command_not_started')
                if action is not None:
                    return action

    def start_view(self):
        pad_start_line = 0
        while True:
            self.update_command_wind('command_tournament')
            self.update_content_wind_tournament()
            self.content_pad_tournament.refresh(pad_start_line, 0,
                                                13, 4,
                                                self.outer_wind_height - 3, self.left_wind_width - 3)
            key = self.outer_wind.getch()

            if key in [81, 113]:  # 'Q' or 'q'
                return 'EXIT'
            elif key == curses.KEY_DOWN:
                if pad_start_line < self.content_pad_tournament.getmaxyx()[0] - (self.bottom_wind_height - 5):
                    pad_start_line += 1
            elif key == curses.KEY_UP:
                if pad_start_line > 0:
                    pad_start_line -= 1
            elif key in [80, 112]:  # 'P' or 'p'
                action = self.start_ranking_menu()
                self.player_wind.addstr(0, 2, ' Player ')
                self.player_wind.refresh()
                self.update_command_wind()
                if action is not None:
                    return action
            elif key in [82, 114]:  # 'R' or 'r'
                action = self.create_form_wind('select_round')
                if action:
                    return 'SELECT_ROUND', action

    def start_ranking_menu(self):
        self.player_wind.addstr(0, 2, ' Player ', curses.A_REVERSE)
        self.player_wind.refresh()
        self.update_command_wind('command_player')
        pad_start_line = 0
        while True:
            self.player_pad.refresh(pad_start_line, 0,
                                    13, self.left_wind_width + 4,
                                    self.outer_wind_height - 3, self.outer_wind_width - 3)
            key = self.outer_wind.getch()
            if key == curses.KEY_DOWN:
                if pad_start_line < self.player_pad.getmaxyx()[0] - (self.bottom_wind_height - 5):
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

    def start_round_view(self, round_data, is_finished=False):
        pad_start_line = 0
        while True:
            self.update_content_pad_round(round_data['matches'])
            self.update_content_wind_round(round_data['round_name'])
            if not is_finished:
                self.update_command_wind('command_round')
            else:
                self.update_command_wind('command_finished_round')
            self.content_pad_round.refresh(pad_start_line, 0,
                                           13, 4,
                                           self.outer_wind_height - 3, self.left_wind_width - 3)
            key = self.outer_wind.getch()
            if key in [81, 113]:  # 'Q' or 'q'
                return 'EXIT'
            elif key == curses.KEY_DOWN:
                if pad_start_line < self.content_pad_round.getmaxyx()[0] - (self.bottom_wind_height - 5):
                    pad_start_line += 1
            elif key == curses.KEY_UP:
                if pad_start_line > 0:
                    pad_start_line -= 1
            elif key in [77, 109] and not is_finished:  # 'M' or 'm'
                action = self.create_form_wind('select_match')
                if action is not None and action != '':
                    return 'SELECT_MATCH', action
                self.update_content_wind_round(round_data['round_name'])
            elif key in [67, 99] and not is_finished:  # 'C' or 'c'
                return 'ROUND_COMPLETE'

    def start_match_view(self, match_data):
        display_answer = [
            'Win left  ',
            'Win right  ',
            'Draw      ',
            'Pending...'
        ]
        result = None
        self.create_match_wind(match_data)
        self.update_command_wind('command_match')
        target_length = self.match_wind.getmaxyx()[1]
        while True:
            self.match_wind.refresh()
            key = self.outer_wind.getch()
            if key in [81, 113]:    # 'Q' or 'q'
                return 'EXIT'
            elif key == curses.KEY_LEFT:
                result = 'MATCH_RESULT', 'WIN_LEFT'
                self.match_wind.addstr(3, (target_length - len(display_answer[0]))//2, display_answer[0])
            elif key == curses.KEY_RIGHT:
                result = 'MATCH_RESULT', 'WIN_RIGHT'
                self.match_wind.addstr(3, (target_length - len(display_answer[0]))//2, display_answer[1])
            elif key in [68, 100]:  # 'D' or 'd'
                result = 'MATCH_RESULT', 'DRAW'
                self.match_wind.addstr(3, (target_length - len(display_answer[0]))//2, display_answer[2])
            elif key in [82, 114]:  # 'R' or 'r'
                result = 'MATCH_RESULT', 'RESET'
                self.match_wind.addstr(3, (target_length - len(display_answer[0]))//2, display_answer[3])
            elif key in [10, 13]:  # Enter key to confirm
                return result


def main(stdscr):
    ViewTournament(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
