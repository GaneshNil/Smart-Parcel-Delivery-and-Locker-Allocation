from math import isfinite

from circular_linked_list import CircularLinkedList
from dispatch_queue import Queue
from hashing import HashTable
from locker import LockerGrid
from parcel import Parcel, SAMPLE_DESTINATIONS, sample_parcels
from searching import binary_search, linear_search
from singly_linked_list import SinglyLinkedList
from sorting import quick_sort


TERMINAL_STATUSES = ("Delivered", "Cancelled")


class ParcelFlow:
    def __init__(self):
        self.parcels = []
        self.hash_table = HashTable()
        self.lockers = LockerGrid()
        self.queue = Queue()
        self.stops = SinglyLinkedList()
        self.routes = {}

    def register(self, parcel_id, recipient, contact, destination, weight):
        parcel_id = parcel_id.strip().upper()
        recipient = recipient.strip()
        destination = destination.strip()
        contact = contact.strip()
        if not parcel_id or not parcel_id.isascii() or not parcel_id.isalnum():
            raise ValueError("Enter an alphanumeric parcel ID, such as P101.")
        if not recipient or not destination:
            raise ValueError("Recipient and destination are required.")
        if not contact.isascii() or not contact.isdigit() or not 7 <= len(contact) <= 15:
            raise ValueError("Contact number must have 7 to 15 digits.")
        if not isfinite(weight) or weight <= 0:
            raise ValueError("Weight must be a positive, finite number.")

        parcel = Parcel(parcel_id, recipient, contact, destination, weight)
        if not self.hash_table.insert(parcel):
            raise ValueError("Parcel ID already exists.")
        self.parcels.append(parcel)
        return parcel

    def require_parcel(self, parcel_id):
        parcel = self.hash_table.search(parcel_id)
        if parcel is None:
            raise ValueError("Parcel not found.")
        return parcel

    def compare_searches(self, parcel_id):
        return (linear_search(self.parcels, parcel_id),
                binary_search(quick_sort(self.parcels), parcel_id))

    def allocate(self, parcel_id, position=None):
        parcel = self.require_parcel(parcel_id)
        if parcel.status != "Registered":
            raise ValueError("Only registered parcels can be assigned a locker.")
        locker = self.lockers.allocate(position)
        if locker is None:
            raise ValueError("No locker is available at the requested position." if position
                             else "All lockers are occupied.")
        parcel.locker = locker
        parcel.status = "Stored"
        return locker

    def release(self, parcel_id):
        parcel = self.require_parcel(parcel_id)
        if parcel.status != "Stored":
            raise ValueError("Only stored parcels can be released manually.")
        self.clear_locker(parcel)
        parcel.status = "Registered"

    def clear_locker(self, parcel):
        if parcel.locker is not None:
            self.lockers.release(*parcel.locker)
            parcel.locker = None

    def create_route(self, name):
        if not name or name in self.routes:
            raise ValueError("Enter a new, nonempty route name.")
        route = CircularLinkedList()
        self.routes[name] = route
        return route

    def remove_location(self, name, location):
        for parcel in self.parcels:
            if (parcel.route == name and parcel.destination == location
                    and parcel.status not in TERMINAL_STATUSES):
                raise ValueError("An active parcel needs this route location.")
        if not self.routes[name].remove(location):
            raise ValueError("Location not found.")

    def route_for(self, destination):
        for name, route in self.routes.items():
            if destination in route.cycle():
                return name

        name = "Custom destinations"
        for index, location in enumerate(SAMPLE_DESTINATIONS):
            if destination == location:
                name = "Route A" if index < 4 else "Route B" if index < 7 else "Route C"
                break
        if name not in self.routes:
            self.create_route(name).add("Distribution Hub")
        self.routes[name].add(destination)
        return name

    def add_stop(self, parcel_id):
        parcel = self.require_parcel(parcel_id)
        if parcel.status in TERMINAL_STATUSES:
            raise ValueError("Only active parcels can have delivery stops.")
        return self.stops.add(parcel_id)

    def remove_stop(self, parcel_id):
        parcel = self.require_parcel(parcel_id)
        if parcel.status in ("Queued", "Dispatched"):
            raise ValueError("This stop is needed until delivery or cancellation.")
        if not self.stops.remove(parcel_id):
            raise ValueError("Stop not found.")

    def enqueue(self, parcel_id):
        parcel = self.require_parcel(parcel_id)
        if parcel.status != "Stored":
            raise ValueError("Only stored parcels can enter the dispatch queue.")
        parcel.route = self.route_for(parcel.destination)
        self.add_stop(parcel_id)
        self.queue.enqueue(parcel_id)
        parcel.status = "Queued"

    def dispatch(self):
        parcel_id = self.queue.dequeue()
        if parcel_id is None:
            return None
        parcel = self.require_parcel(parcel_id)
        self.clear_locker(parcel)
        parcel.status = "Dispatched"
        return parcel

    def deliver(self, parcel_id):
        parcel = self.require_parcel(parcel_id)
        if parcel.status != "Dispatched":
            raise ValueError("Only dispatched parcels can be marked delivered.")
        self.stops.remove(parcel_id)
        parcel.status = "Delivered"

    def cancel(self, parcel_id):
        parcel = self.require_parcel(parcel_id)
        if parcel.status not in ("Registered", "Stored", "Queued"):
            raise ValueError(f"A parcel with status {parcel.status} cannot be cancelled.")
        if parcel.status == "Queued":
            # Move each entry once, preserving the order of the remaining queue.
            last = self.queue.rear
            while True:
                current = self.queue.front
                next_id = self.queue.dequeue()
                if next_id != parcel_id:
                    self.queue.enqueue(next_id)
                if current is last:
                    break
        self.clear_locker(parcel)
        self.stops.remove(parcel_id)
        parcel.route = None
        parcel.status = "Cancelled"

    def delete(self, parcel_id):
        parcel = self.require_parcel(parcel_id)
        if parcel.status not in TERMINAL_STATUSES:
            raise ValueError("Only delivered or cancelled records can be deleted.")
        self.hash_table.delete(parcel_id)
        self.parcels.remove(parcel)

    def load_samples(self):
        added = 0
        for sample in sample_parcels():
            parcel_id = sample.parcel_id
            if self.hash_table.search(parcel_id) is not None:
                continue
            self.register(parcel_id, sample.recipient, sample.contact,
                          sample.destination, sample.weight)
            if self.lockers.count_available() > 0:
                self.allocate(parcel_id)
                self.enqueue(parcel_id)
            added += 1
        return added
