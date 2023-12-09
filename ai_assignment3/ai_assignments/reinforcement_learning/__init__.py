from .q_learning import QLearning
from .. import register_reinforcement_learning_method

register_reinforcement_learning_method('q_learning', QLearning)
