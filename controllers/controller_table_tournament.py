from views.view_table_tournaments import ViewTableTournaments
from models.tournament import Tournament


class ControllerTableTournament:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.raw_data = Tournament.get_data()['tournaments']
        self.data = None
        self.pad_height = None
        self.sorted_content = None
        self.tournament_table_view = None

    def update_from_database(self):
        self.raw_data = Tournament.get_data()['tournaments']
        self.data = {}
        self.clean_data()
        self.pad_height = len(self.data)
        self.sorted_content = []
        self.sort_data(['id'])
        self.tournament_table_view = ViewTableTournaments(self.stdscr, self.pad_height)

    def clean_data(self):
        data_to_clean = self.raw_data.copy()
        for key, value in data_to_clean.items():
            del value["description"], value["rounds"], value["first_pairing"]

            value["participants"] = len(value["participants"])
            value["rounds"] = value.pop("rounds_number")
        self.data = data_to_clean

    def start(self):
        self.update_from_database()
        self.tournament_table_view.initialize()
        line_index = 0
        while True:
            self.tournament_table_view.fill_pad(self.sorted_content)
            action = self.tournament_table_view.start_view(line_index)
            if action == 'BACK':
                return None
            elif action is not None and 'SORT' in action:
                self.sort_data(action[1])
                line_index = action[2]
            elif action == 'NEW_TOURNAMENT':
                return action
            elif 'LOAD_TOURNAMENT' in action:
                tournament_key = self.check_tournament(action[1])
                if tournament_key is not None:
                    return 'LOAD_TOURNAMENT', tournament_key

    @staticmethod
    def sort_key(list_of_dict, sort_fields):
        return sorted(list_of_dict, key=lambda x: tuple([x[field] for field in sort_fields]))

    def sort_data(self, sort_fields):
        data_list = []
        for key, value in self.data.items():
            id_num = int(key.split("_")[1])
            date_start_list = value['date_start'].split('-')
            date_start_num = int(''.join(date_start_list))
            date_end_list = value['date_end'].split('-')
            date_end_num = int(''.join(date_end_list))
            data_list.append({
                'id': id_num,
                'name': value['name'],
                'place': value['place'],
                'date_start': date_start_num,
                'date_end': date_end_num,
                'participants': value['participants'],
                'rounds': value['rounds'],
                'complete': value['complete']
            })
        self.sorted_content = self.sort_key(data_list, sort_fields)

    def check_tournament(self, number):
        tournament_key = f"t_{number}"
        if tournament_key in self.raw_data.keys():
            return tournament_key
