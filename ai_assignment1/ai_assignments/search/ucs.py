from ..problem import Problem
from ..datastructures.priority_queue import PriorityQueue


def get_solver_mapping():
    return dict(ucs=UCS)


class UCS(object):
    def solve(self, problem: Problem):

        pq = PriorityQueue()
        pq.put(problem.get_start_node().cost, problem.get_start_node())

        visited = set()

        while pq:
            node = pq.get()

            if problem.is_end(node):
                return node

            if node not in visited:
                visited.add(node)
                for child in problem.successors(node):
                    if child not in visited:
                        pq.put(child.cost + node.cost, child)

        return None
