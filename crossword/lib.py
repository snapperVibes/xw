### DIRECTIONS ###
import enum
import itertools
from typing import Callable, Iterator, Optional

CellCoords = tuple[int, int]


class _CellState(enum.Enum):
    WHITE = " "
    BLACK = "#"
    OUT_OF_BOUNDS = enum.auto()

    def __bool__(self):
        if self is self.WHITE:
            return True
        if self is self.BLACK:
            return False
        if self is self.OUT_OF_BOUNDS:
            return False
        raise RuntimeError("Invalid enumeration")


WHITE = _CellState.WHITE
BLACK = _CellState.BLACK
OUT_OF_BOUNDS = _CellState.OUT_OF_BOUNDS

# check_cell = partial(isinstance, cp_model.IntVar)
def check_cell(crossword, cell: tuple[int, int]):
    x, y = cell
    width = crossword.shape[0]
    height = crossword.shape[1]
    if (x < 0) or (x + 1 > width):
        return _CellState.OUT_OF_BOUNDS
    if (y < 0) or (y + 1 > height):
        return _CellState.OUT_OF_BOUNDS
    if crossword[x, y] == "#":
        return _CellState.BLACK
    return _CellState.WHITE


class BaseDirection:
    reverse_direction: "BaseDirection"
    sort_rank: int
    try_next_cell: Callable

    def potential_cell_generator(
        self, starting_cell: CellCoords
    ) -> Iterator[CellCoords]:
        raise NotImplementedError

    def get_cells(self, xw, starting_cell: CellCoords) -> list:
        previous_cells: list[CellCoords] = []

        gen = self.potential_cell_generator(starting_cell)
        while gen:
            cell = gen.__next__()
            cell_to_append, should_continue = self.try_next_cell(
                xw, cell, previous_cells
            )
            if cell_to_append:
                previous_cells.append(cell)
            if not should_continue:
                break

        return previous_cells

    def __lt__(self, other):
        return self.sort_rank < other.sort_rank


class Mixin_TryNextCell_ReturnAndContinueIfWhite:
    # Todo: this naming is ATROCIOUS
    def try_next_cell(
        self, xw, cell: CellCoords, previous_cells: list[CellCoords]
    ) -> tuple[Optional[CellCoords], bool]:
        is_valid = check_cell(xw, cell)
        if is_valid is WHITE:
            return cell, True
        return None, False


class _Across(BaseDirection, Mixin_TryNextCell_ReturnAndContinueIfWhite):
    sort_rank = 1

    def potential_cell_generator(
        self, starting_cell: CellCoords
    ) -> Iterator[CellCoords]:
        def generator() -> Iterator[CellCoords]:
            counter = itertools.count()
            while True:
                yield starting_cell[0] + counter.__next__(), starting_cell[1]

        return generator()


class _Down(BaseDirection, Mixin_TryNextCell_ReturnAndContinueIfWhite):
    sort_rank = 2

    def potential_cell_generator(
        self, starting_cell: CellCoords
    ) -> Iterator[CellCoords]:
        def generator() -> Iterator[CellCoords]:
            counter = itertools.count()
            while True:
                yield starting_cell[0], starting_cell[1] + counter.__next__()

        return generator()


Across: _Across = _Across()
Down: _Down = _Down()
