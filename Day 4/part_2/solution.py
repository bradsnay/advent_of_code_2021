"""
--- Part Two ---
On the other hand, it might be wise to try a different strategy: let the giant squid win.

You aren't sure how many bingo boards a giant squid could play at once, so rather than waste time counting its arms,
the safe thing to do is to figure out which board will win last and choose that one. That way, no matter which boards it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after 13 is eventually called and its middle column is completely marked.
If you were to keep playing until this point, the second board would have a sum of unmarked numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score be?

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
        self.raw_board: List[
            List[str]
        ] = []  # Just used for printing state, not calculations.
        self.count_marked_spaces_rows = defaultdict(int)
        self.count_marked_spaces_columns = defaultdict(int)
        self.sum_unmarked_numbers = 0
        self.did_win = False

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
        self.sum_unmarked_numbers -= int(space_value)
        self.count_marked_spaces_rows[board_space.row] += 1
        self.count_marked_spaces_columns[board_space.column] += 1

        self.did_win = (
            self.count_marked_spaces_rows[board_space.row] == 5
            or self.count_marked_spaces_columns[board_space.column] == 5
        )

    def print_board_state(self):
        for row in self.raw_board:
            row_str = ""
            for number in row:
                row_str = (
                    f"{row_str} ({number})"
                    if self.board[number].marked is True
                    else f"{row_str} {number}"
                )
            print(row_str)
        print()


def play_bingo(boards: List[Board], numbers_drawn: List[str]) -> Tuple[int, Board]:
    boards_won = []
    board_indices_won = set()
    for drawing_number in numbers_drawn:
        for board_index in range(len(boards)):
            # Skip boards that already won
            if board_index in board_indices_won:
                continue
            board = boards[board_index]
            board.mark_space(drawing_number)
            if board.did_win is True:
                boards_won.append(
                    (board.sum_unmarked_numbers * int(drawing_number), board)
                )
                board_indices_won.add(board_index)
            # The last board has won.
            if len(boards_won) == len(boards):
                return boards_won[-1]
            board_index += 1

    return boards_won[-1] if len(boards_won) > 0 else None


def read_next_board(file) -> Union[Board, None]:
    file.readline()  # Skip empty line
    new_board = Board()
    for row_index in range(5):
        row_numbers = file.readline().strip().split()
        if row_numbers == []:
            # EOF reached
            return None
        new_board.add_row(row_index, row_numbers)
    return new_board


def read_input_file(file_name: str):
    with open(file_name, "r") as file:
        bingo_numbers = file.readline().strip().split(",")
        boards = []

        board = read_next_board(file)
        while board is not None:
            boards.append(board)
            board = read_next_board(file)
    return boards, bingo_numbers


score, winning_board = play_bingo(*read_input_file("input.txt"))
if winning_board is not None:
    print("We have a winner!")
    print("Score ", score)
    winning_board.print_board_state()
else:
    print("Nobody won!")
