from views.view_menu import ViewMenu
from controllers.controller_table_player import ControllerTablePlayer
from controllers.controller_table_tournament import ControllerTableTournament
from controllers.controller_form import ControllerForm
from controllers.controller_tournament import ControllerTournament


class ControllerMenu:
    """
    Initializes the ControllerMenu with the provided terminal screen (stdscr).
    Sets up the main menu, player table, tournament table, and form controllers.
    """
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.main_menu = ViewMenu(self.stdscr)
        self.player_table = ControllerTablePlayer(self.stdscr)
        self.tournament_table = ControllerTableTournament(self.stdscr)
        self.new_player = ControllerForm(self.stdscr, 'NEW_PLAYER')
        self.new_tournament = ControllerForm(self.stdscr, 'NEW_TOURNAMENT')
        self.tournament = None

    def start(self):
        """
        Main loop for the menu controller.
        Continuously displays the main menu and handles the selected action until 'EXIT' is chosen.
        Actions include creating a new tournament, viewing tournaments, creating a new player, viewing players, or
        loading a specific tournament.
        """
        memory = None
        while True:
            action = self.get_next_action(memory)
            memory = None

            match action:
                case 'EXIT':
                    break
                case 'NEW_TOURNAMENT':
                    memory = self.handle_new_tournament()
                case 'VIEW_TOURNAMENT':
                    memory = self.handle_view_tournament()
                case 'NEW_PLAYER':
                    memory = self.handle_new_player()
                case 'VIEW_PLAYER':
                    self.handle_view_player()
                case ('LOAD_TOURNAMENT', _):
                    self.handle_load_tournament(action[1])
                case _:
                    continue

    def get_next_action(self, memory):
        """
        Retrieves the next action to be performed by the menu controller.
        If no action is stored in memory, it initializes the main menu and waits for the user to make a selection.
        Otherwise, it returns the action stored in memory.
        """
        if memory is None:
            self.main_menu.initialize()
            return self.main_menu.start_menu()
        return memory

    def handle_new_tournament(self):
        form_tournament = self.new_tournament.start()
        return 'VIEW_TOURNAMENT' if form_tournament else None

    def handle_view_tournament(self):
        return self.tournament_table.start()

    def handle_new_player(self):
        form_player = self.new_player.start()
        return 'VIEW_PLAYER' if form_player else None

    def handle_view_player(self):
        self.player_table.start()

    def handle_load_tournament(self, tournament_id):
        """
        Handles loading and managing an existing tournament based on the provided tournament ID.
        Initializes a new tournament controller and starts it.
        """
        self.tournament = ControllerTournament(self.stdscr, tournament_id)
        self.tournament.start()
