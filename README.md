# ParcelFlow — Smart Parcel Delivery and Locker Allocation

ParcelFlow is a command-line mini-project for Semester III Data Structures (CE302). You can register parcels, assign lockers, plan delivery stops, and dispatch parcels in the order they were queued. All seven experiments run in a single Python file.

## Run the app

Open a terminal in the project directory and run the following command. You need Python 3.8 or later. The app runs offline and uses only the Python standard library.

```sh
python3 main.py
```

Enter one command at each `parcelflow>` prompt. The command guide appears at startup. Type `list` to see all parcels or `exit` to save and close the app. On startup, ParcelFlow reloads parcel records, locker assignments, routes, and queue order from `data/parcels.json` if it exists.

## Demo

On an empty registry, enter the commands below. `samples` adds 20 fictional parcels and skips sample IDs already in the registry.

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

## Manage a parcel

1. Enter `register P999`. Provide the recipient's name, a 7–15 digit contact number, the destination, and a positive weight in kilograms.
2. Enter `store P999` to use the first free locker, or `store P999 3 5` to choose row 3, column 5. Rows and columns range from 1 to 10.
3. Enter `enqueue P999` to add the parcel to the dispatch queue and delivery stops. If no route already serves its destination, ParcelFlow adds the destination to Route A.
4. Use `peek` to see which parcel is next and `dispatch` to send it out and free its locker. Once P999 has been dispatched, enter `deliver P999`.

Use `release ID` to free a stored parcel's locker and return it to Registered status. Use `cancel ID` before dispatch to free its locker and remove it from the queue and stops. Use `delete ID` to remove a delivered or cancelled record.

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

## Project files

- [main.py](main.py) contains the CLI, parcel workflow, and seven data structure experiments.
- [VIVA.md](VIVA.md) explains how each experiment works and gives its time and space complexity.
- `data/parcels.json` is created when you save.
