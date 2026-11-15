class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def search(self, stop):
        current = self.head
        while current is not None:
            if current.value == stop:
                return current
            current = current.next
        return None

    def add(self, stop):
        if self.search(stop) is not None:
            return False
        node = Node(stop)
        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        return True

    def remove(self, stop):
        previous = None
        current = self.head
        while current is not None:
            if current.value == stop:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                if current is self.tail:
                    self.tail = previous
                return True
            previous = current
            current = current.next
        return False

    def traverse(self):
        stops = []
        current = self.head
        while current is not None:
            stops.append(current.value)
            current = current.next
        return stops
