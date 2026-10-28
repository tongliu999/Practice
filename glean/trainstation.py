def can_reach(schedule: list[list[str]], start: str, destination: str) -> bool:
    if start == destination:
        return True
    reachable = {start}
    boarded = [False] * len(schedule)

    max_time = 0
    for i in range(len(schedule)):
        max_time = max(len(schedule[i]), max_time)

    for t in range(max_time):
        for i in range(len(schedule)):
            if boarded[i] and t < len(schedule[i]):
                reachable.add(schedule[i][t])
        
        for i in range(len(schedule)):
            if not boarded[i] and t < len(schedule[i]) and schedule[i][t] in reachable:
                boarded[i] = True

    return destination in reachable

def test_can_reach():
    cases = [
        ([["A"]], "A", "A", True),
        ([["A", "B", "C"]], "A", "C", True),
        ([["A", "B", "C"]], "C", "A", False),
        (
            [["A", "B", "C"], ["D", "B", "E"]],
            "A", "E", True,
        ),
        (
            [["A", "B", "C"], ["D", "B", "E"]],
            "A", "D", False,
        ),
        (
            [["A", "B"], ["P", "Q", "B", "Z"]],
            "A", "Z", True,
        ),
        (
            [["A", "X", "B"], ["Y", "B", "Z"]],
            "A", "Z", False,
        ),
        (
            [["P", "A", "Z"]],
            "A", "Z", True,
        ),
        (
            [["A", "B", "A", "C"]],
            "B", "A", True,
        ),
        (
            [["A", "B"], ["C", "D"]],
            "A", "D", False,
        ),
        (
            [["A", "B"], ["B", "C"]],
            "A", "C", False,
        ),
        (
            [["A", "B"], ["X", "B", "C"], ["Y", "Z", "C", "D"]],
            "A", "D", True,
        ),
        (
            [
                ["A", "P", "Q", "R", "H"],
                ["A", "H"],
                ["X", "Y", "H", "Z"],
            ],
            "A", "Z", True,
        ),
    ]

    for i, (schedule, start, destination, expected) in enumerate(cases, 1):
        actual = can_reach(schedule, start, destination)
        assert actual == expected, (
            f"Test {i}, {start} -> {destination}: "
            f"expected {expected}, got {actual}"
        )

    print("All tests passed!")

test_can_reach()
