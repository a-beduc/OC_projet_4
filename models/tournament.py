from models.base_model import _BaseModel
from models.round import Round
from models.pairing import Pairing
from models.player import Player
from typing import Optional, Dict


class Tournament(_BaseModel):
    def __init__(self,
                 name: str,
                 place: str,
                 date_start: str,
                 date_end: str,
                 description: str = "",
                 rounds_number: int = 4,
                 complete: bool = False,
                 save_to_db: bool = True):
        """
        Initialize a new Tournament instance
        :param name:
        :param place:
        :param date_start: YYYY-MM-DD
        :param date_end: YYYY-MM-DD
        :param description:
        :param rounds_number: rounds_number should not be greater than
        <number_of_players - 1>
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
        self.rounds = {}
        self.initialize_rounds_dict()
        self.pairing = None
        self._first_pairing_memory = None
        self.complete = complete
        if save_to_db:
            self.save_to_database()

    @staticmethod
    def _instantiate_players(dict_participants: Dict[str, float]):
        """
        Dictionary comprehension to instantiate Players from their
        corresponding ID
        :param dict_participants: {"p_1": 4, "p_2": 3}
        :return: {"p_1": (<Obj.player>, 4), "p_2": (<Obj.player>, 3)}
        """
        return {participant_id: (Player.from_json(participant_id), score)
                for participant_id, score in dict_participants.items()}

    @classmethod
    def _initialize_instance(cls, item_data: dict[str, object],
                             tournament_id: str):
        """
        Initialize a Tournament instance from the data extracted from a JSON
        file.
        :param item_data: Dictionary containing the data from the JSON
        file.
        :param tournament_id: Unique ID of the tournament. :return: An
        instance of Tournament initialized with the provided data.
        """
        instance = cls(name=item_data["name"],
                       place=item_data["place"],
                       date_start=item_data["date_start"],
                       date_end=item_data["date_end"],
                       description=item_data["description"],
                       rounds_number=item_data["rounds_number"],
                       complete=item_data["complete"],
                       save_to_db=False)
        instance.software_id = tournament_id
        instance._first_pairing_memory = item_data["first_pairing"]
        return instance

    @staticmethod
    def _instantiate_rounds(rounds_data: dict[str, Optional[str]]):
        """
        Create instances of Round objects from the provided data.
        :param rounds_data: {"Round_1" : "r_5", "Round_2" : "r_10"}
        :return: ({"Round_1" : <Obj.Round>, "Round_2" : <Obj.Round>}, Boolean)
        """
        rounds = {}
        round_exist = False
        round_name_list = []
        for round_name, round_id in rounds_data.items():
            if round_id:
                rounds[round_name] = Round.from_json(round_id)
                round_exist = True
                round_name_list.append(round_name)
            else:
                rounds[round_name] = None
        return rounds, round_exist

    def _instantiate_pairing(self, item_data):
        """
        Instantiate the Pairing object based on the participants and
        previous match data. This method uses the participants and the
        matches that have already been played to instantiate a pairing
        object.
        :param item_data: Dictionary containing the data from the
        JSON file. :return: <Obj.Pairing> initialized with the provided data
        """
        list_played_matches = []
        for round_item in self.rounds.values():
            if round_item:
                list_played_matches.extend([tuple(sorted(match.score.keys()))
                                            for match in round_item.matches])
        return Pairing.instantiate_pairing(item_data["participants"].keys(),
                                           item_data["first_pairing"],
                                           list_played_matches)

    @classmethod
    def _create_instance_from_json(cls,
                                   item_data: dict[str, object],
                                   tournament_id: str,
                                   save_to_db: bool = False):
        """
        Create a tournament object from a json dictionary
        Instantiate Players from their corresponding id found in the database
        Instantiate Rounds from their corresponding id found in the database
        Instantiate Pairing from the "first_pairing" found in database and
        Rounds founds in self.rounds
        :param item_data: The dictionary extracted from the tournament.json
        :param tournament_id:
        :param save_to_db: must be false to avoid copy of tournament instance
        in database
        :return: An instance of Tournament initialized with the provided data.
        """
        instance = cls._initialize_instance(item_data, tournament_id)

        # dict comprehension to create instances of Players and score
        instance.participants = instance._instantiate_players(
            item_data["participants"])

        # if value stored in "Round_x": value isn't null, then it will
        # instantiate the Round with the corresponding ID
        instance.rounds, round_exist = instance._instantiate_rounds(
            item_data["rounds"])

        # if at least, one round has already been created, then instantiate
        # the corresponding Pairing
        if round_exist:
            instance.pairing = instance._instantiate_pairing(item_data)

        return instance

    def _prepare_data_to_save(self):
        """
        Prepare data to save in the database.
        :return: dictionary with data to save in the database
        """
        # Get rid of instances of players when storing datas
        data_participants = {participant_id: participant[1]
                             for participant_id, participant
                             in self.participants.items()}

        # Get rid of instances of rounds when storing datas
        data_rounds = {round_name: round_id.software_id if round_id else None
                       for round_name, round_id in self.rounds.items()}

        return {
            "name": self.name,
            "place": self.place,
            "date_start": self.date_start,
            "date_end": self.date_end,
            "description": self.description,
            "participants": data_participants,
            "rounds_number": self.rounds_number,
            "rounds": data_rounds,
            "first_pairing": self._first_pairing_memory,
            "complete": self.complete
        }

    def initialize_rounds_dict(self) -> Dict[str, None]:
        """
        Initialize the rounds dictionary with keys 'Round_1', 'Round_2'
        """
        self.rounds = {f"Round_{i+1}": None for i in range(self.rounds_number)}

    def add_participant(self, player_id: str):
        """
        Add a participant to the tournament and set his/her score to 0
        """
        try:
            if player_id not in self.participants.keys():
                self.participants[player_id] = (Player.from_json(player_id),
                                                0.0)
                self.save_to_database()
        except NameError as ne:
            raise ne

    def initialize_first_round(self):
        """
        Initialize the first round of the tournament by generating pairings
        and creating rounds and matches.
        """
        self.pairing = Pairing(sorted(self.participants.keys()))
        # save the first configuration to allow recreation the same
        # configuration circle in Pairing.
        self._first_pairing_memory = self.pairing.initial_configuration
        self.pairing.generate_circle_configurations()
        match_pairs = self.pairing.generate_first_round_configuration()
        self.rounds["Round_1"] = Round("Round_1", match_pairs)
        self.save_to_database()

    def _update_participants_scores(self, matches):
        """
        Update the participants' scores based on the results of the matches.
        :param matches: List of matches from the completed round.
        """
        for match in matches:
            for player_id, value in match.score.items():
                player, current_score = self.participants[player_id]
                self.participants[player_id] = (player, current_score + value)

    def _are_all_rounds_complete(self):
        """
        Check if all rounds are complete.
        :return: True if all rounds are finished, otherwise False.
        """
        return all(rounds is not None and rounds.is_finished for rounds
                   in self.rounds.values())

    def complete_round(self, round_key: str):
        """
        End a round and update participants' scores.
        :param round_key: ex : 'Round_1'; it can also be called with method
        self.check_current_round()
        """
        current_round = self.check_current_round()
        if round_key == current_round and self.rounds[round_key] is not None:
            try:
                self.rounds[round_key].end_round()
                self._update_participants_scores(
                    self.rounds[round_key].matches)
                if self._are_all_rounds_complete():
                    self.complete = True
                self.save_to_database()

            except ValueError as ve:
                raise ve

    def check_current_round(self):
        """
        Check and return the current round of the tournament.
        :return: ex : 'Round_2'
        """
        for key, round_item in self.rounds.items():
            if round_item and not round_item.is_finished:
                return key

        list_of_round = [key for key, round_item in self.rounds.items()
                         if round_item]
        if list_of_round:
            new_round_number = int(list_of_round[-1].split("_")[-1]) + 1
            return f"Round_{new_round_number}"

    def create_next_round(self):
        """
        Start the next round of the tournament by generating pairings based on
        the current ranking.
        From a dictionary where key=rank from 1 to n and
        value=[list_of_players_id] and the past matches it will create the
        next matches to satisfy two conditions:
            1 - Try to match the players with the highest scores on against
            the others.
            2 - Avoid the repetition of a past match.
        """
        try:
            current_round = self.check_current_round()
            if self.rounds[current_round] is not None:
                raise ValueError

            ranking = self.get_ranking()
            next_pairing = self.pairing.generate_next_round_from_ranking(
                ranking)
            self.rounds[current_round] = Round(name=current_round,
                                               matches_pairs=next_pairing)
            self.save_to_database()

        except KeyError as ke:
            raise ke

    def start_new_round(self):
        """ Methods to call when starting a round to save the time. """
        try:
            current_round = self.check_current_round()
            if self.rounds[current_round].time_start is not None:
                raise ValueError
            self.rounds[current_round].start_round()
            self.save_to_database()

        except KeyError as ke:
            raise ke

    def get_ranking(self):
        """
        Compute and return the current ranking of participants.
        :return: a dictionary where key=rank from 1 to n and
        value=[list_of_players_id]
        """
        scores = [score for player, score in self.participants.values()]
        sorted_scores = sorted(set(scores), reverse=True)
        score_to_rank = {score: str(rank + 1) for rank, score
                         in enumerate(sorted_scores)}
        output = {}
        for key, value in self.participants.items():
            rank = score_to_rank[value[1]]
            output.setdefault(rank, []).append(key)
        return output
