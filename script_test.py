"""This script was created to test the models found in /models"""
from models.tournament import Tournament
from models.player import Player
from models.match import Match
from models.round import Round


def main():
    # create a few Players
    player_a = Player(last_name="Nakamura",
                      first_name="Hikaru",
                      date_of_birth="1986-12-09",
                      chess_id="AA00008")

    player_b = Player(last_name="Carlsen",
                      first_name="Magnus",
                      date_of_birth="1990-11-30",
                      chess_id="AA00001")

    player_c = Player(last_name="Nepomniachtchi",
                      first_name="Ian",
                      date_of_birth="1990-07-14",
                      chess_id="AA00002")

    player_d = Player(last_name="Ding",
                      first_name="Liren",
                      date_of_birth="1992-10-24",
                      chess_id="AA00003")

    list_players = [player_a, player_b, player_c, player_d]

    print("------------------")
    for player in list_players:
        print(repr(player))
    print("------------------")
    print("\n")

    # create a round and add players

    round_1 = Round("Round y")
    match_1 = Match(player_a.software_id,
                    player_b.software_id)
    match_2 = Match(player_c.software_id,
                    player_d.software_id)
    round_1.add_match([match_1, match_2])
    print(f"Round 1 : {repr(round_1)}")
    print(f"Match 1: {repr(match_1)}")
    print(f"Match 2: {repr(match_2)}")

    print("------------------")



if __name__ == '__main__':
    main()
