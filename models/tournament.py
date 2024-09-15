from models.base_model import _BaseModel
from models.round import Round
from models.pairing import Pairing
from models.player import Player
from typing import Dict


class Tournament(_BaseModel):
    def __init__(self,
                 name: str,
                 place: str,
                 date_start: str,
                 date_end: str,
                 description: str = "",
                 rounds_number: int = 4,
                 save_to_db: bool = True):
        """
        Initialize a new Tournament instance
        :param name:
        :param place:
        :param date_start: YYYY-MM-DD
        :param date_end: YYYY-MM-DD
        :param description:
        :param rounds_number: rounds_number should not be greater than <number_of_players - 1>
        :param save_to_db: if true, save the instance in the database
        """
        super().__init__()
        self.name = name
        self.place = place
        self.date_start = date_start
        self.date_end = date_end
        self.description = description
        self.participants = {}
        self.rounds_number = rounds_number
        self.rounds = self.initialize_rounds_dict()
        self.pairing = None
        self._first_pairing_memory = None
        if save_to_db:
            self.save_to_database()

    def instantanciate_players(self, dict_participants: Dict[str, float]):
        """
        Dictionary comphrension to instanciate Players from their corresponding ID
        :param dict_participants:
        {
                "p_1": 4,
                "p_2": 3,
        }
        :return: {
                "p_1": (<Obj.player>, 4),
                "p_2": (<Obj.player>, 3),
            }
        """
        return {participant_id: (Player.from_json(participant_id), score)
                for participant_id, score in dict_participants.items()
                }

    @classmethod
    def _create_instance_from_json(cls,
                                   item_data: dict[str, object],
                                   tournament_id: str,
                                   save_to_db: bool = False):
        """
        Create a tournament object from a json dictionary
        Instantiate Players from their corresponding id found in the database
        Instantiate Rounds from their corresponding id found in the database
        Instantiate Pairing from the "first_pairing" found in database and Rounds founds in self.rounds
        :param item_data: The dictionary extracted from the tournament.json
        :param tournament_id:
        :param save_to_db: must be false to avoid copy of tournament instance in database
        """
        instance = cls(name=item_data["name"],
                       place=item_data["place"],
                       date_start=item_data["date_start"],
                       date_end=item_data["date_end"],
                       description=item_data["description"],
                       rounds_number=item_data["rounds_number"],
                       save_to_db=False)
        instance.software_id = tournament_id
        instance._first_pairing_memory = item_data["first_pairing"]

        # dict comprehension to create instances of Players and score
        instance.participants = instance.instantanciate_players(item_data["participants"])

        # if value stored in "Round_x": value isn't null, then it will instantiate the Round with the corresponding ID
        round_exist = False
        instance.rounds = {}
        round_name_list = []
        for round_name, round_id in item_data["rounds"].items():
            if round_id:
                instance.rounds[round_name] = Round.from_json(round_id)
                round_exist = True
                round_name_list.append(round_name)
            else:
                instance.rounds[round_name] = None
        sorted(round_name_list)

        # if at least, one round has already been created, then instantiate the corresponding Pairing
        if round_exist:
            list_played_matches = []
            for round in instance.rounds.values():
                if round:
                    for match in round.matches:
                        player_id_list = []
                        for player_id in match.score.keys():
                            player_id_list.append(player_id)
                        sorted(player_id_list)
                        current_match = tuple(player_id_list)
                        list_played_matches.append(current_match)

            instance.pairing = Pairing.instantiate_pairing(item_data["participants"].keys(),
                                                           item_data["first_pairing"],
                                                           list_played_matches)
        return instance

    def _prepare_data_to_save(self):
        """
        Prepare data to save in the database.
        :return: dictionary with data to save in the database
        """
        # Get rid of instances of players when storing datas
        data_participants = {}
        for participant_id, participant in self.participants.items():
            data_participants[participant_id] = participant[1]
        data_rounds = {}

        # Get rid of instances of rounds when storing datas
        for round_name, round_id in self.rounds.items():
            if round_id:
                data_rounds[round_name] = round_id.software_id
            else:
                data_rounds[round_name] = None
        data = {
            "name": self.name,
            "place": self.place,
            "date_start": self.date_start,
            "date_end": self.date_end,
            "description": self.description,
            "participants": data_participants,
            "rounds_number": self.rounds_number,
            "rounds": data_rounds,

            # Keep a memory of the first round pairing to allow instantiation of the same circle configuration when
            # reloading
            "first_pairing": self._first_pairing_memory
        }
        return data

    def initialize_rounds_dict(self) -> Dict[str, None]:
        """
        Initialize the rounds dictionary with keys 'Round_1', 'Round_2'
        :return: a dictionary
        """
        rounds = {}
        for i in range(self.rounds_number):
            rounds[f"Round_{i+1}"] = None
        return rounds

    def add_participant(self, player_id: str):
        """
        Add a participant to the tournament and set his/her score to 0
        """
        if player_id not in self.participants.keys():
            self.participants[player_id] = (Player.from_json(player_id), 0)
            self.save_to_database()
        else:
            print(f"Player : {repr(player_software_id)} is already registered")

    def initialize_first_round(self):
        """
        Initialize the first round of the tournament by generating pairings and creating rounds and matches.
        """
        self.pairing = Pairing(sorted(self.participants.keys()))
        # save the first configuration to allow recreation a the same configuration circle in Pairing.
        self._first_pairing_memory = self.pairing.initial_configuration
        self.pairing.generate_circle_configurations()
        match_pairs = self.pairing.generate_first_round_configuration()
        self.rounds["Round_1"] = Round(f"Round_1", match_pairs)
        self.save_to_database()

    def end_round(self, round_key: str):
        """
        End a round and update participants' scores.
        :param round_key: ex : 'Round_1'; it can also be called with method self.check_current_round()
        """
        current_round = self.check_current_round()
        if round_key == current_round and self.rounds[round_key] != None:
            self.rounds[round_key].end_round()
            for match in self.rounds[round_key].matches:
                for player_id, value in match.score.items():
                    self.participants[player_id] = (self.participants[player_id][0], self.participants[player_id][1] + value)
            self.save_to_database()

    def check_current_round(self):
        """
        Check and return the current round of the tournament.
        :return: ex : 'Round_2'
        """
        list_of_round = []
        for key, round in self.rounds.items():
            if round:
                list_of_round.append(key)
        if list_of_round:
            sorted(list_of_round)
            for key in list_of_round:
                if not self.rounds[key].is_finished:
                    return key
            new_round_number = int(list_of_round[-1].split("_")[-1]) + 1
            return f"Round_{new_round_number}"

    def start_next_round(self):
        """
        Start the next round of the tournament by generating pairings based on the current ranking.
        From a dictionary where key=rank from 1 to n and value=[list_of_players_id] and the past matches it will
        create the next matches to satisfy two conditions:
            1 - Try to match the players with the highest scores on against the others.
            2 - Avoid the repetition of a past match.
        """
        current_round = self.check_current_round()
        if self.rounds[current_round] is not None:
            print(f"current round : {current_round} is not finished.")
            return

        ranking = self.get_ranking()
        next_pairing = self.pairing.generate_next_round_from_ranking(ranking)
        self.rounds[current_round] = Round(name=current_round, matches_pairs=next_pairing)
        self.save_to_database()

    def get_ranking(self):
        """
        Compute and return the current ranking of participants.
        :return: a dictionary where key=rank from 1 to n and value=[list_of_players_id]
        """
        scores = [score for player, score in self.participants.values()]
        sorted_scores = sorted(set(scores), reverse=True)
        score_to_rank = {score: str(rank + 1) for rank, score in enumerate(sorted_scores)}
        output = {}
        for key, value in self.participants.items():
            rank = score_to_rank[value[1]]
            output.setdefault(rank, []).append(key)
        return output

    def __repr__(self):
        return (f"Information sur le tournoi :\n"
                f"Nom du tournoi : '{self.name}'\n"
                f"Lieu du tournoi : '{self.place}'\n"
                f"Début du tournoi : '{self.date_start}'\n"
                f"Fin du tournoi : '{self.date_end}'\n"
                f"Description du tournoi : '{self.description}'\n"
                f"Nombre de rounds : '{self.rounds_number}'\n"
                f"Classement : {self.get_ranking()}\n"
                f"Liste des participants : {self.participants}\n"
                f"Liste des rounds : {self.rounds}\n")


def main():
    tournament_2 = Tournament.from_json('t_1')
    print(repr(tournament_2))



if __name__ == "__main__":
    main()
