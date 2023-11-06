import math
from .. problem import Problem
from .. datastructures.priority_queue import PriorityQueue


# please ignore this
def get_solver_mapping():
    return dict(
        gbfs_mh=GBFS_Manhattan,
        gbfs_ch=GBFS_Chebyshev
    )


class GBFS(object):
    def solve(self, problem: Problem):
     try:
        goal = problem.get_end_node()

        pq = PriorityQueue()
        pq.put(0, problem.get_start_node())

        visited = set()

        while pq:
            node = pq.get()
            visited.add(node)

            if problem.is_end(node):
                return node

            for child in problem.successors(node):
                if child not in visited:
                    pq.put(GBFS_Chebyshev().heuristic(child, goal), child)
     except Exception as e:
        print(e.with_traceback())
        return None


# please note that in an ideal world, the heuristics should actually be part
# of the problem definition, as it assumes domain knowledge about the structure
# of the problem, and defines a distance to the goal state


# this is the GBFS variant with the manhattan distance as a heuristic
# it is registered as a solver with the name 'gbfs_mh'
class GBFS_Manhattan(GBFS):
    def heuristic(self, current, goal):
        cy, cx = current.state
        gy, gx = goal.state
        return math.fabs((cy - gy)) + math.fabs(cx - gx)


# this is the GBFS variant with the chebyshev distance as a heuristic
# it is registered as a solver with the name 'gbfs_ch'
class GBFS_Chebyshev(GBFS):
    def heuristic(self, current, goal):
        cy, cx = current.state
        gy, gx = goal.state
        return max(math.fabs(cx - gx), math.fabs(cy - gy))
