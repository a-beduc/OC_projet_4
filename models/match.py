from models.base_model import _BaseModel
from typing import Dict


class Match(_BaseModel):
    def __init__(self,
                 player_1_software_id: str,
                 player_2_software_id: str,
                 save_to_db=True):
        """
        Initialize a new match instance
        before initialization, players are sorted with their id numbers to allows coherence in database.
        :param player_1_software_id: string "p_<number>"
        :param player_2_software_id: string "p_<number>"
        :param save_to_db: if true, save the instance in the database
        """
        super().__init__()
        # sort players ID based on the number and not the string ["p_8", "p_11"] otherwise it causes issues with Pairing
        self.players = sorted([player_1_software_id, player_2_software_id], key=lambda x: int(x.split('_')[1]))
        self.score: Dict[str, float] = {
            self.players[0]: 0.0,
            self.players[1]: 0.0
        }
        self.is_finished: bool = False
        if save_to_db:
            self.save_to_database()

    @classmethod
    def class_name_plural(cls) -> str:
        """
        This must supercharge the _Base_Model.class_name_plural because it would return "matchs"
        """
        return "matches"

    @classmethod
    def _create_instance_from_json(cls,
                                   item_data: Dict[str, object],
                                   match_id: str,
                                   save_to_db: bool = False):
        """
        Create a match object from a json dictionary.
        :param item_data: The dictionary extracted from the tournament.json
        :param match_id:
        :param save_to_db: must be false to avoid copy of match instance in database
        :return: An instance of Match
        """
        is_finished = item_data['complete']
        del item_data['complete']
        match_data = list(item_data.items())

        player_scores = {player_id: score for player_id, score in match_data}
        sorted_players = sorted(player_scores.keys(), key=lambda x: int(x.split('_')[1]))

        instance = cls(player_1_software_id=sorted_players[0],
                       player_2_software_id=sorted_players[1],
                       save_to_db=False)
        instance.software_id = match_id
        instance.score[sorted_players[0]] = player_scores[sorted_players[0]]
        instance.score[sorted_players[1]] = player_scores[sorted_players[1]]
        instance.is_finished = is_finished

        return instance

    def _prepare_data_to_save(self) -> Dict[str, object]:
        """
        Prepare data to save in the database.
        :return: dictionary with data to save in the database
        """
        data = self.score.copy()
        data["complete"] = self.is_finished
        return data

    def _update_match(self, update_is_finished: bool = True):
        self.is_finished = update_is_finished
        self.save_to_database()

    def id_win(self,
               player_software_id: str):
        """
        Save a player victory based on his/her software_id and block any further modifications of the result
        :param player_software_id:
        :return: If the match result has already been decided, return a message without stopping the application.
        """
        if not self.is_finished:
            if player_software_id in self.score:
                self.score[player_software_id] = 1.0
                self._update_match()
            else:
                raise ValueError

    def draw(self):
        """
        Save a draw between players based on his/her software_id and block any further modifications of the result
        :return: If the match result has already been decided, return a message without stopping the application.
        """
        if not self.is_finished:
            self.score = {player_software_id: 0.5 for player_software_id in self.players}
            self._update_match()

    def reset_match_result(self):
        """
        Method that will reinitialize the result of a match, if an error has been made
        :return:
        """
        if self.is_finished:
            self.score = {player_software_id: 0.0 for player_software_id in self.players}
            self._update_match(update_is_finished=False)
