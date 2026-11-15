class LockerGrid:
    def __init__(self):
        self.locker_grid = [[0 for _ in range(10)] for _ in range(10)]

    def valid_position(self, row, column):
        return 1 <= row <= 10 and 1 <= column <= 10

    def is_available(self, row, column):
        return self.valid_position(row, column) and self.locker_grid[row - 1][column - 1] == 0

    def allocate(self, position=None):
        if position is None:
            for row in range(1, 11):
                for column in range(1, 11):
                    if self.is_available(row, column):
                        return self.allocate((row, column))
            return None

        row, column = position
        if not self.is_available(row, column):
            return None
        self.locker_grid[row - 1][column - 1] = 1
        return position

    def release(self, row, column):
        if not self.valid_position(row, column) or self.is_available(row, column):
            return False
        self.locker_grid[row - 1][column - 1] = 0
        return True

    def count_occupied(self):
        return sum(sum(row) for row in self.locker_grid)

    def count_available(self):
        return 100 - self.count_occupied()

    def display(self):
        print("     " + " ".join(f"{column:2}" for column in range(1, 11)))
        for index, row in enumerate(self.locker_grid, 1):
            print(f"{index:2} | " + " ".join(f"{value:2}" for value in row))
        occupied = self.count_occupied()
        print(f"Occupied: {occupied} | Available: {100 - occupied}")
