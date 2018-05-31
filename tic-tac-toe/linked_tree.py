from node import Node


class LinkedTree:
    """
    Linked tree data structure.
    """
    def __init__(self, root_data=None):
        self._root = Node(root_data)

    def __iter__(self):
        """Iterate through all tree elements."""
        data = []

        def recurse(tree):
            if tree.get_root_val() is not None:
                data.append(tree.get_root().data)
            for child in tree.children():
                recurse(child)

        recurse(self)
        for i in data:
            yield i

    def add(self, item):
        """
        item: data for node of the tree
        """
        self._root.children.append(LinkedTree(item))

    def children(self):
        return self._root.children

    def get_root_val(self):
        return self._root

