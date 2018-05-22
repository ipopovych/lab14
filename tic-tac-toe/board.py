class Board:
    x = "x"
    o = "o"
    none = ' '

    def __init__(self):
        self._body = Board.none*9

    def check_field(self):
        """
        Checks the situation on the field.
        return:
                0  : draw
                1  : X won
               -1  : O won
                2  : moves available
        """
        # all the possible winning lines
        b = self._body
        winning_ways = [b[:3], b[3:6], b[6:9],
                        b[0]+b[3]+b[6], b[1]+b[4]+b[7],
                        b[2]+b[5]+b[8],  b[0]+b[4]+b[8],
                        b[2]+b[4]+b[6]]

        if any({self.o} == set(line) for line in winning_ways):
            return -1  # X use fails (0 user wins)
        if any({self.x} == set(line) for line in winning_ways):
            return 1  # X use wins (0 user fails)
        if self.none in set(self._body):
            return 2  # moves available
        else:
            return 0  # game finished with a draw

    def __getitem__(self, item):
        """
        Item setter for the board.
        :param item: index of position, from 1 to 9
        """
        if not(0 <= item < 10):
            raise ValueError('Board size exceeded')
        return self._body[item-1]

    def __setitem__(self, key, value):
        """
        Item setter for the board.
        :param key: index of position, from 1 to 9
        :param value: value to insert, 'x', 'o', or ' '
        """
        if not(0 < key < 10):
            raise ValueError('Board size exceeded')
        if value not in [self.o, self.x, self.none]:
            raise ValueError('Invalid value given')
        self._body = self._body[:key-1] + value + self._body[key:]

    def __str__(self):
        return ' --- \n' + '|' + self._body[:3] + \
               '|\n' + '|' + self._body[3:6] + '|\n' + \
               '|' + self._body[6:9] + '|\n' + ' --- '



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
# print(f.check_field())