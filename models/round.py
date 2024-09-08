from datetime import datetime


class Round:
    def __init__(self, name):
        self.name = name
        self.time_start = datetime.now()
        self.time_end = None
        self.is_finished = False
        self.matches = []

    def add_match(self, match):
        self.matches.append(match)

    def end_round(self):
        if not self.is_finished:
            self.end = datetime.now()
            self.is_finished = True
        else:
            raise ValueError("Round is already finished")

    def get_results(self):
        for match in self.matches:
            print(repr(match))

    def __repr__(self):
        return f"Round : {self.name}, Matches: {len(self.matches)}, Started: {self.time_start}, Ended: {self.time_end}"


def main():
    pass


if __name__ == '__main__':
    main()
