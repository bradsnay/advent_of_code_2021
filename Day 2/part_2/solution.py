"""
--- Part Two ---
Based on your calculations, the planned course doesn't seem to make any sense.
You find the submarine manual and discover that the process is actually slightly more complicated.

In addition to horizontal position and depth, you'll also need to track a third value, aim, which also starts at 0.
The commands also mean something entirely different than you first thought:

down X increases your aim by X units.
up X decreases your aim by X units.
forward X does two things:
It increases your horizontal position by X units.
It increases your depth by your aim multiplied by X.
Again note that since you're on a submarine, down and up do the opposite of what you might expect: "down" means aiming in the positive direction.

Now, the above example does something different:

forward 5 adds 5 to your horizontal position, a total of 5. Because your aim is 0, your depth does not change.
down 5 adds 5 to your aim, resulting in a value of 5.
forward 8 adds 8 to your horizontal position, a total of 13. Because your aim is 5, your depth increases by 8*5=40.
up 3 decreases your aim by 3, resulting in a value of 2.
down 8 adds 8 to your aim, resulting in a value of 10.
forward 2 adds 2 to your horizontal position, a total of 15. Because your aim is 10, your depth increases by 2*10=20 to a total of 60.
After following these new instructions, you would have a horizontal position of 15 and a depth of 60. (Multiplying these produces 900.)

Using this new interpretation of the commands, calculate the horizontal position and depth you would have after following the planned course.
What do you get if you multiply your final horizontal position by your final depth?
"""
from abc import ABC, abstractmethod
from typing import Type


class Command(ABC):
    def __init__(self, magnitude: int):
        self.magnitude = magnitude

    @abstractmethod
    def run_command(self, depth: int, horizontal_position: int, aim: int):
        pass


class DownCommand(Command):
    def run_command(self, depth: int, horizontal_position: int, aim: int):
        return depth, horizontal_position, aim + self.magnitude


class UpCommand(Command):
    def run_command(self, depth: int, horizontal_position: int, aim: int):
        return depth, horizontal_position, aim - self.magnitude


class ForwardCommand(Command):
    def run_command(self, depth: int, horizontal_position: int, aim: int):
        return depth + (aim * self.magnitude), horizontal_position + self.magnitude, aim


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
        current_aim = 0
        with open(self.course_file_name, "r") as file:
            for line in file:
                command_type, magnitude = CoursePlanner.parse_input_line(line)
                command = CommandFactory.fetch_executable_command(command_type)(
                    magnitude
                )
                (
                    current_depth,
                    current_horizontal_position,
                    current_aim,
                ) = command.run_command(
                    current_depth, current_horizontal_position, current_aim
                )
        return current_depth * current_horizontal_position


course_planner = CoursePlanner("input.txt")
print(course_planner.calculate_final_position())
