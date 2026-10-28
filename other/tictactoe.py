def count_games():
    res = 0

    

    return res

def backtrack(board, pieces, turn):
    if completed(board):
        return 1
    
    res = 0
    new_turn = "X" if turn == "O" else "O"
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == "-":
                board[row][column] = turn
            else:
                continue
            res += backtrack(board, pieces + 1, new_turn)
            board[row][column] = "-"

    return res

def completed(board):
    pieces = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != "-":
                pieces += 1
    
    if pieces == 9:
        return True

    for row in board:
        win = True
        initial = row[0]
        if initial == "-":
            continue
        for i in row:
            if i != initial:
                win = False
        
        if win:
            return True

    for column in range(len(board[0])):
        win = True
        initial = board[0][column]
        if initial == "-":
            continue
        for i in range(len(board)):
            if board[i][column] != initial:
                win = False
        
        if win:
            return True

    if (board[0][0] == board[1][1] == board[2][2]) and board[0][0] != "-":
        return True
    
    if (board[0][2] == board[1][1] == board[2][0] and board[0][2] != "-"):
        return True
    
    return False

def test():
    board = [["-"] * 3 for _ in range(3)]
    result = backtrack(board, 0, "X")
    print(f"Expected: 255168, got: {result}")
    assert result == 255168

test()
    
        



            