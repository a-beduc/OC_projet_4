"""This script was created to test the models found in /models"""
from models.tournament import Tournament
from models.player import Player
from models.match import Match
from models.round import Round
import json
import os


def import_player(number):
    with open("data/players.json", "r", encoding="utf-8") as data:
        player = json.load(data)
        return player["players"][number]


def main():

    print(Player.get_all_players())
    print(Player.filter_players(first_name="111"))
    print(Player.filter_players(last_name="DupOnt", first_name="Océane"))

    player_1 = Player(chess_id="aa00002")
    print(player_1.software_id)
    print(player_1.last_name)
    print(player_1.first_name)
    print(repr(player_1))

    # tournament = Tournament()
    # player_1 = Player()
    # player_2 = Player()
    # match_1 = Match()
    # match_2 = Match()
    # round_1 = Round()
    #
    # print(tournament)
    # print(player_1)
    # print(player_2)
    # print(match_1)
    # print(match_2)
    # print(round_1)


if __name__ == '__main__':
    main()
