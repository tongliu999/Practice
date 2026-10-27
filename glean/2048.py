def apply_move(board: list[list[int]], direction: str) -> list[list[int]]:
    grid = []
    horizontal = direction in ("left", "right")

    if horizontal:
        for row in board:
            grid.append([value for value in row if value != 0])
    else:
        for col in range(len(board[0])):
            curr = []
            for row in range(len(board)):
                if board[row][col] != 0:
                    curr.append(board[row][col])
            grid.append(curr)

    for index, line in enumerate(grid):
        if direction in ("right", "down"):
            line.reverse()

        merged = []
        i = 0

        while i < len(line):
            if i + 1 < len(line) and line[i] == line[i + 1]:
                merged.append(line[i] * 2)
                i += 2
            else:
                merged.append(line[i])
                i += 1

        size = len(board[0]) if horizontal else len(board)
        merged.extend([0] * (size - len(merged)))

        if direction in ("right", "down"):
            merged.reverse()

        if horizontal:
            board[index] = merged
        else:
            for row in range(len(board)):
                board[row][index] = merged[row]

    return board