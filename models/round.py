from datetime import datetime
import os.path
import json


class Round:
    def __init__(self, name):

        self.software_id = self.generate_new_software_id()
        self.name = name
        self.time_start = datetime.now()
        self.time_end = None
        self.is_finished = False
        self.matches = []

    @staticmethod
    def get_path():
        base_path = os.path.dirname(__file__)
        path = os.path.join(base_path, '..', 'data', 'rounds.json')
        return path

    @classmethod
    def get_all_rounds(cls):
        with open(cls.get_path(), 'r', encoding="utf-8") as file:
            data = json.load(file)
            return data

    @classmethod
    def from_json(cls, software_id):
        data = cls.get_all_rounds()
        round_data = data["rounds"][software_id]

        round_instance = cls(round_data["name"])
        round_instance.software_id = software_id
        round_instance.time_start = round_data["time_start"]
        round_instance.time_end = round_data["time_end"]
        round_instance.is_finished = round_data["complete"]
        round_instance.matches = round_data["matches"]

        return round_instance

    @classmethod
    def generate_new_software_id(cls):
        data = cls.get_all_rounds()
        rounds_ids = [int(software_id.split("_")[1]) for software_id in data["rounds"].keys()]
        if rounds_ids:
            new_id = max(rounds_ids) + 1
        else:
            new_id = 1

        return f"r_{new_id}"

    def save_round_to_database(self):
        """
        Method to add or update a round in the database
        :return: none
        """
        data = self.get_all_rounds()
        data["rounds"][self.software_id] = {}
        data["rounds"][self.software_id]["name"] = self.name
        data["rounds"][self.software_id]["time_start"] = self.time_start
        data["rounds"][self.software_id]["time_end"] = self.time_end
        data["rounds"][self.software_id]["complete"] = self.is_finished
        data["rounds"][self.software_id]["matches"] = self.matches
        with open(self.get_path(), 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def add_match(self, match_software_id):
        self.matches.append(match_software_id)

    def end_round(self):
        if not self.is_finished:
            self.time_end = datetime.now()
            self.is_finished = True
        else:
            raise ValueError("Round is already finished")

    def __repr__(self):
        return f"Round : {self.name}, Matches: {self.matches}, Started: {self.time_start}, Ended: {self.time_end}"


def main():
    pass


if __name__ == '__main__':
    main()
