from collections import defaultdict

connections = defaultdict(set)

with open("input", "rt") as input_file:
    for line in input_file.readlines():
        line = line.strip()
        if len(line) == 0:
            continue
        a, b = line.split("-")
        connections[a].add(b)
        connections[b].add(a)


cliques_with_t = set()
for first_node, to_nodes in connections.items():
    if first_node.startswith("t"):
        for second_node in to_nodes:
            for third_node in connections[second_node]:
                if third_node in to_nodes:
                    cliques_with_t.add(frozenset({first_node, second_node, third_node}))

print(len(cliques_with_t))


cliques_map: dict[str, set[str]] = {a: set() for a in connections}

with open("input", "rt") as input_file:
    for line in input_file.readlines():
        line = line.strip()
        if len(line) == 0:
            continue
        a, b = line.split("-")

        # attempt to put b into clique of a
        a_clique = cliques_map[a]
        if all(c in connections[b] for c in a_clique):
            a_clique.add(b)
            cliques_map[b] = a_clique

biggest_clique_representative = max(cliques_map, key=lambda a: len(cliques_map[a]))
print(",".join(a for a in sorted(cliques_map[biggest_clique_representative])))