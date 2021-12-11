"""
Day 8 is really long

https://adventofcode.com/2021/day/8
"""

from typing import List

len_to_digits = {
    2: 1,
    4: 4,
    3: 7,
    7: 8
}


def determine_signal_mapping(input_values: List[str]):
    # Reduce the mapping by figuring out the easy numbers first 1,4,7 and 8
    digit_to_input = {}
    for value in input_values:
        value = set(value)
        value_len = len(value)
        if value_len in len_to_digits:
            digit_found = len_to_digits[value_len]
            digit_to_input[digit_found] = value

    # Figure out the rest.
    for value in input_values:
        value = set(value)
        value_len = len(value)
        if value_len == 6:  # 0,6,9
            # Find 9. The union of 1, 4, and 7 is a subset of 9.
            if (digit_to_input[1] | digit_to_input[4] | digit_to_input[7]).issubset(value):
                digit_to_input[9] = value
            # Find 0. The union of 1 and 7 is a subset of 0 so long as 4 is not also a subset because of the middle
            # segment.
            elif (digit_to_input[1] | digit_to_input[7]).issubset(value) and not digit_to_input[4].issubset(value):
                digit_to_input[0] = value
            # Only option left is 6 for a string length of 6
            else:
                digit_to_input[6] = value

        if value_len == 5:  # 2,3,5
            # Find 5. The difference of 4 and 1 is a subset of 5.
            if (digit_to_input[4] - digit_to_input[1]).issubset(value):
                digit_to_input[5] = value
            # Find 3. The union of 1 and 7 is a subset of 3.
            elif (digit_to_input[1] | digit_to_input[7]).issubset(value):
                digit_to_input[3] = value
            # Only option left is 2 for a string length of 5.
            else:
                digit_to_input[2] = value

    return digit_to_input


with open('test_input_2.txt', 'r') as file:
    final_output = 0
    for line in file:
        parsed_line = line.strip().split('|')
        signal_mapping = determine_signal_mapping(parsed_line[0].split())
        sorted_input_value_to_digit = {}
        for digit, input_value in signal_mapping.items():
            sorted_input_value_to_digit["".join(sorted(input_value))] = digit

        output = ""
        for output_value in parsed_line[1].split():
            output = f'{output}{sorted_input_value_to_digit["".join(sorted(output_value))]}'
        final_output += int(output)
print(final_output)
