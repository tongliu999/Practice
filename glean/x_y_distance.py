from collections import deque
import math

def nearest_distance(chars: list[str]) -> int:
    # keep track of last_x and last_y, and compare to current min
    last_x = None
    last_y = None
    res = math.inf

    for i in range(len(chars)):
        if chars[i] == "X":
            last_x = i
        elif chars[i] == "Y":
            last_y = i
        
        if last_x != None and last_y != None:
            res = min(abs(last_x - last_y), res)
        
    return res if res != math.inf else -1

def nearest_distance_2d(grid: list[list[str]]) -> int:
    # part 1: find all O's in grid and put them in queue
    q = deque()
    visited = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    distance = 0

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "X":
                q.append((row, col))
    
    # part 2: BFS until you find the nearest X, go through all of the queue to maintain distance
    while q:
        for i in range(len(q)):
            coord = q.popleft()
            row, col = coord

            if row < 0 or col < 0 or row >= len(grid) or col >= len(grid[0]) or coord in visited:
                continue
                
            if grid[row][col] == "Y":
                return distance
            
            visited.add(coord)
            
            for x, y in directions:
                q.append((row + x, col + y))
            
        distance += 1
    
    return -1

def test_nearest_distance():
    cases = [
        ([], -1),
        (["O"], -1),
        (["X"], -1),
        (["Y"], -1),
        (["X", "Y"], 1),
        (["Y", "X"], 1),
        (["X", "O", "O", "Y"], 3),
        (["Y", "O", "O", "X"], 3),
        (["X", "O", "O", "Y", "O", "X"], 2),
        (["Y", "O", "Y", "O", "X"], 2),
        (["X", "O", "X", "O", "Y"], 2),
        (["X", "O", "Y", "X"], 1),
        (["O", "X", "O"], -1),
        (["Y", "O", "Y"], -1),
        (["O", "Y", "O", "O", "X", "O"], 3),
    ]

    for i, (chars, expected) in enumerate(cases, 1):
        actual = nearest_distance(chars)
        assert actual == expected, (
            f"Test {i}, chars={chars}: "
            f"expected {expected}, got {actual}"
        )

    print("All tests passed!")

def test_nearest_distance_2d():
    cases = [
        ([], -1),
        ([[]], -1),
        ([["O"]], -1),
        ([["X"]], -1),
        ([["Y"]], -1),
        ([["X", "Y"]], 1),
        ([["Y", "O", "X"]], 2),
        ([["X"], ["O"], ["Y"]], 2),
        (
            [["X", "O", "O"],
             ["O", "O", "O"],
             ["O", "O", "Y"]],
            4,
        ),
        (
            [["X", "O", "O"],
             ["O", "O", "Y"],
             ["O", "X", "O"]],
            2,
        ),
        (
            [["X", "O", "O", "Y"],
             ["O", "O", "X", "O"]],
            2,
        ),
        (
            [["X", "O", "Y"],
             ["Y", "O", "X"]],
            1,
        ),
        (
            [["X", "O"],
             ["O", "X"]],
            -1,
        ),
        (
            [["Y", "O"],
             ["O", "Y"]],
            -1,
        ),
    ]

    for i, (grid, expected) in enumerate(cases, 1):
        original = [row[:] for row in grid]
        actual = nearest_distance_2d(grid)

        assert actual == expected, (
            f"Test {i}: expected {expected}, got {actual}"
        )
        assert grid == original, f"Test {i}: grid was modified"

    print("All tests passed!")

test_nearest_distance_2d()