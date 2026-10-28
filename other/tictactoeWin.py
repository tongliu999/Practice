def solve(board: list[str]) -> tuple[str, tuple[int, int] | None]:
    def backtracking(count, piece):
        winner = find_win(board)
        new_piece = "O" if piece == "X" else "X"
        if count == 9:
            return winner
        
        if winner != "-":
            return winner

        result = new_piece
        best_move = None
        for row in board:
            for col in row:
                if col == "-":
                    if not best_move:
                        best_move = (row, col)
                    col = piece
                    result, move = backtracking(count + 1, new_piece)
                    if result == piece:
                        return piece, (row, col)
                    elif result == "-":
                        result = "-"
                        best_move = (row, col)
                    col = "-"
        
        return (result, best_move)


    def find_win(board):
        for row in range(len(board)):
            initial = board[row][0]
            win = True
            if initial == "-":
                continue
            for column in range(len(board[0])):
                if board[column][row] != initial:
                    win = False
            
            if win:
                return initial
        
        for column in range(len(board)):
            initial = board[0][column]
            win = True
            if initial == "-":
                continue
            for row in range(len(column)):
                if board[column][row] != initial:
                    win = False
            
            if win:
                return initial
        
        initial = board[0][0]
        win = True
        for step in range(len(board)):
            if initial == "-":
                continue
            if board[step][step] != initial:
                win = False
            
        if win:
            return initial

        initial = board[0][2]
        win = True
        for step in range(len(board)):
            if initial == "-":
                continue
            if board[step][2 - step] != initial:
                win = False
            
        if win:
            return initial
        
        return "-"

    return backtracking(0, "X")

def test():
    cases = [
        (["XX.", "OO.", "..."], "X", {(0, 2)}),
        (["OO.", "XX.", "X.."], "O", {(0, 2)}),
        (["XXX", "OO.", "..."], "X", {None}),
        (["XX.", "OOO", "X.."], "O", {None}),
        (["XOX", "XOO", "OXX"], "draw", {None}),
        (["XOX", "XOO", "OX."], "draw", {(2, 2)}),
        (["...", "...", "..."], "draw",
         {(r, c) for r in range(3) for c in range(3)}),
    ]

    for i, (board, expected, valid_moves) in enumerate(cases, 1):
        original = board.copy()
        result = solve(board)
        print(f"Test {i}: expected {expected}, got {result}")
        outcome, move = result
        assert outcome == expected
        assert move in valid_moves
        assert board == original

    print("All tests passed!")

test()