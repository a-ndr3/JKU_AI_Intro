import numpy as np
from ai_assignment4.ai_assignments.datastructures.queue import Queue
from ai_assignment4.ai_assignments.decision_tree.dt_node import DecisionTreeNodeBase
from scipy.stats import entropy as sci_entropy

def entropy(y):
    '''Takes in list y and computes its entropy.'''
    positive = sum(y) / len(y)
    negative = 1 - positive
    return sci_entropy([positive, negative], base=2)

def unique_unsorted(L):
    '''Takes in list L and returns its unique values, keeping their order.'''
    _, indeces = np.unique(L, return_index=True)
    return [L[index] for index in sorted(indeces)]

class DecisionTreeNode(DecisionTreeNodeBase):
    def __init__(self, features, labels):
        super().__init__()
        self.features = features
        self.labels = labels

        if self.features is not None and self.labels is not None:
            self.split()

    def get_all_possible_split_points(self):
        nr_samples, nr_features = self.features.shape
        split_points = []
        for f_idx in range(nr_features):
            idx_sort = self.features[:, f_idx].argsort()
            sorted_features = self.features[idx_sort, :]
            sorted_labels = self.labels[idx_sort]

            for i in range(1, nr_samples):
                if sorted_features[i, f_idx] != sorted_features[i - 1, f_idx] and sorted_labels[i] != sorted_labels[i - 1]:
                    split_at = (sorted_features[i, f_idx] + sorted_features[i - 1, f_idx]) / 2
                    split_points.append((f_idx, split_at))

        return split_points

    def get_optimal_split_point(self):
        split_feature, split_point = None, None
        max_info_gain = -np.inf

        all_possible_splits = self.get_all_possible_split_points()

        for f_idx, point in all_possible_splits:
            info_gain = self.compute_information_gain(self.features[:, f_idx], point)

            if info_gain > max_info_gain:
                max_info_gain = info_gain
                split_feature, split_point = f_idx, point

        return split_feature, split_point

    def compute_information_gain(self, x, split_point):
        '''computes the information gain for a given feature x and the given split_point'''

        labels_left_branch = self.labels[x <= split_point]
        labels_right_branch = self.labels[x > split_point]

        weight_left = len(labels_left_branch) / len(x)
        weight_right = len(labels_right_branch) / len(x)

        e_data = entropy(self.labels)
        e_right = entropy(labels_right_branch)
        e_left = entropy(labels_left_branch)
        return e_data - (weight_left * e_left + weight_right * e_right)

    def split(self):
        unique_labels = unique_unsorted(self.labels)
        if len(unique_labels) == 1:
            self.label = unique_labels[0]
            return

        split_feature, split_point = self.get_optimal_split_point()

        if split_feature is not None and split_point is not None:
            left_indices = self.features[:, split_feature] <= split_point
            right_indices = self.features[:, split_feature] > split_point

            left_features, left_labels = self.features[left_indices], self.labels[left_indices]
            right_features, right_labels = self.features[right_indices], self.labels[right_indices]

            self.left_child = DecisionTreeNode(left_features, left_labels)
            self.right_child = DecisionTreeNode(right_features, right_labels)


class ID3():
    def __init__(self):
        self.root = None

    def fit(self, X, y):
        self.root = DecisionTreeNode(X, y)
        return self

    def __str__(self):
        return str(self.root)
    
    def get_height(self, node):
        if node is None:
            return 0
        return max(self.get_height(node.left_child), self.get_height(node.right_child)) + 1
    
    def print_decision_tree(self):
        height = self.get_height(self.root)
        visited = set()
        frontier = Queue()

        lines = ['']

        previous_level = 1
        frontier.put((self.root, 1))

        while frontier.has_elements():
            current, level = frontier.get()
            if level > previous_level:
                lines.append('')
                previous_level = level
            lines[-1] += current.print_node(height, level)
            if current not in visited:
                visited.add(current)
                if current.left_child is not None:
                    frontier.put((current.left_child, level + 1))
                else:
                    if level < height: frontier.put((DecisionTreeNode(None, None), level + 1))
                if current.right_child is not None:
                    frontier.put((current.right_child, level + 1))
                else:
                    if level < height: frontier.put((DecisionTreeNode(None, None), level + 1))

        for line in lines:
            print(line)
        return None
