"""This script was created to test the models found in /models"""
from models.tournament import Tournament


def main():
    # Test new_tournament, do not handle draw yet, it was just to test a tournament
    new_tou = Tournament(name="Tournament test",
                         place="Testland",
                         date_start="2020-12-04",
                         date_end="2020-12-05",
                         description="test of a description",
                         rounds_number=4)
    list_of_players = ["p_1", "p_2", "p_3", "p_4", "p_5", "p_6"]
    for player in list_of_players:
        new_tou.add_participant(player)

    new_tou.initialize_first_round()

    print(new_tou.rounds['Round_1'].matches)

    result = []
    for match in new_tou.rounds['Round_1'].matches:
        print(repr(match))
        x = input('gagnant ? (p_x)')
        result.append(x)

    new_tou.rounds['Round_1'].get_match_by_player_id(result[0]).id_win(result[0])
    new_tou.rounds['Round_1'].get_match_by_player_id(result[1]).id_win(result[1])
    new_tou.rounds['Round_1'].get_match_by_player_id(result[2]).id_win(result[2])
    new_tou.end_round('Round_1')
    new_tou.start_next_round()
    print('############')
    print(new_tou.participants)
    print(new_tou.get_ranking())
    print(new_tou.rounds)
    print('############')
    new_tou.save_to_database()

    result = []
    for match in new_tou.rounds['Round_2'].matches:
        print(repr(match))
        x = input('gagnant ? (p_x)')
        result.append(x)

    new_tou.rounds['Round_2'].get_match_by_player_id(result[0]).id_win(result[0])
    new_tou.rounds['Round_2'].get_match_by_player_id(result[1]).id_win(result[1])
    new_tou.rounds['Round_2'].get_match_by_player_id(result[2]).id_win(result[2])
    new_tou.end_round('Round_2')
    new_tou.start_next_round()
    print('############')
    print(new_tou.participants)
    print(new_tou.get_ranking())
    print(new_tou.rounds)
    print('############')
    new_tou.save_to_database()

    result = []
    for match in new_tou.rounds['Round_3'].matches:
        print(repr(match))
        x = input('gagnant ? (p_x)')
        result.append(x)

    new_tou.rounds['Round_3'].get_match_by_player_id(result[0]).id_win(result[0])
    new_tou.rounds['Round_3'].get_match_by_player_id(result[1]).id_win(result[1])
    new_tou.rounds['Round_3'].get_match_by_player_id(result[2]).id_win(result[2])
    new_tou.end_round('Round_3')
    new_tou.start_next_round()
    print('############')
    print(new_tou.participants)
    print(new_tou.get_ranking())
    print(new_tou.rounds)
    print('############')
    new_tou.save_to_database()

    result = []
    for match in new_tou.rounds['Round_4'].matches:
        print(repr(match))
        x = input('gagnant ? (p_x)')
        result.append(x)

    new_tou.rounds['Round_4'].get_match_by_player_id(result[0]).id_win(result[0])
    new_tou.rounds['Round_4'].get_match_by_player_id(result[1]).id_win(result[1])
    new_tou.rounds['Round_4'].get_match_by_player_id(result[2]).id_win(result[2])
    new_tou.end_round('Round_4')
    print('############')
    print(new_tou.participants)
    print(new_tou.get_ranking())
    print(new_tou.rounds)
    print('############')
    new_tou.save_to_database()


if __name__ == '__main__':
    main()
