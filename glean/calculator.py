def evaluate(expression: str) -> int:
    if not expression:
        return -1
    
    arr = []
    current = 0

    for char in expression:
        if char.isdigit():
            current = current * 10 + int(char)
        elif char == " ":
            continue
        else:
            arr.append(str(current))
            current = 0
            arr.append(char)
    
    arr.append(str(current))

    opstack = []
    numstack = []

    for char in arr:
        if char.isnumeric():
            num1 = int(char)
            if opstack and opstack[-1] == "/":
                opstack.pop()
                num2 = numstack.pop()
                numstack.append(num2 // num1)
            elif opstack and opstack[-1] == "*":
                opstack.pop()
                num2 = numstack.pop()
                numstack.append(num1 * num2)
            else:
                numstack.append(num1)
        else:
            opstack.append(char)


    res = numstack[0]
    i = 1
    print(numstack, opstack)
    for operation in opstack:
        if operation == "+":
            res += numstack[i]
        elif operation == "-":
            res -= numstack[i]
        else:
            continue
        i += 1

    return int(res)

def test():
    cases = [
        ("42", 42),
        ("0", 0),
        ("  12  ", 12),
        ("3 + 2", 5),
        ("3 + 2 * 2", 7),
        (" 3 + 2 * 2 ", 7),
        ("10 - 3", 7),
        ("2 - 3 - 4", -5),
        ("1 - 2 + 3", 2),
        ("6 / 3", 2),
        ("3 / 2", 1),
        ("8 / 3 * 3 + 1", 7),
        ("100 / 10 / 2", 5),
        ("14 - 3 * 4 / 5", 12),
        ("1 - 7 / 2", -2),
        ("2 * 3 * 4", 24),
        ("0 * 8 + 3", 3),
        ("12 + 34 * 2 - 8 / 3", 78),
    ]

    for i, (expression, expected) in enumerate(cases, 1):
        actual = evaluate(expression)
        assert type(actual) is int, (
            f"Test {i}: expected int, got {type(actual).__name__}"
        )
        assert actual == expected, (
            f"Test {i}, {expression!r}: "
            f"expected {expected}, got {actual}"
        )

    print("All tests passed!")

test()      
