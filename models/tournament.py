class Tournament:
    def __init__(self, name, place, date_start, date_end, description="", round_number=4):
        self.name = name
        self.place = place
        self.date_start = date_start
        self.date_end = date_end
        self.round_number = round_number
        self.description = description

        self.rounds = {}
        self.tournament_participants = {}

    def add_tournament_participant(self, player):
        if player.software_id not in self.tournament_participants.keys():
            self.tournament_participants[player.software_id] = (player, 0)
        else:
            print(f"Player : {repr(player)} is already registered")

    def remove_tournament_participant(self, player):
        if player.software_id in self.tournament_participants.keys():
            self.tournament_participants.pop(player.software_id)
        else:
            print(f"Player : {repr(player)} is not registered")

    def modify_tournament_participant_score(self, player, score):
        """
        Method to manually modify the score of a participant if there has been a mistake when result was added
        :param player: Player
        :param score: new score
        """
        if player.software_id in self.tournament_participants.keys():
            self.tournament_participants[player.software_id] = (player, score)
        else:
            print(f"Player : {repr(player)} is not registered")

    def add_round(self, round_name):
        if round_name not in self.rounds.keys():
            self.rounds[round_name.name] = round_name
        else:
            raise ValueError(f"Round name {round_name} already registered")

    def __repr__(self):
        players_repr = ', '.join([f"{player.last_name} {player.first_name}"
                                  for player, _
                                  in self.tournament_participants.values()])
        return (f"Information sur le tournoi :\n"
                f"Nom du tournoi : '{self.name}'\n"
                f"Lieu du tournoi : '{self.place}'\n"
                f"Début du tournoi : '{self.date_start}'\n"
                f"Fin du tournoi : '{self.date_end}'\n"
                f"Description du tournoi : '{self.description}'\n"
                f"Liste des participants : {players_repr}")


def main():
    pass


if __name__ == "__main__":
    main()
