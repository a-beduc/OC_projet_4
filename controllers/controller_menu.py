from views.view_menu import ViewMenu
from controllers.controller_table_player import ControllerTablePlayer
from controllers.controller_table_tournament import ControllerTableTournament


class ControllerMenu:
    def __init__(self, stdscr):
        self.main_menu = ViewMenu(stdscr)
        self.player_table = ControllerTablePlayer(stdscr)
        self.tournament_table = ControllerTableTournament(stdscr)

    def start(self):
        while True:
            self.main_menu.initialize()
            action = self.main_menu.start_menu()
            if action == 'EXIT':
                break
            elif action == 'new_tournament':
                break
            elif action == 'view_tournaments':
                self.tournament_table.start()
            elif action == 'new_player':
                break
            elif action == 'view_players':
                self.player_table.start()
        print(action)
