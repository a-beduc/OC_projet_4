

class Player:
    def __init__(self, last_name="", first_name="", date_of_birth="", chess_id=""):
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.id = chess_id

    def __repr__(self):
        return f'{self.last_name} {self.first_name}'


def main():
    pass


if __name__ == '__main__':
    main()
