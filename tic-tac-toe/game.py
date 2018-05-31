from board import Board
from players import HumanPlayer, ComputerBinary, ComputerAdvanced
import random


class Game:
    def __init__(self):
        """Initializes the game and starts it."""
        print('Welcome. Please, choose game mode: ')
        mode = self._get_mode()
        player1 = HumanPlayer()
        if not isinstance(mode, tuple):
            player2 = HumanPlayer()
        else:
            if mode[1] == 'easy':
                player2 = ComputerBinary()
            else:
                player2 = ComputerAdvanced()

        self._board = Board()
        print('Field index representation:\n{}'.format(self._board.represent()))
        self._players = {1: player1, 2: player2}
        self.current_player = None
        self._start()

    def play(self):
        """Performs the game and prints results, then finishes it
        by returning 0 if game is finished and 1 in user wants to play again"""
        while self._board.check() == 2:  # moves available
            print(self._board)
            # print('current player: {}'.format(str(self._players[self.current_player])))
            self._board = self._players[self.current_player].play(self._board)
            self._change_player()

        if self._board.check() == 'o':
            self._change_player()
            winner = self._players[self.current_player]
            print('\n\nWinning o! Congrats, {}'.format(winner.name))

        elif self._board.check() == 'x':
            self._change_player()
            winner = self._players[self.current_player]
            print('\n\nWinning x! Congrats, {}'.format(winner.name))

        else:
            winners = (self._players[1], self._players[2])
            print('\n\nTIE! Congrats, {}. Anf for you {}, too.'.format(winners[0].name, winners[1].name))
        print(self._board)
        return self._finish()

    # --------------- helper methods -------------------------

    def _get_mode(self):
        """
        Gets the game mode from user.

        return mode: integer, mode of the game
                     2: 2 - players, human - human
                     1: 1 - player, computer - human
        """
        print('1 - Self-play, play with computer')
        print('2 - Multiplay, play with friend')
        try:
            mode = int(input('Enter the number: '))
        except ValueError:
            print('Invalid number')
            return self._get_mode()
        else:
            if mode in [1, 2]:
                if mode == 1:
                    print('Choose difficulty level')
                    print('1 - Easy')
                    print('2 - Hard')
                    try:
                        level = int(input('Enter the number: '))
                    except ValueError:
                        print('Invalid number')
                        return self._get_mode()
                    else:
                        if level in [1, 2]:
                            if level == 1:
                                return mode, 'easy'
                            else:
                                return mode, 'hard'
                        else:
                            return self._get_mode()
                else:
                    return mode
            else:
                return self._get_mode()

    def _start(self):
        """Start the game by choosing the first player and setting up them as current player"""
        beginner = random.choice((1, 2))  # game begins from random player
        if beginner == 1:
            self._players[1].set_symbol('x')
            self._players[2].set_symbol('o')
            self.current_player = 1
        else:
            self._players[2].set_symbol('x')
            self._players[1].set_symbol('o')
            self.current_player = 2
        print('current player: {}'.format(str(self._players[self.current_player])))

    def _change_player(self):
        """Changes current played of the game."""
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

    @staticmethod
    def _finish():
        """Returns 0 if game is finished and 1 in user wants to play again"""
        print('Play again?\nPress Enter to continue or any symbol to exit.\n')
        res = input()
        if res == '':
            print('Continue')
            return 1
        else:
            return 0

