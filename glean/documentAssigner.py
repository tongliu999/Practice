import heapq

def assign_documents_top_k(
    m: int,
    arrival: list[int],
    duration: list[int],
    k: int,
):
    # part 1: keep track of worker use and overall use
    workers = [0] * m
    busy = [0] * m
    total = 0
    failed = 0

    # helper: find open worker 
    def open_worker(num, arrival, duration):
        nonlocal total
        for i in range(num, m):
            if busy[i] <= arrival:
                busy[i] = arrival + duration
                workers[i] += 1
                total += 1
                return True
        for j in range(0, num):
            if busy[j] <= arrival:
                busy[j] = arrival + duration
                workers[j] += 1
                total += 1
                return True
        
        return False

    # go through tasks
    for i in range(len(arrival)):
        start = arrival[i]
        length = duration[i]
        if not open_worker(i % m, start, length):
            failed += 1
    
    heap = []


    for i in range(len(workers)):
        heapq.heappush(heap, (workers[i], i))
        if len(heap) > k:
            heapq.heappop(heap)

    top = []
    top_total = 0
    while heap:
        curr = heapq.heappop(heap)
        top.append(curr[1])
        top_total += curr[0]

    if not arrival:
        percentage = 0.0
    else:
        percentage = round(top_total / len(arrival) * 100, 2)

    print(total, top_total)
    return [sorted(top), round(percentage, 2)]

def test_assign_documents_top_k():
    # Last field: expected counts for every worker.
    cases = [
        (3, [], [], 2, [0, 0, 0]),
        (3, [0], [5], 2, [1, 0, 0]),
        (1, [1, 2], [10, 5], 1, [1]),
        (1, [0, 1, 2], [10, 10, 10], 1, [1]),
        (1, [0, 1, 2], [1, 10, 1], 1, [2]),
        (2, [0, 1], [10, 10], 1, [1, 1]),
        (3, [1, 2, 3, 7], [5, 4, 3, 2], 1, [2, 1, 1]),
        (3, [1, 2, 3, 7], [5, 4, 3, 2], 2, [2, 1, 1]),
        (3, [1, 2, 3, 7], [5, 4, 3, 2], 3, [2, 1, 1]),
        (3, [0, 1, 2, 3], [100, 100, 1, 1], 2, [1, 1, 2]),
        (
            3, [1, 2, 3, 4, 5], [100, 1, 100, 1, 1],
            2, [1, 3, 1],
        ),
    ]

    for i, (m, arrival, duration, k, counts) in enumerate(cases, 1):
        top, percentage = assign_documents_top_k(
            m, arrival, duration, k
        )

        assert len(top) == k, f"Test {i}: wrong number of workers"
        assert len(set(top)) == k, f"Test {i}: duplicate workers"
        assert all(0 <= worker < m for worker in top), (
            f"Test {i}: invalid worker ID"
        )

        selected_count = sum(counts[worker] for worker in top)
        optimal_count = sum(sorted(counts, reverse=True)[:k])
        assert selected_count == optimal_count, (
            f"Test {i}: {top} is not a valid top-k selection"
        )

        expected = (
            round(selected_count / len(arrival) * 100, 2)
            if arrival else 0.0
        )
        assert percentage == expected, (
            f"Test {i}: expected {expected}%, got {percentage}%"
        )

    print("All tests passed!")

test_assign_documents_top_k()