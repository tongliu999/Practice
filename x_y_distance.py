from collections import deque

def nearest_distance_2d(grid: list[list[str]]) -> int:
    # bfs

    # part 1: find all X's and put them in queue
    q = deque()
    visited = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    distance = 0

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "X":
                q.append((row, col))

    # part 2: expand search for Y's and keep track of distance, once we find Y, return distance
    
    while q:
        for i in range(len(q)):
            row, col = q.popleft()
            if ((row, col)) in visited or row < 0 or col < 0 or row >= len(grid) or col >= len(grid[0]):
                continue
            if grid[row][col] == "Y":
                return distance
            
            visited.add((row, col))

            for x, y in directions:
                q.append((row + x, col + y))
        
        distance += 1
    
    return -1 





def test():
    cases = [
        ([], -1),
        ([["O"]], -1),
        ([["X"]], -1),
        ([["Y"]], -1),
        ([["X", "Y"]], 1),
        ([["Y", "O", "X"]], 2),
        ([["X"], ["O"], ["Y"]], 2),
        ([
            ["X", "O", "O"],
            ["O", "O", "O"],
            ["O", "O", "Y"],
        ], 4),
        ([
            ["X", "O", "O"],
            ["O", "O", "Y"],
            ["O", "X", "O"],
        ], 2),
        ([
            ["X", "O", "O", "Y"],
            ["O", "O", "X", "O"],
        ], 2),
        ([
            ["X", "Y", "O"],
            ["O", "O", "X"],
        ], 1),
        ([
            ["X", "O"],
            ["O", "X"],
        ], -1),
    ]

    for i, (grid, expected) in enumerate(cases, 1):
        original = [row[:] for row in grid]
        actual = nearest_distance_2d(grid)
        assert actual == expected, (
            f"Test {i}: expected {expected}, got {actual}"
        )
        assert grid == original, f"Test {i}: input was modified"

    print("All tests passed!")

test()