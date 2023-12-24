from math import lcm
from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 20", "Part 1")
def solve_part1(lines: list):
    modules = create_modules(lines)
    return run_cyles(modules, 1000)

@Runner("Day 20", "Part 2")
def solve_part2(lines: list, id: str):
    modules = create_modules(lines)
    
    # register sniffer modules to track high pulse cycle
    # outputs from feeders to supplied module id
    sniffers = []
    for i in modules[id].inputs:
        s = SnifferModule(i.id+"-sniffer")
        sniffers.append(s)
        modules[i.id].add_destination(s)
    for s in sniffers:
        modules[s.id] = s
    
    # run some cycles and then multiply the high
    # cycle counts together to find the convergence point
    run_cyles(modules, 10000)
    converge = 1
    for s in sniffers:
        converge *= s.high_cycles[0]
    return converge

HIGH_PULSE = 1
LOW_PULSE = 0

class Pulse:
    def __init__(self, from_id: str, to_id: str, ptype: int, cycle: int) -> None:
        self.from_id = from_id
        self.to_id = to_id
        self.ptype = ptype
        self.cycle = cycle
        
    def __repr__(self) -> str:
        return str((self.from_id, self.to_id, self.ptype, self.cycle))
        
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
        
    def send_pulse(self, ptype: int, cycle: int) -> list[Pulse]:
        out = []
        for d in self.dest:
            out.append(Pulse(self.id, d.id, ptype, cycle))
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
        return super().send_pulse(send, pulse.cycle)
    
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
        return super().send_pulse(send, pulse.cycle)

class BroadcastModule(Module):
    def process_pulse(self, pulse: Pulse) -> list[Pulse]:
        return super().send_pulse(pulse.ptype, pulse.cycle)

class OutputModule(Module):
    pass

class SnifferModule(Module):
    def __init__(self, id: str) -> None:
        super().__init__(id)
        self.called = 0
        self.high = 0
        self.low = 0
        self.high_cycles = []
    
    def __repr__(self) -> str:
        return str((self.id, self.called, self.high, self.low, self.high_cycles))
    
    def process_pulse(self, pulse: Pulse) -> list[Pulse]:
        self.called += 1
        if pulse.ptype == HIGH_PULSE:
            self.high += 1
            self.high_cycles.append(pulse.cycle)
        else:
            self.low += 1
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

def run_cyles(modules: list[Module], cycles: int) -> int:
    high_cnt = 0
    low_cnt = 0
    for i in range(cycles):
        queue = [Pulse("button", "broadcaster", LOW_PULSE, i+1)]
        while len(queue) != 0:
            pulse = queue[0]
            if pulse.ptype == HIGH_PULSE:
                high_cnt += 1
            else:
                low_cnt += 1
            queue.extend(modules[pulse.to_id].process_pulse(pulse))
            queue.pop(0)
    return high_cnt * low_cnt
    
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
value = solve_part2(input, "cn")
assert(value == 243902373381257)
