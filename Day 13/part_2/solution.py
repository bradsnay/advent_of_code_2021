"""
--- Day 13: Transparent Origami ---
--- Part 2 ---
https://adventofcode.com/2021/day/13
"""
from typing import Tuple


def print_coordinates(max_x: int, max_y:int, coordinates: set):
    for y in range(max_y + 1):
        print_str = ""
        for x in range(max_x + 1):
            if (x, y) in coordinates:
                print_str += ' # '
            else:
                print_str += " . "
        print(print_str)


def perform_single_fold(should_fold_y: bool, axis_fold_value: int, coordinates: set, max_x: int, max_y: int) -> Tuple[set, int, int]:
    new_coordinates = set()
    for x, y in coordinates:
        # Determine if we're folding x or y.
        folding_index = y if should_fold_y is True else x
        if folding_index > axis_fold_value:
            # The coordinate exists in the section being folded over because it's above the folding line.
            new_index = (axis_fold_value - (folding_index - axis_fold_value))
            if folding_index == y:
                new_coordinates.add((x, new_index))
            if folding_index == x:
                new_coordinates.add((new_index, y))
        elif folding_index == axis_fold_value:
            # The index being folded disappears so don't add it to the new coordinates.
            continue
        else:
            # The coordinate exists in the section that isn't moving so it stays the same.
            new_coordinates.add((x, y))

    if should_fold_y is True:
        max_y = axis_fold_value - 1
    else:
        max_x = axis_fold_value - 1
    return new_coordinates, max_x, max_y


def perform_folds(folding_instructions: list, coordinates: set, max_x: int, max_y: int):
    for axis, axis_value in folding_instructions:
        coordinates, max_x, max_y = perform_single_fold(axis == 'y', axis_value, coordinates, max_x, max_y)
    return coordinates, max_x, max_y


dot_coordinates = set()
folding_instructions = []
max_x = 0
max_y = 0
with open('input.txt', 'r') as file:
    for line in file:
        line = line.strip()
        # The blank line before the folding instructions
        if line == "":
            continue
        # Line is a folding instruction.
        if line.startswith('fold'):
            line = line.split()
            folding_instruction = line[2].split('=')
            folding_instructions.append((folding_instruction[0], int(folding_instruction[1])))
            pass
        # Otherwise it's a coordinate.
        else:
            coordinates = line.split(',')
            x = int(coordinates[0])
            y = int(coordinates[1])
            dot_coordinates.add((x, y))
            max_x = max(max_x, x)
            max_y = max(max_y, y)

new_coordinates, max_x, max_y = perform_folds(folding_instructions, dot_coordinates, max_x, max_y)
print_coordinates(max_x, max_y, new_coordinates)  # PZEHRAER

