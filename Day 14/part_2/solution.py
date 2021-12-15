"""
--- Day 14: Extended Polymerization ---
--- Part 2 ---
https://adventofcode.com/2021/day/14
"""
from collections import Counter


def apply_rules(polymer_template: str, pair_counts: Counter, pair_insertion_rules: dict, num_steps: int) -> Counter:
    character_count = Counter(polymer_template)
    for i in range(num_steps):
        new_pair_counts = Counter()
        for pair, count in pair_counts.items():
            insertion_character = pair_insertion_rules[pair]
            character_count[insertion_character] += count

            generated_pair_after_insertion_1 = pair[0] + insertion_character
            generated_pair_after_insertion_2 = insertion_character + pair[1]

            new_pair_counts[generated_pair_after_insertion_1] += count
            new_pair_counts[generated_pair_after_insertion_2] += count
        pair_counts = new_pair_counts

    return character_count


pair_insertion_rules = {}
with open('input.txt', 'r') as file:
    polymer_template = file.readline().strip()
    # Blank line between polymer template and pair insertion rules
    file.readline()
    for line in file:
        parsed_line = line.strip().split('->')
        match_rule = parsed_line[0].strip()
        insertion_character = parsed_line[1].strip()
        pair_insertion_rules[match_rule] = insertion_character

pair_counts = Counter([polymer_template[i:i + 2] for i in range(len(polymer_template) - 1)])
character_count = apply_rules(polymer_template, pair_counts, pair_insertion_rules, 40)

max_character_count, min_character_count = max(character_count.values()), min(character_count.values())
print(max_character_count - min_character_count)
