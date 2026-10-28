import heapq
from collections import defaultdict
class SuggestionIndex:
    def __init__(self, suggestions: list[tuple[str, int, int]]):
        self.department = defaultdict(list)
        self.scores = {}
        for name, id, score in suggestions:
            if name in self.department[id]:
                continue
            self.department[id].append(name)
            self.scores[(id, name)] = score
        
        for key in self.department.keys():
            self.department[key] = sorted(self.department[key])

    def search(self, prefix: str, department_id: int, k: int) -> list[tuple[str, int, int]]:
        heap = []

        if department_id not in self.department:
            return heap
        
        curr = self.department[department_id]

        for name in curr:
            if name.startswith(prefix):
                heapq.heappush(heap, (-1 * self.scores[(department_id, name)], name))

        res = []
        while heap and len(res) < k:
            score, name = heapq.heappop(heap)
            res.append((name, department_id, -1 * score))

        return res

def test_suggestion_index():
    suggestions = [
        ("python guide", 1, 90),
        ("python basics", 1, 75),
        ("python hiring", 2, 100),
        ("pytorch intro", 1, 85),
        ("python recipes", 1, 85),
        ("python tools", 1, 85),
        ("java guide", 1, 95),
        ("python guide", 2, 60),
        ("py", 1, 50),
    ]

    cases = [
        ("py", 1, 2),
        ("py", 1, 3),
        ("py", 1, 100),
        ("python", 1, 2),
        ("python guide", 1, 1),
        ("python guide extra", 1, 1),
        ("py", 2, 2),
        ("java", 1, 5),
        ("", 1, 3),
        ("", 2, 100),
        ("missing", 1, 3),
        ("py", 999, 3),
        ("py", 1, 0),
    ]

    index = SuggestionIndex(suggestions)

    for i, (prefix, dept, k) in enumerate(cases, 1):
        actual = index.search(prefix, dept, k)

        matches = [
            entry for entry in suggestions
            if entry[0].startswith(prefix) and entry[1] == dept
        ]
        expected_scores = sorted(
            (entry[2] for entry in matches), reverse=True
        )[:k]

        assert len(actual) == len(expected_scores), (
            f"Test {i}: wrong number of results"
        )
        assert len(set(actual)) == len(actual), (
            f"Test {i}: duplicate results"
        )
        assert all(entry in matches for entry in actual), (
            f"Test {i}: invalid result"
        )
        assert [entry[2] for entry in actual] == expected_scores, (
            f"Test {i}: wrong scores or ordering; got {actual}"
        )

    empty = SuggestionIndex([])
    assert empty.search("", 1, 5) == []
    assert empty.search("py", 1, 0) == []

    print("All tests passed!")

test_suggestion_index()
        
