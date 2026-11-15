from singly_linked_list import Node


class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def add(self, location):
        if location in self.cycle():
            return False
        node = Node(location)
        if self.head is None:
            self.head = self.current = node
        else:
            self.tail.next = node
        node.next = self.head
        self.tail = node
        return True

    def remove(self, location):
        if self.head is None:
            return False
        previous = self.tail
        node = self.head
        while True:
            if node.value == location:
                if node is node.next:
                    self.head = self.tail = self.current = None
                    return True
                previous.next = node.next
                if node is self.head:
                    self.head = node.next
                if node is self.tail:
                    self.tail = previous
                if node is self.current:
                    self.current = node.next
                return True
            previous = node
            node = node.next
            if node is self.head:
                return False

    def next_location(self):
        if self.current is None:
            return None
        self.current = self.current.next
        return self.current.value

    def cycle(self):
        locations = []
        node = self.head
        if node is not None:
            while True:
                locations.append(node.value)
                node = node.next
                if node is self.head:
                    break
        return locations

    def complete_cycle(self):
        if self.current is None:
            return []
        locations = [self.current.value]
        start = self.current
        while True:
            locations.append(self.next_location())
            if self.current is start:
                return locations
