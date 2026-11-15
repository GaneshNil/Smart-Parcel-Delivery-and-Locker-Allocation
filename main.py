from sorting import merge_sort, quick_sort
from storage import load, save


MAIN_MENU = """
ParcelFlow | Smart Parcel Delivery and Locker Allocation

1. Register new parcel
2. View all parcels
3. Compare linear and binary search
4. Sort parcel records
5. Manage delivery stops
6. Manage circular routes
7. Manage lockers
8. Manage dispatch queue
9. Search using hash table
10. View hash table statistics
11. Generate parcel report
12. Load sample data
13. Cancel parcel
14. Delete delivered or cancelled record
0. Save and exit
"""


def read_id():
    return input("Parcel ID: ").strip().upper()


def read_position():
    try:
        return int(input("Row (1-10): ")), int(input("Column (1-10): "))
    except ValueError:
        raise ValueError("Enter whole numbers for row and column.") from None


def show_parcels(parcels):
    if not parcels:
        print("No parcels found.")
        return
    rows = [["ID", "Recipient", "Contact", "Destination", "Weight", "Locker", "Status", "Route"]]
    for parcel in parcels:
        rows.append([parcel.parcel_id, parcel.recipient, parcel.contact, parcel.destination,
                     f"{parcel.weight:g} kg", str(parcel.locker) if parcel.locker else "-",
                     parcel.status, parcel.route or "-"])
    widths = [max(len(value) for value in column) for column in zip(*rows)]
    for row in rows:
        print(" | ".join(value.ljust(width) for value, width in zip(row, widths)).rstrip())


def show_path(values):
    print(" -> ".join(values) if values else "Empty.")


def register_parcel(app):
    parcel_id = read_id()
    recipient = input("Recipient name: ")
    contact = input("Contact number: ")
    destination = input("Destination: ")
    try:
        weight = float(input("Weight (kg): "))
    except ValueError:
        raise ValueError("Enter a numeric weight.") from None
    parcel = app.register(parcel_id, recipient, contact, destination, weight)
    print(f"{parcel.parcel_id} registered. Use Manage lockers to store it.")


def search_parcels(app):
    linear, binary = app.compare_searches(read_id())
    print("Linear search")
    show_parcels([linear] if linear else [])
    print("Binary search (parcel IDs in sorted order)")
    show_parcels([binary] if binary else [])


def sort_parcels(app):
    choice = input("1. Quick Sort by ID | 2. Merge Sort by destination | 0. Back\nChoice: ").strip()
    if choice == "1":
        show_parcels(quick_sort(app.parcels))
    elif choice == "2":
        show_parcels(merge_sort(app.parcels))
    elif choice != "0":
        print("Invalid choice.")


def manage_stops(app):
    choice = input("1. Add | 2. Remove | 3. Display | 4. Search | 0. Back\nChoice: ").strip()
    if choice == "1":
        print("Stop added." if app.add_stop(read_id()) else "Stop already exists.")
    elif choice == "2":
        app.remove_stop(read_id())
        print("Stop removed.")
    elif choice == "3":
        for parcel_id in app.stops.traverse():
            parcel = app.require_parcel(parcel_id)
            print(f"{parcel_id} | {parcel.destination}")
        if app.stops.head is None:
            print("No delivery stops.")
    elif choice == "4":
        stop = app.stops.search(read_id())
        if stop is None:
            print("Stop not found.")
        else:
            show_parcels([app.require_parcel(stop.value)])
    elif choice != "0":
        print("Invalid choice.")


def manage_routes(app):
    print("Routes: " + (", ".join(app.routes) or "None"))
    choice = input("1. Create | 2. Add location | 3. Remove location | 4. Display\n"
                   "5. Next location | 6. Complete cycle | 0. Back\nChoice: ").strip()
    if choice == "0":
        return
    if choice not in ("1", "2", "3", "4", "5", "6"):
        print("Invalid choice.")
        return
    name = input("Route name: ").strip()
    if choice == "1":
        app.create_route(name)
        print("Route created.")
        return
    if name not in app.routes:
        raise ValueError("Route not found.")
    route = app.routes[name]
    if choice == "2":
        location = input("Location: ").strip()
        if not location:
            raise ValueError("Location is required.")
        print("Location added." if route.add(location) else "Location already exists.")
    elif choice == "3":
        app.remove_location(name, input("Location: ").strip())
        print("Location removed.")
    elif choice == "4":
        show_path(route.cycle())
        print("Current location: " + (route.current.value if route.current else "-"))
    elif choice == "5":
        print(route.next_location() or "Route is empty.")
    else:
        show_path(route.complete_cycle())


