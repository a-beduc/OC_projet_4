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
        if not self.tournament_started:
            action = self.start_new_tournament()
        else:
            action = self.start_tournament()
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
                pass
            elif 'ADD_PLAYER' in action:
                pass
            elif 'SORT' in action:
                self.name_score = self.sort_key(self.reformat_name_score(), action[1], action[2])
                self.view_tournament.update_player_pad(self.name_score)
                memory_key = 80

    def start_tournament(self):
        self.view_tournament.initialize_started(self.name_score)
        memory_key = None
        while True:
            if memory_key is not None:
                action = self.view_tournament.start_view(memory_key)
            else:
                action = self.view_tournament.start_view()
            memory_key = None
            if action == 'EXIT':
                return 'EXIT'
            elif 'SORT' in action:
                self.name_score = self.sort_key(self.reformat_name_score(), action[1], action[2])
                self.view_tournament.update_player_pad(self.name_score)
                memory_key = 80

    def check_if_tournament_started(self):
        for rounds in self.tournament.rounds.values():
            if rounds is not None:
                self.tournament_started = True
                break

    def reformat_id_name(self):
        return [{'id': key.split('_')[1], 'last_name': value['last_name'], 'first_name': value['first_name']}
                for key, value in self.players.items()
                if key not in self.tournament.participants]

    def reformat_name_score(self):
        return [{'last_name': players.last_name, 'first_name': players.first_name, 'score': score}
                for (players, score) in self.tournament.participants.values()]

    @staticmethod
    def sort_key(list_of_dict, sort_fields, reverse=True):
        return sorted(list_of_dict, key=lambda x: tuple([x[field] for field in sort_fields]), reverse=reverse)
