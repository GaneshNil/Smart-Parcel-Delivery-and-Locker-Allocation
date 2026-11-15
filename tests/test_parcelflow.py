import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from circular_linked_list import CircularLinkedList
from dispatch_queue import Queue
from singly_linked_list import SinglyLinkedList

from hashing import HashTable
from locker import LockerGrid
from parcel import Parcel, sample_parcels
from searching import binary_search, linear_search
from sorting import merge_sort, quick_sort
from system import ParcelFlow
from storage import load, save


class AlgorithmTests(unittest.TestCase):
    def setUp(self):
        self.first, self.second, self.third = sample_parcels()[:3]
        self.parcels = [self.third, self.first, self.second]

    def test_searches(self):
        for search, records in ((linear_search, self.parcels),
                                (binary_search, quick_sort(self.parcels))):
            self.assertIs(search(records, "P102"), self.second)
            self.assertIsNone(search(records, "P999"))
            self.assertIsNone(search([], "P101"))

    def test_quick_sort(self):
        self.assertEqual(quick_sort(self.parcels), [self.first, self.second, self.third])
        self.assertEqual(quick_sort([self.second, self.first, self.second]),
                         [self.first, self.second, self.second])
        self.assertEqual(self.parcels, [self.third, self.first, self.second])
        self.assertEqual(quick_sort([]), [])
        self.assertEqual(quick_sort([self.first]), [self.first])

    def test_merge_sort(self):
        self.assertEqual(merge_sort(self.parcels), [self.third, self.second, self.first])
        same_destination = Parcel("P999", "Test Person", "0000000000", "kothrud", 1)
        self.assertEqual(merge_sort([same_destination, self.third, self.first]),
                         [self.third, same_destination, self.first])
        self.assertEqual(self.parcels, [self.third, self.first, self.second])
        self.assertEqual(merge_sort([]), [])
        self.assertEqual(merge_sort([self.first]), [self.first])

    def test_hash_collisions_and_deletion(self):
        table = HashTable(1)
        for parcel in self.parcels:
            self.assertTrue(table.insert(parcel))
        self.assertFalse(table.insert(self.first))
        self.assertEqual(table.load_factor(), 3)
        self.assertTrue(table.delete("P101"))
        self.assertFalse(table.delete("P101"))
        self.assertIs(table.search("P102"), self.second)
        self.assertIsNone(table.search("P101"))


class LinkedTests(unittest.TestCase):
    def test_stops(self):
        stops = SinglyLinkedList()
        self.assertFalse(stops.remove("P0"))
        self.assertTrue(stops.add("P1"))
        self.assertTrue(stops.add("P2"))
        self.assertFalse(stops.add("P2"))
        self.assertIs(stops.search("P2"), stops.head.next)
        self.assertTrue(stops.remove("P1"))
        self.assertEqual(stops.traverse(), ["P2"])
        self.assertTrue(stops.remove("P2"))
        self.assertIsNone(stops.tail)

    def test_route(self):
        route = CircularLinkedList()
        self.assertIsNone(route.next_location())
        self.assertEqual(route.complete_cycle(), [])
        route.add("Hub")
        self.assertIs(route.head.next, route.head)
        self.assertEqual(route.complete_cycle(), ["Hub", "Hub"])
        route.add("Deccan")
        self.assertIs(route.tail.next, route.head)
        self.assertEqual(route.next_location(), "Deccan")
        self.assertEqual(route.complete_cycle(), ["Deccan", "Hub", "Deccan"])
        self.assertTrue(route.remove("Deccan"))
        self.assertIs(route.current, route.head)
        self.assertTrue(route.remove("Hub"))
        self.assertIsNone(route.tail)

    def test_queue(self):
        queue = Queue()
        self.assertIsNone(queue.dequeue())
        for parcel_id in ("P1", "P2", "P3"):
            queue.enqueue(parcel_id)
        self.assertEqual(queue.peek(), "P1")
        self.assertEqual(queue.dequeue(), "P1")
        self.assertEqual(queue.display_queue(), ["P2", "P3"])
        self.assertEqual(queue.dequeue(), "P2")
        self.assertEqual(queue.dequeue(), "P3")
        self.assertTrue(queue.is_empty())
        self.assertIsNone(queue.rear)


