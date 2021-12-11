"""
--- Day 4: Giant Squid ---
You're already almost 1.5km (almost a mile) below the surface of the ocean, already so deep that you can't see any sunlight.
What you can see, however, is a giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers.
Numbers are chosen at random, and the chosen number is marked on all boards on which it appears.
(Numbers may not appear on all boards.) If all numbers in any row or any column of a board are marked, that board wins.
(Diagonals don't count.)

The submarine has a bingo subsystem to help passengers (currently, you and the giant squid) pass the time.
It automatically generates a random order in which to draw numbers and a random set of boards (your puzzle input).
For example:
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7

The score of the winning board can now be calculated. Start by finding the sum of all unmarked numbers on that board; in this case, the sum is 188.
Then, multiply that sum by the number that was just called when the board won, 24, to get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win first.
 What will your final score be if you choose that board?

"""
from typing import Union, List, Dict, Tuple
from collections import defaultdict


class BoardSpace:
    def __init__(self, value: str, row: int, column: int):
        self.value = value
        self.row = row
        self.column = column
        self.marked = False


class Board:
    def __init__(self):
        self.board: Dict[str, BoardSpace] = {}
        self.raw_board: List[List[str]] = []
        self.marked_spaces: List[BoardSpace] = []
        self.count_marked_spaces_rows = defaultdict(int)
        self.count_marked_spaces_columns = defaultdict(int)
        self.sum_unmarked_numbers = 0
        self.board_won = False

    def add_row(self, row_num: int, row_values: list):
        self.raw_board.append(row_values)
        for column_index in range(len(row_values)):
            row_value = row_values[column_index]
            if self.board.get(row_value) is not None:
                raise Exception(f"There is already a value '{row_value}' on the board.")
            self.board[row_value] = BoardSpace(row_value, row_num, column_index)
            self.sum_unmarked_numbers += int(row_value)

    def mark_space(self, space_value: str):
        if space_value not in self.board:
            return
        board_space = self.board[space_value]
        board_space.marked = True
        self.marked_spaces.append(board_space)
        self.sum_unmarked_numbers -= int(space_value)
        self.count_marked_spaces_rows[board_space.row] += 1
        self.count_marked_spaces_columns[board_space.column] += 1

        self.board_won = self.count_marked_spaces_rows[board_space.row] == 5 or self.count_marked_spaces_columns[
            board_space.column] == 5

    def print_board_state(self):
        for row in self.raw_board:
            row_str = ""
            for number in row:
                if self.board[number].marked is True:
                    row_str = f"{row_str} ({number})"
                else:
                    row_str = f"{row_str} {number}"
            print(row_str)
        print()


def read_next_board(file) -> Union[Board, None]:
    file.readline()  # Skip empty line
    board = Board()
    for row_index in range(5):
        row_numbers = file.readline().strip().split()
        if row_numbers == []:
            # EOF reached
            return None
        board.add_row(row_index, row_numbers)
    return board


def print_all_board_states(boards: list):
    for board in boards:
        board.print_board_state()


def play_bingo(boards: List[Board], numbers_drawn: List[str]) -> Tuple[int, Board]:
    count_of_numbers_drawn = 0
    for drawing_number in numbers_drawn:
        for board in boards:
            board.mark_space(drawing_number)
            if board.board_won is True:
                return board.sum_unmarked_numbers * int(drawing_number), board
        count_of_numbers_drawn += 1


with open('input.txt', 'r') as file:
    bingo_numbers = file.readline().strip().split(',')
    boards = []

    board = read_next_board(file)
    while board is not None:
        boards.append(board)
        board = read_next_board(file)

score, winning_board = play_bingo(boards, bingo_numbers)
print(score)
winning_board.print_board_state()
# print_all_board_states(boards)
