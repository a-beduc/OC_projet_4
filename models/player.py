from models.base_model import _BaseModel
from typing import Dict


class Player(_BaseModel):
    def __init__(self,
                 last_name: str,
                 first_name: str,
                 date_of_birth: str,
                 chess_id: str,
                 save_to_db: bool = True):
        """
        Initialize a new player object.
        :param last_name:
        :param first_name:
        :param date_of_birth: format must follow 'YYYY-MM-DD'
        :param chess_id: format must follow 'AA00000'
        :param save_to_db: If true, it wills save the object into the database
        """
        super().__init__()
        self.last_name = last_name.capitalize()
        self.first_name = first_name.capitalize()
        self.date_of_birth = date_of_birth
        self.chess_id = chess_id.upper()
        if save_to_db:
            self.save_to_database()

    @classmethod
    def _create_instance_from_json(cls, item_data: Dict[str, str], player_id: str, save_to_db: bool = False):
        """
        Create a player object from a json dictionary.
        :param item_data: The dictionary extracted from the tournament.json
        :param player_id:
        :param save_to_db: must be false to avoid copy of player instance in database
        :return: An instance of Player
        """
        instance = cls(
            last_name=item_data["last_name"],
            first_name=item_data["first_name"],
            date_of_birth=item_data["date_of_birth"],
            chess_id=item_data["chess_id"],
            save_to_db=False
        )
        instance.software_id = player_id
        return instance

    def _prepare_data_to_save(self) -> Dict[str, str]:
        """
        Prepare data to save in the database.
        :return: dictionary with data to save in the database
        """
        data = {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "chess_id": self.chess_id}
        return data

    def __repr__(self) -> str:
        return f'software_id : {self.software_id}, {self.last_name} {self.first_name} : {self.chess_id}'


def main():
    """
    Temporary function to test methods and objects
    :return:
    """
    x = Player.get_data()['players']
    print(x)
    new_player = Player(first_name="Magnus", last_name="Carlsen",
                        date_of_birth="1990-11-30", chess_id="AA00000")
    print(repr(new_player))
    new_player.save_to_database()
    jean = Player.from_json(software_id="p_1")
    print(jean)
    print(jean.software_id)
    # could be used to create dynamic pathing with inheritance
    print(Player.__name__.lower())


if __name__ == '__main__':
    main()
