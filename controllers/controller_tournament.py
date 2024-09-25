from models.tournament import Tournament
from models.player import Player
from views.view_tournament import ViewTournament


class ControllerTournament:

    def __init__(self, stdscr, software_id):
        self.stdscr = stdscr
        self.tournament = Tournament.from_json(software_id)
        self.view_tournament = ViewTournament(stdscr)
        self.name_score = self.sort_key(self.reformat_name_score(), ['score'])

    def start(self):
        self.view_tournament.initialize(self.name_score)
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

    def reformat_name_score(self):
        return [{'last_name': players.last_name, 'first_name': players.first_name, 'score': score}
                for (players, score) in self.tournament.participants.values()]

    @staticmethod
    def sort_key(list_of_dict, sort_fields, reverse=True):
        return sorted(list_of_dict, key=lambda x: tuple([x[field] for field in sort_fields]), reverse=reverse)
