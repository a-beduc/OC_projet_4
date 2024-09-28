from models.tournament import Tournament
from models.player import Player
from views.view_tournament import ViewTournament


class ControllerTournament:

    def __init__(self, stdscr, software_id):
        self.stdscr = stdscr
        self.tournament = Tournament.from_json(software_id)
        self.players = Player.get_data()['players']
        self.view_tournament = ViewTournament(stdscr)
        self.name_score = self.sort_key(self.reformat_name_score(), ['score', 'last_name', 'first_name'])
        self.tournament_started = False
        self.check_if_tournament_started()

    def start(self):
        while True:
            if not self.tournament_started:
                action = self.start_new_tournament()
            else:
                action = self.start_tournament()
            if action == 'EXIT':
                return action

    def start_new_tournament(self):
        self.view_tournament.draw_static_elements(self.tournament.name,
                                                  self.tournament.place,
                                                  self.tournament.date_start,
                                                  self.tournament.date_end,
                                                  self.tournament.description)
        self.view_tournament.initialize_unstarted(self.reformat_id_name(), self.reformat_name_score())
        memory_key = None
        while True:
            if memory_key is not None:
                action = self.view_tournament.start_new_view(memory_key)
            else:
                action = self.view_tournament.start_new_view()
            memory_key = None
            if action == 'EXIT':
                return 'EXIT'
            elif 'START_TOURNAMENT' in action:
                self.tournament.initialize_first_round()
                self.tournament_started = True
                return
            elif 'ADD_PLAYER' in action:
                try:
                    int(action[1])
                except ValueError:
                    continue
                player_id = f"p_{action[1]}"
                self.tournament.add_participant(player_id)
                self.name_score = self.sort_key(self.reformat_name_score(), ['last_name', 'first_name'], False)
                self.view_tournament.update_content_pad_players(self.reformat_id_name())
                self.view_tournament.update_ranking_pad(self.name_score)
            elif 'SORT' in action:
                self.name_score = self.sort_key(self.reformat_name_score(), action[1], action[2])
                self.view_tournament.update_ranking_pad(self.name_score)
                memory_key = 80

    def start_tournament(self):
        self.view_tournament.draw_static_elements(self.tournament.name,
                                                  self.tournament.place,
                                                  self.tournament.date_start,
                                                  self.tournament.date_end,
                                                  self.tournament.description)
        self.view_tournament.initialize_started(self.name_score, self.reformat_round_status())

        while True:
            action = self.view_tournament.start_view()
            if action == 'EXIT':
                return 'EXIT'
            elif 'SORT' in action:
                self.name_score = self.sort_key(self.reformat_name_score(), action[1], action[2])
                self.view_tournament.update_ranking_pad(self.name_score)
            elif 'SELECT_ROUND' in action:
                round_id = f"r_{action[1]}"
                selected_round = self.check_round_id(round_id)
                if selected_round is None:
                    continue
                self.start_round(selected_round)

    def start_round(self, selected_round):
        round_data = self.prepare_round(selected_round)
        while True:
            action = self.view_tournament.start_round_view(round_data)
            if action == 'EXIT':
                break
            elif 'SELECT_MATCH' in action:
                match_id = f"m_{action[1]}"
                selected_match = self.check_match_id(match_id, round_data['round_key'])
                if selected_match is None:
                    continue
                self.start_match(selected_match)
            elif 'ROUND_COMPLETE' in action:
                break

    def start_match(self, selected_match):
        match_data = self.prepare_match(selected_match)
        while True:
            action = self.view_tournament.start_match_view(match_data)
            if action == 'EXIT':
                break
            elif 'MATCH_RESULT' in action:
                self.update_match_result(selected_match, action[1])
                break

# TO DO HERE TO DO HERE

    def update_match_result(self, match_obj, result):
        if result == 'WIN_LEFT':
            pass
        elif result == 'WIN_RIGHT':
            pass
        elif result == 'DRAW':
            pass
        elif result == 'RESET':
            pass

    def check_match_id(self, match_id, current_round_key):
        for match in self.tournament.rounds[current_round_key].matches:
            if match.software_id == match_id:
                return match
        return

    def check_round_id(self, round_id):
        for value in self.tournament.rounds.values():
            if value is not None and round_id == value.software_id:
                return value
        return

    def check_if_tournament_started(self):
        for rounds in self.tournament.rounds.values():
            if rounds is not None:
                self.tournament_started = True
                break

    def prepare_match(self, match_obj):
        match_id = match_obj.software_id.split('_')[1]
        player_left = Player.from_json(match_obj.players[0])
        player_right = Player.from_json(match_obj.players[1])
        status = self.reformat_match_result(match_obj.score, player_left.software_id, player_right.software_id)
        return {'match_id': match_id,
                'left': {'last_name': player_left.last_name, 'first_name': player_left.first_name},
                'right': {'last_name': player_right.last_name, 'first_name': player_right.first_name},
                'status': status}

    def prepare_round(self, round_obj):
        round_data = {'round_key': round_obj.name, 'round_name': ' '.join(round_obj.name.split('_')), 'matches': []}
        for match in round_obj.matches:
            player_left = Player.from_json(match.players[0])
            player_right = Player.from_json(match.players[1])
            status = self.reformat_match_result(match.score, player_left.software_id, player_right.software_id)
            match_data = {
                'id': match.software_id.split('_')[1],
                'left': {'last_name': player_left.last_name, 'first_name': player_left.first_name},
                'right': {'last_name': player_right.last_name, 'first_name': player_right.first_name},
                'match_status': status
            }
            round_data['matches'].append(match_data)
        return round_data

    @staticmethod
    def reformat_match_result(match_score, player_left_id, player_right_id):
        player_left_score = match_score[player_left_id]
        player_right_score = match_score[player_right_id]
        if player_left_score == 1.0:
            return 'Win left'
        elif player_right_score == 1.0:
            return 'Win right'
        elif player_left_score == 0.5:
            return 'Draw'
        elif player_left_score == 0.0 and player_right_score == 0.0:
            return 'Pending...'

    def reformat_id_name(self):
        return [{'id': key.split('_')[1], 'last_name': value['last_name'], 'first_name': value['first_name']}
                for key, value in self.players.items()
                if key not in self.tournament.participants]

    def reformat_round_status(self):
        round_list = []
        for key, value in self.tournament.rounds.items():
            round_name = ' '.join(key.split('_'))
            if value is None:
                round_id = 'null'
                status = 'not started'
            else:
                round_id = value.software_id.split('_')[1]
                if value.is_finished is True:
                    status = 'complete'
                else:
                    status = 'pending...'
            round_list.append({'id': round_id, 'round_name': round_name, 'round_status': status})
        return round_list

    def reformat_name_score(self):
        return [{'last_name': players.last_name, 'first_name': players.first_name, 'score': score}
                for (players, score) in self.tournament.participants.values()]

    @staticmethod
    def sort_key(list_of_dict, sort_fields, reverse=True):
        return sorted(list_of_dict, key=lambda x: tuple([x[field] for field in sort_fields]), reverse=reverse)
