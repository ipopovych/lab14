import numpy as np
from binary_tree import LinkedBinaryTree as BTree
from linked_tree import LinkedTree as Tree
from exceptions import BoardSizeExceeded, BusyPosition
from copy import deepcopy


class Player:
    """Represents a tic-tac-toe player"""
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def set_symbol(self, symbol):
        if symbol in ["x", 'o']:
            self.symbol = symbol
        else:
            raise ValueError('Invalid symbol, "x" or "o" expected')

    def _move(self, field, index):
        field[index] = self.symbol
        field.last_move = index
        return field

    def __str__(self):
        return '\nname: {}\nsymbol: {}'.format(self.name, self.symbol)


class HumanPlayer(Player):
    """Represents a human player"""
    def __init__(self, symbol=None):
        name = input('Please, Enter your name: ')
        super().__init__(name, symbol)

    def play(self, current_field):
        """
        Performs one turn of a player and returns modified field.
        :param current_field: Board object
        :return: Board object
        """
        print('Enter the position to put {}'.format(self.symbol))
        try:
            index = int(input('Please, enter the index of position'))
            if current_field.empty_pos(index):
                return self._move(current_field, index)
        except (BoardSizeExceeded, BusyPosition, ValueError) as err:
            print(err)
            print('Invalid index for current board, try again')
            return self.play(current_field)


class ComputerBinary(Player):
    """Represents a computer player with decision making based on binary tree"""
    def __init__(self, symbol=None):
        super().__init__('Computer', symbol)
        if symbol == 'x':
            self.ENEMY = 'o'
        else:
            self.ENEMY = 'x'

    def play(self, current_field):
        free_cells = current_field.free_cells()
        if current_field.is_empty():
            index = np.random.randint(1, len(current_field) + 1)
            return self._move(current_field, index)
        elif len(free_cells) == 1:
            return self._move(current_field, free_cells[0])
        else:
            return self._smart_move(free_cells, current_field)

    # ---------- helper methods to make computer's decision -----------------
    def _smart_move(self, free_cells, current_field):
        """Makes smart move based on BINARY decision making tree and returns modified field"""
        moves = [free_cells.pop(np.random.randint(0, len(free_cells))),
                 free_cells.pop(np.random.randint(0, len(free_cells)))]  # two randomly chosen steps
        # print("POSSIBLE TWO MOVES", moves)
        scores = [self._evaluate(current_field, move) for move in moves]  # grades for moves
        # print("SCORES OF TWO MOVES", scores)
        return self._move(current_field, moves[np.argmax(scores)])  # move to an index with highest score

    def _evaluate(self, field, move):
        """Builds an initial tree with copy of current field as a root, runs recursion."""
        f = deepcopy(field)
        self._move(f, move)  # performing suggested move
        tree = BTree(f)
        return self._perform_recursion(tree)

    def _perform_move(self, field, index):
        """Performs imaginary computer move by projecting it copied current field"""
        field = deepcopy(field)
        field[index] = self.symbol
        field.last_move = index
        return field

    def _enemy_move(self, field, index):
        """Performs human move by projecting it on copied current field"""
        field[index] = self.ENEMY
        field.last_move = index
        return field

    def _perform_recursion(self, tree):
        """Recurse down the tree adding two random available steps on each level.
        When finished, return the graded scale of the tree calculated as sum.
        """
        board = tree.get_root_val()
        state = board.check()  # current state of the game field
        # return scale points according to the result on the leaf:

        if state == 0:  # performed game finished with a tie
            return 0

        elif state == self.symbol:  # performed game finished with computer win
            return 5

        elif state == self.ENEMY:  # performed game finished with computer loose
            return -10

        elif state == 2:  # performed game hasn't finished, moves available on the board
            free_cells = board.free_cells()
            # Performing random enemy's move:
            board = self._enemy_move(board,
                                     free_cells.pop(np.random.randint(0, len(free_cells))))

            # Performing almost random computer's move:
            if len(free_cells) > 1:
                moves = [free_cells.pop(np.random.randint(0, len(free_cells))),
                         free_cells.pop(np.random.randint(0, len(free_cells)))]
                fields = [self._perform_move(board, moves[0]),
                          self._perform_move(board, moves[1])]
                # Expanding the tree
                tree.insert_left(fields[0])
                tree.insert_right(fields[1])
                # calculating score of the leaf by adding scores of children leaves
                return self._perform_recursion(tree.get_right_child()) + \
                       self._perform_recursion(tree.get_left_child())

            elif len(free_cells) == 1:  # one possible cell left to move
                tree.insert_left(self._perform_move(board,
                                                    free_cells.pop(np.random.randint(0, len(free_cells)))))
                return self._perform_recursion(tree.get_left_child())
            else:
                return self._perform_recursion(tree)


class ComputerAdvanced(ComputerBinary):
    # ---------- some REDEFINED helper methods to make computer's decision -----------------
    def _smart_move(self, free_cells, current_field):
        """Makes smart move based on FULL decision making tree and returns modified field"""
        moves = free_cells
        # print("POSSIBLE MOVES", moves)
        scores = [self._evaluate(current_field, move) for move in moves]  # grades for moves
        # print("SCORES MOVES", scores)
        return self._move(current_field, moves[np.argmax(scores)])  # move to an index with highest score

    def _evaluate(self, field, move):
        """Builds an initial tree with copy of current field as a root, runs recursion."""
        f = deepcopy(field)
        self._move(f, move)  # performing suggested move
        tree = Tree(f)
        return self._perform_recursion(tree)

    def _perform_recursion(self, tree):
        """Recurse down the tree adding all available steps on each level.
        When finished, return the graded scale of the tree calculated as sum.
        """
        board = tree.get_root_val()
        state = board.data.check()  # current state of the game field
        # return scale points according to the result on the leaf:

        if state == 0:  # performed game finished with a tie
            return 0

        elif state == self.symbol:  # performed game finished with computer win
            return 5

        elif state == self.ENEMY:  # performed game finished with computer loose
            return -10

        elif state == 2:  # performed game hasn't finished, moves available on the board
            free_cells = board.data.free_cells()

            # Adding all possible random enemy's moves to tree:
            for cell in free_cells:
                tree.add(self._enemy_move(board.data, cell))

            for subtree in tree.children():
                board = subtree.get_root_val()
                free_cells = board.data.free_cells()
                if not len(free_cells) == 0:  # base case
                    return self._perform_recursion(subtree)
                for cell in free_cells:
                    subtree.add(self._perform_move(board.data, cell))

            # calculating score of every leaf by adding scores of children leaves
            count = 0
            for subtree in tree.children():
                for el in subtree.children():
                    count += self._perform_recursion(el)
            return count
