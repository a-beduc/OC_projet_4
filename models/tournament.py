
class Tournament:
    def __init__(self, information, list_of_players, round_numer=4):
        self.name = information["name"]
        self.place = information["place"]
        self.date_start = information["date_start"]
        self.date_end = information["date_end"]
        self.round_number = round_numer
        self.current_round = 0
        self.list_of_players = list_of_players
        self.description = information["description"]

        self.current_score = {}
        self.initialise_score()

    def initialise_score(self):
        for player in self.list_of_players:
            self.current_score[repr(player)] = 0

    def __repr__(self):
        players_repr = ', '.join([repr(player) for player in self.list_of_players])
        return (f"Information sur le tournoi :\n"
                f"Nom du tournoi : '{self.name}'\n"
                f"Lieu du tournoi : '{self.place}'\n"
                f"Début du tournoi : '{self.date_start}'\n"
                f"Fin du tournoi : '{self.date_end}'\n"
                f"Description du tournoi : '{self.description}'\n"
                f"Liste des participants : {players_repr}")


def main():
    tournament = Tournament()
    print(tournament.round_number)


if __name__ == "__main__":
    main()
