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
        players = sorted([player_1_software_id, player_2_software_id])
        self.score: Dict[str, float] = {
            players[0]: 0,
            players[1]: 0
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
    def _create_instance_from_json(cls, item_data: Dict[str, object], match_id: str, save_to_db: bool = False):
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

        player_1_software_id, score_player_1 = match_data[0]
        player_2_software_id, score_player_2 = match_data[1]

        instance = cls(player_1_software_id=player_1_software_id,
                       player_2_software_id=player_2_software_id,
                       save_to_db=False)
        instance.software_id = match_id
        instance.score[player_1_software_id] = score_player_1
        instance.score[player_2_software_id] = score_player_2
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

    def id_win(self, player_software_id: str):
        """
        Save a player victory based on his/her software_id and block any further modifications of the result
        :param player_software_id:
        :return: If the match result has already been decided, return a message without stopping the application.
        """
        if not self.is_finished:
            if player_software_id in self.score:
                self.score[player_software_id] = 1
                self.is_finished = True
                self.save_to_database()
            else:
                raise ValueError(f"Software_id : {player_software_id} is not valid.")
        else:
            print(f"Match ID : {self.software_id} ; Match result has already been decided.")

    def draw(self):
        """
        Save a draw between players based on his/her software_id and block any further modifications of the result
        :return: If the match result has already been decided, return a message without stopping the application.
        """
        if not self.is_finished:
            for player_software_id in self.score:
                self.score[player_software_id] = 0.5
            self.is_finished = True
            self.save_to_database()
        else:
            print(f"Match ID : {self.software_id} ; Match result has already been decided.")

    def reset_match_result(self):
        """
        Method that will reinitialize the result of a match, if an error has been made
        :return:
        """
        if self.is_finished:
            for player_software_id in self.score:
                self.score[player_software_id] = 0
            self.is_finished = False
            self.save_to_database()
        else:
            raise ValueError("Match result has not been decided yet.")

    def __repr__(self) -> str:
        player_info = []
        for player_software_id, score in self.score.items():
            player_info.append(f"Player {player_software_id}: {score}")

        if self.is_finished:
            return f"ID Match : {self.software_id} is finished ; Result: {', '.join(player_info)}"
        else:
            return (f"ID Match : {self.software_id} is not finished ; "
                    f"Result pending: {list(self.score.keys())[0]} vs {list(self.score.keys())[1]}.")


def main():
    """
    Temporary function to test methods and objects
    :return:
    """
    match = Match.get_data()
    print(match)

    match_1 = Match("p_9", "p_2")
    print(repr(match_1))
    print(match_1.score)
    print(match_1.software_id)
    match_1.save_to_database()
    match_3 = Match.from_json("m_2")
    print(match_3.score)
    print(match_3.is_finished)
    print(repr(match_3))


if __name__ == '__main__':
    main()
