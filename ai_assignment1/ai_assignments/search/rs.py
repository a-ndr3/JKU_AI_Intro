from .. problem import Problem
import random


# please ignore this
def get_solver_mapping():
    return dict(rs=RS)


class RS(object):
 def solve(self, problem : Problem):
    random.seed(1234)
    current = problem.get_start_node()
    while not problem.is_end(current):
        nodes = problem.successors(current)
        current = random.choice(nodes)
    return current
