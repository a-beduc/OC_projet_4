import curses
from curses.textpad import Textbox


class ViewTournament:
    """ A class for displaying and managing the views of a tournament. """

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
        '[p] Player Menu',
        '[q] Quit'
    ]

    COMMAND_FINISHED_ROUND = [
        '[↓][↑] Navigate',
        '[p] Player Menu',
        '[q] Quit'
    ]

    COMMAND_MATCH = [
        '[←] Win Left',
        '[→] Win Right',
        '[d] Draw',
        '[q] Quit'
    ]

    SORT_FIELDS = [
        ['last_name', 'first_name', 'score'],
        ['score', 'last_name', 'first_name']
    ]

    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)

        # some dimensions based on the dimension of the terminal used for drawing windows and pads
        self.outer_wind_height, self.outer_wind_width = stdscr.getmaxyx()[0], stdscr.getmaxyx()[1] - 2
        self.left_wind_width = (self.outer_wind_width - 3) * 2 // 3
        self.right_wind_width = self.outer_wind_width - self.left_wind_width - 2
        self.bottom_wind_height = self.outer_wind_height - 10

        # curses windows and pads used for modifying parts of the terminal
        self.outer_wind = None
        self.info_wind = None
        self.command_wind = None
        self.content_wind = None
        self.match_wind = None
        self.ranking_wind = None
        self.content_pad_players = None
        self.content_pad_tournament = None
        self.content_pad_round = None
        self.ranking_pad = None
        self.current_pad = None

        self.pad_start_line = 0
        self.commands = {
            'command_not_started': self.COMMAND_NOT_STARTED,
            'command_player': self.COMMAND_PLAYERS,
            'command_tournament': self.COMMAND_TOURNAMENT,
            'command_round': self.COMMAND_ROUND,
            'command_finished_round': self.COMMAND_FINISHED_ROUND,
            'command_match': self.COMMAND_MATCH
        }

        # dictionary used to map user input to methods
        self.key_action = {
            'move_down': self.move_pad_down,
            'move_up': self.move_pad_up,
            'add_player': self.add_player,
            'ranking_menu': self.ranking_menu,
            'begin_tournament': self.begin_tournament,
            'quit': self.quit,
            'select_round': self.select_round,
            'sort_name': self.sort_name,
            'sort_score': self.sort_score,
            'select_match': self.select_match,
            'complete_round': self.complete_round,
            'win_left': self.win_left,
            'win_right': self.win_right,
            'draw': self.draw,
        }

    def draw_static_elements(self,
                             name="{{default_name}}",
                             place="{{default_place}}",
                             date_start="{{default_date_start}}",
                             date_end="{{default_date_end}}",
                             description="{{default_description}}"):
        """ Create the elements that will not be modified. """
        self.outer_wind = self.create_outer_wind(name)
        self.info_wind = self.create_information_wind(name, place, date_start, date_end, description)
        self.command_wind = self.create_command_wind()
        self.content_wind = self.create_content_wind()
        self.ranking_wind = self.create_ranking_wind()

    def initialize_unstarted(self, list_available_players, list_participants_score):
        """ Create and update the base view of a non-started tournament. """
        self.update_command_wind('command_not_started')
        self.update_ranking_pad(list_participants_score)
        self.update_content_wind_ranking()
        self.update_content_pad_players(list_available_players)
        self.update_ranking_pad(list_participants_score)

    def initialize_started(self, list_participants_score, list_rounds):
        """ Create and update the base view of a started tournament. """
        self.update_command_wind()
        self.update_ranking_pad(list_participants_score)
        self.update_content_wind_tournament()
        self.update_content_pad_tournament(list_rounds)

    def create_outer_wind(self, title="{{default_title}}"):
        """ Create the outer window that will be used as a parent by others windows. """
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
        """ Create and update the information window in the top left corner. """
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
        """ Create the command window in the top right corner. """
        command_wind = self.outer_wind.derwin(8, self.right_wind_width, 1, self.left_wind_width + 1)
        command_wind.clear()
        command_wind.refresh()
        return command_wind

    def create_ranking_wind(self):
        """ Create the ranking window in the bottom right corner. """
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
        """ Create the content window in the bottom left corner. """
        bottom_left_wind = self.outer_wind.derwin(self.bottom_wind_height, self.left_wind_width, 9, 1)
        bottom_left_wind.box()
        bottom_left_wind.refresh()
        return bottom_left_wind

    def create_form_wind(self, form_type):
        """ Create a temporary window to get user input """
        data_map = {
            'add_player': [' Add Player ', 'ID : '],
            'select_round': [' Select Round ', 'ID : '],
            'select_match': [' Select Match ', 'ID : ']
        }
        form_add_ranking_wind = self.content_wind.derwin(3, len(data_map[form_type][0]) + 6,
                                                         (self.content_wind.getmaxyx()[0] - 3) // 2,
                                                         (self.content_wind.getmaxyx()[1] - len(data_map[form_type][0])
                                                          - 6) // 2)
        form_width = form_add_ranking_wind.getmaxyx()[1] // 2
        form_add_ranking_wind.clear()
        form_add_ranking_wind.box()
        form_add_ranking_wind.addstr(0, 2, data_map[form_type][0])
        form_add_ranking_wind.addstr(1, form_width - len(data_map[form_type][1]), data_map[form_type][1])
        input_win = form_add_ranking_wind.derwin(1, 5, 1, form_width)
        form_add_ranking_wind.refresh()
        input_win.refresh()
        box = Textbox(input_win)
        curses.curs_set(1)
        box.edit()
        curses.curs_set(0)
        user_input = box.gather().strip()
        return user_input

    def create_match_wind(self, match_data):
        """ Create a temporary window get user input on the outcome of a match. """
        content_wind_h, content_wind_w = self.content_wind.getmaxyx()
        self.match_wind = self.content_wind.derwin(6, content_wind_w - 8,
                                                   (content_wind_h - 6) // 2, 2)
        self.match_wind.clear()
        self.match_wind.box()
        self.match_wind.addstr(0, 2, f" Match n°{match_data['match_id']} ")
        target_length = self.match_wind.getmaxyx()[1] - 8
        match_string = self.reformat_name_vs_name(match_data['left'], match_data['right'], target_length)
        self.match_wind.addstr(2, 3, match_string)
        self.match_wind.addstr(3, (target_length + 8 - len(match_data['status'])) // 2, match_data['status'])
        self.match_wind.refresh()

    def update_command_wind(self, command_key='command_tournament'):
        """ Use the mapping of commands in the attributes of the class to update command window. """
        self.command_wind.clear()
        self.command_wind.box()
        self.command_wind.addstr(0, 2, ' Commands ')
        for i in range(len(self.commands[command_key])):
            self.command_wind.addstr(i + 1, 2, self.commands[command_key][i])
        self.command_wind.refresh()

    def update_ranking_pad(self, list_tuple_player_score=None):
        """ Create a pad in the ranking window to allow the user to scroll down and up if needed. """
        if not list_tuple_player_score:
            new_pad_height = 1
        else:
            new_pad_height = len(list_tuple_player_score) + 1
        self.ranking_pad = curses.newpad(new_pad_height, self.right_wind_width - 6)

        if list_tuple_player_score:
            for idx, player_score in enumerate(list_tuple_player_score):
                line = self.reformat_name_score(player_score)
                self.ranking_pad.addstr(idx, 0, line)

        self.ranking_pad.refresh(0, 0,
                                 13, self.left_wind_width + 4,
                                 self.outer_wind_height - 3, self.outer_wind_width - 3)

    def update_content_wind_ranking(self):
        """ Add a header to the ranking window """
        self.content_wind.clear()
        self.content_wind.box()
        self.content_wind.addstr(0, 2, ' Available players ')
        headers = self.reformat_id_player_name({'id': ' #ID',
                                                'last_name': 'Last Name',
                                                'first_name': 'First Name'})
        self.content_wind.addstr(2, 2, headers)
        self.content_wind.refresh()

    def update_content_pad_players(self, list_dict_id_player):
        """ Fill the content pad with the list of players that are not already participants of the Tournament. """
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
        """ Create the headers of the content pad for the tournament view. """
        self.content_wind.clear()
        self.content_wind.box()
        self.content_wind.addstr(0, 2, ' Rounds ')
        headers = self.reformat_id_round_status({'id': ' #ID',
                                                 'round_name': 'Rounds',
                                                 'round_status': 'Status'})
        self.content_wind.addstr(2, 2, headers)
        self.content_wind.refresh()

    def update_content_pad_tournament(self, list_dict_rounds):
        """ Fill the content pad with the rounds of the tournament. """
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
        """ Create the headers of the content pad for the round view. """
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
        """ Fill the content pad with the matches of the round. """
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
        """ Utility method to clean data before display """
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
        """ Utility method to clean data before display """
        if len(round_name) < target_length:
            return round_name.ljust(target_length)
        else:
            return round_name[:target_length - 1] + '.'

    def reformat_name_score(self, player_name_score):
        """ Utility method to clean data before display """
        separator = ' | '
        target_length = self.right_wind_width - 6 - len(separator) - len('Score')
        player_string = self.reformat_name([player_name_score['last_name'], player_name_score['first_name']],
                                           target_length)
        score_string = str(player_name_score['score']).ljust(len('Score'))
        return separator.join([player_string, score_string])

    def reformat_id_player_name(self, id_player_name):
        """ Utility method to clean data before display """
        separator = ' | '
        target_length = self.left_wind_width - 6 - len(separator) - len('#000')
        player_string = self.reformat_name([id_player_name['last_name'], id_player_name['first_name']],
                                           target_length)
        id_string = str(id_player_name['id']).rjust(len('#000'))
        return separator.join([id_string, player_string])

    def reformat_id_round_status(self, id_round_status):
        """ Utility method to clean data before display """
        separator = ' | '
        target_length = self.left_wind_width - 6 - 2 * len(separator) - len('#000') - len('not started')
        round_string = self.reformat_name_round(id_round_status['round_name'], target_length)
        id_string = str(id_round_status['id']).rjust(len('#000')) if id_round_status['id'] is not None else 'null'
        status_string = str(id_round_status['round_status']).ljust(len('not started'))
        return separator.join([id_string, round_string, status_string])

    def reformat_name_vs_name(self, player_left, player_right, target_length):
        """ Utility method to clean data before display """
        match_string_left = self.reformat_name([player_left['last_name'], player_left['first_name']],
                                               target_length // 2, 'right')
        match_string_right = self.reformat_name([player_right['last_name'], player_right['first_name']],
                                                target_length // 2)
        return ' vs '.join([match_string_left, match_string_right])

    def reformat_id_match_status(self, id_match_status):
        """ Utility method to clean data before display """
        separator = ' | '
        target_length = self.left_wind_width - 6 - 2 * len(separator) - len('#000') - len('pending...') - len(" vs ")
        match_string = self.reformat_name_vs_name(id_match_status['left'], id_match_status['right'], target_length)
        id_string = str(id_match_status['id']).rjust(len('#000'))
        status_string = str(id_match_status['match_status']).ljust(len('pending...'))
        return separator.join([id_string, match_string, status_string])

    def move_pad_up(self):
        """ Method following a user input, move the pad one line up. """
        if self.pad_start_line > 0:
            self.pad_start_line -= 1

    def move_pad_down(self):
        """ Method following a user input, move the pad one line down. """
        if self.pad_start_line < self.current_pad.getmaxyx()[0] - (self.bottom_wind_height - 5):
            self.pad_start_line += 1

    def add_player(self):
        """ Method following a user input, send request to add a player to controller. """
        action = self.create_form_wind('add_player')
        if action is not None or '':
            return 'ADD_PLAYER', action

    @staticmethod
    def begin_tournament():
        """ Method following a user input, send request to begin tournament to controller. """
        return 'START_TOURNAMENT'

    @staticmethod
    def ranking_menu():
        """ Method following a user input, send request to start the ranking_menu to controller. """
        return 'RANKING'

    @staticmethod
    def quit():
        """ Method following a user input, send request to leave current menu to controller. """
        return 'EXIT'

    def sort_score(self):
        """ Method following a user input, send request to sort the ranking display based on score to controller. """
        return 'SORT', self.SORT_FIELDS[1], True

    def sort_name(self):
        """ Method following a user input, send request to sort the ranking display based on name to controller. """
        return 'SORT', self.SORT_FIELDS[0], False

    def select_round(self):
        """ Method following a user input, send request to select a specific round to controller. """
        action = self.create_form_wind('select_round')
        if action:
            return 'SELECT_ROUND', action

    def select_match(self):
        """ Method following a user input, send request to select a specific match to controller. """
        action = self.create_form_wind('select_match')
        if action is not None and action != '':
            return 'SELECT_MATCH', action

    @staticmethod
    def complete_round():
        """ Method following a user input, send request to mark current round as complete to controller. """
        return 'ROUND_COMPLETE'

    @staticmethod
    def win_left():
        """ Method following a user input, send request to update match result to controller. """
        return 'MATCH_RESULT', 'WIN_LEFT'

    @staticmethod
    def win_right():
        """ Method following a user input, send request to update match result to controller. """
        return 'MATCH_RESULT', 'WIN_RIGHT'

    @staticmethod
    def draw():
        """ Method following a user input, send request to update match result to controller. """
        return 'MATCH_RESULT', 'DRAW'

    def start_new_view(self):
        """ View displaying non-started tournament, wait for specific input to transmit to controller. """
        self.pad_start_line = 0
        self.current_pad = self.content_pad_players
        self.ranking_wind.addstr(0, 2, ' Ranking ')
        self.ranking_wind.refresh()
        self.update_command_wind('command_not_started')

        local_key_action = {
            curses.KEY_DOWN: self.key_action['move_down'],
            curses.KEY_UP: self.key_action['move_up'],
            ord('A'): self.key_action['add_player'],
            ord('a'): self.key_action['add_player'],
            ord('p'): self.key_action['ranking_menu'],
            ord('P'): self.key_action['ranking_menu'],
            ord('B'): self.key_action['begin_tournament'],
            ord('b'): self.key_action['begin_tournament'],
            ord('q'): self.key_action['quit'],
            ord('Q'): self.key_action['quit']
        }

        while True:
            self.current_pad.refresh(self.pad_start_line, 0,
                                     13, 4,
                                     self.outer_wind_height - 3, self.left_wind_width - 3)
            key = self.outer_wind.getch()
            action = local_key_action.get(key)
            if action:
                result = action()
                if result:
                    return result

    def start_tournament_view(self):
        """ View displaying started tournament, wait for specific input to transmit to controller. """
        local_key_action = {
            curses.KEY_DOWN: self.key_action['move_down'],
            curses.KEY_UP: self.key_action['move_up'],
            ord('R'): self.key_action['select_round'],
            ord('r'): self.key_action['select_round'],
            ord('P'): self.key_action['ranking_menu'],
            ord('p'): self.key_action['ranking_menu'],
            ord('Q'): self.key_action['quit'],
            ord('q'): self.key_action['quit']
        }

        self.pad_start_line = 0
        self.current_pad = self.content_pad_tournament
        self.ranking_wind.addstr(0, 2, ' Ranking ')
        self.ranking_wind.refresh()
        self.update_command_wind('command_tournament')
        self.update_content_wind_tournament()

        while True:
            self.update_content_wind_tournament()
            self.current_pad.refresh(self.pad_start_line, 0,
                                     13, 4,
                                     self.outer_wind_height - 3, self.left_wind_width - 3)
            key = self.outer_wind.getch()
            action = local_key_action.get(key)
            if action:
                result = action()
                if result:
                    return result

    def start_ranking_menu(self):
        """ View modifying ranking window, wait for specific input to transmit to controller. """
        local_key_action = {
            curses.KEY_DOWN: self.key_action['move_down'],
            curses.KEY_UP: self.key_action['move_up'],
            ord('P'): self.key_action['sort_name'],
            ord('p'): self.key_action['sort_name'],
            ord('S'): self.key_action['sort_score'],
            ord('s'): self.key_action['sort_score'],
            ord('Q'): self.key_action['quit'],
            ord('q'): self.key_action['quit']
        }

        self.pad_start_line = 0
        self.current_pad = self.ranking_pad
        self.ranking_wind.addstr(0, 2, ' Ranking ', curses.A_REVERSE)
        self.ranking_wind.refresh()
        self.update_command_wind('command_player')

        while True:
            self.current_pad.refresh(self.pad_start_line, 0,
                                     13, self.left_wind_width + 4,
                                     self.outer_wind_height - 3, self.outer_wind_width - 3)
            key = self.outer_wind.getch()
            action = local_key_action.get(key)
            if action:
                result = action()
                if result:
                    return result

    def start_round_view(self, round_data, is_finished=False):
        """ View displaying a round of a tournament, wait for specific input to transmit to controller. """
        local_key_action = {
            curses.KEY_DOWN: self.key_action['move_down'],
            curses.KEY_UP: self.key_action['move_up'],
            ord('M'): self.key_action['select_match'],
            ord('m'): self.key_action['select_match'],
            ord('C'): self.key_action['complete_round'],
            ord('c'): self.key_action['complete_round'],
            ord('P'): self.key_action['ranking_menu'],
            ord('p'): self.key_action['ranking_menu'],
            ord('Q'): self.key_action['quit'],
            ord('q'): self.key_action['quit']
        }

        self.pad_start_line = 0
        if is_finished:
            self.update_command_wind('command_finished_round')
            to_delete = (ord('M'), ord('m'), ord('C'), ord('c'))
            for key in to_delete:
                local_key_action.pop(key, None)
        else:
            self.update_command_wind('command_round')

        while True:
            self.update_content_pad_round(round_data['matches'])
            self.current_pad = self.content_pad_round
            self.update_content_wind_round(round_data['round_name'])
            self.current_pad.refresh(self.pad_start_line, 0,
                                     13, 4,
                                     self.outer_wind_height - 3, self.left_wind_width - 3)
            key = self.outer_wind.getch()
            action = local_key_action.get(key)
            if action:
                result = action()
                if result:
                    return result

    def start_match_view(self, match_data):
        """ View displaying a window of a selected match, wait for specific input to transmit to controller. """
        local_key_action = {
            curses.KEY_LEFT: self.key_action['win_left'],
            curses.KEY_RIGHT: self.key_action['win_right'],
            ord('D'): self.key_action['draw'],
            ord('d'): self.key_action['draw'],
            ord('Q'): self.key_action['quit'],
            ord('q'): self.key_action['quit']
        }

        self.create_match_wind(match_data)
        self.update_command_wind('command_match')

        while True:
            self.match_wind.refresh()
            key = self.outer_wind.getch()
            action = local_key_action.get(key)
            if action:
                result = action()
                if result:
                    return result
