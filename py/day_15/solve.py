import numpy as np
import itertools
from collections import deque, defaultdict
import heapq

def parse_input(filename):
  with open(filename) as file:
    lines = file.readlines()
    return np.matrix([[int(c) for c in line.strip()] for line in lines])

def neighbours(i, j, max_size):
    raw_neighbours = [
        (1, 0), (0, 1), (-1, 0), (0, -1)
    ]
    return [
        (i + ii, j + jj) for ii, jj in raw_neighbours
        if 0 <= i + ii < max_size and 0 <= j + jj < max_size
    ]

def to_graph_dict(matrix):
    graph = defaultdict(lambda: dict())
    n, _ = matrix.shape
    for i in range(n):
        for j in range(n):
            for ii, jj in neighbours(i,j, n):
                graph[(i, j)][(ii, jj)] = matrix[ii, jj]
    return graph


def dijkstra(graph, st):
    distances = {v: float('inf') for v in graph}
    distances[st] = 0

    pq = [(0, st)]
    while len(pq) > 0:
        d, current = heapq.heappop(pq)
        if d > distances[current]:
            continue
        for neighbor, weight in graph[current].items():
            distance = d + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances

def truncate_nine(n):
    if n <= 8:
        return n + 1
    else:
        return truncate_nine(n-9)

def gen_real_map(mat):
    n, _ = mat.shape
    new_mat = np.zeros((n*5, n*5))
    for i in range(5):
        for j in range(5):
            sub_mat = np.vectorize(truncate_nine)((i+j) + mat - 1)
            new_mat[n*i:n*i+n, n*j:n*j+n] = sub_mat
    return new_mat

def main_p1():
  cave_map = parse_input("ex.txt")
  graph = to_graph_dict(cave_map)
  # print(graph)
  dist = dijkstra(graph, (0,0))
  n, _ = cave_map.shape
  print(dist[n-1,n-1])
  new_map = gen_real_map(cave_map)
  graph = to_graph_dict(new_map)
  dist = dijkstra(graph, (0,0))
  n, _ = new_map.shape
  print(dist[n-1,n-1])


if __name__ == '__main__':
  main_p1()


