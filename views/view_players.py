import curses


def reformat_id(software_id):
    length_id_target = 4
    software_id = software_id.split("_")[1] if "_" in software_id else software_id
    return f"#{software_id.zfill(length_id_target)}"


def reformat_name(name, target_length):
    if len(name) < target_length:
        return name.ljust(target_length)
    else:
        return name[:target_length - 1] + "."


def create_content(variable_length,
                software_id="#ID  ",
                last_name="Last Name",
                first_name="First Name",
                birth_date="Birth Date",
                chess_id="ChessID"):
    separator = " │ "

    software_id = reformat_id(software_id) if "_" in software_id else "#ID  "

    name_length = (variable_length - 4 - (len(software_id) + len(birth_date) + len(chess_id) + (4 * len(separator)))) // 2

    first_name = reformat_name(first_name, name_length)
    last_name = reformat_name(last_name, name_length)

    return separator.join([software_id, last_name, first_name, birth_date, chess_id])


def create_separator_line(width, content):
    separator = " │ "
    parts = content.split(separator)
    line = ""
    for i, part in enumerate(parts):
        if i > 0:
            line += "─┼─"
        line += "─" * len(part)
    return line



def main(stdscr):
    curses.curs_set(0)
    height, width = stdscr.getmaxyx()
    outer_height, outer_width = height, width - 2
    outer_wind = curses.newwin(outer_height, outer_width, 0, 1)
    outer_wind.box()
    text = " List of PLayers "
    outer_wind.addstr(0, (outer_width - len(text)) // 2, text)
    content_headers = create_content(outer_width)
    outer_wind.addstr(2, 2, content_headers)
    outer_wind.addstr(3, 2, create_separator_line(outer_width, content_headers))
    outer_wind.refresh()

    height_data, width_data = outer_wind.getmaxyx()
    data_wind = outer_wind.derwin(height_data - 4, width_data, 4, 0)

    data = {
        "p_1": {
            "last_name": "Dupont",
            "first_name": "Jean",
            "date_of_birth": "1990-05-14",
            "chess_id": "AA00001"
        },
        "p_2": {
            "last_name": "Martin",
            "first_name": "Marie",
            "date_of_birth": "1988-09-23",
            "chess_id": "AA00002"
        },
        "p_3": {
            "last_name": "Durand",
            "first_name": "Paul",
            "date_of_birth": "1992-11-10",
            "chess_id": "AA00003"
        },
        "p_4": {
            "last_name": "Bernard",
            "first_name": "Lucie",
            "date_of_birth": "1995-03-08",
            "chess_id": "AA00004"
        },
        "p_5": {
            "last_name": "Dupont",
            "first_name": "Océane",
            "date_of_birth": "1992-11-10",
            "chess_id": "AA00005"
        },
        "p_6": {
            "last_name": "Carlsen",
            "first_name": "Magnus",
            "date_of_birth": "1990-11-30",
            "chess_id": "AA00010"
        }
    }

    i = 0
    for key, value in data.items():
        line = create_content(
            width_data,
            software_id=key,
            last_name=value["last_name"],
            first_name=value["first_name"],
            birth_date=value["date_of_birth"],
            chess_id=value["chess_id"]
        )
        data_wind.addstr(i, 2, line)
        i += 1

    data_wind.refresh()
    outer_wind.getch()


if __name__ == '__main__':
    curses.wrapper(main)
