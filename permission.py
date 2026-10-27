from collections import defaultdict
def access_roots(nodes: list[dict], user_id: str) -> list[tuple[str, str]]:
    roots = []
    adj = defaultdict(list)
    permissions = defaultdict(list)
    for node in nodes:
        id, type, parent, user = node
        if not parent:
            roots.append(id)
            continue
        adj[parent].append(id)
        permissions[user].append(id)

