import curses


class ViewTournament:
    COMMAND_BASE = [
        '[t] Tournament Menu',
        '[p] Player Menu',
        '[q] Quit'
    ]

    COMMAND_PLAYERS = [
        '[↓][↑] Navigate',
        '[p] Sort Name',
        '[s] Sort Score',
        '[q] Back to Menu'
    ]

    COMMAND_TOURNAMENT = [
        '[↓][↑] Navigate',
        '[Enter] Select',
        '[q] Back to Menu'
    ]

    COMMAND_ROUND = [
        '[↓][↑] Navigate',
        '[Enter] Select',
        '[q] Back to Tournament'
    ]

    COMMAND_MATCH = [
        '[←] Win Left',
        '[→] Win Right',
        '[=] Draw',
        '[r] Reset',
        '[q] Quit'
    ]

    temporary_name_score = [("Dupont", "Jean", 1),
                            ("Martin", "Mamamadddad", 2),
                            ("Durand", "Pddsdsqfd", 2.5),
                            ("Bernard", "Ldsqdqsd6sdqqs", 5),
                            ("Dupont", "Odvoisvsovdsv", 0),
                            ("Carlsen", "Mamamadddad_2", 80),
                            ("Dupont", "Jean_2", 8),
                            ("Martin", "Mamamadddad_2", 8),
                            ("Durand", "Pddsdsqfd_2", 8.5),
                            ("Bernard", "Ldsqdqsd6sdqqs_2", 8),
                            ("Dupont", "Odvoisvsovdsv_2", 8),
                            ("Carlsen", "Mamamadddad_3", 40),
                            ("Dupont", "Jean_3", 51),
                            ("Martin", "Mamamadddad_3", 52),
                            ("Durand", "Pddsdsqfd_3", 52.5),
                            ("Bernard", "Ldsqdqsd6sdqqs_3", 55),
                            ("Dupont", "Odvoisvsovdsv_3", 50),
                            ("Last", "Element", 10)]

    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.outer_wind_height, self.outer_wind_width = stdscr.getmaxyx()[0], stdscr.getmaxyx()[1] - 2
        self.left_wind_width = (self.outer_wind_width - 3) * 2 // 3
        self.right_wind_width = self.outer_wind_width - self.left_wind_width - 2
        self.bottom_wind_height = self.outer_wind_height - 10
        self.commands = {
            'command_base': self.COMMAND_BASE,
            'command_player': self.COMMAND_PLAYERS,
            'command_tournament': self.COMMAND_TOURNAMENT,
            'command_round': self.COMMAND_ROUND,
            'command_match': self.COMMAND_MATCH
        }
        self.players = self.temporary_name_score.copy()

        self.outer_wind = self.create_outer_wind()
        self.info_wind = self.create_information_wind()
        self.command_wind = self.create_command_wind()
        self.tournament_wind = self.create_tournament_wind()
        self.player_wind = self.create_player_wind()
        self.player_pad = self.create_player_pad()
        self.update_player_pad(self.players)
        self.start()

    def create_outer_wind(self, title="{{default_title}}"):
        outer_wind = curses.newwin(self.outer_wind_height, self.outer_wind_width, 0, 0)
        outer_wind.box()
        box_title = f" {title} "
        outer_wind.addstr(0, (self.outer_wind_width - len(box_title)) // 2, box_title)
        outer_wind.keypad(True)
        outer_wind.refresh()
        return outer_wind

    def create_information_wind(self,
                                name="{{default_name}}",
                                place="{{default_place}}",
                                date_start="{{default_date_start}}",
                                date_end="{{default_date_end}}",
                                description="{{default_description}}"):
        info_wind = self.outer_wind.derwin(8, self.left_wind_width, 1, 1)
        info_wind.box()
        info_wind.addstr(0, 2, ' Information ')
        info_wind.addstr(1, 2, f"Name : {name}")
        info_wind.addstr(2, 2, f"Place : {place} ")
        info_wind.addstr(3, 2, f"Date Start : {date_start}")
        info_wind.addstr(4, 2, f"Date End : {date_end}")
        line_1 = f"Description : {description}"
        line_2 = ""
        if len(line_1) > self.left_wind_width:
            line_2 = line_1[self.left_wind_width - 4:]
            line_1 = line_1[:self.left_wind_width - 4]
        if len(line_2) > self.left_wind_width:
            line_2 = line_2[:self.left_wind_width - 7] + "..."
        info_wind.addstr(5, 2, line_1)
        info_wind.addstr(6, 2, line_2)
        info_wind.refresh()
        return info_wind

    def create_command_wind(self, command_key='command_base'):
        command_wind = self.outer_wind.derwin(8, self.right_wind_width, 1, self.left_wind_width + 1)
        command_wind.clear()
        command_wind.box()
        command_wind.addstr(0, 2, ' Commands ')
        for i in range(len(self.commands[command_key])):
            command_wind.addstr(i + 1, 2, self.commands[command_key][i])
        command_wind.refresh()
        return command_wind

    def create_tournament_wind(self):
        bottom_left_wind = self.outer_wind.derwin(self.bottom_wind_height, self.left_wind_width, 9, 1)
        bottom_left_wind.box()
        bottom_left_wind.addstr(0, 2, ' Tournament ')
        bottom_left_wind.refresh()
        return bottom_left_wind

    @staticmethod
    def reformat_name(player_name, target_length):
        name = ", ".join(player_name)
        if len(name) < target_length:
            player_string = name.ljust(target_length)
        else:
            player_string = name[:target_length - 1] + "."
        return player_string

    def reformat_name_score(self, player_name_score):
        separator = ' | '
        target_length = self.right_wind_width - 6 - len(separator) - len('Score')
        player_string = self.reformat_name(player_name_score[:2], target_length)
        score_string = str(player_name_score[2]).ljust(len('Score'))
        return separator.join([player_string, score_string])

    def create_player_pad(self):
        pad_height = len(self.players) + 1
        player_pad = curses.newpad(pad_height, self.right_wind_width - 6)
        player_pad.refresh(0, 0,
                           13, self.left_wind_width + 4,
                           self.outer_wind_height - 3, self.outer_wind_width - 3)
        return player_pad

    def update_player_pad(self, list_tuple_player_score):
        for idx, player_score in enumerate(list_tuple_player_score):
            line = self.reformat_name_score(player_score)
            self.player_pad.addstr(idx, 0, line)
        self.player_pad.refresh(0, 0,
                                13, self.left_wind_width + 4,
                                self.outer_wind_height - 3, self.outer_wind_width - 3)

    def create_player_wind(self):
        player_wind = self.outer_wind.derwin(self.bottom_wind_height, self.right_wind_width,
                                             9, self.left_wind_width + 1)
        player_wind.box()
        player_wind.addstr(0, 2, ' Player ')
        text_menu = self.reformat_name_score(('Last Name', 'First Name', 'Score'))
        player_wind.addstr(2, 3, text_menu)
        player_wind.refresh()
        return player_wind

    def start(self):
        running = True
        while running:
            key = self.outer_wind.getch()
            if key in [84, 116]:  # 'T'  or 't'
                self.tournament_wind.addstr(0, 2, ' Tournament ', curses.A_REVERSE)
                self.tournament_wind.refresh()
                self.command_wind = self.create_command_wind('command_tournament')
                self.outer_wind.getch()
                self.tournament_wind.addstr(0, 2, ' Tournament ')
                self.tournament_wind.refresh()
                self.command_wind = self.create_command_wind()
            elif key in [80, 112]:  # 'P' or 'p'
                self.player_wind.addstr(0, 2, ' Player ', curses.A_REVERSE)
                self.player_wind.refresh()
                self.command_wind = self.create_command_wind('command_player')
                self.start_player_menu()
                self.player_wind.addstr(0, 2, ' Player ')
                self.player_wind.refresh()
                self.command_wind = self.create_command_wind()
            elif key in [81, 113]:  # 'Q' or 'q'
                running = False

    def start_player_menu(self):
        running = True
        pad_start_line = 0
        while running:
            self.player_pad.refresh(pad_start_line, 0,
                                    13, self.left_wind_width + 4,
                                    self.outer_wind_height - 3, self.outer_wind_width - 3)
            key = self.outer_wind.getch()
            if key == curses.KEY_DOWN:
                if pad_start_line < len(self.players) - (self.bottom_wind_height - 5):
                    pad_start_line += 1
            elif key == curses.KEY_UP:
                if pad_start_line > 0:
                    pad_start_line -= 1
            elif key in [81, 113]:  # 'Q' or 'q'
                running = False


def main(stdscr):
    ViewTournament(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
