from views.view_table_players import ViewTablePlayers
from models.player import Player


class ControllerTablePlayer:
    """
    Controller class responsible for managing and displaying the table of players.
    It interacts with the player data from the database and uses ViewTablePlayer to display the data.
    """
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.data = None
        self.pad_height = None
        self.sorted_content = None
        self.player_table_view = None

    def start(self):
        """
        Starts the player table view. It continuously listens for user input to either return to the main menu or
        sort the data.
        """
        self.update_from_database()
        self.player_table_view.initialize('List of Players')
        while True:
            self.player_table_view.fill_pad(self.sorted_content)
            action = self.player_table_view.start_view()

            match action:
                case 'BACK':
                    return None
                case ('SORT', _):
                    self.sort_data(action[1])
                case _:
                    continue

    def update_from_database(self):
        """
        Fetches player data from the database and initializes the table view with the updated data.
        The player data is sorted by the default field ('id') initially.
        """
        self.data = Player.get_data()['players']
        self.pad_height = len(self.data)
        self.sorted_content = []
        self.sort_data(['id'])
        self.player_table_view = ViewTablePlayers(self.stdscr, self.pad_height)

    @staticmethod
    def sort_key(list_of_dict, sort_fields):
        """ Sorts a list of dictionaries based on the specified fields. """
        return sorted(list_of_dict, key=lambda x: tuple([x[field] for field in sort_fields]))

    def sort_data(self, sort_fields):
        """ Sorts the player data based on the specified fields and updates the sorted_content attribute. """
        data_list = []
        for key, value in self.data.items():
            id_num = int(key.split('_')[1])
            date_of_birth_list = value['date_of_birth'].split('-')
            date_of_birth_num = int(''.join(date_of_birth_list))
            data_list.append({
                'id': id_num,
                'last_name': value['last_name'].capitalize(),
                'first_name': value['first_name'].capitalize(),
                'date_of_birth': date_of_birth_num,
                'chess_id': value['chess_id'],
            })
        self.sorted_content = self.sort_key(data_list, sort_fields)
