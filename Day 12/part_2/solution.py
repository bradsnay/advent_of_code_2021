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
    node_being_explored_twice=None,
) -> List[List[str]]:
    # We've reached the end. Return the path with the end node tacked on.
    if start_node == end_node:
        return [path + [end_node]]
    # Only visit start node once.
    if start_node == "start" and start_node in path:
        return []
    # Don't traverse a sub-path where the start node is the one we've already visited twice.
    if start_node == node_being_explored_twice:
        return []
    # This is the end of the given path and it's not our specified end node so it's invalid
    if start_node not in graph:
        return []
    # We've identified a start node that we've seen before.
    if is_small_cave(start_node) and start_node in path:
        # If we haven't already considered a cave to visit again. Make it this one.
        if node_being_explored_twice is None:
            node_being_explored_twice = start_node
        # Otherwise this is an invalid path because we can only visit one small cave twice.
        else:
            return []
    paths = []
    for node in graph[start_node]:
        # Find all remaining paths starting at a child node of start_node.
        new_paths = find_all_paths(
            graph, node, end_node, path + [start_node], node_being_explored_twice
        )
        paths.extend(new_paths)
    return paths


graph = defaultdict(set)
with open("input.txt", "r") as file:
    for line in file:
        parsed_line = line.strip().split("-")
        start_node = parsed_line[0]
        end_node = parsed_line[1]
        graph[start_node].add(end_node)
        graph[end_node].add(start_node)

result = find_all_paths(graph, "start", "end", [])
print(len(result))
