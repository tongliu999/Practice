from collections import deque, defaultdict
class LRUCache:
    def __init__(self, capacity: int):
        self.distinct = 0
        self.capacity = capacity
        self.count = defaultdict(int)
        self.values = defaultdict(int)
        self.q = deque()

    def get(self, key: int) -> int:
        if key not in self.values:
            return -1
        
        self.q.appendleft(key)
        self.count[key] += 1

        return self.values[key]

    def put(self, key: int, value: int) -> None:
        if key not in self.values:
            self.distinct += 1
        
        self.values[key] = value
        self.count[key] += 1
        self.q.appendleft(key)

        while self.capacity < self.distinct:
            print(self.q)
            curr = self.q.pop()
            self.count[curr] -= 1

            if self.count[curr] == 0:
                del self.values[curr]
                self.distinct -= 1
        
def test_lru_cache():
    cache = LRUCache(2)
    assert cache.get(99) == -1

    cache.put(1, 10)
    cache.put(2, 20)
    assert cache.get(1) == 10

    cache.put(3, 30)
    assert cache.get(2) == -1
    assert cache.get(3) == 30
    assert cache.get(1) == 10

    cache.put(4, 40)
    assert cache.get(3) == -1
    assert cache.get(1) == 10
    assert cache.get(4) == 40

    # Updating an existing key.
    cache = LRUCache(2)
    cache.put(1, 10)
    cache.put(2, 20)
    cache.put(1, 100)
    cache.put(3, 30)
    assert cache.get(1) == 100
    assert cache.get(2) == -1
    assert cache.get(3) == 30

    # Capacity one and a zero value.
    cache = LRUCache(1)
    cache.put(7, 0)
    assert cache.get(7) == 0
    cache.put(7, 70)
    assert cache.get(7) == 70
    cache.put(8, 80)
    assert cache.get(7) == -1
    assert cache.get(8) == 80

    # Repeated accesses before eviction.
    cache = LRUCache(2)
    cache.put(1, 10)
    cache.put(2, 20)
    for _ in range(10):
        assert cache.get(1) == 10

    cache.put(3, 30)
    assert cache.get(2) == -1
    assert cache.get(1) == 10

    cache.put(4, 40)
    assert cache.get(3) == -1
    assert cache.get(1) == 10
    assert cache.get(4) == 40

    # An evicted key can be inserted again.
    cache = LRUCache(1)
    cache.put(1, 10)
    cache.put(2, 20)
    cache.put(1, 100)
    assert cache.get(2) == -1
    assert cache.get(1) == 100

    print("All tests passed!")

test_lru_cache()