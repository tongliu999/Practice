from collections import defaultdict

def exclusive_time(n: int, logs: list[str]) -> list[int]:
    res = [0] * n
    boundary = -1
    stack = []

    for i in range(len(logs)):
        curr = logs[i].split(":")
        id = int(curr[0])
        state = curr[1]
        end = int(curr[2])
        prevId = 0

        if boundary == -1:
            boundary = end

        if state == "start":
            if stack:
                prevId = stack[-1]
            
            res[prevId] += end - boundary
            boundary = end
            stack.append(id)
        else:
            stack.pop()
            res[id] += end - boundary + 1
            boundary = end + 1
        
        print(res)
    
    return res
            


        




def test():
    cases = [
        (1, ["0:start:0", "0:end:0"], [1]),
        (2, [
            "0:start:0", "1:start:2",
            "1:end:5", "0:end:6"
        ], [3, 4]),
        (1, [
            "0:start:0", "0:start:2",
            "0:end:3", "0:end:5"
        ], [6]),
        (3, [
            "2:start:0", "2:end:1",
            "0:start:2", "0:end:3",
            "1:start:4", "1:end:6"
        ], [2, 3, 2]),
        (3, ["1:start:5", "1:end:5"], [0, 1, 0]),
    ]

    for index, (n, logs, expected) in enumerate(cases, 1):
        actual = exclusive_time(n, logs)
        print(f"Test {index}: expected {expected}, got {actual}")
        assert actual == expected

    print("All tests passed!")

test()