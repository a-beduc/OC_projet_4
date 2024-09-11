from models.base_model import _BaseModel


class Match(_BaseModel):
    def __init__(self, player_1_software_id, player_2_software_id):
        super().__init__()
        self.score = {
            player_1_software_id: 0,
            player_2_software_id: 0
        }
        self.is_finished = False
        self.save_to_database()

    @classmethod
    def class_name_plural(cls):
        return "matches"

    @classmethod
    def _create_instance_from_json(cls, item_data, software_id):
        is_finished = item_data['complete']
        del item_data['complete']
        match_data = list(item_data.items())

        player_1_software_id, score_player_1 = match_data[0]
        player_2_software_id, score_player_2 = match_data[1]

        instance = cls(player_1_software_id=player_1_software_id,
                       player_2_software_id=player_2_software_id)
        instance.software_id = software_id
        instance.score[player_1_software_id] = score_player_1
        instance.score[player_2_software_id] = score_player_2
        instance.is_finished = is_finished

        return instance

    def _prepare_data_to_save(self):
        data = self.score
        data["complete"] = self.is_finished
        return data

    def player_id_win(self, player_software_id):
        if not self.is_finished:
            if player_software_id in self.score:
                self.score[player_software_id] = 1
                self.is_finished = True
            else:
                raise ValueError(f"Software_id : {player_software_id} is not valid.")
        else:
            raise ValueError("Match result has already been decided.")

    def players_draw(self):
        if not self.is_finished:
            for player_software_id in self.score:
                self.score[player_software_id] = 0.5
            self.is_finished = True
        else:
            raise ValueError("Match result has already been decided.")

    def get_player_score(self, software_id):
        """ Relic of an older version of the model, probably useless now, need s/o opinion"""
        if software_id in self.score:
            return self.score[software_id]
        else:
            raise ValueError(f"Player not found with software_id : {software_id}")

    def reset_match_result(self):
        if self.is_finished:
            for player_software_id in self.score:
                self.score[player_software_id] = 0
            self.is_finished = False
        else:
            raise ValueError("Match result has not been decided yet.")

    def __repr__(self):
        player_info = []
        for player_software_id, score in self.score.items():
            player_info.append(f"Player {player_software_id}: {score}")

        if self.is_finished:
            return f"Match result: {', '.join(player_info)}"
        else:
            return f"Match between {list(self.score.keys())[0]} and {list(self.score.keys())[1]} is not finished yet."


def main():
    match = Match.get_data()
    print(match)

    match_1 = Match("p_1", "p_2")
    print(repr(match_1))
    print(match_1.score)
    print(match_1.software_id)
    match_1.save_to_database()
    match_3 = Match.from_json("m_5")
    print(match_3.score)
    print(match_3.is_finished)
    print(repr(match_3))


if __name__ == '__main__':
    main()
