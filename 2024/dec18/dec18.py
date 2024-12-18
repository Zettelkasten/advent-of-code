import networkx as nx
from networkx.exception import NetworkXNoPath

height = 71
width = 71

orientations = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}


def make_graph_from_free_tiles(free_tiles):
    graph = nx.Graph()

    graph.add_nodes_from(
        [(x, y) for x in range(width) for y in range(height) if (x, y) in free_tiles])
    graph.add_edges_from(
        [
            ((x, y), (x + dir_x, y + dir_y))
            for (x, y) in free_tiles
            for (dir_x, dir_y) in orientations.values()
            if (x + dir_x, y + dir_y) in free_tiles]
    )
    return graph


with open("input", "rt") as input_file:
    free_tiles = {(x, y) for x in range(width) for y in range(height)}
    graph = nx.grid_2d_graph(width, height)
    for row in input_file.readlines():
        x, y = row.strip().split(",")
        free_tiles.remove((int(x), int(y)))

        graph.remove_node((int(x), int(y)))

        try:
            print(nx.shortest_path_length(graph, (0, 0), target=(width - 1, height - 1), weight=None))
        except NetworkXNoPath:
            print(f"That's it, cannot reach the end after removing {x},{y}")
            break
