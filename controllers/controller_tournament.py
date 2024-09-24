from models.tournament import Tournament
from models.player import Player
from views.view_tournament import ViewTournament


class ControllerTournament:
    def __init__(self, stdscr):
        self.stdscr = stdscr