def manage_lockers(app):
    choice = input("1. Display grid | 2. Check availability | 3. Allocate automatically\n"
                   "4. Allocate specific locker | 5. Release | 0. Back\nChoice: ").strip()
    if choice == "1":
        app.lockers.display()
    elif choice == "2":
        row, column = read_position()
        if not app.lockers.valid_position(row, column):
            raise ValueError("Row and column must be from 1 to 10.")
        print("Available." if app.lockers.is_available(row, column) else "Occupied.")
    elif choice in ("3", "4"):
        parcel_id = read_id()
        position = read_position() if choice == "4" else None
        if position and not app.lockers.valid_position(*position):
            raise ValueError("Row and column must be from 1 to 10.")
        print(f"Locker assigned: {app.allocate(parcel_id, position)}")
    elif choice == "5":
        app.release(read_id())
        print("Locker released. Parcel returned to Registered status.")
    elif choice != "0":
        print("Invalid choice.")


def manage_queue(app):
    choice = input("1. Enqueue | 2. Dispatch next | 3. Peek | 4. Display\n"
                   "5. Mark delivered | 0. Back\nChoice: ").strip()
    if choice == "1":
        parcel_id = read_id()
        app.enqueue(parcel_id)
        print(f"Queued for {app.require_parcel(parcel_id).route}.")
    elif choice == "2":
        parcel = app.dispatch()
        if parcel is None:
            print("Dispatch queue is empty.")
        else:
            print(f"{parcel.parcel_id} dispatched on {parcel.route}. Locker released.")
    elif choice == "3":
        print(app.queue.peek() or "Dispatch queue is empty.")
    elif choice == "4":
        show_path(app.queue.display_queue())
    elif choice == "5":
        app.deliver(read_id())
        print("Parcel marked delivered.")
    elif choice != "0":
        print("Invalid choice.")


def show_report(app):
    show_parcels(merge_sort(app.parcels))
    print(f"Total parcels: {len(app.parcels)}")
    for status in ("Registered", "Stored", "Queued", "Dispatched", "Delivered", "Cancelled"):
        print(f"{status}: {sum(parcel.status == status for parcel in app.parcels)}")
    print(f"Occupied lockers: {app.lockers.count_occupied()}")
    print(f"Available lockers: {app.lockers.count_available()}")


def run_menu(app):
    while True:
        print(MAIN_MENU)
        try:
            choice = input("Choice: ").strip()
            if choice == "0":
                return
            if choice == "1":
                register_parcel(app)
            elif choice == "2":
                show_parcels(app.parcels)
            elif choice == "3":
                search_parcels(app)
            elif choice == "4":
                sort_parcels(app)
            elif choice == "5":
                manage_stops(app)
            elif choice == "6":
                manage_routes(app)
            elif choice == "7":
                manage_lockers(app)
            elif choice == "8":
                manage_queue(app)
            elif choice == "9":
                parcel = app.hash_table.search(read_id())
                show_parcels([parcel] if parcel else [])
            elif choice == "10":
                app.hash_table.display()
            elif choice == "11":
                show_report(app)
            elif choice == "12":
                print(f"Sample parcels added: {app.load_samples()}")
            elif choice == "13":
                app.cancel(read_id())
                print("Parcel cancelled.")
            elif choice == "14":
                app.delete(read_id())
                print("Parcel deleted.")
            else:
                print("Invalid choice.")
        except ValueError as error:
            print(error)


def main():
    try:
        app = load()
    except (OSError, ValueError) as error:
        print(f"Could not open saved data. {error}")
        return 1
    while True:
        try:
            run_menu(app)
        except (EOFError, KeyboardInterrupt):
            print()
            try:
                save(app)
            except OSError as error:
                print(f"Could not save parcel data. {error}")
                return 1
            break
        try:
            save(app)
        except OSError as error:
            print(f"Could not save parcel data. Return to the menu to retry. {error}")
        else:
            break
    print("Parcel data saved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
