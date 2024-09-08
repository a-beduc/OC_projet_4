class Match:
    def __init__(self, player_1, player_2):
        self.scores = {
            player_1.software_id: [player_1, 0],
            player_2.software_id: [player_2, 0]
        }
        self.is_finished = False

    def player_id_win(self, software_id):
        if not self.is_finished:
            if software_id in self.scores:
                self.scores[software_id][1] = 1
                self.is_finished = True
            else:
                raise ValueError(f"Software_id : {software_id} is not valid.")
        else:
            raise ValueError("Match result has already been decided.")

    def players_draw(self):
        if not self.is_finished:
            for player_data in self.scores.values():
                player_data[1] = 0.5
            self.is_finished = True
        else:
            raise ValueError("Match result has already been decided.")

    def get_player_score(self, software_id):
        if software_id in self.scores:
            return self.scores[software_id][1]
        else:
            raise ValueError(f"Player not found with software_id : {software_id}")

    def reset_match_result(self):
        if self.is_finished:
            for player_data in self.scores.values():
                player_data[1] = 0
            self.is_finished = False
        else:
            raise ValueError("Match result has not been decided yet.")

    def __repr__(self):
        player_info = []
        for player_data in self.scores.values():
            player = player_data[0]
            score = player_data[1]
            player_info.append(f"{player.last_name} {player.first_name}: {score}")

        if self.is_finished:
            return f"Match result: {', '.join(player_info)}"
        else:
            return (f"Match between {player_info[0].split(':')[0]} and {player_info[1].split(':')[0]} "
                    f"is not finished yet.")


def main():
    pass


if __name__ == '__main__':
    main()
