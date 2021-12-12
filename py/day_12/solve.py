from collections import defaultdict, Counter

def parse_input(filename):
    with open(filename) as file:
        edges = [ l.strip().split("-") for l in file.readlines() ]

    graph = defaultdict(lambda: [])
    for s, d in edges:
        graph[s].append(d)
        graph[d].append(s)

    return graph

def can_revisit_big_caves(new_node, current_path):
    return new_node.isupper() or new_node not in current_path

def two_most_common_counts(ncp):
    counter = Counter([node for node in ncp if node.islower()])
    return tuple([ count for element, count in counter.most_common(2) ])

def can_revisit_big_caves_and_one_small(new_node, current_path):
    ncp = list(current_path)
    ncp.append(new_node)
    return new_node.isupper() or (
        new_node != "start" and
        two_most_common_counts(ncp) in { (2, 1), (1, 1) }
    )

def traverse(graph, revisit_check):
    start_node = "start"
    paths = [[start_node]]
    already_explored = set()
    full_paths = set()
    while paths:
        current_path = paths.pop()
        if tuple(current_path) not in already_explored:
            already_explored.add(tuple(current_path))
            current_node = current_path[-1]
            for child in graph[current_node]:
                if revisit_check(child, current_path):
                    new_path = list(current_path)
                    new_path.append(child)
                    paths.append(new_path)
                    if child == "end":
                        full_paths.add(tuple(new_path))
                        already_explored.add(tuple(new_path))
    return full_paths

def main():
    graph = parse_input("input.txt")
    paths = traverse(graph, can_revisit_big_caves)
    print(len(paths), "paths found if you can only visit big caves multiple times")
    paths = traverse(graph, can_revisit_big_caves_and_one_small)
    print(len(paths), "paths found if you can also re-visit one small cave once")

if __name__ == '__main__':
    main()

