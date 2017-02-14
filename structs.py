from heapq import heappop, heappush, heapify
from collections import deque


class Stack():
    """Represents a FILO stack"""
    def __init__(self, init_list=[]):
        "docstring"
        self.stack = init_list

    def add(self, elem):
        """Adds elem to stack"""
        self.stack.append(elem)

    def pop(self):
        """Removes elem from stack"""
        return self.stack.pop()

    def is_empty(self):
        """Checks if stack is empty"""
        return len(self.stack) == 0

    def contains(self, elem):
        """Check if stack contains elem"""
        return elem in self.stack

    def size(self):
        """Size of stack"""
        return len(self.stack)
    
class Queue(object):
    """Represents a FIFO queue"""
    def __init__(self, init_list=None):
        "docstring"
        if init_list:
            self._data = deque(init_list)
        else:
            self._data = deque()

    def add(self, elem):
        """Adds elem to queue"""
        self._data.append(elem)

    def pop(self):
        """Removes elem from queue"""
        return self._data.popleft()

    def is_empty(self):
        """Checks if empty"""
        return len(self._data) == 0

    def contains(self, elem):
        """Checks if queue contains elem"""
        return elem in self._data

    def size(self):
        """Size of queue"""
        return len(self._data)

class Heap(object):
    """Represents a heap"""
    def __init__(self, initial=None, key=lambda x: x):
        self.key = key
        if initial:
            self._data = [(key(item), item) for item in initial]
            heapify(self._data)
        else:
            self._data = []

    def add(self, item):
        """Adds item to heap"""
        heappush(self._data, (self.key(item), item))

    def pop(self):
        """Removes elem from heap"""
        return heappop(self._data)[1]

    def is_empty(self):
        """Checks if empty"""
        return self._data

    def contains(self, elem):
        """Checks if heap contains elem"""
        return elem in self._data

    def size(self):
        """Size of heap"""
        return len(self._data)
