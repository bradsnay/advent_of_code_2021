"""
--- Day 3: Binary Diagnostic ---
The submarine has been making some odd creaking noises, so you ask it to produce a diagnostic report just in case.

The diagnostic report (your puzzle input) consists of a list of binary numbers which, when decoded properly, can tell
you many useful things about the conditions of the submarine. The first parameter to check is the power consumption.

You need to use the binary numbers in the diagnostic report to generate two new binary numbers (called the gamma rate and the epsilon rate).
The power consumption can then be found by multiplying the gamma rate by the epsilon rate.

Each bit in the gamma rate can be determined by finding the most common bit in the corresponding position of all numbers in the diagnostic report. For example, given the following diagnostic report:

00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
Considering only the first bit of each number, there are five 0 bits and seven 1 bits. Since the most common bit is 1, the first bit of the gamma rate is 1.

The most common second bit of the numbers in the diagnostic report is 0, so the second bit of the gamma rate is 0.

The most common value of the third, fourth, and fifth bits are 1, 1, and 0, respectively, and so the final three bits of the gamma rate are 110.

So, the gamma rate is the binary number 10110, or 22 in decimal.

The epsilon rate is calculated in a similar way; rather than use the most common bit, the least common bit from each position is used. So, the epsilon rate is 01001, or 9 in decimal. Multiplying the gamma rate (22) by the epsilon rate (9) produces the power consumption, 198.

Use the binary numbers in your diagnostic report to calculate the gamma rate and epsilon rate, then multiply them together. What is the power consumption of the submarine? (Be sure to represent your answer in decimal, not binary.)
"""


def parse_input_line(file_line):
    return file_line.strip()


def parse_input_line_int(file_line):
    return int(file_line.strip(), 2)


columns = {}

with open('input.txt', 'r') as file:
    for line in file:
        value = parse_input_line(line)
        # print(value)
        for column_index in range(len(value)):
            bit = int(value[column_index])
            if columns.get(column_index) is None:
                columns[column_index] = {}
            if columns[column_index].get(bit) is None:
                columns[column_index][bit] = 0
            columns[column_index][bit] += 1

binary_gamma_rate = ""
binary_epsilon_rate = ""
for column_index in columns.keys():
    bit_counts = columns[column_index]

    max_bit_value = None
    min_bit_value = None

    max_bit_count = None
    min_bit_count = None
    for bit_value, bit_count in bit_counts.items():
        if max_bit_count is None:
            max_bit_count = bit_count
            max_bit_value = bit_value
        if min_bit_count is None:
            min_bit_count = bit_count
            min_bit_value = bit_value

        if bit_count > max_bit_count:
            max_bit_count = bit_count
            max_bit_value = bit_value
        if bit_count < min_bit_count:
            min_bit_count = bit_count
            min_bit_value = bit_value
    binary_gamma_rate = f"{binary_gamma_rate}{max_bit_value}"
    binary_epsilon_rate = f"{binary_epsilon_rate}{min_bit_value}"

print(columns)
print("trivial solution")

decimal_gamma_rate = int(binary_gamma_rate, 2)
decimal_epsilon_rate = int(binary_epsilon_rate, 2)
final_result = decimal_epsilon_rate * decimal_gamma_rate
print(f"G:{binary_gamma_rate} ({decimal_gamma_rate})")
print(f"E:{binary_epsilon_rate} ({decimal_epsilon_rate})")
print(f"F:{'{0:b}'.format(final_result)} ({final_result})")
