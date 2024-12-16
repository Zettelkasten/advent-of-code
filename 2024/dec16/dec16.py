import networkx as nx

map = {}
height = 0
length = 0

movements = []

with open("input", "rt") as input_file:
    read_movements = False
    for line in input_file.readlines():
        line = line.strip()
        if line == "":
            assert not read_movements
            read_movements = True
        else:
            if read_movements:
                movements.extend(list(line))
            else:
                # read map
                if length == 0:
                    length = len(line)
                else:
                    assert length == len(line)
                row = height
                for col, c in enumerate(line):
                    map[(col, row)] = c
                height += 1

import networkx
graph = nx.Graph()

orientations = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}

graph.add_nodes_from(
    [(x, y, orientation) for (x, y), val in map.items() if val in ".SE" for orientation in orientations.keys()])
graph.add_weighted_edges_from(
    [
        ((x, y, o), (x + dir_x, y + dir_y, o), 1)
        for (x, y) in map.keys()
        for o, (dir_x, dir_y) in orientations.items()
        if map[(x, y)] in ".SE" and map[(x + dir_x, y + dir_y)] in ".SE"]
)
o_list = list(orientations.keys())
graph.add_weighted_edges_from(
    [
        ((x, y, o), (x, y, o_list[(i + 1) % len(o_list)]), 1000)
        for (x, y) in map.keys()
        for i, o in enumerate(o_list)
        if map[(x, y)] in ".SE"]
)

# find start and end
start_pos = [(x, y) for (x, y), val in map.items() if val == "S"]
assert len(start_pos) == 1
start_x, start_y = start_pos[0]
del start_pos
start_orientation = ">"

end_pos = [(x, y) for (x, y), val in map.items() if val == "E"]
assert len(end_pos) == 1
end_x, end_y = end_pos[0]
del end_pos

shortest_lengths_by_orientation = {}
for o in orientations.keys():
    shortest_path_length = nx.shortest_path_length(graph, (start_x, start_y, start_orientation), target=(end_x, end_y, o), weight="weight")
    shortest_lengths_by_orientation[o] = shortest_path_length

best_orientation = [o for o, length in shortest_lengths_by_orientation.items() if length == min(shortest_lengths_by_orientation.values())]
assert len(best_orientation) == 1
best_orientation = best_orientation[0]

print(shortest_lengths_by_orientation[best_orientation])

good_viewing_points = set()
for path in nx.all_shortest_paths(graph, (start_x, start_y, start_orientation), target=(end_x, end_y, best_orientation), weight="weight"):
    for x, y, o in path:
        good_viewing_points.add((x, y))

print(len(good_viewing_points))