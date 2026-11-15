from singly_linked_list import Node


class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def is_empty(self):
        return self.front is None

    def enqueue(self, parcel_id):
        node = Node(parcel_id)
        if self.is_empty():
            self.front = node
        else:
            self.rear.next = node
        self.rear = node

    def dequeue(self):
        if self.is_empty():
            return None
        parcel_id = self.front.value
        self.front = self.front.next
        if self.is_empty():
            self.rear = None
        return parcel_id

    def peek(self):
        if not self.is_empty():
            return self.front.value
        return None

    def display_queue(self):
        parcel_ids = []
        current = self.front
        while current is not None:
            parcel_ids.append(current.value)
            current = current.next
        return parcel_ids
