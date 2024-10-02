import curses
from curses.textpad import Textbox


class ViewForm:
    """
    Class responsible for displaying and interacting with a form in the
    terminal using the curses module. The form uses the default size of a
    terminal on a Mac (24 lines and 80 columns).
    """

    OUTER_HEIGHT = 24
    OUTER_WIDTH = 78
    ERROR_WINDOW_WIDTH = 40

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
        """
        Initialize the ViewForm class.
        :param stdscr: Screen object initialized by curses.wrapper()
        :param element: Type of form ('NEW_PLAYER' or 'NEW_TOURNAMENT')
        """
        curses.curs_set(0)
        if element in ['NEW_PLAYER', 'NEW_TOURNAMENT']:
            self.element = element
            if element == 'NEW_PLAYER':
                self.title = ' New Player '
                self.question = ViewForm.QUESTION_PLAYER
            else:
                self.title = ' New Tournament '
                self.question = ViewForm.QUESTION_TOURNAMENT

        self.new_textboxes = True
        self.textboxes = []
        self.terminal_h, self.terminal_w = stdscr.getmaxyx()
        self.outer_wind = None
        self.command_wind = None
        self.menu_wind = None
        self.error_wind = None
        self.validation_wind = None
        self.selected_index = 0

        self.KEY_ACTIONS = {
            curses.KEY_DOWN: self.move_down,
            curses.KEY_UP: self.move_up,
            curses.KEY_RIGHT: self.modify_textbox,
            curses.KEY_ENTER: self.modify_textbox,
            10: self.modify_textbox,
            13: self.modify_textbox,
            ord('q'): self.quit_form,
            ord('Q'): self.quit_form,
            ord('v'): self.validate_form,
            ord('V'): self.validate_form
        }

    def initialize(self):
        """
        Initialize and create all the windows required for the form.
        """
        self.new_textboxes = True
        self.textboxes = []

        # create the outer line and is used as a base for other windows
        # placement
        self.outer_wind = self.create_window(
            height=self.OUTER_HEIGHT,
            width=self.OUTER_WIDTH,
            start_y=(self.terminal_h - self.OUTER_HEIGHT) // 2,
            start_x=(self.terminal_w - self.OUTER_WIDTH) // 2,
            title=self.title, has_border=True, outer=True)

        self.command_wind = self.create_window(height=len(ViewForm.COMMANDS),
                                               width=self.OUTER_WIDTH - 2,
                                               start_y=2,
                                               start_x=1)
        self.update_command_wind()

        # Display the questions on the left of the form
        self.menu_wind = self.create_window(height=2 * len(self.question),
                                            width=(self.OUTER_WIDTH - 2) // 2,
                                            start_y=len(ViewForm.COMMANDS) + 3,
                                            start_x=1)
        self.update_menu_wind()

        self.validation_wind = self.create_window(
            height=1,
            width=len(" >>> CONFIRM <<< ") + 3,
            start_y=len(ViewForm.COMMANDS) + 2 * len(self.question) + 5,
            start_x=(self.OUTER_WIDTH - len(" >>> CONFIRM <<< ")) // 2)
        self.update_validation_wind()

        self.error_wind = self.create_window(
            height=3,
            width=40,
            start_y=len(ViewForm.COMMANDS) + 2 * len(self.question) + 4,
            start_x=(self.OUTER_WIDTH - 40) // 2)
        self.print_menu()

    def create_window(self, height, width, start_y, start_x, title="",
                      has_border=False, outer=False):
        """
        Create a curses window with given dimensions and properties.
        :param height: Height of the window
        :param width: Width of the window
        :param start_y: Y-coordinate of the window's starting position
        :param start_x: X-coordinate of the window's starting position
        :param title: Optional title to display at the top of the window
        :param has_border: Boolean indicating if the window should have a
        border
        :param outer: Boolean indicating if this is the main (outer) window
        :return: <obj.Window>
        """
        if outer:
            window = curses.newwin(height, width, start_y, start_x)
            window.keypad(True)
        else:
            window = self.outer_wind.derwin(height, width, start_y, start_x)
        if has_border:
            window.box()
        if title:
            window.addstr(0, (width - len(title)) // 2, title)
        window.refresh()
        return window

    def update_command_wind(self):
        """
        Update the command window with the list of available commands.
        """
        for idx, line in enumerate(ViewForm.COMMANDS):
            x_position = (self.outer_wind.getmaxyx()[1] - len(line)) // 2
            self.command_wind.addstr(idx, x_position, line)
        self.command_wind.refresh()

    def update_menu_wind(self):
        """
        Update the menu window with the list of questions. One question every
        other line.
        """
        for idx, question in enumerate(self.question):
            x_position = (self.OUTER_WIDTH - 2) // 2 - len(question) - 1
            self.menu_wind.addstr(2 * idx, x_position, question)
        self.menu_wind.refresh()

    def update_validation_wind(self, reverse=False):
        """
        Update the validation button window.
        :param reverse: Boolean indicating if the text should be displayed in
        reverse video (highlighted)
        """
        self.validation_wind.clear()
        validation_text = " >>> CONFIRM <<< "
        self.validation_wind.addstr(0, 0, validation_text)
        if reverse:
            self.validation_wind.addstr(0, 0, validation_text,
                                        curses.A_REVERSE)
        self.validation_wind.refresh()

    def create_textbox(self, index_y):
        """
        Create a textbox (input field) for a specific question.
        :param index_y: Y-coordinate index for placing the textbox
        """
        new_wind = self.create_window(
            1,
            (self.outer_wind.getmaxyx()[1] - 2) // 2,
            index_y + 3 + self.command_wind.getmaxyx()[0],
            self.outer_wind.getmaxyx()[1] // 2)
        box = Textbox(new_wind)
        self.textboxes.append(box)

    def print_menu(self):
        """
        Display the menu with the list of questions and highlight the selected
        one.
        """
        self.menu_wind.clear()
        for idx, question in enumerate(self.question):
            x_position = self.menu_wind.getmaxyx()[1] - len(question) - 1
            self.menu_wind.addstr(2 * idx, x_position, question)
            if self.new_textboxes:
                index_y = 2 * idx
                self.create_textbox(index_y)
        self.new_textboxes = False
        if self.selected_index is not None:
            x_position = (self.menu_wind.getmaxyx()[1] -
                          len(self.question[self.selected_index // 2]) - 1)
            self.menu_wind.addstr(2 * (self.selected_index // 2),
                                  x_position,
                                  self.question[self.selected_index // 2],
                                  curses.A_REVERSE)
        self.menu_wind.refresh()

    def display_error(self, error_msg=''):
        """
        Display an error message in the error window.
        :param error_msg: The error message to display
        """
        self.error_wind.clear()
        self.error_wind.addstr(
            1,
            (self.error_wind.getmaxyx()[1] - len(error_msg)) // 2,
            error_msg)
        self.error_wind.addstr(
            2,
            (self.error_wind.getmaxyx()[1] - len('[press any key]')) // 2,
            '[press any key]')
        self.error_wind.refresh()
        self.outer_wind.getch()
        self.error_wind.clear()
        self.error_wind.refresh()
        self.update_validation_wind()

    @staticmethod
    def quit_form():
        return 'BACK'

    def move_down(self):
        """
        Move the selection down to the next question. Using % to circle.
        """
        self.selected_index = (
                (self.selected_index + 2) % (len(self.question) * 2))

    def move_up(self):
        """
        Move the selection up to the previous question. Using % to circle.
        """
        self.selected_index = (
                (self.selected_index - 2) % (len(self.question) * 2))

    def modify_textbox(self):
        """
        Allow the user to modify the content of the selected textbox.
        """
        curses.curs_set(1)
        textbox_id = self.selected_index // 2
        self.textboxes[textbox_id].edit()
        curses.curs_set(0)

    def validate_form(self):
        return self.validation_button()

    def start_view(self, error_msg=''):
        """
        Start the main loop for the form interaction.
        :param error_msg: Optional error message to display at the beginning
        :return: Result indicating the action to take after the form is closed
        """
        if error_msg != '':
            self.display_error(error_msg)
        while True:
            self.print_menu()
            key = self.outer_wind.getch()
            action = self.KEY_ACTIONS.get(key)
            if action:
                result = action()
                if result:
                    return result

    def validation_button(self):
        """
        Handle the interaction when the validation button is pressed.
        :return: Tuple containing the action, element type, and form content
        to the controller
        """
        self.print_menu()
        self.update_validation_wind(reverse=True)
        while True:
            key = self.outer_wind.getch()

            if key == curses.KEY_ENTER or key in [10, 13]:
                form_content = [item.gather().strip() for item
                                in self.textboxes]
                return 'VALIDATE', self.element, form_content
            elif key in [ord('B'), ord('b'), ord('Q'), ord('q')]:
                self.update_validation_wind()
                break
