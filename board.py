from rules import get_groups, get_affecting

class Board:
    def __init__(self, string):
        string = string.split("\n")

        changed = True
        while changed:
            changed = False
            for r in range(len(string)):
                if len(string[r]) == 0:
                    string.pop(r)
                    changed = True
                    break

        # matrix of list
        self.posibilities = [[[str(i+1) for i in range(9)] for c in range(9)] for r in range(9)]

        # matrix of hash set of tuples
        self.affecting = [[get_affecting(r,c) for c in range(9)] for r in range(9)]

        # matrix of characters
        self.board = [[' ' for c in range(9)] for r in range(9)]

        # matrix of list of hash set of tuples
        self.groups = [[[get_groups(r,c,d) for d in ("row", "col", "sqr")] for c in range(9)] for r in range(9)]

        # matrix of list of hash set of tuples
        self.squares = [[[get_groups(r,c,d) for d in ("sqr")] for c in range(0,9,3)] for r in range(0,9,3)]

        for r, row in enumerate(string):
            for c, val in enumerate(row):
                self.set_value(r, c, val)

    def solve(self):
        change = True
        while change:
            change = False
            # search for len(posibilities) == 1
            for r in range(9):
                for c in range(9):
                    if len(self.posibilities[r][c]) == 1 and self.board[r][c] == " ":
                        change = True
                        self.set_value(r, c, self.posibilities[r][c][0])

            #  # try to find sole posibilities in groups
            #  for r in range(9):
            #      for c in range(9):
            #          if self.board[r][c] != " ":
            #              for group in self.groups[r][c]:
            #                  other_pos = set()
            #                  for coord in group:
            #                      other_pos = other_pos.union(self.posibilities[coord[0]][coord[1]])

    def set_value(self, row, col, val):
        self.board[row][col] = val
        for a in self.affecting[row][col]:
            p = self.posibilities[a[0]][a[1]]
            if val in p:
                p.remove(val)
                if len(p) == 1:
                    self.set_value(a[0],a[1], p[0])


    def print(self):
        print("\n")
        print("+---+---+---+")
        for r, row in enumerate(self.board):
            out_string = "|"
            for c, char in enumerate(row):
                out_string += char
                if (c+1)%3 == 0:
                    out_string += "|"
            print(out_string)

            if (r+1)%3 == 0:
                print("+---+---+---+")

