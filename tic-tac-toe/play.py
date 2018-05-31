from game import Game


if __name__ == '__main__':
    res = 1
    while res != 0:
        game = Game()
        res = game.play()