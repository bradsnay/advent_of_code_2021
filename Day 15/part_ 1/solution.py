"""
--- Day 15: Chiton ---
https://adventofcode.com/2021/day/15
"""
from typing import List, Tuple, Dict
from queue import PriorityQueue


def print_grid(grid: List[List[int]]):
    for x in range(len(grid)):
        print_str = ""
        for y in range(len(grid[x])):
            print_str += str(grid[x][y])
        print(print_str)


def create_priority_queue_and_weight_map(
    grid: List[List[int]],
) -> Tuple[PriorityQueue, Dict[Tuple[int, int], int]]:
    queue = PriorityQueue()
    known_weights = {}
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if x == 0 and y == 0:
                known_weights[(x, y)] = 0
                queue.put((0, (x, y)))
            else:
                known_weights[(x, y)] = 9223372036854775807
                queue.put((9223372036854775807, (x, y)))

    return queue, known_weights


def fetch_neighbor_indices(
    x: int, y: int, max_x: int, max_y: int
) -> List[Tuple[int, int]]:
    neighboring_indices = []
    if x - 1 > 0:
        neighboring_indices.append((x - 1, y))
    if x + 1 < max_x:
        neighboring_indices.append((x + 1, y))
    if y - 1 > 0:
        neighboring_indices.append((x, y - 1))
    if y + 1 < max_y:
        neighboring_indices.append((x, y + 1))
    return neighboring_indices


def find_shortest_path(
    pqueue: PriorityQueue,
    known_weights: Dict[Tuple[int, int], int],
    grid: List[List[int]],
    starting_point: Tuple[int, int],
    ending_point: Tuple[int, int],
):
    """
    Dijkstra's algorithm w/ priority queue
    """
    while not pqueue.empty():
        weight, u = pqueue.get()
        ux, uy = u
        neighbor_indices = fetch_neighbor_indices(
            ux, uy, ending_point[0], ending_point[1]
        )
        for v in neighbor_indices:
            vx, vy = v
            neighbor_weight = weight + grid[vx][vy]
            if neighbor_weight < known_weights[(vx, vy)]:
                known_weights[v] = neighbor_weight
                pqueue.put((neighbor_weight, v))
    return known_weights[ending_point[0] - 1, ending_point[1] - 1]


grid = []
with open("input.txt", "r") as file:
    for line in file:
        grid.append([int(val) for val in line.strip()])

starting_point = (0, 0)
ending_point = (len(grid[0]), len(grid))
queue, known_weights = create_priority_queue_and_weight_map(grid)
print(find_shortest_path(queue, known_weights, grid, starting_point, ending_point))
