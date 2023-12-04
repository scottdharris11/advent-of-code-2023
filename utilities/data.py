"""return lines from file in list minus new line characters"""
def read_lines(filename):
    lines = []
    with open(filename, "r") as handle:
        for line in handle:
            lines.append(line.rstrip())
    return lines

"""parse set of integers from line delimited by seperator"""
def parse_integers(line: str, seperator):
    """
    >>> parse_integers("10, 32, 44", ",")
    [10, 32, 44]
    """
    svalues = line.split(seperator)
    values = []
    for s in svalues:
        if s.strip() == "":
            continue
        values.append(int(s))
    return values

"""parse a grid of integers from the supplied lines"""
def parse_integer_grid(lines: list):
    """
    >>> parse_integer_grid(["1 3 5", "7 9 0", "3 2 6"])
    [[1, 3, 5], [7, 9, 0], [3, 2, 6]]
    """
    grid = []
    for l in lines:
        grid.append(parse_integers(l, " "))
    return grid
