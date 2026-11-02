from datetime import datetime
from collections import defaultdict

def is_valid_date(date_string):
    if len(date_string) != 19:
        return False

    try:
        datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
        return True
    except ValueError:
        return False

def parse_logs(lines: list[str]) -> list[dict]:
    res = []
    valid = set(["INFO", "WARN", "ERROR", "DEBUG"])

    for log in lines:
        curr = log.strip().split(maxsplit=3)

        if len(curr) < 4:
            continue
            
        time = curr[0]
        level = curr[1]
        service = curr[2]
        message = curr[3]
        user_id = None

        if level not in valid or not is_valid_date(time):
            continue

        for word in message.split():
            if word.startswith("user_id="):
                id = word.split("=", maxsplit=1)
                if id[1].isnumeric():
                    user_id = id[1]
                    break
        
        entry = {"timestamp": time, "level": level, "service": service, "message": message, "user_id": user_id}

        res.append(entry)
    
    return res
            
        

def search_logs(logs: list[dict], query: str) -> dict:
    tokens = query.split()
    filters = {}
    supported = {"level", "service", "userid", "start", "end"}
    i = 0

    # Parse filters at the beginning.
    while i < len(tokens):
        key, separator, value = tokens[i].partition(":")
        if not separator or key not in supported:
            break

        filters[key] = value
        i += 1

    contains = " ".join(tokens[i:])
    res = []

    for log in logs:
        if "level" in filters:
            if log["level"] != filters["level"].upper():
                continue

        if "service" in filters:
            if log["service"] != filters["service"]:
                continue

        if "userid" in filters:
            if log["user_id"] != filters["userid"]:
                continue

        if "start" in filters:
            start = filters["start"] + "T00:00:00"
            if log["timestamp"] < start:
                continue

        if "end" in filters:
            end = filters["end"] + "T00:00:00"
            if log["timestamp"] >= end:
                continue

        if contains not in log["message"]:
            continue

        res.append(log)

    return {"count": len(res), "logs": res}


def test_parse_logs():
    timestamp = "2026-01-15T10:30:00"

    def expected(level, service, message, user_id=None):
        return {
            "timestamp": timestamp,
            "level": level,
            "service": service,
            "message": message,
            "user_id": user_id,
        }

    cases = [
        ([], []),
        (
            [f"{timestamp} INFO auth Login user_id=123"],
            [expected("INFO", "auth", "Login user_id=123", "123")],
        ),
        (
            [f"{timestamp} ERROR payment Request timed out"],
            [expected("ERROR", "payment", "Request timed out")],
        ),
        (
            [
                f"{timestamp} INFO auth First",
                "malformed",
                f"{timestamp} WARN api Second",
            ],
            [
                expected("INFO", "auth", "First"),
                expected("WARN", "api", "Second"),
            ],
        ),
        (
            [f"{timestamp} DEBUG api user_id=12 user_id=34"],
            [expected("DEBUG", "api", "user_id=12 user_id=34", "12")],
        ),
        (
            [f"{timestamp} INFO auth user_id=abc user_id=007"],
            [expected("INFO", "auth", "user_id=abc user_id=007", "007")],
        ),
        (
            [f"{timestamp} INFO auth user_id=123=abc"],
            [expected("INFO", "auth", "user_id=123=abc")],
        ),
        (
            [f"{timestamp} INFO auth prefix_user_id=123"],
            [expected("INFO", "auth", "prefix_user_id=123")],
        ),
        (
            [f"  {timestamp}   INFO  auth  hello  world \n"],
            [expected("INFO", "auth", "hello  world")],
        ),
        (
            [f"{timestamp}\tINFO\tauth\tLogin\tuser_id=42"],
            [expected("INFO", "auth", "Login\tuser_id=42", "42")],
        ),
        (
            [
                "",
                "   ",
                f"{timestamp} INFO",
                f"{timestamp} INFO auth",
                f"{timestamp} TRACE auth Hello",
                "2026-02-30T10:30:00 INFO auth Hello",
                "2026-01-15T25:30:00 INFO auth Hello",
                "2026-01-15 INFO auth Hello",
            ],
            [],
        ),
    ]

    for i, (lines, wanted) in enumerate(cases, 1):
        actual = parse_logs(lines)
        assert actual == wanted, (
            f"Test {i}:\nexpected {wanted!r}\ngot      {actual!r}"
        )

    print("All tests passed!")

test_parse_logs()

