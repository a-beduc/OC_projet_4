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
    tournament_information = {
        "name": "1er tournoi",
        "place": "Lyon",
        "date_start": "2024-09-05",
        "date_end": "2024-09-15",
        "description": "Tournoi organisé par la fédération des echecs de Villeurbannes."
    }
    players = ["1", "3"]
    list_players = []
    for player in players:
        data = import_player(player)
        instance_of_player = Player(data["last_name"], data["first_name"], data["date_of_birth"], data["id"])
        list_players.append(instance_of_player)
    print(list_players)

    tournament = Tournament(tournament_information, list_players)
    print(repr(tournament))
    print(tournament.current_score)

    print(tournament.current_score["Dupont Jean"])

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
