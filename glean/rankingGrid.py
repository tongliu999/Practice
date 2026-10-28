import heapq

def matrix_ranks(matrix: list[list[int]]) -> list[list[int]]:
    rows = [1] * len(matrix)
    cols = [1] * len(matrix[0])
    heap = []

    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            heapq.heappush(heap, (matrix[row][col], row, col))

    while heap:
        value, row, col = heapq.heappop(heap)

        rank = max(rows[row], cols[col])
        matrix[row][col] = rank
        rows[row] = rank + 1
        cols[col] = rank + 1
    
    return matrix

def test_matrix_ranks():
    cases = [
        ([[7]], [[1]]),
        (
            [[10, 40, 20, 30]],
            [[1, 4, 2, 3]],
        ),
        (
            [[30], [10], [20]],
            [[3], [1], [2]],
        ),
        (
            [[1, 5], [4, 2]],
            [[1, 2], [2, 1]],
        ),
        (
            [[1, 2], [3, 4]],
            [[1, 2], [2, 3]],
        ),
        (
            [[-3, -1], [-2, 0]],
            [[1, 2], [2, 3]],
        ),
        (
            [[1, 2, 3], [4, 5, 6]],
            [[1, 2, 3], [2, 3, 4]],
        ),
        (
            [[6, 5, 4], [3, 2, 1]],
            [[4, 3, 2], [3, 2, 1]],
        ),
        (
            [
                [3, 1, 9],
                [8, 2, 7],
                [4, 6, 5],
            ],
            [
                [2, 1, 6],
                [6, 2, 5],
                [3, 5, 4],
            ],
        ),
    ]

    for i, (matrix, expected) in enumerate(cases, 1):
        original = [row[:] for row in matrix]
        actual = matrix_ranks(matrix)
        assert actual == expected, (
            f"Test {i}, input={original}: "
            f"expected {expected}, got {actual}"
        )

    print("All tests passed!")

test_matrix_ranks()