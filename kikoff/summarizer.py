from collections import defaultdict
def summarize_requests(lines: list[str]) -> dict[str, dict]:
    request_count = defaultdict(int)
    request_duration = defaultdict(int)
    request_errors = defaultdict(int)   

    def is_error(status):
        if status >= 500 and status <= 599:
            return True
        
        return False

    for request in lines:
        curr = request.strip().split()

        if len(curr) < 4 or len(curr) > 4:
            continue

        request_id = curr[0]
        name = curr[1]
        try:
            status = int(curr[2])
            duration = int(curr[3])
        except ValueError:
            continue

        if status < 100 or status > 599:
            continue

        if duration < 0:
            continue

        request_count[name] += 1
        request_duration[name] += duration
        request_errors[name] += 1 if is_error(status) else 0
    
    res = {}

    for key in request_count.keys():
        curr = {}
        curr["count"] = request_count[key]
        curr["errors"] = request_errors[key]
        curr["avg_duration_ms"] = round(request_duration[key] / request_count[key], 2)

        res[key] = curr
    
    return res

def test_summarize_requests():
    cases = [
        ([], {}),
        (
            [
                "",
                "garbage",
                "r1 /a 200",
                "r1 /a 200 10 extra",
                "r1 /a nope 10",
                "r1 /a 200 nope",
                "r1 /a 99 10",
                "r1 /a 600 10",
                "r1 /a 200 -1",
                "r1 /a 200 1.5",
            ],
            {},
        ),
        (
            [
                "r1 /login 200 40",
                "r2 /login 500 60",
                "r3 /checkout 201 90",
                "malformed",
            ],
            {
                "/login": {
                    "count": 2,
                    "errors": 1,
                    "avg_duration_ms": 50.0,
                },
                "/checkout": {
                    "count": 1,
                    "errors": 0,
                    "avg_duration_ms": 90.0,
                },
            },
        ),
        (
            ["  r1\t/a   200  5 \n"],
            {"/a": {"count": 1, "errors": 0, "avg_duration_ms": 5.0}},
        ),
        (
            ["r1 /a 200 10", "r1 /a 503 20"],
            {"/a": {"count": 2, "errors": 1, "avg_duration_ms": 15.0}},
        ),
        (
            [
                "r1 /a 100 0",
                "r2 /a 499 10",
                "r3 /a 500 20",
                "r4 /a 599 30",
            ],
            {"/a": {"count": 4, "errors": 2, "avg_duration_ms": 15.0}},
        ),
        (
            ["r1 /a 200 1", "r2 /a 200 0", "r3 /a 200 0"],
            {"/a": {"count": 3, "errors": 0, "avg_duration_ms": 0.33}},
        ),
    ]

    for i, (lines, expected) in enumerate(cases, 1):
        actual = summarize_requests(lines)
        assert actual == expected, (
            f"Test {i}:\nexpected {expected!r}\ngot      {actual!r}"
        )

    print("All tests passed!")

test_summarize_requests()