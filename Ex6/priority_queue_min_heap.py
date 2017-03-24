#!/usr/bin/python3
import math


class PriorityQueueItem:
    """ Provides a handle for a queue item.
    A simple class implementing a key-value pair,
    where the key is an integer, and the value can
    be an arbitrary object. Index is the heap array
    index of the item.
    """
    def __init__(self, key, value, index):
        self._key = key
        self._value = value
        self._index = index

    def __lt__(self, other):
        """ Enables us to compare two items with a < b.
        The __lt__ method defines the behavior of the
        < (less than) operator when applied to two
        objects of this class. When using the code a < b,
        a.__lt__(b) gets evaluated.
        There are many other such special methods in Python.
        See "python operator overloading" for more details.
        """
        return self._key < other._key

    def __gt__(self, other):
        return self._key > other._key

    def get_heap_index(self):
        """ Return heap index of item."""
        return self._index

    def set_heap_index(self, index):
        """ Update heap index of item."""
        self._index = index


class PriorityQueueMinHeap:
    """Priority queue implemented as min heap."""

    def __init__(self):
        """Create a new empty Priority Queue.
        >>> pqmh = PriorityQueueMinHeap()
        >>> type(pqmh._list) is list
        True
        >>> len(pqmh._list)
        0
        """
        self._list = []

    """
    TO DO:
    Create methods:
    insert(self, key, value) -> return inserted item object
    get_min(self) -> return item._key and item._value
    delete_min(self) -> return item._key an item._value
    change_key(item, new_key), no return value
    size() -> return current heap size

    Plus your choice of additional helper (private) methods
    Helpful would be e.g.
    _repair_heap_up(), _repair_heap_down(), _swap_items() ...

    Use private methods (_method_name) if they only get accessed within the
    class.
    Private methods have a leading underscore:
    def _swap_items(self, i, j):
        # Swap items with indices i,j (also swap their indices!)
        ...

    """

    def insert(self, key, value):
        """
        >>> pqmh = PriorityQueueMinHeap()
        >>> a = PriorityQueueItem(100, "A", 0)
        >>> pqmh._list.append(a)
        >>> b = PriorityQueueItem(1000, "B", 1)
        >>> pqmh._list.append(b)
        >>> c = PriorityQueueItem(10000, "C", 2)
        >>> pqmh._list.append(c)
        >>> pqmh.insert(10, "D")
        >>> print(pqmh._list[0]._key)
        10
        >>> print(pqmh._list[1]._key)
        100
        >>> print(pqmh._list[2]._key)
        10000
        >>> print(pqmh._list[3]._key)
        1000
        """
        index = len(self._list)
        item = PriorityQueueItem(key, value, index)
        self._list.append(item)
        self._repair_heap_up(index)

    def size(self):
        """
        >>> pqmh = PriorityQueueMinHeap()
        >>> a = PriorityQueueItem(10, "A", 0)
        >>> pqmh._list.append(a)
        >>> pqmh._list.append(a)
        >>> pqmh._list.append(a)
        >>> pqmh.size()
        3
        """
        return len(self._list)

    def get_min(self):
        """
        >>> pqmh = PriorityQueueMinHeap()
        >>> pqmh.get_min() is None
        True
        >>> pqmh.insert(100, "A")
        >>> pqmh.insert(1000, "B")
        >>> pqmh.insert(10000, "C")
        >>> pqmh.insert(10, "D")
        >>> pqmh.get_min()._key
        10
        >>> pqmh.get_min()._value
        'D'
        >>> pqmh.get_min()._index
        0
        """
        if len(self._list) > 0:
            return self._list[0]
        else:
            return None

    def delete_min(self):
        """
        >>> pqmh = PriorityQueueMinHeap()
        >>> a = PriorityQueueItem(1, "A", 0)
        >>> pqmh._list.append(a)
        >>> b = PriorityQueueItem(10, "B", 1)
        >>> pqmh._list.append(b)
        >>> c = PriorityQueueItem(100, "C", 2)
        >>> pqmh._list.append(c)
        >>> d = PriorityQueueItem(1000, "D", 3)
        >>> pqmh._list.append(d)
        >>> pqmh.delete_min()
        >>> len(pqmh._list)
        3
        >>> print(pqmh._list[0]._key)
        10
        >>> print(pqmh._list[1]._key)
        1000
        >>> print(pqmh._list[2]._key)
        100
        """
        self._swap_items(0, len(self._list) - 1)
        self._list.pop()
        self._repair_heap_down(0)

    def change_key(self, item, key):
        """
        >>> pqmh = PriorityQueueMinHeap()
        >>> a = PriorityQueueItem(10, "A", 0)
        >>> pqmh._list.append(a)
        >>> b = PriorityQueueItem(100, "B", 1)
        >>> pqmh._list.append(b)
        >>> c = PriorityQueueItem(1000, "C", 2)
        >>> pqmh._list.append(c)
        >>> d = PriorityQueueItem(10000, "D", 3)
        >>> pqmh._list.append(d)
        >>> pqmh.change_key(b, 5)
        >>> print(pqmh._list[0]._key)
        5
        >>> print(pqmh._list[1]._key)
        10
        >>> print(pqmh._list[2]._key)
        1000
        >>> print(pqmh._list[3]._key)
        10000
        >>> a = pqmh._list[1]
        >>> pqmh.change_key(a, 50000)
        >>> print(pqmh._list[0]._key)
        5
        >>> print(pqmh._list[1]._key)
        10000
        >>> print(pqmh._list[2]._key)
        1000
        >>> print(pqmh._list[3]._key)
        50000
        """
        index = item._index
        if (self._list[index]._key == item._key and
           self._list[index]._value == item._value):
            self._list[index]._key = key
            self._repair_heap_up(index)
            self._repair_heap_down(index)

    def _swap_items(self, i, j):
        """
        >>> a = PriorityQueueItem(10, "A", 0)
        >>> b = PriorityQueueItem(20, "B", 1)
        >>> pqmh = PriorityQueueMinHeap()
        >>> pqmh._list.append(a)
        >>> pqmh._list.append(b)
        >>> pqmh._swap_items(0, 1)
        >>> print(pqmh._list[0]._key)
        20
        >>> print(pqmh._list[0]._value)
        B
        >>> print(pqmh._list[0]._index)
        0
        >>> print(pqmh._list[1]._key)
        10
        >>> print(pqmh._list[1]._value)
        A
        >>> print(pqmh._list[1]._index)
        1
        """
        index_i = self._list[i].get_heap_index()
        index_j = self._list[j].get_heap_index()
        self._list[i], self._list[j] = self._list[j], self._list[i]
        self._list[j].set_heap_index(index_j)
        self._list[i].set_heap_index(index_i)

    def _repair_heap_up(self, index):
        """
        >>> pqmh = PriorityQueueMinHeap()
        >>> a = PriorityQueueItem(100, "A", 0)
        >>> pqmh._list.append(a)
        >>> b = PriorityQueueItem(1000, "B", 1)
        >>> pqmh._list.append(b)
        >>> c = PriorityQueueItem(10000, "C", 2)
        >>> pqmh._list.append(c)
        >>> d = PriorityQueueItem(10, "D", 3)
        >>> pqmh._list.append(d)
        >>> pqmh._repair_heap_up(3)
        >>> print(pqmh._list[0]._key)
        10
        >>> print(pqmh._list[1]._key)
        100
        >>> print(pqmh._list[2]._key)
        10000
        >>> print(pqmh._list[3]._key)
        1000
        """
        if len(self._list) > 1:
            parent = int(math.floor((index - 1) / 2))
            if parent >= 0:
                if self._list[parent] > self._list[index]:
                    self._swap_items(parent, index)
                    self._repair_heap_up(parent)

    def _repair_heap_down(self, index):
        """
        >>> pqmh = PriorityQueueMinHeap()
        >>> a = PriorityQueueItem(17, "A", 0)
        >>> pqmh._list.append(a)
        >>> b = PriorityQueueItem(4, "B", 1)
        >>> pqmh._list.append(b)
        >>> c = PriorityQueueItem(5, "C", 2)
        >>> pqmh._list.append(c)
        >>> d = PriorityQueueItem(8, "D", 3)
        >>> pqmh._list.append(d)
        >>> pqmh._repair_heap_down(0)
        >>> print(pqmh._list[0]._key)
        4
        >>> print(pqmh._list[1]._key)
        8
        >>> print(pqmh._list[2]._key)
        5
        >>> print(pqmh._list[3]._key)
        17
        """
        if len(self._list) > 1 and index < len(self._list)/2:
            child_1 = 2 * index + 1
            child_2 = 2 * index + 2
            if child_2 >= len(self._list):
                child_2 = child_1
            if (self._list[child_1] < self._list[index] or
                    self._list[child_2] < self._list[index]):
                if self._list[child_1] < self._list[child_2]:
                    self._swap_items(child_1, index)
                    self._repair_heap_down(child_1)
                else:
                    self._swap_items(child_2, index)
                    self._repair_heap_down(child_2)


if __name__ == "__main__":
    # Create priority queue object.
    pq1 = PriorityQueueMinHeap()
    # Insert some flights into queue.
    pq1_item1 = pq1.insert(1, "Airforce One")
    pq1_item2 = pq1.insert(45, "Bermuda Triangle Blues (Flight 45)")
    pq1_item3 = pq1.insert(666, "Flight 666")
    # ....
