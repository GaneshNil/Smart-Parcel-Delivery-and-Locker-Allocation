import json
from math import isfinite
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data" / "parcels.json"
DONE = ("Delivered", "Cancelled")
AREAS = ("Kothrud", "Karve Nagar", "Deccan", "Shivajinagar", "Baner",
         "Wakad", "Hadapsar", "Viman Nagar", "Katraj", "Hinjewadi")

# Lab 1: searching
def linear_search(records, parcel_id):
    for parcel in records:
        if parcel["parcel_id"] == parcel_id:
            return parcel


def binary_search(records, parcel_id):
    left, right = 0, len(records) - 1
    while left <= right:
        # Compare with the middle ID to discard half of the sorted range.
        middle = (left + right) // 2
        key = records[middle]["parcel_id"]
        if key == parcel_id:
            return records[middle]
        if key < parcel_id:
            left = middle + 1
        else:
            right = middle - 1

# Lab 2: sorting
def quick_sort(records):
    if len(records) < 2:
        return records[:]

    # Keep equal IDs together so only the smaller and larger groups recurse.
    pivot = records[len(records) // 2]["parcel_id"]
    before = [p for p in records if p["parcel_id"] < pivot]
    equal = [p for p in records if p["parcel_id"] == pivot]
    after = [p for p in records if p["parcel_id"] > pivot]
    return quick_sort(before) + equal + quick_sort(after)


def merge_sort(records):
    if len(records) < 2:
        return records[:]
    middle = len(records) // 2
    left = merge_sort(records[:middle])
    right = merge_sort(records[middle:])

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        # Take from the left on ties to keep equal destinations in order.
        if left[i]["destination"].casefold() <= right[j]["destination"].casefold():
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # One half may still have records left after the other runs out.
    return merged + left[i:] + right[j:]

# Labs 3, 5 and 7: singly linked stops, circular routes, and FIFO queue
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


# Stops and the queue end at None. Routes link the tail back to the head.
class Chain:
    def __init__(self, values=(), circular=False):
        self.head = self.tail = self.current = None
        self.circular = circular
        for value in values:
            self.append(value)

    def append(self, value):
        node = Node(value)
        if self.tail:
            self.tail.next = node
        else:
            self.head = self.current = node
        self.tail = node
        if self.circular:
            node.next = self.head

    def remove(self, value):
        previous, node = None, self.head
        for item in self.values():
            if item == value:
                # A single-node route points to itself, but removing it empties the list.
                following = node.next if self.head is not self.tail else None
                if previous:
                    previous.next = following
                else:
                    self.head = following

                # Repair the tail and route cursor if either pointed at the removed node.
                if node is self.tail:
                    self.tail = previous
                if self.circular and self.tail:
                    self.tail.next = self.head
                if node is self.current:
                    self.current = following
                return value
            previous, node = node, node.next

    def values(self, start=None):
        first = start or self.head
        node = first
        while node:
            yield node.value
            node = node.next
            if node is first:  # Stop after one pass around a circular route.
                break


# Lab 9: separate chaining. A bucket holds references to parcel records.
def bucket_for(buckets, parcel_id):
    index = 0
    for letter in parcel_id:
        index = (index * 31 + ord(letter)) % len(buckets)
    return buckets[index]


def register(buckets, records, parcel_id, name, contact, destination, weight):
    bucket = bucket_for(buckets, parcel_id)
    if not parcel_id.isalnum() or linear_search(bucket, parcel_id):
        raise ValueError("Enter a unique alphanumeric ID.")
    if not name or not destination or not contact.isdigit() or not 7 <= len(contact) <= 15:
        raise ValueError("Enter a name, destination and 7–15 digit contact number.")
    if not isfinite(weight) or weight <= 0:
        raise ValueError("Enter a positive, finite weight.")

    # The registry and the bucket share the same parcel record.
    parcel = dict(
        parcel_id=parcel_id, recipient=name, contact=contact, destination=destination,
        weight=weight, status="Registered", locker=None, route=None,
    )
    records.append(parcel)
    bucket.append(parcel)
    return parcel

# Lab 6: 0 means a free locker, and 1 means an occupied locker.
def store(parcel, grid, coordinates):
    if parcel["status"] != "Registered":
        raise ValueError("Only registered parcels can be stored.")

    # Try lockers row by row unless the user supplies one position.
    choices = (
        (row, column) for row in range(1, 11) for column in range(1, 11)
    )
    if coordinates:
        choices = [tuple(int(number) for number in coordinates)]
    for row, column in choices:
        if 1 <= row <= 10 and 1 <= column <= 10 and not grid[row - 1][column - 1]:
            break
    else:
        raise ValueError("Locker unavailable. Use row and column from 1 to 10.")

    # The user counts from 1. Python list indexes start at 0.
    grid[row - 1][column - 1] = 1
    parcel.update(locker=(row, column), status="Stored")


def enqueue(parcel, queue, stops, routes):
    if parcel["status"] != "Stored":
        raise ValueError("Only stored parcels can be queued.")

    # Use an existing route that serves this destination, or add it to Route A.
    destination = parcel["destination"]
    for name, route in routes.items():
        if destination in route.values():
            break
    else:
        name = "Route A"
        routes.setdefault(name, Chain(["Distribution Hub"], circular=True)).append(destination)

    # Append at the tail so earlier parcels are dispatched first.
    parcel.update(status="Queued", route=name)
    queue.append(parcel["parcel_id"])
    if parcel["parcel_id"] not in stops.values():
        stops.append(parcel["parcel_id"])


def show(records):
    header = "ID | Recipient | Contact | Destination | kg | Status | Locker | Route"
    print(header if records else "No parcels found.")
    for p in records:
        print("{parcel_id} | {recipient} | {contact} | {destination} | {weight} | "
              "{status} | {locker} | {route}".format(**p))


def main(path=DATA):
    content = path.read_text(encoding="utf-8") if path.exists() else ""
    if content.strip():
        data = json.loads(content)
    else:
        data = dict(parcels=[], stops=[], queue=[], routes=[])

    # Rebuild the linked structures from the order saved in JSON.
    records = data["parcels"]
    stops, queue = Chain(data["stops"]), Chain(data["queue"])
    routes = {}
    for entry in data["routes"]:
        route = Chain(entry["locations"], circular=True)
        routes[entry["name"]] = route
        for location in route.values():
            if location == entry["current"]:
                break
            route.current = route.current.next

    # Rebuild the hash index and locker grid from the parcel records.
    buckets = [[] for _ in range(13)]
    grid = [[0] * 10 for _ in range(10)]
    for parcel in records:
        key = parcel["parcel_id"]
        bucket = bucket_for(buckets, key)
        if linear_search(bucket, key):
            raise ValueError("Duplicate ID in saved data.")
        bucket.append(parcel)
        if parcel["locker"]:
            row, column = parcel["locker"]
            if not (1 <= row <= 10 and 1 <= column <= 10) or grid[row - 1][column - 1]:
                raise ValueError("Invalid locker in saved data.")
            grid[row - 1][column - 1] = 1

    queued_ids = [p["parcel_id"] for p in records if p["status"] == "Queued" and p["locker"]]
    saved_queue = list(queue.values())
    if set(saved_queue) != set(queued_ids) or len(saved_queue) != len(queued_ids):
        raise ValueError("Invalid dispatch queue in saved data.")

    print("""ParcelFlow commands
register ID | list | search ID | quick | merge | hash ID | buckets
grid | store ID [row col] | release ID | queue | peek | enqueue ID | dispatch
deliver ID | cancel ID | delete ID | stops | addstop ID | removestop ID | findstop ID
routes | route NAME | next NAME | cycle NAME | addloc NAME / LOCATION
remloc NAME / LOCATION | samples | exit""")

    while True:
        try:
            command, _, argument = input("> ").strip().partition(" ")
            if command == "exit":
                break

            words = argument.upper().split()
            parcel_id = words[0] if words else "-"
            coordinates = words[1:]
            bucket = bucket_for(buckets, parcel_id)
            parcel = linear_search(bucket, parcel_id)

            if command == "register":
                name = input("Recipient: ").strip()
                contact = input("Contact: ").strip()
                destination = input("Destination: ").strip()
                weight = float(input("kg: "))
                register(buckets, records, parcel_id, name, contact, destination, weight)
            elif command in ("list", "quick", "merge"):
                sorters = {"quick": quick_sort, "merge": merge_sort}
                sort = sorters.get(command, list)
                show(sort(records))
            elif command in ("search", "hash"):
                if command == "search":
                    print("Linear:", bool(linear_search(records, parcel_id)))
                    # Binary search needs sorted IDs. Quick Sort returns a copy.
                    parcel = binary_search(quick_sort(records), parcel_id)
                show([parcel] if parcel else [])
            elif command == "buckets":
                for i, chain in enumerate(buckets):
                    ids = [p["parcel_id"] for p in chain]
                    extra = max(0, len(chain) - 1)
                    print(i, ids, "collisions:", extra)
                print(f"Load factor: {len(records) / len(buckets):.2f}")
            elif command == "grid":
                for row in grid:
                    print(*row)
                occupied = sum(sum(row) for row in grid)
                print("Occupied:", occupied, "Available:", 100 - occupied)
            elif command == "samples":
                for i in range(20):
                    key = f"P{101 + i}"
                    if not linear_search(bucket_for(buckets, key), key):
                        name = f"Recipient {i + 1}"
                        contact = f"000000{i + 1:04}"
                        destination = AREAS[i % len(AREAS)]
                        sample = register(buckets, records, key, name, contact, destination, 1 + i / 10)
                        if sum(sum(row) for row in grid) < 100:
                            store(sample, grid, [])
                            enqueue(sample, queue, stops, routes)
            elif command in ("routes", "queue", "stops", "peek"):
                first = [queue.head.value] if queue.head else []
                views = {
                    "routes": routes, "queue": queue.values(),
                    "stops": stops.values(), "peek": first,
                }
                print(*views[command])
            elif command in ("route", "next", "cycle", "addloc", "remloc"):
                name, _, location = argument.partition("/")
                name = name.strip()
                location = location.strip()
                if command == "addloc":
                    if not name or not location:
                        raise ValueError("Use addloc NAME / LOCATION.")
                    route = routes.setdefault(name, Chain(circular=True))
                    if location not in route.values():
                        route.append(location)
                elif name not in routes:
                    print("Route not found.")
                elif command == "remloc":
                    if any(p["route"] == name and p["destination"] == location
                           and p["status"] not in DONE for p in records):
                        raise ValueError("An active parcel needs this location.")
                    routes[name].remove(location)
                else:
                    route = routes[name]
                    if command == "next" and route.current:
                        route.current = route.current.next
                        print(route.current.value)
                    elif command == "cycle" and route.current:
                        locations = list(route.values(route.current))
                        locations.append(route.current.value)
                        print(" -> ".join(locations))
                    else:
                        print(" -> ".join(route.values()) or "Empty route.")
            elif command == "dispatch":
                # FIFO dispatch removes the head and releases its locker.
                if not queue.head:
                    raise ValueError("Queue is empty.")
                next_id = queue.remove(queue.head.value)
                parcel = linear_search(bucket_for(buckets, next_id), next_id)
                row, column = parcel["locker"]
                grid[row - 1][column - 1] = 0
                parcel.update(locker=None, status="Dispatched")
                print("Dispatched:", next_id)
            elif command in ("store", "enqueue", "release", "cancel", "deliver", "delete",
                             "addstop", "removestop", "findstop") and parcel:
                status = parcel["status"]
                if command == "store":
                    store(parcel, grid, coordinates)
                elif command == "enqueue":
                    enqueue(parcel, queue, stops, routes)
                elif command == "findstop":
                    print("Found." if parcel_id in stops.values() else "Stop not found.")
                elif (
                    command == "addstop" and status not in DONE and parcel_id not in stops.values()
                ):
                    stops.append(parcel_id)
                elif command == "removestop" and status in ("Registered", "Stored"):
                    stops.remove(parcel_id)
                elif command == "delete" and status in DONE:
                    records.remove(parcel)
                    bucket.remove(parcel)
                elif command == "deliver" and status == "Dispatched":
                    parcel["status"] = "Delivered"
                    stops.remove(parcel_id)
                elif (command == "release" and status == "Stored") or (
                        command == "cancel" and status in ("Registered", "Stored", "Queued")):
                    if parcel["locker"]:
                        row, column = parcel["locker"]
                        grid[row - 1][column - 1] = 0
                    parcel.update(locker=None, status="Registered")
                    if command == "cancel":
                        # Remove only this parcel so the remaining queue stays in order.
                        queue.remove(parcel_id)
                        stops.remove(parcel_id)
                        parcel.update(status="Cancelled", route=None)
                else:
                    raise ValueError("Action unavailable for this status.")
            else:
                raise ValueError("Unknown command or parcel.")
        except ValueError as error:
            print(error)
        except (EOFError, KeyboardInterrupt):
            break

    # Save values and their order. The node links are rebuilt on the next run.
    saved_routes = []
    for name, route in routes.items():
        current = route.current.value if route.current else None
        saved_routes.append(dict(name=name, locations=list(route.values()), current=current))
    data.update(stops=list(stops.values()), queue=list(queue.values()), routes=saved_routes)

    path.parent.mkdir(exist_ok=True)
    # Write the new file before replacing the last saved copy.
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(data, indent=2), encoding="utf-8")
    temporary.replace(path)


if __name__ == "__main__":
    main()
