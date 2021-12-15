"""
--- Day 14: Extended Polymerization ---

https://adventofcode.com/2021/day/14
"""
from collections import Counter
from typing import Tuple


def apply_rules(
    polymer_template: str, pair_insertion_rules: dict
) -> Tuple[str, int, int]:
    new_polymer_template = ""
    character_counts = Counter()
    for i in range(len(polymer_template)):
        char = polymer_template[i]
        character_counts[char] += 1
        pair = (
            f"{char}{polymer_template[i+1]}" if i + 1 < len(polymer_template) else None
        )
        new_polymer_template += char
        if pair in pair_insertion_rules:
            new_char = pair_insertion_rules[pair]
            new_polymer_template += new_char
            character_counts[new_char] += 1
    return (
        new_polymer_template,
        max(character_counts.values()),
        min(character_counts.values()),
    )


pair_insertion_rules = {}
with open("input.txt", "r") as file:
    polymer_template = file.readline().strip()
    # Blank line between polymer template and pair insertion rules
    file.readline()
    for line in file:
        parsed_line = line.strip().split("->")
        match_rule = parsed_line[0].strip()
        insertion_character = parsed_line[1].strip()
        pair_insertion_rules[match_rule] = insertion_character

for i in range(10):
    polymer_template, max_character_count, min_character_count = apply_rules(
        polymer_template, pair_insertion_rules
    )
print(max_character_count - min_character_count)
