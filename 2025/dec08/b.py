import numpy
from tqdm import tqdm
coords = numpy.asarray([line.split(",") for line in open("input")], dtype=numpy.float32)  # [B,3]

num_els = len(coords)

clusters = {i: frozenset({i}) for i in range(num_els)}

def dist(i, j):
    all_dists =[]
    for ii in clusters[i]:
        for jj in clusters[j]:
            this_dist = numpy.linalg.norm(coords[ii] - coords[jj])
            all_dists.append(this_dist)
    return min(all_dists)

all_lists = sorted([(i, j) for i in range(num_els) for j in range(num_els) if i < j], key=lambda x: dist(x[0], x[1]))

for closest_i, closest_j in all_lists:
    new_set = frozenset(clusters[closest_i] | clusters[closest_j])
    print("Connected", closest_i, closest_j, "aka", coords[closest_i], coords[closest_j], "which ")
    for el in new_set:
        clusters[el] = new_set
    if len(set(clusters.values())) == 1:
        print("WHAA", int(coords[closest_i][0]) * int(coords[closest_j][0]))
        break
