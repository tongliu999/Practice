def game_winner(n: int, k: int) -> str:
    visited = {}

    def backtracking(win, curr, player):
        if curr + k >= win or (curr in visited and visited[curr]):
            return player

        new_player = 1 if player == 2 else 2

        if curr in visited and not visited[curr]:
            return new_player

        for i in range(1, k + 1):
            if backtracking(win, curr + i, new_player) == player:
                visited[curr] = True
                return player
        
        visited[curr] = False
        return new_player
    
    return backtracking(n, 0, 1)

def test():
    cases = [
        (1, 1, 1),
        (3, 3, 1),
        (4, 3, 2),
        (5, 3, 1),
        (7, 2, 1),
        (6, 2, 2),
        (2, 1, 2),
        (3, 1, 1),
        (2, 5, 1),
    ]

    for n, k, expected in cases:
        print(f"Testing n={n}, k={k}")
        actual = game_winner(n, k)
        assert actual == expected, f"Expected {expected}, got {actual}"

    print("All tests passed!")

def test2():
    cases = [
        (7, 2, 1),
    ]

    for n, k, expected in cases:
        print(f"Testing n={n}, k={k}")
        actual = game_winner(n, k)
        assert actual == expected, f"Expected {expected}, got {actual}"

    print("All tests passed!")    

test()