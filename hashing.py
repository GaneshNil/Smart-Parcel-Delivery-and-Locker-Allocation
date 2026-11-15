class HashTable:
    def __init__(self, capacity=13):
        self.buckets = [[] for _ in range(capacity)]
        self.size = 0

    def hash_index(self, parcel_id):
        index = 0
        for character in parcel_id:
            index = (index * 31 + ord(character)) % len(self.buckets)
        return index

    def insert(self, parcel):
        if self.search(parcel.parcel_id) is not None:
            return False
        self.buckets[self.hash_index(parcel.parcel_id)].append(parcel)
        self.size += 1
        return True

    def search(self, parcel_id):
        for parcel in self.buckets[self.hash_index(parcel_id)]:
            if parcel.parcel_id == parcel_id:
                return parcel
        return None

    def delete(self, parcel_id):
        bucket = self.buckets[self.hash_index(parcel_id)]
        for index, parcel in enumerate(bucket):
            if parcel.parcel_id == parcel_id:
                bucket.pop(index)
                self.size -= 1
                return True
        return False

    def load_factor(self):
        return self.size / len(self.buckets)

    def display(self):
        collisions = 0
        for index, bucket in enumerate(self.buckets):
            ids = " -> ".join(parcel.parcel_id for parcel in bucket)
            extra = max(0, len(bucket) - 1)
            collisions += extra
            print(f"{index:2} | {ids or '-'}" + (f" ({extra} collisions)" if extra else ""))
        print(f"Current collisions: {collisions} | Load factor: {self.load_factor():.2f}")
