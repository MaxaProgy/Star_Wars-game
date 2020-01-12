from game import Game


def main():
    game = StarWars()
    game.run()


class StarWars(Game):
    def __init__(self):
        super(StarWars, self).__init__()


if __name__ == '__main__':
    main()
