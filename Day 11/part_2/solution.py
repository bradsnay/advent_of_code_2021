"""
--- Day 11: Dumbo Octopus ---
https://adventofcode.com/2021/day/11
"""
from typing import List
from copy import deepcopy


def is_point_in_valid_range(
    x: int, y: int, energy_levels: List[List[int]], flashed_indices_this_step: set
) -> bool:
    return (
        0 <= x < len(energy_levels)
        and 0 <= y < len(energy_levels[x])
        and not (x, y) in flashed_indices_this_step
    )


def increment_adjacent_octopus(
    x: int, y: int, energy_levels: List[List[int]], flashed_indices_this_step: set
):
    for diff_x in [-1, 0, 1]:
        for diff_y in [-1, 0, 1]:
            inc_x = x + diff_x
            inc_y = y + diff_y
            if is_point_in_valid_range(
                inc_x, inc_y, energy_levels, flashed_indices_this_step
            ):
                energy_levels[inc_x][inc_y] += 1


def flash_adjacent_octopus(
    x: int, y: int, energy_levels: List[List[int]], flashed_indices_this_step: set
) -> int:
    if not is_point_in_valid_range(x, y, energy_levels, flashed_indices_this_step):
        return 0

    if energy_levels[x][y] <= 9:
        return 0

    # There was a flash at this index, set this energy level to 0
    energy_levels[x][y] = 0
    flashed_indices_this_step.add((x, y))

    # Since we flashed, we need to increment all adjacent indices
    increment_adjacent_octopus(x, y, energy_levels, flashed_indices_this_step)

    # Now check if we need to flash in all other directions and propagate as needed.
    flashes_found = 1
    for diff_x in [-1, 0, 1]:
        for diff_y in [-1, 0, 1]:
            flashes_found += flash_adjacent_octopus(
                x + diff_x, y + diff_y, energy_levels, flashed_indices_this_step
            )
    return flashes_found


def simulate_one_step(energy_levels: List[List[int]]) -> int:
    # First increase each octopus by 1
    for x in range(len(energy_levels)):
        for y in range(len(energy_levels[x])):
            energy_levels[x][y] += 1

    # Then flash all adjacent octopus where necessary
    flashed_indices_this_step = set()
    num_flashes = 0
    for x in range(len(energy_levels)):
        for y in range(len(energy_levels[x])):
            num_flashes += flash_adjacent_octopus(
                x, y, energy_levels, flashed_indices_this_step
            )
    return num_flashes


energy_levels = []
total_octopi = 0
with open("input.txt", "r") as file:
    for line in file:
        levels = [int(level) for level in line.strip()]
        total_octopi += len(levels)
        energy_levels.append(levels)

# Since we mutate the array in part 1, we need to make a copy for part 2
energy_levels_part_2 = deepcopy(energy_levels)

# Part 1
num_steps = 100
num_flashes = 0
for n in range(num_steps):
    num_flashes += simulate_one_step(energy_levels)
print(f"Part 1: {num_flashes}")

# Part 2
num_steps = 0
while True:
    num_steps += 1
    flashes_this_step = simulate_one_step(energy_levels_part_2)
    if flashes_this_step == total_octopi:
        print(f"Part 2: {num_steps}")
        break
