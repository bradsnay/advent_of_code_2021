"""
--- Part Two ---
The crabs don't seem interested in your proposed solution. Perhaps you misunderstand crab engineering?

As it turns out, crab submarine engines don't burn fuel at a constant rate. Instead, each change of 1 step in horizontal position costs 1 more unit of fuel than the last: the first step costs 1, the second step costs 2, the third step costs 3, and so on.

As each crab moves, moving further becomes more expensive. This changes the best horizontal position to align them all on; in the example above, this becomes 5:

Move from 16 to 5: 66 fuel
Move from 1 to 5: 10 fuel
Move from 2 to 5: 6 fuel
Move from 0 to 5: 15 fuel
Move from 4 to 5: 1 fuel
Move from 2 to 5: 6 fuel
Move from 7 to 5: 3 fuel
Move from 1 to 5: 10 fuel
Move from 2 to 5: 6 fuel
Move from 14 to 5: 45 fuel
This costs a total of 168 fuel. This is the new cheapest possible outcome; the old alignment position (2) now costs 206 fuel instead.

Determine the horizontal position that the crabs can align to using the least fuel possible so they can make you an escape route! How much fuel must they spend to align to that position?
"""
from time import time
from collections import defaultdict
from statistics import median


lower_bound = None
upper_bound = None
with open("input.txt", 'r') as file:
    positions = defaultdict(int)
    input_size = 0
    for position in file.readline().strip().split(','):
        position = int(position)
        positions[position] += 1
        input_size += 1
        if lower_bound is None or lower_bound > position:
            lower_bound = position
        if upper_bound is None or upper_bound < position:
            upper_bound = position

start_time = time()
fuel_needed = 0
position_to_align_at = int(median(positions.keys()))
for current_position, position_count in positions.items():
    positions_moved = abs(position_to_align_at - current_position)
    fuel_needed += positions_moved * (1 + positions_moved) / 2 * position_count
print(f"Median solution -> Fuel needed {fuel_needed} Position: {position_to_align_at} Time: {time() - start_time} "
      f"seconds")

start_time = time()
min_fuel_needed = None
best_position = None
for position_to_align_at in range(lower_bound, upper_bound):
    fuel_needed = 0
    for current_position, position_count in positions.items():
        positions_moved = abs(position_to_align_at - current_position)
        fuel_needed += positions_moved * (1 + positions_moved) / 2 * position_count

    if min_fuel_needed is None or min_fuel_needed > fuel_needed:
        min_fuel_needed = fuel_needed
        best_position = position_to_align_at

print(f"Inital solution -> Fuel needed: {min_fuel_needed}, Position: {best_position}, Time: {time() - start_time} "
      f"seconds")




