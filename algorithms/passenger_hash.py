from entities.passenger import Passenger

class HashTable:
    FREE = 0
    OCCUPIED = 1
    DELETED = 2

    def __init__(self, initial_size=10):
        self.size = initial_size
        self._table = [None] * self.size
        self._states = [self.FREE] * self.size
        self._count = 0
        self.load_factor_threshold = 0.7

    def _hash(self, key):
        return sum(ord(ch) for ch in key) % self.size

    def _next_index(self, base, i):
        return (base + i * i) % self.size

    def insert(self, passenger):
        key = passenger.passport
        index = self._hash(key)
        i = 0
        first_deleted = -1

        while i < self.size:
            current_index = self._next_index(index, i)
            if self._states[current_index] == self.FREE:
                if first_deleted != -1:
                    current_index = first_deleted
                self._table[current_index] = passenger
                self._states[current_index] = self.OCCUPIED
                self._count += 1
                if self._count > self.size * self.load_factor_threshold:
                    self._rehash()
                return True
            elif self._states[current_index] == self.DELETED and first_deleted == -1:
                first_deleted = current_index
            elif self._states[current_index] == self.OCCUPIED and self._table[current_index].passport == key:
                return False
            i += 1

        if i == self.size:
            self._rehash()
            return self.insert(passenger)

    def find(self, key):
        index = self._hash(key)
        i = 0
        while i < self.size:
            current_index = self._next_index(index, i)
            if self._states[current_index] == self.OCCUPIED and self._table[current_index].passport == key:
                return self._table[current_index]
            i += 1
        return None

    def delete(self, key):
        index = self._hash(key)
        i = 0
        while i < self.size:
            current_index = self._next_index(index, i)
            if self._states[current_index] == self.OCCUPIED and self._table[current_index].passport == key:
                self._states[current_index] = self.DELETED
                self._table[current_index] = None
                self._count -= 1
                return True
            i += 1
        return False

    def _rehash(self):
        old_table = self._table
        old_states = self._states
        old_size = self.size

        self.size *= 2
        self._table = [None] * self.size
        self._states = [self.FREE] * self.size
        self._count = 0

        for i in range(old_size):
            if old_states[i] == self.OCCUPIED:
                self.insert(old_table[i])

    def get_all_passengers(self):
        return [self._table[i] for i in range(self.size) if self._states[i] == self.OCCUPIED]