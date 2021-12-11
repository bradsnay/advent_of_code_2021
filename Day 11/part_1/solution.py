"""
--- Day 11: Dumbo Octopus ---
https://adventofcode.com/2021/day/11
"""
from typing import List


def is_point_in_valid_range(x: int, y: int, energy_levels: List[List[int]], flashed_indices_this_step: set) -> bool:
    return 0 <= x < len(energy_levels) and 0 <= y < len(energy_levels[x]) and not (x, y) in flashed_indices_this_step


def increment_adjacent(x: int, y: int, energy_levels: List[List[int]], flashed_indices_this_step: set):
    for diff_x in [-1, 0, 1]:
        for diff_y in [-1, 0, 1]:
            new_x = x + diff_x
            new_y = y + diff_y
            if is_point_in_valid_range(new_x, new_y, energy_levels, flashed_indices_this_step):
                energy_levels[new_x][new_y] += 1


def flash_adjacent_octopuses(x: int, y: int, energy_levels: List[List[int]], flashed_indices_this_step: set) -> int:
    if not is_point_in_valid_range(x, y, energy_levels, flashed_indices_this_step):
        return 0

    if energy_levels[x][y] <= 9:
        return 0
    # There was a flash at this index, set this energy level to 0
    energy_levels[x][y] = 0
    flashed_indices_this_step.add((x, y))
    # Since we flashed, we need to increment all adjacent indices
    increment_adjacent(x, y, energy_levels, flashed_indices_this_step)

    # Now check if we need to flash in all other directions and propagate as needed.
    flashes_found = 1
    for diff_x in [-1, 0, 1]:
        for diff_y in [-1, 0, 1]:
            flashes_found += flash_adjacent_octopuses(x + diff_x, y + diff_y, energy_levels, flashed_indices_this_step)
    return flashes_found


def simulate_one_step(energy_levels: List[List[int]]) -> int:
    # First increase each octopus by 1
    for x in range(len(energy_levels)):
        for y in range(len(energy_levels[x])):
            energy_levels[x][y] += 1
    # Then flash all adjacent octopi where necessary
    flashed_indices_this_step = set()
    num_flashes = 0
    for x in range(len(energy_levels)):
        for y in range(len(energy_levels[x])):
            num_flashes += flash_adjacent_octopuses(x, y, energy_levels, flashed_indices_this_step)
    return num_flashes

energy_levels = []
with open('input.txt', 'r') as file:
    for line in file:
        energy_levels.append([int(level) for level in line.strip()])

num_steps = 100
num_flashes = 0
for n in range(num_steps):
    num_flashes += simulate_one_step(energy_levels)
print(num_flashes)
