from ..problem import Problem
from ..datastructures.queue import Queue


def get_solver_mapping():
    return dict(dfs=DFS)


class DFS(object):
    def solve(self, problem: Problem):

        stk = [problem.get_start_node()]

        visited = set()
        visited.add(problem.get_start_node())

        while stk:
            node = stk.pop()

            if problem.is_end(node):
                return node

            unvisited = [child for child in problem.successors(node) if child not in visited]
            unvisited.reverse()

            for child in unvisited:
                visited.add(child)
                stk.append(child)

        return None
