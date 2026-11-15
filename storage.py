import json
from pathlib import Path

from system import ParcelFlow, TERMINAL_STATUSES


DATA_PATH = Path(__file__).resolve().parent / "data" / "parcels.json"


def save(app, path=DATA_PATH):
    data = {
        "parcels": [vars(parcel) for parcel in app.parcels],
        "stops": app.stops.traverse(),
        "queue": app.queue.display_queue(),
        "routes": [
            {"name": name, "locations": route.cycle(),
             "current": route.current.value if route.current is not None else None}
            for name, route in app.routes.items()
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def load(path=DATA_PATH):
    app = ParcelFlow()
    try:
        content = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return app
    if not content.strip():
        return app

    try:
        data = json.loads(content)
        for entry in data["routes"]:
            route = app.create_route(entry["name"])
            for location in entry["locations"]:
                if not route.add(location):
                    raise ValueError("Duplicate route location.")
            current = entry["current"]
            if current is not None:
                if current not in route.cycle():
                    raise ValueError("Unknown current route location.")
                while route.current.value != current:
                    route.next_location()
            elif route.head is not None:
                raise ValueError("Missing current route location.")

        for record in data["parcels"]:
            parcel = app.register(record["parcel_id"], record["recipient"], record["contact"],
                                  record["destination"], record["weight"])
            parcel.status = record["status"]
            parcel.route = record["route"]
            locker = record["locker"]
            if parcel.status in ("Stored", "Queued"):
                if locker is None or app.lockers.allocate(tuple(locker)) is None:
                    raise ValueError("Invalid or duplicate locker assignment.")
                parcel.locker = tuple(locker)
            elif locker is not None or parcel.status not in (
                    "Registered", "Dispatched", *TERMINAL_STATUSES):
                raise ValueError("Invalid parcel status or locker assignment.")
            if parcel.status in ("Queued", "Dispatched"):
                if parcel.route not in app.routes or parcel.destination not in app.routes[parcel.route].cycle():
                    raise ValueError("An active delivery is missing its route or destination.")

        for parcel_id in data["stops"]:
            if not app.add_stop(parcel_id):
                raise ValueError("Duplicate delivery stop.")
        for parcel_id in data["queue"]:
            if app.require_parcel(parcel_id).status != "Queued":
                raise ValueError("Dispatch queue contains a parcel with the wrong status.")
            app.queue.enqueue(parcel_id)

        queue_ids = app.queue.display_queue()
        expected_ids = {parcel.parcel_id for parcel in app.parcels if parcel.status == "Queued"}
        if set(queue_ids) != expected_ids or len(queue_ids) != len(expected_ids):
            raise ValueError("Dispatch queue entries do not match the queued parcels.")
        stop_ids = set(app.stops.traverse())
        for parcel in app.parcels:
            if parcel.status in ("Queued", "Dispatched") and parcel.parcel_id not in stop_ids:
                raise ValueError("An active delivery is missing its stop.")
    except (ValueError, TypeError, KeyError, AttributeError, IndexError, OverflowError) as error:
        raise ValueError(f"Invalid parcel data in {path}: {error}") from error
    return app
