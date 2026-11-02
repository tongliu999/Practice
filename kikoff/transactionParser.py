def format_transactions(lines: list[str]) -> list[str]:
    res = []
    barrier = "---------------------------"
    curr = "---------------------------"

    for transaction in lines:
        components = [
            field.strip()
            for field in transaction.strip().split(",")
        ]

        if not components or len(components) < 4:
            continue

        place = components[0]
        price = f"{float(components[1]):.2f}"
        date = components[2]
        status = components[3]

        curr += "\n| " + place + " $" + price + " |\n| " + date + " " + status + " |\n" + barrier
        res.append(curr)
        curr = barrier
    
    return res

def test_format_transactions():
    def block(merchant, amount, date, status):
        return "\n".join([
            "-" * 27,
            f"| {merchant} ${amount} |",
            f"| {date} {status} |",
            "-" * 27,
        ])

    cases = [
        ([], []),
        (["", "   ", "\t"], []),
        (
            ["Coffee Shop,10.5,2026-01-15,pending"],
            [block("Coffee Shop", "10.50", "2026-01-15", "pending")],
        ),
        (
            [
                "Coffee Shop,10.5,2026-01-15,pending",
                "Bookstore,20,2026-01-16,completed",
            ],
            [
                block("Coffee Shop", "10.50", "2026-01-15", "pending"),
                block("Bookstore", "20.00", "2026-01-16", "completed"),
            ],
        ),
        (
            [" Coffee Shop , 10.50 , 2026-01-15 , pending "],
            [block("Coffee Shop", "10.50", "2026-01-15", "pending")],
        ),
        (
            ["", "Store,0,2026-01-01,completed", "   "],
            [block("Store", "0.00", "2026-01-01", "completed")],
        ),
        (
            ["Small Purchase,0.01,2026-02-01,pending"],
            [block("Small Purchase", "0.01", "2026-02-01", "pending")],
        ),
        (
            ["A  B,1000.2,2026-03-01,completed"],
            [block("A  B", "1000.20", "2026-03-01", "completed")],
        ),
    ]

    for i, (lines, expected) in enumerate(cases, 1):
        actual = format_transactions(lines)
        assert actual == expected, (
            f"Test {i}:\nexpected {expected!r}\ngot      {actual!r}"
        )

    print("All tests passed!")

test_format_transactions()
