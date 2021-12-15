"""
--- Day 15: Chiton ---
--- Part 2 ---
https://adventofcode.com/2021/day/15
"""
from typing import List, Tuple, Dict, Union
from queue import PriorityQueue


def print_grid(grid: List[List[int]]):
    for x in range(len(grid)):
        print_str = ""
        for y in range(len(grid[x])):
            print_str += str(grid[x][y])
        print(print_str)


def create_priority_queue_and_weight_map(
    grid: Union[List[List[int]], Dict[int, Dict[int, int]]],
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


def find_shortest_path_weight(
    pqueue: PriorityQueue,
    known_weights: Dict[Tuple[int, int], int],
    grid: Union[List[List[int]], Dict[int, Dict[int, int]]],
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


def generate_sub_grid(grid: List[List[int]]) -> List[List[int]]:
    new_grid = []
    for x in range(len(grid)):
        row = []
        for y in range(len(grid[x])):
            new_val = grid[x][y] + 1
            if new_val > 9:
                new_val = 1
            row.append(new_val)
        new_grid.append(row)
    return new_grid


def generate_part_2_grid(grid: List[List[int]]) -> Dict[int, Dict[int, int]]:
    sub_grids = {(0, 0): grid}
    for x in range(5):
        for y in range(4):
            sub_grids[x, y + 1] = generate_sub_grid(sub_grids[x, y])
        if x != 4:
            sub_grids[x + 1, 0] = sub_grids[x, 1]
    full_grid = {}
    for coordinate, sub_grid in sub_grids.items():
        mx, my = coordinate
        for x in range(len(sub_grid)):
            new_x = mx * len(sub_grid) + x
            if new_x not in full_grid:
                full_grid[new_x] = {}
            for y in range(len(grid[x])):
                new_y = my * len(grid[x]) + y
                full_grid[new_x][new_y] = sub_grid[x][y]

    return full_grid


grid = []
with open("input.txt", "r") as file:
    for line in file:
        grid.append([int(val) for val in line.strip()])

print("Part 1")
ending_point = (len(grid[0]), len(grid))
queue, known_weights = create_priority_queue_and_weight_map(grid)
print(find_shortest_path_weight(queue, known_weights, grid, ending_point))

print("Part 2")
part_2_grid = generate_part_2_grid(grid)
ending_point = (len(part_2_grid[0]), len(part_2_grid))
queue, known_weights = create_priority_queue_and_weight_map(part_2_grid)
print(find_shortest_path_weight(queue, known_weights, part_2_grid, ending_point))
