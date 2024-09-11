import os.path
import json


class Match:
    def __init__(self, player_1_software_id, player_2_software_id):

        self.software_id = self.generate_new_software_id()
        self.score = {
            player_1_software_id: 0,
            player_2_software_id: 0
        }
        self.is_finished = False

    @staticmethod
    def get_path():
        base_path = os.path.dirname(__file__)
        path = os.path.join(base_path, '..', 'data', 'matches.json')
        return path

    @classmethod
    def get_all_matches(cls):
        with open(cls.get_path(), "r", encoding="utf-8") as file:
            data = json.load(file)
            return data

    @classmethod
    def from_json(cls, software_id):
        data = cls.get_all_matches()
        match_data = data["matches"][software_id]
        is_finished = match_data["complete"]
        del match_data["complete"]
        match_data_item = list(match_data.items())

        player_1_software_id, score_player_1 = match_data_item[0]
        player_2_software_id, score_player_2 = match_data_item[1]

        match_instance = cls(player_1_software_id, player_2_software_id)
        match_instance.software_id = software_id
        match_instance.score[player_1_software_id] = score_player_1
        match_instance.score[player_2_software_id] = score_player_2
        match_instance.is_finished = is_finished

        return match_instance

    @classmethod
    def generate_new_software_id(cls):
        data = cls.get_all_matches()
        matches_ids = [int(software_id.split("_")[1]) for software_id in data["matches"].keys()]
        if matches_ids:
            new_id = max(matches_ids) + 1
        else:
            new_id = 1

        return f"m_{new_id}"

    def save_match_to_database(self):
        """
        Method to add or update a match in the database
        :return: none
        """
        data = self.get_all_matches()
        data["matches"][self.software_id] = self.score
        data["matches"][self.software_id]["complete"] = self.is_finished
        with open(self.get_path(), "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

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
    match = Match.get_all_matches()
    print(match)
    match_2 = match["matches"]
    print(match_2)
    match_1 = Match("p_1", "p_2")
    print(repr(match_1))
    print(match_1.score)
    print(match_1.software_id)
    match_1.save_match_to_database()
    match_3 = Match.from_json("m_5")
    print(match_3.score)
    print(match_3.is_finished)
    print(repr(match_3))


if __name__ == '__main__':
    main()
