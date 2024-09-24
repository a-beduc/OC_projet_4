import curses
from curses.textpad import Textbox


class ViewForm:
    QUESTION_PLAYER = [
        ' Last Name : ',
        ' First Name : ',
        ' Birth Date (YYYY-MM-DD) : ',
        ' Chess ID : '
    ]

    QUESTION_TOURNAMENT = [
        ' Name : ',
        ' Place : ',
        ' Start Date (YYYY-MM-DD) : ',
        ' End Date (YYYY-MM-DD) : ',
        ' Rounds : ',
        ' Description : '
    ]

    COMMANDS = [
        "[↓][↑] Move, [q] Quit, [v] Validate",
        "[→] Modify, [Enter] Confirm modifications",
        "[Enter] Confirm form, [b] Back to modifications"
    ]

    def __init__(self, stdscr, element):
        curses.curs_set(0)
        if element in ['NEW_PLAYER', 'NEW_TOURNAMENT']:
            self.element = element
            if element == 'NEW_PLAYER':
                self.title = ' New Player '
                self.question = ViewForm.QUESTION_PLAYER
            else:
                self.title = ' New Tournament '
                self.question = ViewForm.QUESTION_TOURNAMENT
        self.stdscr = stdscr
        self.new_textboxes = True
        self.textboxes = []
        self.terminal_h, self.terminal_w = stdscr.getmaxyx()
        self.outer_wind = None
        self.command_wind = None
        self.menu_wind = None
        self.error_wind = None
        self.validation_wind = None

    def initialize(self):
        self.new_textboxes = True
        self.textboxes = []
        self.outer_wind = self.create_outer_wind()
        self.command_wind = self.create_command_wind()
        self.menu_wind = self.create_menu_wind()
        self.error_wind = self.create_error_wind()
        self.validation_wind = self.create_validation_wind()
        self.print_menu()

    def create_outer_wind(self):
        outer_wind = curses.newwin(24, 80,
                                   (self.terminal_h - 24) // 2,
                                   (self.terminal_w - 80) // 2)
        outer_wind.keypad(True)
        outer_wind.box()
        outer_wind.addstr(0, (80 - len(self.title)) // 2, self.title)
        outer_wind.refresh()
        return outer_wind

    def create_command_wind(self):
        command_wind = self.outer_wind.derwin(len(ViewForm.COMMANDS),
                                              self.outer_wind.getmaxyx()[1] - 2,
                                              2,
                                              1)
        for idx, line in enumerate(ViewForm.COMMANDS):
            x_position = (self.outer_wind.getmaxyx()[1] - len(line)) // 2
            command_wind.addstr(idx, x_position, line)
        command_wind.refresh()
        return command_wind

    def create_menu_wind(self):
        menu_height = 2 * len(self.question)
        menu_width = (self.outer_wind.getmaxyx()[1] - 2) // 2
        menu_wind = self.outer_wind.derwin(menu_height,
                                           menu_width,
                                           3 + self.command_wind.getmaxyx()[0],
                                           1)
        for idx, question in enumerate(self.question):
            x_position = menu_width - len(question) - 1
            menu_wind.addstr(2 * idx, x_position, question)

        menu_wind.refresh()
        return menu_wind

    def create_validation_wind(self):
        validation_text = " >>> CONFIRM <<< "
        validation_wind = self.outer_wind.derwin(1,
                                                 len(validation_text) + 3,
                                                 5 + self.command_wind.getmaxyx()[0] + self.menu_wind.getmaxyx()[0],
                                                 (self.outer_wind.getmaxyx()[1] - len(validation_text)) // 2)
        validation_wind.addstr(0, 0, validation_text)
        validation_wind.refresh()
        return validation_wind

    def create_error_wind(self):
        error_wind = self.outer_wind.derwin(3,
                                            40,
                                            4 + self.command_wind.getmaxyx()[0] + self.menu_wind.getmaxyx()[0],
                                            (self.outer_wind.getmaxyx()[1] - 40) // 2)
        return error_wind

    def create_textbox(self, index_y):
        id_textbox = index_y // 2
        new_wind = self.outer_wind.derwin(1, (self.outer_wind.getmaxyx()[1] - 2) // 2,
                                          index_y + 3 + self.command_wind.getmaxyx()[0],
                                          self.outer_wind.getmaxyx()[1] // 2)
        new_wind.refresh()
        box = Textbox(new_wind)
        item = id_textbox, new_wind, box
        self.textboxes.append(item)

    def print_menu(self, selected_index=None):
        self.menu_wind.clear()
        for idx, question in enumerate(self.question):
            x_position = self.menu_wind.getmaxyx()[1] - len(question) - 1
            self.menu_wind.addstr(2 * idx, x_position, question)
            if self.new_textboxes:
                index_y = 2 * idx
                self.create_textbox(index_y)
        self.new_textboxes = False
        if selected_index is not None:
            x_position = self.menu_wind.getmaxyx()[1] - len(self.question[selected_index // 2]) - 1
            self.menu_wind.addstr(2 * (selected_index // 2), x_position, self.question[selected_index // 2],
                                  curses.A_REVERSE)
        self.menu_wind.refresh()

    def start_view(self, error_msg=''):
        if error_msg != '':
            self.error_wind.clear()
            self.error_wind.addstr(1, (self.error_wind.getmaxyx()[1] - len(error_msg)) // 2, error_msg)
            self.error_wind.addstr(2, (self.error_wind.getmaxyx()[1] - len('[press any key]')) // 2, '[press any key]')
            self.error_wind.refresh()
            self.outer_wind.getch()
            self.error_wind.clear()
            self.error_wind.refresh()
            self.validation_wind.addstr(0, 0, " >>> CONFIRM <<< ")
            self.validation_wind.refresh()
        running = True
        current_line_index = 0
        while running:
            self.print_menu(current_line_index)
            key = self.outer_wind.getch()
            if key in [81, 113]:  # 'Q' or 'q'
                return 'BACK'
            elif key == curses.KEY_DOWN:
                current_line_index = (current_line_index + 2) % (len(self.question) * 2)
            elif key == curses.KEY_UP:
                current_line_index = (current_line_index - 2) % (len(self.question) * 2)
            elif key == curses.KEY_RIGHT or key in [curses.KEY_ENTER, 10, 13]:
                curses.curs_set(1)
                textbox_id = current_line_index // 2
                self.textboxes[textbox_id][2].edit()
                curses.curs_set(0)
            elif key in [86, 118]:  # 'V' or 'v'
                action = self.validation_button()
                if action is not 'BACK':
                    return action

    def validation_button(self):
        self.print_menu()
        self.validation_wind.clear()
        self.validation_wind.addstr(0, 0, " >>> CONFIRM <<< ", curses.A_REVERSE)
        self.validation_wind.refresh()
        second_running = True
        while second_running:
            second_key = self.outer_wind.getch()
            if second_key == curses.KEY_ENTER or second_key in [10, 13]:
                form_content = [item[2].gather().strip() for item in self.textboxes]
                return 'VALIDATE', self.element, form_content
            elif second_key in [66, 98]:  # 'B' or 'b'
                self.validation_wind.clear()
                self.validation_wind.addstr(0, 0, " >>> CONFIRM <<< ")
                self.validation_wind.refresh()
                return 'BACK'


def main(stdscr):
    view = ViewForm(stdscr, "NEW_TOURNAMENT")
    view.initialize()
    view.start_view()


if __name__ == '__main__':
    curses.wrapper(main)
