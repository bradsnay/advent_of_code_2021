"""
--- Part Two ---
Next, you need to find the largest basins so you know what areas are most important to avoid.

A basin is all locations that eventually flow downward to a single low point. Therefore, every low point has a basin, although some basins are very small. Locations of height 9 do not count as being in any basin, and all other locations will always be part of exactly one basin.

The size of a basin is the number of locations within the basin, including the low point. The example above has four basins.

The top-left basin, size 3:

2199943210
3987894921
9856789892
8767896789
9899965678
The top-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678
The middle basin, size 14:

2199943210
3987894921
9856789892
8767896789
9899965678
The bottom-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678
Find the three largest basins and multiply their sizes together. In the above example, this is 9 * 14 * 9 = 1134.

What do you get if you multiply together the sizes of the three largest basins?


"""
from typing import List
from heapq import heappush, heappop
from time import time


def find_basin_size(height_map: List[List[int]], x: int, y: int) -> int:
    if x < 0 or y < 0 or x == len(height_map) or y == len(height_map[x]):
        return 0
    value = height_map[x][y]
    if value == 9:
        return 0
    height_map[x][y] = 9
    x_basin = find_basin_size(height_map, x + 1, y) + find_basin_size(height_map, x - 1, y)
    y_basin = find_basin_size(height_map, x, y + 1) + find_basin_size(height_map, x, y - 1)
    return 1 + x_basin + y_basin


with open('input.txt', 'r') as file:
    height_map = []
    for line in file:
        height_map.append([int(height) for height in line.strip()])


start_time = time()
basin_sizes = []
for x in range(len(height_map)):
    for y in range(len(height_map[x])):
        basin_size = find_basin_size(height_map, x, y)
        if basin_size != 0:
            # Use negative size here because heaps store smallest value at root.
            heappush(basin_sizes, -basin_size)

# Negate value because we store as negative to maintain heap invariant
result = -(heappop(basin_sizes) * heappop(basin_sizes) * heappop(basin_sizes))
print(f"{time()- start_time} seconds")
print(result)
