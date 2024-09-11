from models.base_model import _BaseModel


class Tournament(_BaseModel):
    def __init__(self, name, place, date_start, date_end, description="", rounds_number=4):
        super().__init__()
        self.name = name
        self.place = place
        self.date_start = date_start
        self.date_end = date_end
        self.description = description
        self.participants = []
        self.rounds_number = rounds_number
        self.rounds = self.initialize_rounds()
        self.save_to_database()

    @classmethod
    def _create_instance_from_json(cls, item_data, software_id):
        instance = cls(name=item_data["name"],
                       place=item_data["place"],
                       date_start=item_data["date_start"],
                       date_end=item_data["date_end"],
                       description=item_data["description"],
                       rounds_number=item_data["rounds_number"])
        instance.software_id = software_id
        instance.participants = item_data["participants"]
        instance.rounds = item_data["rounds"]
        return instance

    def _prepare_data_to_save(self):
        data = {
            "name": self.name,
            "place": self.place,
            "date_start": self.date_start,
            "date_end": self.date_end,
            "description": self.description,
            "participants": self.participants,
            "rounds_number": self.rounds_number,
            "rounds": self.rounds
        }
        return data

    def initialize_rounds(self):
        rounds = {}
        for i in range(self.rounds_number + 1):
            rounds[f"Round_{i}"] = ""
        return rounds

    def add_tournament_participant(self, player_software_id):
        if player_software_id not in self.participants:
            self.participants[player_software_id] = (player_software_id, 0)
        else:
            print(f"Player : {repr(player_software_id)} is already registered")

    def remove_tournament_participant(self, player_software_id):
        if player_software_id in self.participants:
            self.participants.pop(player_software_id)
        else:
            print(f"Player with ID:{player_software_id} is not registered \n"
                  f"check list of participants ID: {self.participants}")

    def update_round(self, round_key, round_software_id):
        if round_software_id not in self.rounds.values():
            self.rounds[round_key] = round_software_id
        else:
            raise ValueError(f"Round with ID {round_software_id} is already registered")

    def __repr__(self):
        return (f"Information sur le tournoi :\n"
                f"Nom du tournoi : '{self.name}'\n"
                f"Lieu du tournoi : '{self.place}'\n"
                f"Début du tournoi : '{self.date_start}'\n"
                f"Fin du tournoi : '{self.date_end}'\n"
                f"Description du tournoi : '{self.description}'\n"
                f"Nombre de rounds : '{self.rounds_number}'\n"
                f"Liste des participants : {self.participants}\n"
                f"Liste des rounds : {self.rounds}\n")


def main():
    tournament = Tournament.from_json("t_1")
    print(tournament)
    tournament_2 = Tournament(name="Tournoi de test",
                              place="Test-land",
                              date_start="2020-02-01",
                              date_end="2020-02-02",
                              description="Test description",
                              rounds_number=4)
    tournament_2.participants = ['p_1', 'p_3', 'p_4', 'p_5']
    tournament_2.rounds = {'round_1': 'r_5',
                           'round_2': 'r_6',
                           'round_3': 'r_7',
                           'round_4': 'r_8'
                        }
    tournament_2.save_to_database()


if __name__ == "__main__":
    main()
