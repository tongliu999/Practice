def balance_parentheses(s: str) -> str:
    if not s:
        return ""
    
    stack = []
    removed = set()
    res = ""

    for i in range(len(s)):
        if s[i] == "(":
            stack.append(i)
        elif not stack:
            removed.add(i)
        else:
            stack.pop()
        
    for i in stack:
        removed.add(i)
    
    for i in range(len(s)):
        if i in removed:
            continue
            
        res += s[i]

    return res        

def test():
    # Each case gives the minimum number of deletions.
    cases = [
        ("", 0),
        ("(", 1),
        (")", 1),
        ("()", 0),
        (")(", 2),
        ("(())", 0),
        ("()())", 1),
        ("(()()", 1),
        ("))((", 4),
        ("(((", 3),
        (")))", 3),
        ("())(()", 2),
        ("(()())()", 0),
    ]

    for s, deletions in cases:
        actual = balance_parentheses(s)
        assert isinstance(actual, str)

        # Accept any balanced result.
        balance = 0
        for char in actual:
            assert char in "()"
            balance += 1 if char == "(" else -1
            assert balance >= 0, f"{s!r}: unbalanced result {actual!r}"
        assert balance == 0, f"{s!r}: unbalanced result {actual!r}"

        # Result must preserve the original character order.
        remaining = iter(s)
        assert all(char in remaining for char in actual), (
            f"{actual!r} is not a subsequence of {s!r}"
        )

        assert len(s) - len(actual) == deletions, (
            f"{s!r}: expected {deletions} deletions, got {actual!r}"
        )

    print("All tests passed!")

test()
