"""
--- Part Two ---
Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture;
you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in your list will
only ever be horizontal, vertical, or a diagonal line at exactly 45 degrees. In other words:

An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
Considering all lines from the above example would now produce the following diagram:

1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....
You still need to determine the number of points where at least two lines overlap.
 In the above example, this is still anywhere in the diagram with a 2 or larger - now a total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?


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

        # Vertical line
        if self.starting_point.x == self.ending_point.x:
            start = self.starting_point.y
            end = self.ending_point.y
            # Move down
            if end > start:
                while start <= end:
                    points.append(Point(self.starting_point.x, start))
                    start += 1
            # Move up
            elif start > end:
                while start >= end:
                    points.append(Point(self.starting_point.x, start))
                    start -= 1
            return points

        # Horizontal line
        if self.starting_point.y == self.ending_point.y:
            start = self.starting_point.x
            end = self.ending_point.x
            # Move left
            if end > start:
                while start <= end:
                    points.append(Point(start, self.starting_point.y))
                    start += 1
            # Move right
            elif start > end:
                while start >= end:
                    points.append(Point(start, self.starting_point.y))
                    start -= 1
            return points

        # Diagonal line
        start_x = self.starting_point.x
        end_x = self.ending_point.x
        start_y = self.starting_point.y
        end_y = self.ending_point.y
        # Move diagonally up left
        if start_x > end_x and start_y > end_y:
            while start_x >= end_x and start_y >= end_y:
                points.append(Point(start_x, start_y))
                start_x -= 1
                start_y -= 1
        # Move diagonally up right
        elif start_x < end_x and start_y > end_y:
            while start_x <= end_x and start_y >= end_y:
                points.append(Point(start_x, start_y))
                start_x += 1
                start_y -= 1
        # Move diagonally down left
        elif start_x > end_x and start_y < end_y:
            while start_x >= end_x and start_y <= end_y:
                points.append(Point(start_x, start_y))
                start_x -= 1
                start_y += 1
        # Move diagonally down right
        elif start_x < end_x and start_y < end_y:
            while start_x <= end_x and start_y <= end_y:
                points.append(Point(start_x, start_y))
                start_x += 1
                start_y += 1
        return points


class Grid:
    def __init__(self, lines: List[Line]):
        self.lines = lines
        self.grid = {}
        self.max_x = None
        self.max_y = None
        self.overlapping_points = set()
        self._build_grid()

    def _build_grid(self):
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
        # Just used for printing the grid state
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
# grid.print_grid()
print(grid.count_overlapping_points())
