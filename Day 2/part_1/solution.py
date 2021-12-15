"""
--- Day 2: Dive! ---
--- Part One ---
Now, you need to figure out how to pilot this thing.

It seems like the submarine can take a series of commands like forward 1, down 2, or up 3:

forward X increases the horizontal position by X units.
down X increases the depth by X units.
up X decreases the depth by X units.
Note that since you're on a submarine, down and up affect your depth, and so they have the opposite result of what you might expect.

The submarine seems to already have a planned course (your puzzle input). You should probably figure out where it's going. For example:

forward 5
down 5
forward 8
up 3
down 8
forward 2
Your horizontal position and depth both start at 0. The steps above would then modify them as follows:

forward 5 adds 5 to your horizontal position, a total of 5.
down 5 adds 5 to your depth, resulting in a value of 5.
forward 8 adds 8 to your horizontal position, a total of 13.
up 3 decreases your depth by 3, resulting in a value of 2.
down 8 adds 8 to your depth, resulting in a value of 10.
forward 2 adds 2 to your horizontal position, a total of 15.
After following these instructions, you would have a horizontal position of 15 and a depth of 10. (Multiplying these together produces 150.)

Calculate the horizontal position and depth you would have after following the planned course. What do you get if you multiply your final horizontal position by your final depth?
"""
from abc import ABC, abstractmethod
from typing import Type


class Command(ABC):
    def __init__(self, magnitude: int):
        self.magnitude = magnitude

    @abstractmethod
    def run_command(self, depth: int, horizontal_position: int):
        pass


class UpCommand(Command):
    def run_command(self, depth: int, horizontal_position: int):
        return depth - self.magnitude, horizontal_position


class ForwardCommand(Command):
    def run_command(self, depth: int, horizontal_position: int):
        return depth, horizontal_position + self.magnitude


class DownCommand(Command):
    def run_command(self, depth: int, horizontal_position: int):
        return depth + self.magnitude, horizontal_position


class CommandFactory:
    FORWARD = "forward"
    UP = "up"
    DOWN = "down"

    factory = {
        FORWARD: ForwardCommand,
        UP: UpCommand,
        DOWN: DownCommand,
    }

    @staticmethod
    def fetch_executable_command(command_type: str) -> Type[Command]:
        if command_type not in CommandFactory.factory:
            raise TypeError(f"Command type '{command_type}' is invalid.")
        return CommandFactory.factory[command_type]


class CoursePlanner:
    def __init__(self, course_file_name):
        self.course_file_name = course_file_name

    @staticmethod
    def parse_input_line(line) -> tuple:
        command_type, magnitude = line.strip().split()
        return command_type, int(magnitude)

    def calculate_final_position(self) -> int:
        current_depth = 0
        current_horizontal_position = 0
        with open(self.course_file_name, "r") as file:
            for line in file:
                command_type, magnitude = CoursePlanner.parse_input_line(line)
                command = CommandFactory.fetch_executable_command(command_type)(
                    magnitude
                )
                current_depth, current_horizontal_position = command.run_command(
                    current_depth, current_horizontal_position
                )
        return current_depth * current_horizontal_position


course_planner = CoursePlanner("input.txt")
print(course_planner.calculate_final_position())
