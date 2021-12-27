from collections import defaultdict
import heapq

"""
#0123456789a#
#hhhhhhhhhhh#
##1A#.#.#.###
  2A#.#.#.#
  #########

let's denote hallway places h0 to ha
and rooms A1, A2, B1, B2, C1, C2, D1, D2
"""

graphText = """
A2 -- A1
C2 -- C1
D2 -- D1
B2 -- B1
H0 -- H1
H1 -- H2
H2 -- H3
H3 -- H4
H4 -- H5
H5 -- H6
H6 -- H7
H7 -- H8
H8 -- H9
H9 -- HA
A1 -- H2
B1 -- H4
C1 -- H6
D1 -- H8
"""

def parse(text):
    edges = [
        tuple(map(lambda x: x.strip(),l.split("--")))
        for l in text.strip().split("\n")
    ]
    return edges

def build_graph(edges):
    graph = defaultdict(lambda: {})
    for v1, v2 in edges:
        graph[v1][v2] = 1
        graph[v2][v1] = 1
    return graph


def dijkstra(graph, st):
    distances = {v: float('inf') for v in graph}
    distances[st] = 0
    parents = {st: st}
    pq = [(0, st)]
    while len(pq) > 0:
        d, current = heapq.heappop(pq)
        if d > distances[current]:
            continue
        for neighbor, weight in graph[current].items():
            distance = d + weight
            if distance < distances[neighbor]:
                parents[neighbor] = current
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances, parents

def find_path(parents, start, target):
    path = []
    current = target
    while current != start:
        path.append(current)
        current = parents[current]
    path.append(start)
    return path


def compute_paths():
    edges = parse(graphText)
    graph = build_graph(edges)

    paths = {}
    for v1 in graph.keys():
        dijk_dist, parents = dijkstra(graph, v1)
        for v2, distance in dijk_dist.items():
            path = find_path(parents, v1, v2)
            paths[(v1, v2)] = list(reversed(path))
    return paths
