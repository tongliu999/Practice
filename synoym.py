from collections import defaultdict

def synonym_groups(sentences: list[str]) -> list[list[str]]:
    dictionary = defaultdict(list)
    res = []
    visited = set()

    if len(sentences) == 0:
        return []
    
    #part 1, isolate words into dictionary to determine synoyms
    for sentence in sentences:
        arr = sentence.split(" ")
        for i in range(2, len(arr) - 2):
            dictionary[(arr[i - 2], arr[i - 1], arr[i + 1], arr[i + 2])].append(arr[i])

    adj_list = defaultdict(list)


    #part 2, sort the words into final response
    for key in dictionary.keys():
        for word in dictionary[key]:
            for add in dictionary[key]:
                if add != word:
                    adj_list[word].append(add)

    def dfs(word):
        if not adj_list[word] or word in visited:
            return []

        visited.add(word)
        curr = []

        for word in adj_list[word]:
            curr.append(word)
            curr.extend(dfs(word))
        
        return curr
            
    for key in adj_list:
        if key in visited:
            continue

        component = dfs(key)
        res.append(sorted(list(set(component))))
                

    return sorted(res)

    
def test():
    cases = [
        (
            ["the cat sat"],
            [],
        ),
        (
            ["a b red c d"],
            [],
        ),
        (
            ["a b red c d", "a b red c d"],
            [],
        ),
        (
            ["a b red c d", "a b blue c d"],
            [["blue", "red"]],
        ),
        (
            [
                "i really like the movie",
                "i really love the movie",
                "we all love this place",
                "we all enjoy this place",
            ],
            [["enjoy", "like", "love"]],
        ),
        (
            [
                "a b red c d",
                "a b blue c d",
                "e f small g h",
                "e f big g h",
            ],
            [["big", "small"], ["blue", "red"]],
        ),
        (
            [
                "a b red c d",
                "a b blue c e",
                "x b green c d",
            ],
            [],
        ),
        (
            [
                "a b red c d e f",
                "a b blue c d e f",
            ],
            [["blue", "red"]],
        ),
        (
            [
                "a b alpha c d",
                "a b beta c d",
                "e f gamma g h",
                "e f delta g h",
                "i j beta k l",
                "i j gamma k l",
            ],
            [["alpha", "beta", "delta", "gamma"]],
        ),
    ]

    for i, (sentences, expected) in enumerate(cases, 1):
        actual = synonym_groups(sentences)
        assert actual == expected, (
            f"Test {i}: expected {expected}, got {actual}"
        )

    print("All tests passed!")

test()