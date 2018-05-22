class Node:
    """
    A node fot binary decision tree
    """
    def __init__(self, value=None):
        self.data = value
        self.children = []