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
        self.posibilities = [[{str(i + 1) for i in range(9)} for _ in range(9)] for _ in range(9)]

        # matrix of hash set of tuples
        self.affecting = [[get_affecting(r, c) for c in range(9)] for r in range(9)]

        # matrix of characters
        self.board = [[' ' for _ in range(9)] for _ in range(9)]

        # matrix of list of hash set of tuples
        self.groups = [[[get_groups(r, c, d) for d in ("row", "col", "sqr")] for c in range(9)] for r in range(9)]

        # matrix of list of hash set of tuples
        self.sqrs = [[get_groups(r, c, "sqr") for c in range(0, 9, 3)] for r in range(0, 9, 3)]
        self.rows = [[get_groups(r, c, "row") for c in range(1)] for r in range(9)]
        self.cols = [[get_groups(r, c, "col") for c in range(9)] for r in range(1)]

        for r, row in enumerate(string):
            for c, val in enumerate(row):
                self.set_value(r, c, val)
        self.print("START OF GAME")

    def solve(self):
        change = True

        while change:
            change = False
            for r in range(9):
                for c in range(9):
                    if len(self.posibilities[r][c]) == 1 and self.board[r][c] == " ":
                        change = True
                        self.set_value(r, c, list(self.posibilities[r][c])[0])

            if not change:
                change = self.find_sole_posibilities_in_group()
            if not change:
                change = self.find_group_subsets()

    def find_sole_posibilities_in_group(self):
        change = False
        for r in range(9):
            for c in range(9):
                b = self.is_sole_posibility_in_group(r,c)
                change = change or b

    def is_sole_posibility_in_group(self, row, col):
        change = False
        if self.board[row][col] == " ":
            for group in self.groups[row][col]:
                if self.board[row][col] == " ":
                    for pos in self.posibilities[row][col]:
                        alone = True
                        for coord in group - {(row, col)}:
                            if self.board[coord[0]][coord[1]] == " " and pos in self.posibilities[coord[0]][coord[1]]:
                                alone = False
                                break
                        if alone:
                            self.set_value(row, col, pos)
                            change = True
                            break
        return change


    def find_group_subsets(self):
        self.print("starting to find subset")
        pair_contributors = []
        did_something = False
        for group_type in (self.rows, self.cols, self.sqrs):
            for superset in group_type:
                for subset in superset:
                    vec_with_posses = sorted([(vec, self.posibilities[vec[0]][vec[1]]) for vec in subset
                                           if len(self.posibilities[vec[0]][vec[1]]) > 1],
                                          key=lambda x: len(x[1]))
                    for posibility in vec_with_posses:
                        vecs = [posibility[0]]
                        total_posibilities = set(posibility[1])

                        other_vec_with_posses = sorted([v for v in vec_with_posses if v != posibility], key=lambda x: len(x[1].difference(total_posibilities)))
                        for other_posibility in other_vec_with_posses:
                            if len(other_posibility[1].difference(total_posibilities)) <= 1:
                                vecs.append(other_posibility[0])
                                total_posibilities = total_posibilities.union(other_posibility[1])
                                if len(vecs) >= len(total_posibilities):
                                    if len(total_posibilities) == 2:
                                        pair_contributors.append(vecs)
                                    for pos in set(subset).difference(vecs):
                                        inter = self.posibilities[pos[0]][pos[1]].intersection(total_posibilities)
                                        if len(inter) > 0:
                                            print("removing (%s) from (%s,%s)" %(inter, pos[0], pos[1]))
                                            self.try_remove_posibilities(pos[0], pos[1], total_posibilities)
                                            # do not ask for sole posibilities it would already be before removing a posibility
                                            did_something = True
        if not did_something:
            self.print("start finding quantum pairs")
            pair_contributors = [sorted(v) for v in pair_contributors]
            for vecs1 in pair_contributors:
                not_vecs1 = [v for v in pair_contributors if v != vecs1]
                for vecs2 in not_vecs1:
                    posibilities = self.posibilities[vecs1[0][0]][vecs1[0][1]]

                    if posibilities == self.posibilities[vecs2[0][0]][vecs2[0][1]]:
                        combined = vecs1 + vecs2
                        rows = {v[0] for v in combined}
                        cols = {v[1] for v in combined}
                        if len(cols) == 2:
                            print("there is a quantum pair for %s: %s" % (posibilities, combined))
                            for r in rows:
                                for c in range(9):
                                    if (r, c) not in combined:
                                        inter = self.posibilities[r][c].intersection(posibilities)
                                        if len(inter) > 0:
                                            print("removing (%s) from (%s,%s)" %(inter, r, c))
                                            self.try_remove_posibilities(r, c, posibilities)
                                            did_something = True
                        if len(rows) == 2:
                            print("there is a quantum pair for %s: %s" % (posibilities, combined))
                            for r in range(9):
                                for c in cols:
                                    if (r, c) not in combined:
                                        other = self.posibilities[r][c]
                                        print(other)
                                        inter = other.intersection(posibilities)
                                        if len(inter) > 0:
                                            print("removing (%s) from (%s,%s)" %(inter, r, c))
                                            self.try_remove_posibilities(r, c, posibilities)
                                            did_something = True
                            #  print("col %s: %s in rows
        if not did_something:
            self.print("start finding quantum trios")
            pair_contributors = [sorted(v) for v in pair_contributors]
            for vecs1 in pair_contributors:
                not_vecs1 = [v for v in pair_contributors if v != vecs1]
                for vecs2 in not_vecs1:
                    not_vecs2 = [v for v in not_vecs1 if v != vecs2]
                    for vecs3 in not_vecs2:
                        pass # find y wing
        return did_something

    def set_value(self, row, col, val):
        if self.board[row][col] == " ":
            self.board[row][col] = val
            if val != " ":
                self.posibilities[row][col] = {val}
                for a in self.affecting[row][col]:
                    if self.board[a[0]][a[1]] == val:
                        raise Exception
                    self.try_remove_posibilities(a[0], a[1], self.posibilities[row][col])
                self.print("inserted %s to (%s,%s)" % (val, row, col))

    def try_remove_posibilities(self, row, col, vals):
        p = self.posibilities[row][col]
        if len(p) > 1:
            p -= vals
            if len(p) == 1:
                self.set_value(row,col, list(p)[0])

    def print(self, msg = ""):
        print("%s\n" % msg)
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
