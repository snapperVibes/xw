import itertools
from collections import defaultdict
from functools import partial
from typing import Any

import numpy as np
from ortools.sat.python import cp_model

from crossword.lib import BLACK, Across, Down, check_cell

xw = np.ones((3, 3), str)
xw[2, 0] = xw[0, 2] = BLACK.value

ascii_domain = cp_model.Domain(ord("A"), ord("Z"))

# fmt: off
vocab_strs = ["as", "in", "is", "it", "if", "at", "fun", "tad", "nag", "sag", "nut", "go", "to", "no", "do" ] # fmt: on
vocab_tups = map(lambda word: [ord(letter.upper()) for letter in word], vocab_strs)

allowed_assignments =  defaultdict(lambda: [])
for word in vocab_tups:
    allowed_assignments[len(word)].append(word)




def solve_with_cp(grid):
    assert grid.shape == (3, 3)

    grid_size = 3
    model = cp_model.CpModel()  # Step 1

    cells: dict[[int, int], Any] = {}
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i, j] == BLACK.value:
                cells[i, j] = ord(grid[i, j])
            else:
                cells[i, j] = model.NewIntVarFromDomain(
                    ascii_domain, "cells[{},{}]".format(i, j)
                )


    # Create words
    clue_count = 1

    def determine_variables(cells):
        def is_start_of_word_across(cell):
            previous_cell = cell[0] - 1, cell[1]
            if check_cell(xw, cell) and (not check_cell(xw, previous_cell)):
                return True
            return False

        def is_start_of_word_down(cell):
            previous_cell = cell[0], cell[1] - 1
            if check_cell(xw, cell) and (not check_cell(xw, previous_cell)):
                return True
            return False

        variables = []
        clue_num = 0

        def _new_variable(
                direction, cell: tuple[int, int], clue_num: int
        ):
            return direction.get_cells(xw, cell)

        new_variable_across = partial(_new_variable, Across)
        new_variable_down = partial(_new_variable, Down)

        for y, row in enumerate(xw):
            for x, is_empty in enumerate(row):
                # Todo: I don't like flags
                increment_clue_num_flag = False
                cell = x, y
                is_across = is_start_of_word_across(cell)
                is_down = is_start_of_word_down(cell)

                if not (is_across or is_down):
                    continue

                clue_num += 1
                if is_across:
                    variables.append(new_variable_across(cell, clue_num))
                if is_down:
                    variables.append(new_variable_down(cell, clue_num))

        return variables

    a = determine_variables(cells)
    words = []
    for word in a:
        b = tuple(cells[tup] for tup in word)
        words.append(b)
        model.AddAllowedAssignments(b, allowed_assignments[len(b)])
    # a = words[0]    # 1 down
    # b = words[1]    # 2 across
    # c = words[2]    # 3 across
    # d = words[3]    # 2 down
    # e = words[4]    # 1 across
    # f = words[5]    # 3 down


    for word in words:
        model.AddAllowedAssignments(word, allowed_assignments[len(word)])

    totals = []
    for word in words:
        totals.append(
            sum((cell * (26 ** i)) for i, cell in enumerate(word))
       )

    # Ensure each word in unique
    combinations = itertools.combinations(totals, 2)
    for combo in combinations:
        model.Add(combo[0] != combo[1])






    solver = cp_model.CpSolver()

    result = np.zeros((grid_size, grid_size)).astype(str)
    status = solver.Solve(model)
    if not(status in (cp_model.FEASIBLE, cp_model.OPTIMAL)):
        print("OH NO!")
        if status == cp_model.UNKNOWN:
            print("UNKNOWN")
        elif status == cp_model.MODEL_INVALID:
            print("MODEL INVALID")
        elif status == cp_model.INFEASIBLE:
            print("INFEASIBLE")
        raise RuntimeError
    for i in range(grid_size):
        for j in range(grid_size):
            result[i, j] = chr(solver.Value(cells[i, j]))
    return result


res = solve_with_cp(xw)
print(res)
