from models.base_model import _BaseModel


class Player(_BaseModel):
    def __init__(self, last_name, first_name, date_of_birth, chess_id):
        super().__init__()
        self.last_name = last_name.capitalize()
        self.first_name = first_name.capitalize()
        self.date_of_birth = date_of_birth
        self.chess_id = chess_id.upper()
        self.save_to_database()

    @classmethod
    def _create_instance_from_json(cls, item_data, software_id):
        instance = cls(last_name=item_data["last_name"],
                       first_name=item_data["first_name"],
                       date_of_birth=item_data["date_of_birth"],
                       chess_id=item_data["chess_id"])
        instance.software_id = software_id
        return instance

    def _prepare_data_to_save(self):
        data = {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "chess_id": self.chess_id}
        return data

    def __repr__(self):
        return f'software_id : {self.software_id}, {self.last_name} {self.first_name} : {self.chess_id}'

    # @classmethod
    # def filter_players(cls, software_id="", last_name="", first_name="", date_of_birth="", chess_id=""):
    #     """
    #     Check in the database if there are players that match the criteria provided as arguments.
    #     :param software_id: can be an int or a str
    #     :param last_name: can be written as "Xjd54jDod"
    #     :param first_name: can be written as "XjdjD564od"
    #     :param date_of_birth: must be written as YYYY-MM-DD
    #     :param chess_id: can be written as "Aa00065"
    #     :return: a list of tuples (software_id, {last_name, first_name, date_of_birth, chess_id})
    #     """
    #     data = cls.get_data()
    #     matching_players = []
    #
    #     if software_id is not str:
    #         software_id = str(software_id)
    #
    #     for player_id, player in data["players"].items():
    #         if (
    #                 (not software_id or player_id == software_id) and
    #                 (not last_name or player["last_name"] == last_name.capitalize()) and
    #                 (not first_name or player["first_name"] == first_name.capitalize()) and
    #                 (not date_of_birth or player["date_of_birth"] == date_of_birth) and
    #                 (not chess_id or player["chess_id"] == chess_id.upper())
    #         ):
    #             matching_players.append((player_id, player))
    #
    #     if matching_players:
    #         return matching_players
    #     else:
    #         raise ValueError("No players found with your criteria")
    #
    # @classmethod def from_json(cls, software_id="", last_name="", first_name="", date_of_birth="", chess_id=""):
    # """ Class method used to initialize a Player object from arguments to select a player from a JSON file and
    # return a player object. :param software_id: "p_number" :param last_name: "Dupont" :param first_name: "Jean"
    # :param date_of_birth: YYYY-MM-DD :param chess_id: AA00001 :return: Player object """ matching_player =
    # cls.filter_players(software_id=software_id, last_name=last_name, first_name=first_name,
    #                       date_of_birth=date_of_birth, chess_id=chess_id)
    #
    #     # If no matching player is found, raise an error
    #     if matching_player is None:
    #         raise ValueError("No matching players found")
    #
    #     # If multiple players match the given criteria, display them and raise an error
    #     elif len(matching_player) > 1:
    #         print("Multiple matching players found")
    #         for player in matching_player:
    #             print(
    #                 f"ID : {player[0]}, "
    #                 f"Name : {player[1]['first_name']} {player[1]['last_name']}, "
    #                 f"Chess_ID : {player[1]['chess_id']}")
    #         raise ValueError("Precise criteria of search to reduce number of results")
    #
    #     # If exactly one matching player is found, assign the player's data to the instance of Player
    #     else:
    #         player_data = matching_player[0]
    #         extracted_software_id = player_data[0]
    #         extracted_last_name = player_data[1]["last_name"]
    #         extracted_first_name = player_data[1]["first_name"]
    #         extracted_date_of_birth = player_data[1]["date_of_birth"]
    #         extracted_chess_id = player_data[1]["chess_id"]
    #         player_instance = cls(extracted_last_name,
    #                               extracted_first_name,
    #                               extracted_date_of_birth,
    #                               extracted_chess_id)
    #         # Manually assign software_id
    #         player_instance.software_id = extracted_software_id
    #         return player_instance


def main():
    x = Player.get_data()
    print(x)
    new_player = Player(first_name="Magnus", last_name="Carlsen",
                        date_of_birth="1990-11-30", chess_id="AA00010")
    print(repr(new_player))
    new_player.save_to_database()
    jean = Player.from_json(software_id="p_1")
    print(jean)
    print(jean.software_id)
    # could be used to create dynamic pathing with inheritance
    print(Player.__name__.lower())


if __name__ == '__main__':
    main()
