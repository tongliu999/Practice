from collections import deque

def min_total_distance(grid: list[str]) -> int:
    if not grid or not grid[0]:
        return -1

    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    targets = [
        (row, col)
        for row in range(rows)
        for col in range(cols)
        if grid[row][col] == "x"
    ]

    totals = [[0] * cols for _ in range(rows)]
    reached = [[0] * cols for _ in range(rows)]

    # Find distances from each target to every reachable cell.
    for start in targets:
        queue = deque([(start[0], start[1], 0)])
        seen = {start}

        while queue:
            row, col, distance = queue.popleft()

            totals[row][col] += distance
            reached[row][col] += 1

            for dr, dc in directions:
                nr, nc = row + dr, col + dc

                if (
                    0 <= nr < rows
                    and 0 <= nc < cols
                    and grid[nr][nc] != "w"
                    and (nr, nc) not in seen
                ):
                    seen.add((nr, nc))
                    queue.append((nr, nc, distance + 1))

    # Only consider cells reachable from every target.
    best = float("inf")

    for row in range(rows):
        for col in range(cols):
            if (
                grid[row][col] != "w"
                and reached[row][col] == len(targets)
            ):
                best = min(best, totals[row][col])

    return best if best != float("inf") else -1

def test_min_total_distance():
    cases = [
        (["x"], 0),
        (["x."], 0),
        (["xx"], 1),
        (["xxx"], 2),
        (["x.x"], 2),
        (["x.x.x"], 4),
        (["xwx"], -1),
        (
            ["x.x",
             "...",
             ".x."],
            4,
        ),
        (
            ["x.w.x",
             "..w..",
             "....."],
            8,
        ),
        (
            ["xx",
             "xx"],
            4,
        ),
        (
            ["x..",
             "...",
             "..x"],
            4,
        ),
        (
            ["x..",
             "www",
             "..x"],
            -1,
        ),
        (
            ["xw.",
             "www",
             "..."],
            0,
        ),
    ]

    for i, (grid, expected) in enumerate(cases, 1):
        original = grid[:]
        actual = min_total_distance(grid)

        assert actual == expected, (
            f"Test {i}, grid={original}: "
            f"expected {expected}, got {actual}"
        )
        assert grid == original, f"Test {i}: grid was modified"

    print("All tests passed!")

test_min_total_distance()