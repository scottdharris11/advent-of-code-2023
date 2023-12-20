from math import lcm
from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 20", "Part 1")
def solve_part1(lines: list):
    modules = create_modules(lines)
    high_cnt = 0
    low_cnt = 0
    for _ in range(1000):
        queue = [Pulse("button", "broadcaster", LOW_PULSE)]
        while len(queue) != 0:
            pulse = queue[0]
            if pulse.ptype == HIGH_PULSE:
                high_cnt += 1
            else:
                low_cnt += 1
            queue.extend(modules[pulse.to_id].process_pulse(pulse))
            queue.pop(0)
    return high_cnt * low_cnt

@Runner("Day 20", "Part 2")
def solve_part2(lines: list):
    modules = create_modules(lines)
    
    # register sniffer modules to track inputs into last module
    # before output which is a conjunction module
    sniffers = []
    for input in modules["rx"].inputs[0].inputs:
        sm = SnifferModule(input.id + "-sniffer")
        modules[sm.id] = sm
        sniffers.append(sm)
        input.add_destination(sm)
        print(input)
        
    # run cycles until we find the min cycle for each sniffer
    # where it produced saw high output
    cycle_cnt = 0
    sniffer_checks = {}
    while True:
        cycle_cnt += 1
        queue = [Pulse("button", "broadcaster", LOW_PULSE)]
        while len(queue) != 0:
            pulse = queue[0]
            queue.extend(modules[pulse.to_id].process_pulse(pulse))
            queue.pop(0)
        
        done = True
        for s in sniffers:
            if cycle_cnt == 1:
                s.sent_high = False
            elif s.sent_high and s.id not in sniffer_checks:
                print((s.id, cycle_cnt))
                sniffer_checks[s.id] = cycle_cnt
            if s.id not in sniffer_checks:
                done = False
            
        if done:
            break
    
    # least common multiple of sniffer values is convergence point
    return lcm(*sniffer_checks.values())

HIGH_PULSE = 1
LOW_PULSE = 0

class Pulse:
    def __init__(self, from_id: str, to_id: str, ptype: int) -> None:
        self.from_id = from_id
        self.to_id = to_id
        self.ptype = ptype
        
    def __repr__(self) -> str:
        return str((self.from_id, self.to_id, self.ptype))
        
class Module:
    def __init__(self, id: str) -> None:
        self.id = id
        self.inputs = []
        self.dest = []
        
    def __repr__(self) -> str:
        iids = []
        for i in self.inputs:
            iids.append(i.id)    
        dids = []
        for d in self.dest:
            dids.append(d.id)
        return ", ".join(iids) + " -> " + self.id + " -> " + ", ".join(dids)
            
    def add_destination(self, d: "Module") -> None:
        self.dest.append(d)
    
    def add_input(self, i: "Module") -> None:
        self.inputs.append(i)
        
    def send_pulse(self, ptype: int) -> list[Pulse]:
        out = []
        for d in self.dest:
            out.append(Pulse(self.id, d.id, ptype))
        return out
    
    def process_pulse(self, _: Pulse) -> list[Pulse]:
        return []
    
class FlipFlopModule(Module):
    def __init__(self, id: str) -> None:
        super().__init__(id)
        self.on = False
    
    def __repr__(self) -> str:
        return super().__repr__() + ": " + str(self.on)
        
    def process_pulse(self, pulse: Pulse) -> list[Pulse]:
        if pulse.ptype == HIGH_PULSE:
            return []
        self.on = not self.on
        send = LOW_PULSE
        if self.on:
            send = HIGH_PULSE
        return super().send_pulse(send)

class ConjunctionModule(Module):
    def __init__(self, id: str) -> None:
        super().__init__(id)
        self.last = {}
        
    def __repr__(self) -> str:
        return super().__repr__() + ": " + str(self.last)
    
    def add_input(self, i: "Module") -> None:
        self.last[i.id] = LOW_PULSE
        super().add_input(i)
    
    def process_pulse(self, pulse: Pulse) -> list[Pulse]:
        self.last[pulse.from_id] = pulse.ptype
        send = LOW_PULSE
        for l in self.last.values():
            if l == LOW_PULSE:
                send = HIGH_PULSE
                break
        return super().send_pulse(send)

class BroadcastModule(Module):
    def process_pulse(self, pulse: Pulse) -> list[Pulse]:
        return super().send_pulse(pulse.ptype)

class OutputModule(Module):
    pass

class SnifferModule(Module):
    def __init__(self, id: str) -> None:
        super().__init__(id)
        self.sent_high = False
        
    def process_pulse(self, pulse: Pulse) -> list[Pulse]:
        self.sent_high = pulse.ptype == HIGH_PULSE
        return []

def create_modules(lines: list[str]) -> dict[str,Module]:
    modules = {}
    for line in lines:
        id = line.split()[0]
        if id == "broadcaster":
            modules[id] = BroadcastModule(id)
        elif id[0] == "%":
            modules[id[1:]] = FlipFlopModule(id[1:])
        elif id[0] == "&":
            modules[id[1:]] = ConjunctionModule(id[1:])
    
    for line in lines:
        pieces = line.split()
        id = pieces[0]
        if id[0] == "%" or id[0] == "&":
            id = id[1:]
        for d in pieces[2:]:
            d = d.replace(",", "")
            if d not in modules:
                modules[d] = OutputModule(d)
            modules[id].add_destination(modules[d])
            modules[d].add_input(modules[id])
    
    return modules

# Part 1
input = read_lines("input/day20/input.txt")
sample = read_lines("input/day20/sample.txt")
sample2 = read_lines("input/day20/sample2.txt")

value = solve_part1(sample)
assert(value == 32000000)
value = solve_part1(sample2)
assert(value == 11687500)
value = solve_part1(input)
assert(value == 818723272)

# Part 2
value = solve_part2(sample2)
assert(value == 15)
value = solve_part2(input)
assert(value == -1)
