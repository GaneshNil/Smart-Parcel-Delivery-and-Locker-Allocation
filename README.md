# ParcelFlow — Smart Parcel Delivery and Locker Allocation

ParcelFlow is an offline Semester III CE302 mini-project. A parcel desk needs to find parcels, prevent locker double bookings, and dispatch stored parcels in arrival order. The application uses one parcel registry to connect those operations with delivery stops and recurring routes.

## Objectives and features

- Register parcels with unique IDs, check their status, and compare search results across the registry and hash table.
- Allocate one of 100 lockers, plan delivery stops and routes, and dispatch parcels in FIFO order.
- Generate sorted reports and restore the same working state after a restart.

## Run the project

Use Python 3.8 or later. The project uses the Python standard library and runs offline.

From the `ParcelFlow` directory:

```sh
python3 main.py
python3 -m unittest discover -s tests -v
```

The first run starts empty. Option **12** adds 20 fictional parcels with IDs `P101` through `P120`. It skips IDs already present and stores and queues new samples while lockers are available. Option **0** saves to `data/parcels.json`. The app creates that file on first save.

## Seven selected assignments

| Lab | Topic | Source and application |
| --- | --- | --- |
| 1 | Searching | `searching.py` finds an ID using linear and binary search |
| 2 | Sorting | `sorting.py` runs Quick Sort by ID and stable Merge Sort by destination |
| 3 | Singly linked list | `singly_linked_list.py` keeps the ordered delivery stops |
| 5 | Circular linked list | `circular_linked_list.py` stores recurring routes and supports one full circuit |
| 6 | 2D array | `locker.py` tracks and allocates 100 lockers |
| 7 | Queue | `dispatch_queue.py` dispatches parcels in FIFO order using linked nodes |
| 9 | Hash table | `hashing.py` indexes parcel IDs and displays collisions and load factor |

`main.py` handles the menu, `parcel.py` defines records and sample inputs, `system.py` coordinates the lifecycle, `storage.py` saves and restores JSON, and `tests/test_parcelflow.py` tests the structures and integrated workflows. The queue module is named `dispatch_queue.py` to avoid shadowing Python's standard-library `queue` module.

## Lifecycle

`Registered → Stored → Queued → Dispatched → Delivered`

Register a parcel in option **1**, allocate its locker in option **7**, and enqueue it in option **8**. Enqueuing ensures the parcel has a delivery stop and joins an existing route that serves the destination or adds the destination to a default route. The stop stays active until delivery. Dispatch releases the locker immediately. A manual release is available while stored and returns the parcel to Registered.

Option **13** cancels a registered, stored, or queued parcel. Cancellation releases its locker and removes its stop and queue entry when present. Option **14** removes a delivered or cancelled record from both the registry and hash index.

## Example demonstration

1. Load samples with **12**. Use **3** with `P102` and `P999` to compare a hit and a miss. Use **4 → 1** and **4 → 2** for the two sort orders.
2. Use **10** to display occupied buckets, collision counts, and a load factor of `1.54` (20 records in 13 buckets).
3. Use **6 → 6**, then enter `Route A`, to walk a cycle through Distribution Hub, Kothrud, Karve Nagar, Deccan, and Shivajinagar, returning to the hub.
4. Cancel `P102` with **13**. Use **8 → 2** to dispatch `P101`, then **8 → 3** to peek at the next parcel, `P103`.
5. Use **7 → 1** to see 18 occupied lockers. Save with **0**, restart, and check the next parcel and locker totals again.

Sample dispatch output:

```text
P101 dispatched on Route A. Locker released.
```

## Algorithm complexity

Here, *n* is the number of records or nodes in the operation, *g* is locker capacity, *b* is the number of hash buckets, and *k* is the parcel ID length. The table treats other string comparisons as constant-time for short input fields. Auxiliary space includes temporary result lists.

| Operation | Best time | Average time | Worst time | Auxiliary space |
| --- | --- | --- | --- | --- |
| Linear search | O(1) | O(n) | O(n) | O(1) |
| Binary search on ID-sorted records | O(1) | O(log n) | O(log n) | O(1) |
| Quick Sort by ID | O(n log n) | O(n log n) | O(n²) | O(n) including the copy, O(log n) maximum stack |
| Merge Sort by destination | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Stop search or removal | O(1) | O(n) | O(n) | O(1) |
| Add a new stop with duplicate check | O(n) | O(n) | O(n) | O(1) |
| List or route traversal | O(n) | O(n) | O(n) | O(n) for the result |
| Add a new route location | O(n) | O(n) | O(n) | O(n) for the duplicate-check list |
| Remove a route location | O(1) | O(n) | O(n) | O(1) |
| Advance a route, or enqueue, dequeue, peek | O(1) | O(1) | O(1) | O(1) |
| Queue display or cancellation scan | O(n) | O(n) | O(n) | O(n) for display, O(1) for scan live space |
| Check, allocate a chosen cell, or release | O(1) | O(1) | O(1) | O(1) |
| Find first free cell | O(1) | Depends on occupancy | O(g) | O(1) |
| Count or display lockers | O(g) | O(g) | O(g) | O(1) for each printed row in the fixed grid |
| Hash insert, search, or delete | O(k) | O(k + n/b) with good distribution and short keys | O(k + n) for short keys | O(1) |
| Hash load factor | O(1) | O(1) | O(1) | O(1) |

The search comparison builds an ID-sorted copy with Quick Sort before running Binary Search. Linked lists and the queue use O(n) storage for nodes, the grid uses O(g), and the hash table uses O(b + n). The hash table has a fixed 13 buckets, so average chain length grows as more parcels are registered.

## Future scope

Potential extensions include grouping stops by delivery area, adding a delivery history, and resizing the hash table as the registry grows.

See the [viva guide](VIVA.md) for implementation walkthroughs and demonstration prompts.
# Smart-Parcel-Delivery-and-Locker-Allocation
