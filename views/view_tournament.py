import curses


def main(stdscr):
    curses.curs_set(0)

    height, width = stdscr.getmaxyx()

    outer_wind = curses.newwin(height, width - 2, 0, 1)
    outer_wind.box()

    text = " Tournament {x} "
    outer_wind.addstr(0, 2, text)
    outer_wind.refresh()

    height_in, width_in = outer_wind.getmaxyx()

    height_top = 8
    height_black_top = 1
    height_black_bottom = 1
    height_bottom = height_in - (height_top + height_black_top + height_black_bottom)

    width_left = (width_in - 3) * 2 // 3
    width_right = width_in - (width_left + 2)

    commands_wind = outer_wind.derwin(height_top, width_right, height_black_top, width_left + 1)
    commands_wind.box()
    commands_wind.addstr(0, 2, " Commands ")
    commands_wind.addstr(1, 2, "[p] Ranking")
    commands_wind.addstr(2, 2, "[r] Round")
    commands_wind.addstr(3, 2, "[q] Quit")
    commands_wind.addstr(4, 2, "[Enter] Select match")
    commands_wind.addstr(5, 2, "[←] Win Left, [→] Win Right")
    commands_wind.addstr(6, 2, "[=] Draw, [Backspace] Reset")
    commands_wind.refresh()

    info_wind = outer_wind.derwin(height_top, width_left, height_black_top, 1)
    info_wind.box()
    info_wind.addstr(0, 2, " Information ")
    info_wind.addstr(1, 2, "Name : {name}")
    info_wind.addstr(2, 2, "Place : {place} ")
    info_wind.addstr(3, 2, "Date Start : {date_start}")
    info_wind.addstr(4, 2, "Date End : {date_end}")
    description = ("Description : {Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
                   "tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "
                   "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure "
                   "dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
                   "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit "
                   "anim id est laborum.}")
    description_2 = ""
    if len(description) > width_left:
        description_2 = description[width_left - 4:]
        description = description[:width_left - 4]
    if len(description_2) > width_left:
        description_2 = description_2[:width_left - 7] + "..."

    info_wind.addstr(5, 2, description)
    info_wind.addstr(6, 2, description_2)
    info_wind.refresh()

    score_wind = outer_wind.derwin(height_bottom, width_right, height_black_top + height_top, width_left + 1)
    score_wind.box()

    players = [("Dupont", "Jean", 125.5), ("Martin", "Marie", 92), ("Durand", "Paul", 6), ("Bernard", "Lucie", 4.5),
               ("Dupont", "Océane", 3), ("Carlsen", "Magnus", 1)]
    name_text = []
    target_length = width_right - 4
    for player in players:
        new_name = player[0] + ', ' + player[1][0] + ' '
        score = ' ' + str(player[2])
        number_dots = target_length - len(new_name) - len(score)
        new_text = new_name + ("." * number_dots) + score
        name_text.append(new_text)

    score_wind.addstr(0, 2, " Ranking ")

    for idx, element in enumerate(name_text):
        score_wind.addstr(idx + 2, 2, f"{name_text[idx]}")
    score_wind.refresh()

    height_match = 7

    matches_wind = outer_wind.derwin(height_bottom - height_match, width_left, height_black_top + height_top, 1)
    matches_wind.box()
    matches_wind.addstr(0, 2, " Round {x} ")

    results = {"R": " | Win Right ",
               "L": " | Win Left  ",
               "D": " | Draw      ",
               "P": " | Pending..."}

    selected = {"Y": "[x]", "N": "[ ]"}

    names = ["Dupont, J",
             "Martin, M",
             "Durand, P",
             "Bernard, L",
             "Dupont, O",
             "Carlsen, M"]

    matches_dict = {
        "m_1": [selected["Y"], names[0], names[1], results["R"]],
        "m_2": [selected["N"], names[2], names[3], results["L"]],
        "m_3": [selected["N"], names[4], names[5], results["D"]],
        "m_4": [selected["N"], names[0], names[1], results["P"]]
    }

    matches_text = []
    matches_target_length = width_left - 4
    for value in matches_dict.values():
        text_part_1 = value[0] + " "
        text_part_2 = value[1] + " vs " + value[2] + " "
        text_end = value[3]
        number_dots = matches_target_length - len(text_part_1) - len(text_part_2) - len(text_end)
        new_text = text_part_1 + text_part_2 + ('.' * number_dots) + text_end
        matches_text.append(new_text)

    for index, match_text in enumerate(matches_text):
        matches_wind.addstr(index + 2, 2, match_text)

    matches_wind.refresh()

    match_wind = outer_wind.derwin(height_match, width_left, height_bottom - height_match + height_top + 1, 1)
    match_wind.box()
    match_wind.addstr(0, 2, " Selected Match ")
    match_wind.addstr(2, 2, "Match_ID : <m_1>")
    match_wind.addstr(3, 2, "Match : <Left Player> VS <Right Player>")
    match_wind.addstr(4, 2, "Status : Left Player Win | Right Player Win | Draw | Pending")
    match_wind.refresh()

    match_wind.getch()


if __name__ == "__main__":
    curses.wrapper(main)
