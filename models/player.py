import json
import os


class Player:
    def __init__(self, software_id="", last_name="", first_name="", date_of_birth="", chess_id=""):
        """
        Initialise a Player object. If the provided criteria match exactly one player found in Database,
        it assigns the player's data to the instance. Otherwise, it raises an error.
        :param software_id: Internal ID used in the database
        :param last_name:
        :param first_name:
        :param date_of_birth: Must be written as YYYY-MM-DD
        :param chess_id: International ID used by the federation
        """
        matching_player = self.filter_players(software_id=software_id,
                                              last_name=last_name,
                                              first_name=first_name,
                                              date_of_birth=date_of_birth,
                                              chess_id=chess_id)

        # If no matching player is found, raise an error
        if matching_player is None:
            raise ValueError("No matching players found")

        # If multiple players match the given criteria, display them and raise an error
        elif len(matching_player) > 1:
            print("Multiple matching players found")
            for player in matching_player:
                print(
                    f"ID : {player[0]}, "
                    f"Name : {player[1]['first_name']} {player[1]['last_name']}, "
                    f"Chess_ID : {player[1]['chess_id']}")
            raise ValueError("Precise criteria of search to reduce number of results")

        # If exactly one matching player is found, assign the player's data to the instance
        else:
            player_data = matching_player[0]
            self.software_id = player_data[0]
            self.last_name = player_data[1]["last_name"]
            self.first_name = player_data[1]["first_name"]
            self.date_of_birth = player_data[1]["date_of_birth"]
            self.chess_id = player_data[1]["chess_id"]

    def __repr__(self):
        return f'software_id : {self.software_id}, {self.last_name} {self.first_name} : {self.chess_id}'

    @staticmethod
    def get_path():
        base_path = os.path.dirname(__file__)
        path = os.path.join(base_path, '..', 'data', 'players.json')
        return path

    @classmethod
    def get_all_players(cls):
        """
        Loads all players from the JSON file, it is a class method to access data without an instance of Player.
        :return: A dictionary of dictionaries containing all players datas
        """
        with open(cls.get_path(), "r", encoding="utf-8") as data:
            data = json.load(data)
            return data

    @classmethod
    def filter_players(cls, software_id="", last_name="", first_name="", date_of_birth="", chess_id=""):
        """
        Check in the database if there are players that match the criteria provided as arguments.
        :param software_id: can be an int or a str
        :param last_name: can be written as "Xjd54jDod"
        :param first_name: can be written as "XjdjD564od"
        :param date_of_birth: must be written as YYYY-MM-DD
        :param chess_id: can be written as "Aa00065"
        :return: a list of tuples (software_id, {last_name, first_name, date_of_birth, chess_id})
        """
        data = cls.get_all_players()
        matching_players = []

        if software_id is not str:
            software_id = str(software_id)

        for player_id, player in data["players"].items():
            if (
                    (not software_id or player_id == software_id) and
                    (not last_name or player["last_name"] == last_name.capitalize()) and
                    (not first_name or player["first_name"] == first_name.capitalize()) and
                    (not date_of_birth or player["date_of_birth"] == date_of_birth) and
                    (not chess_id or player["chess_id"] == chess_id.upper())
            ):
                matching_players.append((player_id, player))

        if matching_players:
            return matching_players
        else:
            print("No players found with your criteria")
            return None


def main():
    pass


if __name__ == '__main__':
    main()
