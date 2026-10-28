import math
from collections import defaultdict, deque

class CSATTracker:
    def __init__(self, window_size: int):
        self.totalScore = 0
        self.scores = defaultdict(int)
        self.ids = {}
        self.window_size = window_size
        self.que = deque()

    def record(self, conversation_id: str, score: int, timestamp: int):
        self.clean(timestamp)
        if conversation_id in self.ids:
            return False
        
        self.scores[score] += 1
        self.ids[conversation_id] = score
        self.totalScore += score
        self.que.append((timestamp + self.window_size, conversation_id, score))
        return True

    def get_average(self, current_time: int) -> float:
        self.clean(current_time)
        if len(self.ids) == 0:
            return 0

        return round(self.totalScore / len(self.ids), 2)

    def update(self, conversation_id: str, score: int):
        if conversation_id not in self.ids:
            return False
        
        old_score = self.ids[conversation_id]
        diff = score - old_score
        self.totalScore += diff
        self.scores[score] += 1
        self.scores[old_score] -= 1
        self.ids[conversation_id] = score

    def get_percentile(self, current_time: int, p: int) -> int | None:
        
        self.clean(current_time)
        curr = 0

        if len(self.ids) == 0:
            return None
        
        count = math.ceil(p * len(self.ids) / 100)
        while count > 0:
            curr += 1
            count -= self.scores[curr]
        
        return curr

    def clean(self, current_time):
        while self.que and self.que[0][0] < current_time:
            _, conversation_id, _ = self.que.popleft()
            score = self.ids.pop(conversation_id)
            self.totalScore -= score
            self.scores[score] -= 1

def test():
    t = CSATTracker(5)
    assert t.get_average(0) == 0.0
    assert t.get_percentile(0, 50) is None

    t.record("a", 5, 1)
    t.record("b", 3, 2)
    assert t.get_average(2) == 4.0
    assert t.get_percentile(2, 50) == 3
    assert t.get_percentile(2, 100) == 5

    t.update("a", 1)
    assert t.get_average(2) == 2.0
    assert t.get_percentile(2, 50) == 1

    t.update("a", 2)
    assert t.get_average(2) == 2.5
    assert t.get_percentile(2, 100) == 3

    assert t.get_average(6) == 2.5
    assert t.get_average(7) == 3.0

    t.update("a", 5)
    t.update("missing", 4)
    assert t.get_average(7) == 3.0
    assert t.get_average(8) == 0.0
    assert t.get_percentile(8, 90) is None

    t = CSATTracker(10)
    t.record("a", 1, 1)
    t.record("b", 2, 2)
    t.record("c", 2, 3)
    assert t.get_average(3) == 1.67
    assert t.get_percentile(3, 1) == 1
    assert t.get_percentile(3, 50) == 2

    t = CSATTracker(0)
    t.record("a", 4, 10)
    assert t.get_average(10) == 4.0
    assert t.get_average(11) == 0.0
    assert t.get_percentile(11, 100) is None

    print("All tests passed!")

test()