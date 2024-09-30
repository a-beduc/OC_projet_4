from controllers import controller_tournament
from views.view_menu import ViewMenu
from controllers.controller_table_player import ControllerTablePlayer
from controllers.controller_table_tournament import ControllerTableTournament
from controllers.controller_form import ControllerForm
from controllers.controller_tournament import ControllerTournament


class ControllerMenu:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.main_menu = ViewMenu(self.stdscr)
        self.player_table = ControllerTablePlayer(self.stdscr)
        self.tournament_table = ControllerTableTournament(self.stdscr)
        self.new_player = ControllerForm(self.stdscr, 'NEW_PLAYER')
        self.new_tournament = ControllerForm(self.stdscr, 'NEW_TOURNAMENT')
        self.tournament = None

    def start(self):
        memory = None
        while True:
            if memory is None:
                self.main_menu.initialize()
                action = self.main_menu.start_menu()
            else:
                action = memory
                memory = None
            if action == 'EXIT':
                break
            elif action == 'NEW_TOURNAMENT':
                form_tournament = self.new_tournament.start()
                if form_tournament is not None:
                    memory = 'VIEW_TOURNAMENT'
            elif action == 'VIEW_TOURNAMENT':
                output = self.tournament_table.start()
                if output is not None:
                    if 'NEW_TOURNAMENT' in output:
                        memory = 'NEW_TOURNAMENT'
                    elif 'LOAD_TOURNAMENT' in output:
                        memory = output
            elif action == 'NEW_PLAYER':
                form_player = self.new_player.start()
                if form_player is not None:
                    memory = 'VIEW_PLAYER'
            elif action == 'VIEW_PLAYER':
                self.player_table.start()
            elif 'LOAD_TOURNAMENT' in action:
                self.tournament = ControllerTournament(self.stdscr, action[1])
                self.tournament.start()

        print(action)
