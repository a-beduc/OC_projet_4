import os.path
import json
from abc import ABC, abstractmethod
from typing import Dict


class _BaseModel(ABC):
    def __init__(self):
        self.software_id = self.generate_new_software_id()

    @classmethod
    def class_name_plural(cls):
        return f"{cls.__name__.lower()}s"

    @classmethod
    def get_path(cls):
        base_path = os.path.dirname(__file__)
        return os.path.join(base_path, '..', 'data', f"{cls.class_name_plural()}.json")

    @classmethod
    def get_data(cls):
        with open(cls.get_path(), 'r', encoding='utf-8') as file:
            return json.load(file)

    @classmethod
    def generate_new_software_id(cls):
        data = cls.get_data()
        ids = [int(software_id.split("_")[1]) for software_id in data[cls.class_name_plural()].keys()]
        if ids:
            new_id = max(ids) + 1
        else:
            new_id = 1
        class_letter = cls.__name__[0].lower()
        return f"{class_letter}_{new_id}"

    @classmethod
    def from_json(cls, software_id):
        data = cls.get_data()
        item_data = data[cls.class_name_plural()][software_id]
        return cls._create_instance_from_json(item_data, software_id)

    @classmethod
    @abstractmethod
    def _create_instance_from_json(cls, item_data, software_id):
        raise NotImplementedError

    def save_to_database(self):
        data = self.get_data()
        data[self.class_name_plural()][self.software_id] = self._prepare_data_to_save()
        with open(self.get_path(), 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    @abstractmethod
    def _prepare_data_to_save(self) -> Dict[str, object]:
        raise NotImplementedError


def main():
    base = _BaseModel()
    print(base)


if __name__ == '__main__':
    main()
