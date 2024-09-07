

class Match:
    def __init__(self, player_1, player_2):
        self.scores = {
            player_1.software_id: [player_1, 0],
            player_2.software_id: [player_2, 0]
        }
        self.match_played = False

    def player_id_win(self, software_id):
        if not self.match_played:
            if software_id in self.scores:
                self.scores[software_id][1] = 1
                self.match_played = True
            else:
                raise ValueError(f"Software_id : {software_id} is not valid.")
        else:
            raise ValueError("Match result has already been decided.")

    def players_draw(self):
        if not self.match_played:
            for player_data in self.scores.values():
                player_data[1] = 0.5
            self.match_played = True
        else:
            raise ValueError("Match result has already been decided.")

    def get_player_score(self, software_id):
        if software_id in self.scores:
            return self.scores[software_id][1]
        else:
            raise ValueError(f"Player not found with software_id : {software_id}")


def main():
    pass


if __name__ == '__main__':
    main()
