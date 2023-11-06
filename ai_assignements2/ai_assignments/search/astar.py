import math
from ..problem import Problem
from ..datastructures.priority_queue import PriorityQueue


# please ignore this
def get_solver_mapping():
    return dict(
        astar_ec=ASTAR_Euclidean,
        astar_mh=ASTAR_Manhattan
    )


class ASTAR(object):
    def solve(self, problem: Problem):

        goal = problem.get_end_node()
        start = problem.get_start_node()

        pq = PriorityQueue()
        pq.put(0, start)

        costSoFar = {start: ASTAR_Manhattan().heuristic(start, goal)}

        visited = set()

        while pq:
            node = pq.get()
            visited.add(node)

            if problem.is_end(node):
                return node

            for child in problem.successors(node):
                if child not in visited:
                    g = child.cost
                    h = ASTAR_Manhattan().heuristic(child, goal)
                    newcost = g + h

                    if child not in costSoFar or child.cost < costSoFar.get(child):
                        costSoFar[child] = child.cost
                        pq.put(newcost, child)

        return None


# please note that in an ideal world, the heuristics should actually be part
# of the problem definition, as it assumes domain knowledge about the structure
# of the problem, and defines a distance to the goal state


# this is the ASTAR variant with the euclidean distance as a heuristic
# it is registered as a solver with the name 'astar_ec'
class ASTAR_Euclidean(ASTAR):
    def heuristic(self, current, goal):
        cy, cx = current.state
        gy, gx = goal.state
        return math.sqrt((cy - gy) ** 2 + (cx - gx) ** 2)


# this is the ASTAR variant with the manhattan distance as a heuristic
# it is registered as a solver with the name 'astar_mh'
class ASTAR_Manhattan(ASTAR):
    def heuristic(self, current, goal):
        cy, cx = current.state
        gy, gx = goal.state
        return math.fabs((cy - gy)) + math.fabs(cx - gx)
