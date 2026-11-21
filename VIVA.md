# ParcelFlow viva guide

| Lab | Implementation and complexity |
| --- | --- |
| 1. Searching | Linear Search scans until it finds the ID or reaches the end. It takes O(1) best-case time, O(n) average and worst-case time, and O(1) space. Binary Search halves the range at each step. It takes O(1) best-case time, O(log n) average and worst-case time, and O(1) space. The CLI runs Quick Sort before Binary Search. |
| 2. Sorting | Quick Sort partitions by the middle record's ID into smaller, equal, and larger groups. On distinct keys, balanced and average partitions take O(n log n) time, while unbalanced partitions can take O(n²) time and temporary space. Balanced partitions use O(n) peak temporary space. Merge Sort divides the list in half and merges by destination in O(n log n) time and O(n) auxiliary space. Equal destinations keep their original order. |
| 3. Singly linked list | Each stop node holds a parcel ID and a reference to the next stop. Finding or removing a stop can scan O(n) nodes. Appending takes O(1) once the duplicate check is complete. |
| 5. Circular linked list | The last node links to the first. Advancing to the next location takes O(1), and displaying a complete route takes O(n). Traversal stops when it returns to its starting node. |
| 6. 2D array | A cell holds 0 for free or 1 for occupied. Checking a selected cell takes O(1). Automatic assignment checks the first cell in the best case and scans up to all 100 cells in the worst case. The grid stores 100 values. |
| 7. Queue | Enqueue appends at the tail. Dispatch takes the value from the head and removes that node. Both take O(1) time. Cancelling a parcel can scan O(n) nodes and preserves FIFO order for the remaining parcels. |
| 9. Hash table | The hash function reads each character of the ID. Colliding IDs share the same bucket and lookup scans that bucket. With k characters and n records across b buckets, lookup takes O(k) in the best case, about O(k + n/b) on well-distributed short keys, and O(k + n) for short keys in the worst case. Load factor is n/b. |

The three linked structures use the same `Node` and `Chain` code. Stops and the queue end at `None`. A route links its tail back to its head. Records live in one list and buckets reference the same record objects. Queue and stop nodes store parcel IDs.
