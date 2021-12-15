"""
--- Part Two ---
Considering every single measurement isn't as useful as you expected: there's just too much noise in the data.

Instead, consider sums of a three-measurement sliding window. Again considering the above example:

199  A
200  A B
208  A B C
210    B C D
200  E   C D
207  E F   D
240  E F G
269    F G H
260      G H
263        H
Start by comparing the first and second three-measurement windows.
The measurements in the first window are marked A (199, 200, 208); their sum is 199 + 200 + 208 = 607.
The second window is marked B (200, 208, 210); its sum is 618. The sum of measurements in the second window is larger than the sum of the first, so this first comparison increased.

Your goal now is to count the number of times the sum of measurements in this sliding window increases from the previous sum.
 So, compare A with B, then compare B with C, then C with D, and so on. Stop when there aren't enough measurements left to create a new three-measurement sum.

In the above example, the sum of each three-measurement window is as follows:

A: 607 (N/A - no previous sum)
B: 618 (increased)
C: 618 (no change)
D: 617 (decreased)
E: 647 (increased)
F: 716 (increased)
G: 769 (increased)
H: 792 (increased)
In this example, there are 5 sums that are larger than the previous sum.

Consider sums of a three-measurement sliding window. How many sums are larger than the previous sum?
"""


def parse_input_line(input_line):
    return int(input_line.strip())


def fetch_sliding_window_sum(depths_list: list, start_index: int, window_size: int = 3):
    if start_index + window_size > len(depths_list):
        return None

    window_sum = 0
    current_index = start_index
    for i in range(window_size):
        window_sum = window_sum + parse_input_line(depths_list[current_index])
        current_index = current_index + 1
    return window_sum


file1 = open("input.txt", "r")
lines = file1.readlines()

last_value = None
increase_count = 0
for index in range(len(lines)):
    line = lines[index]
    value = fetch_sliding_window_sum(lines, index)
    if value is None:
        continue
    if last_value is None:
        print(f"{value} (N/A - no previous measurement)")
    if last_value is not None:
        if value > last_value:
            increase_count = increase_count + 1
            print(f"{value} (increased)")
        if value < last_value:
            print(f"{value} (decreased)")
        if value == last_value:
            print(f"{value} (no change)")
    last_value = value

print(f"Increase Count: {increase_count}")
