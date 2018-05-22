class Board:
    X = 1
    O = 0

    def __init__(self):
        self._body = []
        for r in range(3):
            self._body.append([None, None, None])
        self._lastposition = None
        self._lastturn = None

    def check_field(self):
        # all the possible winning lines
        winning_ways = self._body + [[a[0] for a in self._body]] + \
               [[a[1] for a in self._body]] + [[a[2] for a in self._body]] + \
               [[self._body[0][0], self._body[1][1], self._body[2][2]]] + \
               [[self._body[0][2], self._body[1][1], self._body[2][0]]]

        empty = False
        for line in winning_ways:
            shut = 0
            cell = line[0]
            if cell is None:
                shut = 0
                empty = True
            if cell == self.X and shut >= 0:
                shut += 1
                if shut == 4:
                    return 1  # X user wins
            if cell == self.X and shut < 0:
                shut = 0
            if cell == self.O and shut < 0:
                shut -= 1
                if shut == -4:
                    return -1  # X use fails (0 user wins)
            if cell == self.O and shut > 0:
                shut = 0
        if empty:
            return 2  # moves available
        else:
            return 0  # game finished with a draw

    def build(self):
        pass


f = Board()
print(f.check_field())