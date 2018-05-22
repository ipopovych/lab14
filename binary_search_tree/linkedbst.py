"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node is not None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """
        Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self.
        """
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right is None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left is None \
                and not currentNode.right is None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left is None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """
        Return the height of tree
        :return: int
        """

        def recheight(node):
            """
            Helper function
            :param top:
            :return:
            """
            if node is None:
                return 0
            else:
                return max(recheight(node.left), recheight(node.right)) + 1

        node = self._root
        return recheight(node) - 1

    def isBalanced(self):
        """
        Return True if tree is balanced
        """
        return self.height() < 2 * log(self._size, 2)

    def rangeFind(self, low, high):
        """
        Returns a list of the items in the tree, where low <= item <= high.
        """
        elems = []

        def recurse(current, low, high):
            if current is None:
                return elems
            if low < current.data:
                recurse(current.left, low, high)

            if low <= current.data <= high:
                elems.append(current.data)

            if high > current.data:
                recurse(current.right, low, high)

        recurse(self._root, low, high)
        return elems

    def rebalance(self):
        """
        Rebalances the tree.
        """
        lst = sorted([item for item in self])
        self.clear()
        while len(lst) != 0:
                self.add(lst.pop((len(lst) - 1) // 2))

    def rebalanced(self):
        """
        Returns rebalanced version of the tree.
        """
        lst = sorted([item for item in self])
        temp = LinkedBST()
        while len(lst) != 0:
            temp.add(lst.pop((len(lst) - 1) // 2))
        return temp

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        """
        def go_left(current, item):
            next = current.left
            if next is None or next.data <= item:
                return current.data
            elif next.data > item:
                return go_left(next, item)

        def go_right(current, item):
            next = current.right
            if next is None:
                return None
            elif next.data <= item:
                return go_right(next, item)
            elif next.data > item:
                return next.data

        # working with temporary created rebalanced version of current tree
        tree = self.rebalanced()
        current = tree._root
        if current.data > item:
            return go_left(current, item)
        elif current.data <= item:
            return go_right(current, item)

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        """
        def go_left(current, item):
            next = current.left
            if next is None:
                return None
            elif next.data < item:
                return next.data
            elif next.data >= item:
                return go_left(next, item)

        def go_right(current, item):
            next = current.right
            if next is None or next.data >= item:
                return current.data
            elif next.data < item:
                return go_right(next, item)

        tree = self.rebalanced()
        current = tree._root
        if current.data < item:
            return go_right(current, item)
        elif current.data >= item:
            return go_left(current, item)
