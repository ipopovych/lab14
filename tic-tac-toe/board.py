from exceptions import BoardSizeExceeded, BusyPosition


class Board:
    x = "x"
    o = "o"
    none = ' '

    def __init__(self):
        """
        Initializes tic-tac-toe board.
        size: number of all cells on the board
        body: string representation of board
        last_move: index of the last move performed
        repr: string representation of index numbers
        """
        self._size = 9  # DEFAULT SIZE 3X3, not really changable for now.
        self._body = Board.none*self._size
        self.last_move = None
        self._repr = ''.join([str(i) for i in range(1, self._size+1)])

    def check(self):
        """
        Checks the situation on the field.
        return:
                 0  : draw
                "x" : X won
                "o" : O won
                2  : moves available
        """
        # all the possible winning lines
        b = self._body
        winning_ways = [b[:3], b[3:6], b[6:9],
                        b[0]+b[3]+b[6], b[1]+b[4]+b[7],
                        b[2]+b[5]+b[8],  b[0]+b[4]+b[8],
                        b[2]+b[4]+b[6]]

        if any({self.o} == set(line) for line in winning_ways):
            return 'o'  # X user fails (0 user wins)
        if any({self.x} == set(line) for line in winning_ways):
            return 'x' # X user wins (0 user fails)
        if self.none in set(self._body):
            return 2  # moves available
        else:
            return 0  # game finished with a draw

    def __len__(self):
        return self._size

    def is_empty(self):
        """Returns True if Board is empty"""
        return set(self._body) == {' '}

    def free_cells(self):
        """Returns a list of free cells of the board"""
        available = []
        for index, pos in enumerate(self):
            if pos == self.none:
                available.append(index+1)
        return available

    def empty_pos(self, key):
        """Returns True if given position is empty.
        :param key: index of the position, from 1 to 9"""
        self._valid_index(key)
        if self._body[key - 1] == self.none:
            return True
        else:
            raise BusyPosition('Position already taken.')

    def _valid_index(self, index):
        """Returns True if given index is appropriate for the board."""
        if 0 < index < self._size+1:
            return True
        else:
            raise BoardSizeExceeded('Board size exceeded')

    def __iter__(self):
        for position in self._body:
            yield position

    def __getitem__(self, key):
        """
        Item setter for the board.
        :param key: index of position, from 1 to 9
        """
        self._valid_index(key)
        return self._body[key-1]

    def __setitem__(self, key, value):
        """
        Item setter for the board.
        :param key: index of position, from 1 to 9
        :param value: value to insert, 'x', 'o', or ' '
        """
        self._valid_index(key)
        if value not in [self.o, self.x, self.none]:
            raise ValueError('Invalid value given')
        self._body = self._body[:key-1] + value + self._body[key:]

    def __str__(self):
        return self.represent(mode='real')

    def represent(self, mode='repr'):
        """
        :param mode: if 'real', returns real field
                     if 'repr', returns index representation
        :return: string, field
        """
        if mode == 'repr':
            field = self._repr
        else:
            field = self._body

        return ' --- \n' + '|' + field[:3] + \
               '|\n' + '|' + field[3:6] + '|\n' + \
               '|' + field[6:9] + '|\n' + ' --- '






# f = Board()
# f[1] = 'x'
# f[2] = 'o'
# f[3] = 'x'
# f[4] = 'o'
# f[5] = 'x'
# f[6] = 'x'
# f[7] = 'o'
# f[8] = 'x'
# f[9] = 'o'
# print(f)
# print(f.check())