class LockerTests(unittest.TestCase):
    def test_allocate_release_and_capacity(self):
        lockers = LockerGrid()
        self.assertIsNone(lockers.allocate((0, 11)))
        self.assertEqual(lockers.allocate((1, 1)), (1, 1))
        self.assertIsNone(lockers.allocate((1, 1)))
        for _ in range(99):
            self.assertIsNotNone(lockers.allocate())
        self.assertEqual(lockers.count_occupied(), 100)
        self.assertEqual(lockers.count_available(), 0)
        self.assertIsNone(lockers.allocate())
        self.assertTrue(lockers.release(1, 1))
        self.assertFalse(lockers.release(1, 1))
        self.assertTrue(lockers.is_available(1, 1))
        self.assertEqual(lockers.allocate(), (1, 1))


class WorkflowTests(unittest.TestCase):
    def test_registration_and_sample_collisions(self):
        app = ParcelFlow()
        self.assertEqual(app.load_samples(), 20)
        self.assertEqual(app.load_samples(), 0)
        with self.assertRaises(ValueError):
            app.register("p101", "Test Recipient", "0000000000", "Kothrud", 1)
        with self.assertRaises(ValueError):
            app.register("P999", "Test Recipient", "0000000000", "Kothrud", float("nan"))
        self.assertEqual(app.hash_table.size, 20)
        self.assertTrue(any(len(bucket) > 1 for bucket in app.hash_table.buckets))
        parcel = app.hash_table.search("P102")
        self.assertEqual(app.compare_searches("P102"), (parcel, parcel))

    def test_dispatch_cancellation_and_delivery(self):
        app = ParcelFlow()
        app.load_samples()
        locker = app.require_parcel("P102").locker
        with self.assertRaises(ValueError):
            app.enqueue("P102")
        with self.assertRaises(ValueError):
            app.remove_location("Route A", "Karve Nagar")
        app.cancel("P102")
        self.assertEqual(app.require_parcel("P102").status, "Cancelled")
        self.assertTrue(app.lockers.is_available(*locker))
        self.assertIsNone(app.stops.search("P102"))
        self.assertEqual(app.dispatch().parcel_id, "P101")
        self.assertEqual(app.dispatch().parcel_id, "P103")
        self.assertEqual(app.require_parcel("P101").status, "Dispatched")
        self.assertIsNone(app.require_parcel("P101").locker)
        with self.assertRaises(ValueError):
            app.cancel("P101")
        app.deliver("P101")
        with self.assertRaises(ValueError):
            app.cancel("P101")
        app.delete("P101")
        self.assertEqual(app.compare_searches("P101"), (None, None))
        self.assertIsNone(app.hash_table.search("P101"))


class StorageTests(unittest.TestCase):
    def test_missing_empty_and_invalid_files(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "parcels.json"
            self.assertEqual(load(path).parcels, [])
            path.write_text("  ", encoding="utf-8")
            self.assertEqual(load(path).parcels, [])
            path.write_text("{", encoding="utf-8")
            with self.assertRaises(ValueError):
                load(path)
            self.assertEqual(path.read_text(encoding="utf-8"), "{")

    def test_round_trip(self):
        app = ParcelFlow()
        app.load_samples()
        app.cancel("P102")
        app.dispatch()
        app.routes["Route A"].next_location()
        app.create_route("Empty")
        expected_queue = app.queue.display_queue()
        with TemporaryDirectory() as directory:
            path = Path(directory) / "parcels.json"
            save(app, path)
            rebuilt = load(path)
            save(rebuilt, path)
            rebuilt = load(path)
        self.assertEqual([vars(parcel) for parcel in rebuilt.parcels],
                         [vars(parcel) for parcel in app.parcels])
        self.assertEqual(rebuilt.queue.display_queue(), expected_queue)
        self.assertEqual(rebuilt.stops.traverse(), app.stops.traverse())
        self.assertEqual(rebuilt.lockers.locker_grid, app.lockers.locker_grid)
        self.assertEqual(rebuilt.routes["Route A"].cycle(), app.routes["Route A"].cycle())
        self.assertEqual(rebuilt.routes["Route A"].current.value, "Kothrud")
        self.assertIsNone(rebuilt.routes["Empty"].head)
        self.assertEqual(rebuilt.load_samples(), 0)
        self.assertIs(rebuilt.hash_table.search("P101"), rebuilt.parcels[0])
        self.assertEqual(rebuilt.dispatch().parcel_id, "P103")
