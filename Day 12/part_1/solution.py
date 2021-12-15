"""
--- Day 12: Passage Pathing ---
https://adventofcode.com/2021/day/12
"""
from collections import defaultdict
from typing import Dict, List, Set


def is_small_cave(node: str) -> bool:
    return node.islower()


def find_all_paths(
    graph: Dict[str, Set[str]],
    start_node: str,
    end_node: str,
    path: list,
) -> List[List[str]]:
    # We can only visit a small cave once.
    if is_small_cave(start_node) and start_node in path:
        return []
    # We've reached the end. Return the path with the end node tacked on.
    if start_node == end_node:
        return [path + [end_node]]
    # This is the end of the given path and it's not our specified end node so it's invalid
    if start_node not in graph:
        return []

    paths = []
    for node in graph[start_node]:
        # Find all remaining paths starting at a child node of start_node.
        new_paths = find_all_paths(graph, node, end_node, path + [start_node])
        paths.extend(new_paths)
    return paths


graph = defaultdict(set)
with open("input.txt", "r") as file:
    for line in file:
        parsed_line = line.strip().split("-")
        start_node = parsed_line[0]
        end_node = parsed_line[1]
        graph[start_node].add(end_node)
        # Create reverse entry
        graph[end_node].add(start_node)

result = find_all_paths(graph, "start", "end", [])
print(len(result))
