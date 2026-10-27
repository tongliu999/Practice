from collections import deque

def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    if not board or not board[0] or not words:
        return []

    # Build the trie.
    root = {}
    for word in words:
        node = root
        for char in word:
            node = node.setdefault(char, {})
        node["#"] = word

    found = set()
    visited = set()
    rows, cols = len(board), len(board[0])
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def dfs(row, col, node):
        if (
            row < 0 or col < 0
            or row >= rows or col >= cols
            or (row, col) in visited
        ):
            return

        char = board[row][col]
        if char not in node:
            return

        child = node[char]

        if "#" in child:
            found.add(child.pop("#"))

        visited.add((row, col))

        for dr, dc in directions:
            dfs(row + dr, col + dc, child)

        visited.remove((row, col))

        if not child:
            del node[char]

    for row in range(rows):
        for col in range(cols):
            dfs(row, col, root)

    return sorted(found)

def test_find_words():
    sample = [
        ["a", "b", "c", "e"],
        ["s", "f", "c", "s"],
        ["a", "d", "e", "e"],
    ]

    cases = [
        ([], ["a"], []),
        ([[]], ["a"], []),
        (sample, [], []),
        ([["a"]], ["a", "b", "aa"], ["a"]),
        ([["a"]], ["a", "a"], ["a"]),
        (
            sample,
            ["see", "abcced", "abcb", "see"],
            ["abcced", "see"],
        ),
        (
            [["c", "a", "t"]],
            ["car", "cat", "ca", "c", "cat"],
            ["c", "ca", "cat"],
        ),
        (
            [["a", "b", "c"]],
            ["cba", "abc", "ac", "aba"],
            ["abc", "cba"],
        ),
        (
            [["a", "b"], ["c", "d"]],
            ["abdc", "acdb", "abcd", "ad", "aba"],
            ["abdc", "acdb"],
        ),
        (
            [["a", "a"], ["a", "a"]],
            ["aaaaa", "aaa", "a", "aaaa", "aa", "aaa"],
            ["a", "aa", "aaa", "aaaa"],
        ),
        (
            [
                ["c", "a", "a"],
                ["a", "a", "a"],
                ["b", "c", "d"],
            ],
            ["aab", "xyz"],
            ["aab"],
        ),
    ]

    for i, (board, words, expected) in enumerate(cases, 1):
        original = [row[:] for row in board]
        actual = find_words(board, words)

        assert actual == expected, (
            f"Test {i}: expected {expected}, got {actual}"
        )
        assert board == original, f"Test {i}: board was modified"

    print("All tests passed!")

test_find_words()