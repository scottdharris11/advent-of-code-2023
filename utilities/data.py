def read_lines(filename):
    lines = []
    with open(filename, "r") as handle:
        for line in handle:
            lines.append(line.rstrip())
    return lines
