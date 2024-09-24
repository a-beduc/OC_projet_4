from views.view_table_players import ViewTablePlayers
from models.player import Player


class ControllerTablePlayer:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.data = None
        self.pad_height = None
        self.sorted_content = None
        self.player_table_view = None

    def update_from_database(self):
        self.data = Player.get_data()['players']
        self.pad_height = len(self.data)
        self.sorted_content = []
        self.sort_data(['id'])
        self.player_table_view = ViewTablePlayers(self.stdscr, self.pad_height)

    def start(self):
        self.update_from_database()
        self.player_table_view.initialize()
        line_index = 0
        while True:
            self.player_table_view.fill_pad(self.sorted_content)
            action = self.player_table_view.start_view(line_index)
            if action == 'BACK':
                return None
            elif action is not None and 'SORT' in action:
                self.sort_data(action[1])
                line_index = action[2]

    @staticmethod
    def sort_key(list_of_dict, sort_fields):
        return sorted(list_of_dict, key=lambda x: tuple([x[field] for field in sort_fields]))

    def sort_data(self, sort_fields):
        data_list = []
        for key, value in self.data.items():
            id_num = int(key.split('_')[1])
            date_of_birth_list = value['date_of_birth'].split('-')
            date_of_birth_num = int(''.join(date_of_birth_list))
            data_list.append({
                'id': id_num,
                'last_name': value['last_name'],
                'first_name': value['first_name'],
                'date_of_birth': date_of_birth_num,
                'chess_id': value['chess_id'],
            })
        self.sorted_content = self.sort_key(data_list, sort_fields)
