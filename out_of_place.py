def fix_almost_sorted(nums: list[int]) -> list[int]:
    fix = None

    for i in range(1, len(nums)):
        if nums[i] < nums[i - 1]:
            if i == len(nums) - 1:
                fix = i
                break

            num1 = nums[i - 1]
            num2 = nums[i]
            if num1 > nums[i + 1]:
                fix = i - 1
            else:
                fix = i
            break

    if fix is None:
        return nums
    
    insert = nums.pop(fix)
    
    midpoint = len(nums) // 2
    l = 0
    r = len(nums)
    while l < r:
        if insert >= nums[midpoint]:
            l = midpoint + 1
        else:
            r = midpoint
        
        midpoint = (l + r) // 2

    nums.append(0)
    prev = insert
    for i in range(l, len(nums)):
        temp = nums[i]
        nums[i] = prev
        prev = temp

    return nums

def test():
    cases = [
        ([1], [1]),
        ([1, 2, 3], [1, 2, 3]),
        ([2, 1], [1, 2]),
        ([1, 2, 9, 3, 4, 5], [1, 2, 3, 4, 5, 9]),
        ([1, 3, 4, 2, 5], [1, 2, 3, 4, 5]),
        ([5, 1, 2, 3, 4], [1, 2, 3, 4, 5]),
        ([2, 3, 4, 5, 1], [1, 2, 3, 4, 5]),
        ([1, 4, 2, 3, 5], [1, 2, 3, 4, 5]),
        ([1, 1, 2], [1, 1, 2]),
        ([2, 2, 2], [2, 2, 2]),
        ([2, 1, 2, 2], [1, 2, 2, 2]),
        ([2, 3, 1, 3], [1, 2, 3, 3]),
        ([1, 3, 2, 2, 4], [1, 2, 2, 3, 4]),
        ([-3, 0, -2, -1, 1], [-3, -2, -1, 0, 1]),
    ]

    for i, (nums, expected) in enumerate(cases, 1):
        original = nums[:]
        actual = fix_almost_sorted(nums)
        assert actual == expected, (
            f"Test {i}, input {original}: "
            f"expected {expected}, got {actual}"
        )

    print("All tests passed!")

test()

            