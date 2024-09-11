from datetime import datetime
from models.base_model import _BaseModel


class Round(_BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.time_start = str(datetime.now())
        self.time_end = None
        self.is_finished = False
        self.matches = []

    @classmethod
    def _create_instance_from_json(cls, item_data, software_id):
        instance = cls(name=item_data["name"])
        instance.software_id = software_id
        instance.time_start = item_data["time_start"]
        instance.time_end = item_data["time_end"]
        instance.is_finished = item_data["complete"]
        instance.matches = item_data["matches"]
        return instance

    def _prepare_data_to_save(self):
        data = {
            "name": self.name,
            "time_start": self.time_start,
            "time_end": self.time_end,
            "complete": self.is_finished,
            "matches": self.is_finished
        }
        return data

    def add_match(self, match_software_id):
        self.matches.append(match_software_id)

    def end_round(self):
        if not self.is_finished:
            self.time_end = str(datetime.now())
            self.is_finished = True
        else:
            raise ValueError("Round is already finished")

    def __repr__(self):
        return f"Round : {self.name}, Matches: {self.matches}, Started: {self.time_start}, Ended: {self.time_end}"


def main():
    round_1 = Round("Round x")
    # round_2 = Round.from_json("r_2")
    print(round_1)
    # print(round_2)
    round_1.add_match("m_1")
    round_1.add_match("m_2")
    value = input("just to delay exec")
    print(value)
    round_1.end_round()
    round_1.save_to_database()


if __name__ == '__main__':
    main()
