"""This script was created to test the models found in /models"""
from models.tournament import Tournament
from models.player import Player
from models.match import Match
from models.round import Round
import json


def import_player(number):
    with open("data/players.json", "r", encoding="utf-8") as data:
        player = json.load(data)
        return player["players"][number]


def main():
    player_a = Player.from_json(software_id="p_1")
    player_b = Player.from_json(software_id="p_2")
    player_c = Player.from_json(software_id="p_3")
    player_d = Player.from_json(software_id="p_4")
    list_players = [player_a, player_b, player_c, player_d]

    name = "Le grand tournoi"
    place = "Lyon"
    date_start = "18-09-2024"
    date_end = "25-09-2024"
    description = "grand tournoi organisé par la ville de Lyon"

    tournament_a = Tournament(name, place, date_start, date_end, description)
    for player in list_players:
        tournament_a.add_tournament_participant(player)
    round_a = Round("Round 1")
    tournament_a.add_round(round_a)
    match_a = Match(player_a, player_b)
    match_b = Match(player_c, player_d)
    round_a.add_match(match_a)
    round_a.add_match(match_b)

    print("---------1---------")
    print(repr(tournament_a))
    print("--------2----------")
    print(tournament_a.rounds)
    print("--------3-----------")
    print(tournament_a.participants)
    print("---------4-----------")
    print("---------5-----------")
    print("----------6----------")
    print(tournament_a.rounds[round_a.name].matches)
    print("----------7----------")
    tournament_a.rounds[round_a.name].matches[0].player_id_win(player_a.software_id)
    print(tournament_a.rounds[round_a.name].matches)
    print("-----------8---------")
    tournament_a.rounds[round_a.name].matches[1].players_draw()
    print(tournament_a.rounds[round_a.name].matches)


if __name__ == '__main__':
    main()
