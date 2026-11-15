# ParcelFlow viva guide

Start with **12** to load the sample parcels. Follow `P101` through the registry, its locker, its queue position, and Route A. Dispatch it with **8 → 2** and mark it delivered with **8 → 5**. Use the hash search to see its updated status.

| Lab | What to explain and show |
| --- | --- |
| **1. Searching** | Linear Search checks each parcel in registry order and takes O(n) in the worst case. Binary Search compares the middle ID and discards half the remaining range each step, taking O(log n) once the input is sorted. Both use O(1) auxiliary space. Show that `P102` returns the same object through both searches. |
| **2. Sorting** | Quick Sort partitions a copy around a pivot, then sorts each partition. Its typical time is O(n log n), with O(n²) for unbalanced partitions. It recurses on the smaller partition, keeping the stack to O(log n). Merge Sort splits the records in half, then merges in destination order in O(n log n) time. When destinations match, the left record goes first, preserving their order. Both reports use O(n) auxiliary space including the output. |
| **3. Singly linked list** | A stop node stores a parcel ID and a `next` reference. Traverse from `head` until `None`. To remove a middle stop, update the previous node's `next` reference to bypass it. Search, traversal, and a duplicate-checked add take O(n) worst-case time. Try adding and removing a stop for a newly registered parcel. |
| **5. Circular linked list** | The last location points back to the first. Next advances in O(1). A complete circuit stops when the current node is the same object as the starting node again, taking O(n) time. With one location, the node points to itself. Show a complete Route A cycle from a location other than the hub. |
| **6. 2D array** | Each cell contains 0 for available or 1 for occupied. Menu coordinates are 1-based, so `(1, 1)` maps to grid index `[0][0]`. A chosen locker is checked in O(1). Automatic allocation scans row by row in up to O(g) time. Show a locker becoming available after dispatch. |
| **7. Queue** | `front` points to the next parcel and `rear` to the last. Enqueue links a node after `rear`, and dequeue moves `front` forward. Both take O(1). After removing the final node, both references are empty. Cancel a parcel between two queued parcels and confirm the others keep their order. |
| **9. Hash table** | Multiply the current hash by 31, add the next character code, and take the remainder by capacity. IDs at the same index share a bucket through separate chaining. Lookup scans only that bucket and can take O(n) string comparisons if all records collide. Load factor is number of records divided by bucket count. Show a chain with multiple IDs after loading samples. |

**Why do the search results stay consistent?** The registry and hash buckets refer to the same parcel objects. Locker coordinates and status live on that object. The queue and stop list store IDs. On startup, JSON supplies the parcel records and the saved ordering needed to rebuild the index, grid, and linked structures.

**What keeps a parcel from being dispatched twice?** Enqueuing requires Stored status and changes it to Queued. Dispatch removes the head entry and changes the parcel to Dispatched. Cancellation removes the entry while preserving the remaining FIFO order.
