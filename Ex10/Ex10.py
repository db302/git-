#!usr/bin/env python
import random
import timeit


class Node:
    """ Implements a node of linked list and binary tree
    """
    def __init__(self, key=None, value=None, nextNode=None, prevNode=None):
        # if not type(key) == int:
        #     raise TypeError("Key musst be int")
        # if not type(value) == str:
        #     raise TypeError("Value musst be str")
        self.key = key
        self.value = value
        self.nextNode = nextNode
        self.prevNode = prevNode
        self.parent = None
        self.lChild = None
        self.rChild = None

    def __repr__(self):
        return str(self.key)


class BinarySearchTree:
    """ Class for implementing binary search tree
    >>> bst = BinarySearchTree()
    >>> bst.treedepth()
    0
    >>> bst.to_string()
    'null'
    >>> bst.insert(Node(4, "b"))
    >>> bst.treedepth()
    1
    >>> bst.insert(Node(2, "a"))
    >>> bst.treedepth()
    2
    >>> bst.insert(Node(7, "e"))
    >>> bst.treedepth()
    2
    >>> bst.insert(Node(9, "d"))
    >>> bst.treedepth()
    3
    >>> bst.insert(Node(6, "c"))
    >>> bst.treedepth()
    3
    >>> bst.to_string()
    '[(4, "b"), left: [(2, "a"), left: null, right: null], right: \
[(7, "e"), left: [(6, "c"), left: null, right: null], right: \
[(9, "d"), left: null, right: null]]]'
    >>> bst.lookup(6).value
    'c'
    """
    def __init__(self):
        self.itemCount = 0
        self.head = Node()
        self.last = self.head
        self.root = None
        self.depth = 0

    def treedepth(self):
        return self.depth

    def lookup(self, key):
        if not type(key) == int:
            raise TypeError("Key musst be int")
        if self.root is None:
            returnValue = None
        else:
            current = self.root
            lookupCompleted = 0
            while not lookupCompleted:  # search trough the binary tree
                if current.key == key:  # key found
                    returnValue = current
                    lookupCompleted = 1
                else:
                    # search in the right path of current node
                    if key > current.key:
                        # leaf reached, key not found
                        if current.rChild is None:
                            returnValue = None
                            lookupCompleted = 1
                        else:  # search a level lower
                            current = current.rChild
                    else:  # search in the left path of current node
                        # leaf reached, key not found
                        if current.lChild is None:
                            returnValue = None
                            lookupCompleted = 1
                        else:  # search a level lower
                            current = current.lChild
        return returnValue

    def insert(self, node):
        # print(node)
        # Check for type of node, wont work...
        # if type(node).__name__ is not "Node":
        #    raise TypeError("node musst be Node")
        level = 1
        if self.root is None:
            self.root = node
            self.last = node
            self.head.nextNode = node
        else:
            current = self.root
            lookupCompleted = 0
            while not lookupCompleted:  # search trough the binary tree
                if node.key == current.key:  # key found
                    current.value = node.value
                    lookupCompleted = 1
                else:
                    level += 1
                    # search in the right path of current node
                    if node.key > current.key:
                        # leaf reached, key not found
                        if current.rChild is None:
                            current.rChild = node
                            node.parent = current
                            node.nextNode = current
                            node.prevNode = current.prevNode
                            current.prevNode = node
                            current.prevNode.nextNode = node
                            lookupCompleted = 1
                        else:  # search a level lower
                            current = current.rChild
                    else:  # search in the left path of current node
                        # leaf reached, key not found
                        if current.lChild is None:
                            current.lChild = node
                            node.parent = current
                            node.nextNode = current.nextNode
                            node.prevNode = current
                            current.nextNode = node
                            current.nextNode.prevNode = node
                            lookupCompleted = 1
                        else:  # search a level lower
                            current = current.lChild
        self.itemCount += 1
        self.depth = max(level, self.depth)

    def to_string(self):
        if self.root is not None:
            output = ""
            output = self._node_to_string(self.root, output)
        else:
            output = "null"
        return output

    def _node_to_string(self, node, output):
        output += "[(" + str(node.key) + ", \"" + \
                    str(node.value) + "\"), left: "
        if node.lChild is None:
            output += "null"
        else:
            output = self._node_to_string(node.lChild, output)
        output += ", right: "
        if node.rChild is None:
            output += "null"
        else:
            output = self._node_to_string(node.rChild, output)
        output += "]"
        # print(output)
        return output

if __name__ == "__main__":
    rt1 = []
    rt2 = []
    d1 = []
    d2 = []
    nlist = []
    for i in range(10, 16+1):
        n = 2**i
        nlist.append(n)
        lst1 = []
        lst2 = []
        for j in range(1, n+1):
            lst1.append(j)
        # print(len(lst1))
        lst2[:] = lst1[:]
        random.shuffle(lst2)
        # print(len(lst2))
        # print(lst1)
        # print(lst2)
        bst1 = BinarySearchTree()
        bst2 = BinarySearchTree()
        rt1.append(timeit.timeit('while len(lst1) >  0: \
                    bst1.insert(Node(lst1.pop()))', "from \
                    __main__ import lst1, bst1, Node", number=1))
        # print(bst1.to_string())
        d1.append(bst1.treedepth())
        rt2.append(timeit.timeit('while len(lst2) >  0: \
                    bst2.insert(Node(lst2.pop()))', "from \
                    __main__ import lst2, bst2, Node", number=1))
        # print(bst2.to_string())
        d2.append(bst2.treedepth())
    for k in range(len(nlist)):
        print("Runtime:")
        print(nlist[k], rt1[k], rt2[k])
        print("Depth:")
        print(nlist[k], d1[k], d2[k])
