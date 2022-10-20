def get_groups(row, col, direction):
    out = set()
    if direction == "row":
        out = out.union([(row, c) for c in range(9)])
    if direction == "col":
        out = out.union([(r, col) for r in range(9)])
    if direction == "sqr":
        start_r = row - row%3
        start_c = col - col%3
        for r in range(start_r, start_r + 3):
            out = out.union([(r, c) for c in range(start_c, start_c + 3)])

    return out


def get_affecting(row, col):
    out = set()
    for direction in ("row", "col", "sqr"):
        out = out.union(get_groups(row, col, direction))
    out -= {(row, col)}
    return out

