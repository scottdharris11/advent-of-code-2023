class PriorityQueue:
    def __init__(self) -> None:
        self.items = []
	
    def empty(self) -> bool:
        return len(self.items) == 0
 
    def next(self) -> any:
        n = len(self.items) - 1
        next = self.items[n]
        self.items = self.items[:n]
        return next[0]
    
    def queue(self, obj: any, priority: int):
        qi = (obj, priority)
        
        idx = -1
        for i, item in enumerate(self.items):
            if item[1] < priority:
                idx = i
                break
        
        if idx == -1:
            self.items.append(qi)
        else:
            self.items.insert(idx, qi)

class SearchMove:
    def __init__(self, cost: int, state) -> None:
        self.cost = cost
        self.state = state
    
    def __repr__(self) -> str:
        return str((self.cost, self.state))
        
class Searcher:
    def is_goal(self, obj) -> bool:
        return True
    
    def possible_moves(self, obj) -> list[SearchMove]:
        return []
    
    def distance_from_goal(self, obj) -> int:
        return 0

class SearchSolution:
    def __init__(self, cost: int, path) -> None:
        self.cost = cost
        self.path = path
    
    def __repr__(self) -> str:
        return str((self.cost, self.path))

class Search:
    def __init__(self, searcher: Searcher) -> None:
        self.searcher = searcher
       
    # utilize a-star search approach to find the path to the goal
    # with the lowest cost. 
    def best(self, init: SearchMove) -> SearchSolution:
        q = PriorityQueue()
        q.queue(init.state, init.cost)
        cost = {init.state: init.cost}
        from_state = {}
        goal = None
        while not q.empty():
            current = q.next()
            if self.searcher.is_goal(current):
                goal = current
                break
            
            for move in self.searcher.possible_moves(current):
                nCost = cost[current] + move.cost
                cCost = cost.get(move.state, -1)
                if cCost == -1 or nCost < cCost:
                    cost[move.state] = nCost
                    priority = nCost + self.searcher.distance_from_goal(move.state)
                    q.queue(move.state, priority)
                    from_state[move.state] = current
     
        if goal == None:
            return None

        path = [goal]
        current = goal
        while current != init.state:
            current = from_state[current]
            path.insert(0, current)
        
        return SearchSolution(cost[goal], path)
