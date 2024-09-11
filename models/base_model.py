import os.path
import json


class BaseModel:
    def __init__(self):
        self.software_id = self.generate_new_software_id()

    @classmethod
    def get_filename(cls):
        """
        Method to dynamically handle the filename of the datas linked to the class, should work with inheritance
        matches.json will need to be supercharged in child Match(BaseModel)
        :return: classnames.json
        """
        return f"{cls.__name__.lower()}s.json"

    @classmethod
    def get_path(cls):
        base_path = os.path.dirname(__file__)
        return os.path.join(base_path, '..', 'data', cls.get_filename())

    @classmethod
    def get_data(cls):
        with open(cls.get_path(), 'r', encoding='utf-8') as file:
            return json.load(file)

    @classmethod
    def generate_new_software_id(cls):
        data = cls.get_data()
        ids = [int(software_id.split("_")[1]) for software_id in data[cls.__name__.lower()].keys()]

        new_id = cls._check_list_for_missing_numbers(ids)
        class_letter = cls.__name__[0].lower()

        return f"{class_letter}_{new_id}"

    @staticmethod
    def _check_list_for_missing_numbers(list_of_numbers):
        """
        Method to check a list of numbers and return a missing number in the sequence
        examples :
        [1, 3, 2, 6, 4] return 5
        [0] return ValueError "There is a problem with ids found, one of them is lower than 1"
        [] return 1
        [2, 5] return 1
        [1, 2, 3] return 4
        :param list_of_numbers:
        :return: number
        """
        list_of_numbers.sort()
        if list_of_numbers:
            if min(list_of_numbers) < 1:
                raise ValueError("There is a problem with ids found, one of them is lower than 1")
            elif min(list_of_numbers) > 1:
                return 1
            else:
                for i in range(1, len(list_of_numbers)):
                    if list_of_numbers[i] - list_of_numbers[i - 1] > 1:
                        return list_of_numbers[i - 1] + 1
                return list_of_numbers[-1] + 1
        else:
            return 1

    @classmethod
    def from_json(cls):
        pass

    @classmethod
    def filter(cls):
        pass

    def save_to_database(self):
        pass

    def remove_from_database(self):
        pass


def main():
    pass


if __name__ == '__main__':
    main()

