"""
--- Day 5: Hydrothermal Venture ---
You come across a field of hydrothermal vents on the ocean floor! These vents constantly produce large, opaque clouds, so it would be best to avoid them if possible.

They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents (your puzzle input) for you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the coordinates of one end the line segment and x2,y2 are the coordinates of the other end. These line segments include the points at both ends. In other words:

An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....
In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position is shown as the number of lines which cover that point or . if no line covers that point. The top-left pair of 1s, for example, comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.

To avoid the most dangerous areas, you need to determine the number of points where at least two lines overlap. In the above example, this is anywhere in the diagram with a 2 or larger - a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two lines overlap?
"""
from typing import List, Union


class Point:
    def __init__(self, x: Union[str, int], y: Union[str, int]):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return f"X:{self.x} Y:{self.y}"


class Line:
    def __init__(self, starting_point: Point, ending_point: Point):
        self.starting_point = starting_point
        self.ending_point = ending_point

    def fetch_points_along_line(self) -> List[Point]:
        points = []

        # Horizontal line
        if self.starting_point.x == self.ending_point.x:
            start = self.starting_point.y
            end = self.ending_point.y
            # Move right
            if end > start:
                while start <= end:
                    points.append(Point(self.starting_point.x, start))
                    start += 1
            # Move left
            elif start > end:
                while start >= end:
                    points.append(Point(self.starting_point.x, start))
                    start -= 1
            return points

        # Vertical line
        elif self.starting_point.y == self.ending_point.y:
            start = self.starting_point.x
            end = self.ending_point.x
            # Move down
            if end > start:
                while start <= end:
                    points.append(Point(start, self.starting_point.y))
                    start += 1
            # Move up
            elif start > end:
                while start >= end:
                    points.append(Point(start, self.starting_point.y))
                    start -= 1
            return points

        return points


class Grid:
    def __init__(self, lines: List[Line]):
        self.lines = lines
        self.grid = {}
        self.max_x = None
        self.max_y = None
        self.overlapping_points = set()

    def build_grid(self):
        for line in self.lines:
            points = line.fetch_points_along_line()
            for point in points:
                x, y = point.x, point.y
                self._determine_max_xy(x, y)
                if y not in self.grid:
                    self.grid[y] = {}
                if x not in self.grid[y]:
                    self.grid[y][x] = 0
                self.grid[y][x] += 1
                if self.grid[y][x] >= 2 and (y, x) not in self.overlapping_points:
                    self.overlapping_points.add((y, x))

    def _determine_max_xy(self, x: int, y: int):
        if self.max_x is None:
            self.max_x = x
        if self.max_y is None:
            self.max_y = y
        if x > self.max_x:
            self.max_x = x
        if y > self.max_y:
            self.max_y = y

    def count_overlapping_points(self) -> int:
        return len(self.overlapping_points)

    def print_grid(self):
        for y in range(self.max_y + 1):
            row_string = ""
            for x in range(self.max_x + 1):
                if y in self.grid and x in self.grid[y]:
                    row_string = f"{row_string} {self.grid[y][x]}"
                else:
                    row_string = f"{row_string} ."
            print(row_string)


with open("input.txt", "r") as file:
    raw_line = file.readline().strip().split("->")
    lines = []
    while raw_line != [""]:
        start_point = Point(*raw_line[0].strip().split(","))
        end_point = Point(*raw_line[1].strip().split(","))
        lines.append(Line(start_point, end_point))
        raw_line = file.readline().strip().split("->")

grid = Grid(lines)
grid.build_grid()
# grid.print_grid()
print(grid.count_overlapping_points())
