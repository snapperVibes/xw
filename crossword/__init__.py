# import enum
# from typing import Tuple, Any
# import numpy as np
#
# import blacksquare
#
#
# class _Direction(enum.Enum):
#     ACROSS = "across"
#     DOWN = "down"
#
#
# ACROSS = _Direction.ACROSS
# DOWN = _Direction.DOWN
#
# BLACK = "."
#
#
# CellIndex = Tuple[int, int]
# WordIndex = Tuple[int, _Direction]
#
#
# class Types:
#     Key = Tuple[int, _Direction]
#     Index = Tuple[int, int]
#
#
# class Crossword:
#     def __init__(self):
#         self._grid = None
#         self._word_indexes = {}
#
#     @staticmethod
#     def from_dataframe(df):
#         xw = Crossword()
#         xw._grid = df
#         xw._update_word_indexes()
#         return xw
#
#     def __getitem__(self, item):
#         assert len(item) == 2
#         if isinstance(item[1], int):
#             return self._grid[item[0]][item[1]]
#         elif isinstance(item[1], _Direction):
#             return self._word_indexes[item]
#         else:
#             raise IndexError("Couldn't get item")
#
#     def __setitem__(self, key, value):
#         assert len(key) == 2
#         if isinstance(key[1], int):
#             row, col = key
#             previous_value = self._grid[row][col]
#             if previous_value == BLACK and value != previous_value:
#                 self._update_word_indexes()
#             self._grid[row][col] = value
#             if value == BLACK and previous_value != BLACK:
#                 self._update_word_indexes()
#             return
#         elif isinstance(key[1], _Direction):
#             raise RuntimeError
#             # return self._word_indexes[key]
#         else:
#             raise IndexError("Couldn't get item")
#
#     # Todo
#     # def _update_word_indexes(self):
#     #     self._word_indexes = {}
#     #     # Create Rows
#     #     directions = [ACROSS, DOWN]
#     #     slices = (self._grid, self._grid.T)
#     #     for direction, slice in zip(directions, slices):
#     #         counter = 0
#     #         for _index_a, _a in enumerate(slice):
#     #             the_counter_should_be_incremented_when_possible = True
#     #
#     #             for _index_b, value in enumerate(_a):
#     #                 if value == BLACK:
#     #                     the_counter_should_be_incremented_when_possible = True
#     #                     continue
#     #
#     #                 if the_counter_should_be_incremented_when_possible:
#     #                     counter += 1
#     #                     the_counter_should_be_incremented_when_possible = False
#     #
#     #                 # I'm pretty sure this could be 1 line
#     #                 word_so_far = self._word_indexes.get((counter, direction))
#     #                 if word_so_far is None:
#     #                     word_so_far = ""
#     #                 self._word_indexes[(counter, direction)] = word_so_far + value
#     #
#     #     print(self._word_indexes)
#
#
# class Cell:
#     pass
