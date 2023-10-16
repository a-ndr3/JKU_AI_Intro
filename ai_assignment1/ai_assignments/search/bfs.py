from .. problem import Problem
from .. datastructures.queue import Queue


# please ignore this
def get_solver_mapping():
    return dict(bfs=BFS)


class BFS(object):
    def solve(self, problem: Problem):

        queue = Queue()
        queue.put(problem.get_start_node())

        visited = set()
        visited.add(problem.get_start_node())

        while queue:
            node = queue.get()

            if problem.is_end(node):
                return node

            for child in problem.successors(node):
                if child not in visited:
                    visited.add(child)
                    queue.put(child)

        return None
