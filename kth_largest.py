def kth_largest(a: list[int], b: list[int], k: int) -> int:
    # Search the shorter array.
    if len(a) > len(b):
        a, b = b, a

    m, n = len(a), len(b)
    low = max(0, k - n)
    high = min(k, m)

    while low <= high:
        x = (low + high) // 2
        y = k - x

        i = m - x
        j = n - y

        a_selected = a[i] if x > 0 else float("inf")
        b_selected = b[j] if y > 0 else float("inf")

        a_unselected = a[i - 1] if i > 0 else float("-inf")
        b_unselected = b[j - 1] if j > 0 else float("-inf")

        if (a_selected >= b_unselected
                and b_selected >= a_unselected):
            return min(a_selected, b_selected)

        if a_selected < b_unselected:
            high = x - 1
        else:
            low = x + 1

def test():
    cases = [
        ([1], [], 1, 1),
        ([], [5, 8], 1, 8),
        ([], [5, 8], 2, 5),
        ([1, 5, 11, 20], [3, 11, 14], 3, 11),
        ([1, 5, 11, 20], [3, 11, 14], 4, 11),
        ([1, 5, 11, 20], [3, 11, 14], 7, 1),
        ([2, 2, 2], [2], 4, 2),
        ([1, 2], [10, 20, 30], 3, 10),
        ([10, 20, 30], [1, 2], 4, 2),
        ([1, 3, 5], [2, 4, 6], 1, 6),
        ([1, 3, 5], [2, 4, 6], 6, 1),
        ([-10, -5, -1], [-8, -2], 3, -5),
        ([-3, 0, 4], [-2, 0, 5], 4, 0),
        ([0, 0], [0, 0], 2, 0),
    ]

    for i, (a, b, k, expected) in enumerate(cases, 1):
        original_a, original_b = a[:], b[:]
        actual = kth_largest(a, b, k)
        assert actual == expected, (
            f"Test {i}: expected {expected}, got {actual}"
        )
        assert a == original_a and b == original_b, (
            f"Test {i}: inputs were modified"
        )

    print("All tests passed!")

test()