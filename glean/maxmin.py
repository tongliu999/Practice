def max_min_piece(nums: list[int], k: int) -> int:
    required = k + 1

    def can_split(target):
        pieces = 0
        current = 0

        for num in nums:
            current += num

            if current >= target:
                pieces += 1
                current = 0

        return pieces >= required

    low = min(nums)
    high = sum(nums) // required

    while low < high:
        mid = (low + high + 1) // 2

        if can_split(mid):
            low = mid
        else:
            high = mid - 1

    return low