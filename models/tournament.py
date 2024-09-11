import os
import json


class Tournament:
    def __init__(self, name, place, date_start, date_end, description="", rounds_number=4):

        self.software_id = self.generate_new_software_id()
        self.name = name
        self.place = place
        self.date_start = date_start
        self.date_end = date_end
        self.description = description
        self.rounds_number = rounds_number

        self.rounds = {}
        self.participants = []

    @staticmethod
    def get_path():
        base_path = os.path.dirname(__file__)
        path = os.path.join(base_path, '..', 'data', 'tournaments.json')
        return path

    @classmethod
    def get_all_tournaments(cls):
        with open(cls.get_path(), 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data

    @classmethod
    def from_json(cls, software_id):
        data = cls.get_all_tournaments()
        tournament_data = data["tournaments"][software_id]
        tournament_instance = cls(name=tournament_data["name"],
                                  place=tournament_data["place"],
                                  date_start=tournament_data["date_start"],
                                  date_end=tournament_data["date_end"],
                                  description=tournament_data["description"],
                                  rounds_number=tournament_data["rounds_number"])
        tournament_instance.software_id = software_id
        tournament_instance.participants = tournament_data["participants"]
        tournament_instance.rounds = tournament_data["rounds"]
        return tournament_instance

    @classmethod
    def generate_new_software_id(cls):
        data = cls.get_all_tournaments()
        tournaments_ids = [int(software_id.split('_'))[1] for software_id in data["tournaments"].keys()]
        if tournaments_ids:
            new_id = max(tournaments_ids) + 1
        else:
            new_id = 1

        return f"t_{new_id}"

    def save_tournament_in_database(self):
        """
        Method to add or update a tournament in the database
        :return: none
        """
        data = self.get_all_tournaments()
        data["tournaments"][self.software_id] = {}
        data["tournaments"][self.software_id]["name"] = self.name
        data["tournaments"][self.software_id]["place"] = self.place
        data["tournaments"][self.software_id]["date_start"] = self.date_start
        data["tournaments"][self.software_id]["date_end"] = self.date_end
        data["tournaments"][self.software_id]["description"] = self.description
        data["tournaments"][self.software_id]["participants"] = self.participants
        data["tournaments"][self.software_id]["rounds_number"] = self.rounds_number
        data["tournaments"][self.software_id]["rounds"] = self.rounds
        with open(self.get_path(), 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    def add_tournament_participant(self, player_software_id):
        if player_software_id not in self.participants:
            self.participants[player.software_id] = (player, 0)
        else:
            print(f"Player : {repr(player)} is already registered")

    def remove_tournament_participant(self, player):
        if player.software_id in self.participants.keys():
            self.participants.pop(player.software_id)
        else:
            print(f"Player : {repr(player)} is not registered")

    def modify_tournament_participant_score(self, player, score):
        """
        Method to manually modify the score of a participant if there has been a mistake when result was added
        :param player: Player
        :param score: new score
        """
        if player.software_id in self.participants.keys():
            self.participants[player.software_id] = (player, score)
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
                                  in self.participants.values()])
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
