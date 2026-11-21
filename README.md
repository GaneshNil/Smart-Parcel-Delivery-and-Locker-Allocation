# ParcelFlow — Smart Parcel Delivery and Locker Allocation

ParcelFlow is an offline Python mini-project for Semester III Data Structures (CE302). All application code is in `main.py`. Run it from this directory with Python 3.8 or later.

```sh
python3 main.py
```

Type commands at the prompt. Use `samples` to add 20 fictional parcels, or type `register P999` and enter the requested details. Sample IDs already in the registry are skipped. Use `exit` to save to `data/parcels.json`. The app reads the same JSON format as the earlier version.

## Demo

On an empty registry, enter these commands in order.

```text
samples
search P102
search P999
quick
merge
stops
cycle Route A
buckets
cancel P102
dispatch
peek
deliver P101
grid
exit
```

The dispatch prints `Dispatched: P101`, the next parcel is `P103`, and the grid shows 18 occupied lockers. Restart the app and use `peek` to confirm the queue was saved.

For a new parcel, use `store P999` to choose the first free locker or `store P999 3 5` to choose a specific locker. Then use `enqueue P999`. Enqueuing adds a delivery stop and assigns a route. New destinations join Route A by default. Dispatch and cancellation release the parcel's locker.

## Seven experiments

| Lab | Concept | Commands |
| --- | --- | --- |
| 1 | Linear and binary search | `search ID` |
| 2 | Quick Sort by ID and Merge Sort by destination | `quick`, `merge` |
| 3 | Singly linked delivery stops | `stops`, `addstop ID`, `findstop ID`, `removestop ID` |
| 5 | Circular linked delivery routes | `route NAME`, `next NAME`, `cycle NAME`, `addloc NAME / LOCATION`, `remloc NAME / LOCATION` |
| 6 | 10×10 locker array | `grid`, `store ID [row col]`, `release ID` |
| 7 | Linked FIFO dispatch queue | `enqueue ID`, `queue`, `peek`, `dispatch` |
| 9 | Hash table with separate chaining | `hash ID`, `buckets`, `delete ID` for completed or cancelled records |

See the [viva guide](VIVA.md) for the implementation and complexity of each experiment.
