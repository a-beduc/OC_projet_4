import os.path
import json
from abc import ABC, abstractmethod
from typing import Dict


class _BaseModel(ABC):
    """
    Abstract base class for all models, take care of every actions that require an interaction with the database.
    2024/09/14 In the current project it allows models that inherit the methods to write and read into JSON files.
    """
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
        """
        Create a new exclusive software ID for an instance of a class.
        The id is generated based on the class name and the number of the last instance found in the database.
        :return: str: '<class_first_letter>_<number>'
        """
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
        """
        create an instance of a class from a JSON file.
        :param software_id: str: '<class_first_letter>_<number>'
        :return instance: an instance of a class
        """
        data = cls.get_data()
        item_data = data[cls.class_name_plural()][software_id]
        return cls._create_instance_from_json(item_data, software_id, save_to_db=False)

    @classmethod
    @abstractmethod
    def _create_instance_from_json(cls, item_data, software_id, save_to_db=False):
        """
        Abstract method that creates an instance of a class from a dictionary extracted from the JSON file.
        It must be implemented in every class that inherit this method.
        :param item_data: Dictionary of the JSON file.
        :param software_id: String of the software ID.
        :param save_to_db: Boolean, must be false to avoid copy of the instance in the database during initialization.
        """
        raise NotImplementedError

    def save_to_database(self):
        """
        Save the instance of a class to a JSON file.
        """
        data = self.get_data()
        data[self.class_name_plural()][self.software_id] = self._prepare_data_to_save()
        with open(self.get_path(), 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    @abstractmethod
    def _prepare_data_to_save(self) -> Dict[str, object]:
        """
        Abstract method that prepares the instance of a class from a dictionary extracted from the JSON file.
        It must be implemented in every class that inherit this method.
        :return: Dict[str, object]
        """
        raise NotImplementedError
