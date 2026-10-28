import math

def max_min_piece(nums: list[int], k: int) -> int:
    if k == 0:
        return sum(nums)

    # part 1: see if we can make pieces of x length
    def check(num):
        pieces = 0
        curr = 0
        for i in nums:
            curr += i

            if curr >= num:
                pieces += 1
                curr = 0
        return pieces >= k + 1

    # part 2: find x length using binary search
    l = 0
    r = math.ceil(sum(nums) / k + 1)

    while l < r:
        midpoint = (l + r) // 2
        if check(midpoint):
            l = midpoint + 1
        else:
            r = midpoint

    return r - 1

def test_max_min_piece():
    cases = [
        ([5], 0, 5),
        ([3, 3, 3], 0, 9),
        ([4, 1, 1, 1, 4], 4, 1),
        ([5, 1, 4, 2, 8, 3], 2, 6),
        ([1, 1, 1, 10], 1, 3),
        ([10, 1, 1, 1], 1, 3),
        ([1, 100, 1], 1, 1),
        ([8, 1, 1, 8], 1, 9),
        ([5, 5, 5, 5, 5], 1, 10),
        ([2, 2, 2, 2, 2], 2, 2),
        ([1, 2, 3, 4, 5], 1, 6),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9], 5, 6),
        ([100000, 100000, 100000, 100000], 1, 200000),
    ]

    for i, (nums, k, expected) in enumerate(cases, 1):
        actual = max_min_piece(nums, k)
        assert actual == expected, (
            f"Test {i}, nums={nums}, k={k}: "
            f"expected {expected}, got {actual}"
        )

    print("All tests passed!")

test_max_min_piece()