from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 25", "Part 1")
def solve_part1(lines: list[str]):
    cgraph = parse_components(lines)
    cgroups = cgraph.component_groups()
    return len(cgroups[0]) * len(cgroups[1])

@Runner("Day 25", "Part 2")
def solve_part2(lines: list):
    return None

class Component:
    def __init__(self, id: str) -> None:
        self.id = id
        self.connections = set()
    
    def __repr__(self) -> str:
        return str((self.id, self.connections))

class ComponentGraph:
    def __init__(self) -> None:
        self.graph = {}
        self.time = 0
    
    def add_connection(self, a: str, b: str) -> None:
        if a not in self.graph:
            self.graph[a] = Component(a)
        if b not in self.graph:
            self.graph[b] = Component(b)
        self.graph[a].connections.add(b)
        self.graph[b].connections.add(a)
    
    def component_groups(self) -> list[set[str]]:
        # for each component, attempt to find path from control component to it
        # four different times, each successive time blocking the path previously
        # found.  theory is if we can find it the fourth time, then it didn't need
        # to traverse the node connections between groups, and therefore that node
        # is part of the left side group (with the control)
        lgroup = set()
        rgroup = set()
        control = list(self.graph.keys())[0]
        lgroup.add(control)
        for comp in self.graph.keys():
            if comp == control:
                continue
            left = True
            blocked = set()
            for _ in range(4):
                path = self.__bfs(control, comp, blocked)
                if path == None:
                    left = False
                    break
                for i in range(0, len(path)-1):
                    blocked.add((path[i], path[i+1]))
            if left:
                lgroup.add(comp)
            else:
                rgroup.add(comp)
        return (lgroup, rgroup)

    def __bfs(self, c: str, goal: str, blocked: set[tuple[str]]) -> list[str]:
        queue = []
        queue.append(tuple([c]))
        visited = set()
        while len(queue) > 0:
            p = queue.pop(0)
            c = p[-1]
            visited.add(c)
            if c == goal:
                return p
            for conn in self.graph[c].connections:
                if conn in visited:
                    continue
                comp2conn = (c, conn)
                conn2comp = (conn, c)
                if comp2conn in blocked or conn2comp in blocked:
                    continue
                queue.append(tuple([*p, conn]))
        return None

def parse_components(lines) -> ComponentGraph:
    cgraph = ComponentGraph()
    for line in lines:
        k, connections = line.split(":")
        for c in connections.lstrip().rstrip().split(" "):
            cgraph.add_connection(k, c)
    return cgraph

# Part 1
input = read_lines("input/day25/input.txt")
sample = read_lines("input/day25/sample.txt")

value = solve_part1(sample)
assert(value == 54)
value = solve_part1(input)
assert(value == 552695)

# Part 2
value = solve_part2(sample)
assert(value == None)
value = solve_part2(input)
assert(value == None)
