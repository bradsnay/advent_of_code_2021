"""
Day 8 is really long

https://adventofcode.com/2021/day/8
"""

len_to_digits = {
    2: 1,
    4: 4,
    3: 7,
    7: 8
}

with open('input.txt', 'r') as file:
    digit_count = 0
    for line in file:
        output_values = line.strip().split('|')[1]
        print(output_values)
        for value in output_values.split():
            if len(value) in len_to_digits:
                digit_count += 1
print(digit_count)
