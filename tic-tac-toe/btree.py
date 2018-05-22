from btnode import Node


class BTree:
    """
    Binary decision tree data structure
    """
    def __init__(self, root=None):
        self._root = root

    def __iter__(self):
        data = []

        def recurse(node):
            if node is not None:
                data.append(node.data)
            for child in node.children:
                recurse(child)

        return (yield i for i in data)

    def add(self, item):
        """
        item: node for the tree
        """
        self._root.children.append(BTree(item))

