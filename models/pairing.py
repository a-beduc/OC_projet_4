import random
import copy


class Pairing:
    def __init__(self, list_of_players, new_pairing=True):
        self.list_of_players = list_of_players
        self.possibles_configurations = []
        self.played_matches = set()
        if new_pairing:
            self.initial_configuration = self.randomize_players()

    def randomize_players(self):
        shuffled_list = self.list_of_players.copy()
        random.shuffle(shuffled_list)
        return tuple(shuffled_list)

    @staticmethod
    def rearrange_list(old_list):
        new_list = [old_list[0], old_list[-1]]
        new_list.extend(old_list[1:-1])
        return new_list

    @staticmethod
    def generate_pairing(list_configuration):
        set_configuration = set()
        for i in range(int(len(list_configuration) / 2)):
            pair = [list_configuration[i], list_configuration[-i-1]]
            pair = sorted(pair)
            set_configuration.add(tuple(pair))
        return set_configuration

    def generate_circle_configurations(self):
        current_configuration = list(copy.deepcopy(self.initial_configuration))
        i = 1
        while i < len(self.initial_configuration):
            current_configuration = self.rearrange_list(current_configuration)
            current_set = self.generate_pairing(current_configuration)
            self.possibles_configurations.append(current_set)
            i += 1

    def add_to_memory(self, round_matches):
        for match in round_matches:
            self.played_matches.add(match)

    def generate_first_round_configuration(self):
        matches = self.possibles_configurations.pop()
        self.add_to_memory(matches)
        return matches

    def generate_round_configuration_from_match(self, match):
        for configuration in self.possibles_configurations:
            if match in configuration:
                next_round_configuration = configuration
                self.possibles_configurations.remove(configuration)
                self.add_to_memory(next_round_configuration)
                return next_round_configuration

    def try_to_generate_next_round(self, list_of_players):
        for i in range(len(list_of_players)):
            for j in range(i+1, len(list_of_players)):
                match_test = [list_of_players[i], list_of_players[j]]
                match_test = tuple(sorted(match_test))
                if match_test not in self.played_matches:
                    next_round = self.generate_round_configuration_from_match(match_test)
                    return next_round

    def generate_next_round_from_ranking(self, dict_ranking):
        ranking_key = []
        for key in dict_ranking.keys():
            ranking_key.append(key)
        sorted(ranking_key)
        i = 0
        starting_list = dict_ranking[ranking_key[0]]
        result = None
        while not result:
            list_test = starting_list.copy()
            next_list = []
            if i > 0:
                next_list.extend(dict_ranking[ranking_key[i]])
            list_test.extend(next_list)
            result = self.try_to_generate_next_round(list_test)
            i += 1
        return result

    @classmethod
    def instantiate_pairing(cls, list_of_players, initial_configuration, list_played_matches):
        instance = cls(list_of_players=list_of_players,
                       new_pairing=False)
        instance.initial_configuration = initial_configuration
        instance.generate_circle_configurations()
        instance.played_matches.update(list_played_matches)
        instance.possibles_configurations = [config for config in instance.possibles_configurations
                                             if not config & instance.played_matches]
        return instance


def main():
    lists = ["p_1", "p_2", "p_3", "p_4", "p_5", "p_6"]
    paired = Pairing(lists)
    paired.generate_circle_configurations()
    print(paired.possibles_configurations)
    print(paired.initial_configuration)
    print("------------------")
    x = paired.generate_first_round_configuration()
    print("------------------")
    print(f"current round : {x}")
    print(f"reste configuration : {paired.possibles_configurations}")
    print(f"Match joué : {paired.played_matches}")
    print(paired.initial_configuration)
    print("-----------------")
    y = paired.try_to_generate_next_round(['p_2', 'p_3', 'p_4'])
    print(f"current round : {y}")
    print(f"reste configuration : {paired.possibles_configurations}")
    print(f"Match joué : {paired.played_matches}")
    print(paired.initial_configuration)
    print("-----------------")
    y = paired.try_to_generate_next_round(['p_2', 'p_3', 'p_4'])
    print(f"current round : {y}")
    print(f"reste configuration : {paired.possibles_configurations}")
    print(f"Match joué : {paired.played_matches}")
    print(paired.initial_configuration)
    print("-----------------")
    y = paired.try_to_generate_next_round(['p_2'])
    print(f"current round : {y}")
    print(f"reste configuration : {paired.possibles_configurations}")
    print(f"Match joué : {paired.played_matches}")
    print(paired.initial_configuration)
    print("-----------------")


if __name__ == "__main__":
    main()
