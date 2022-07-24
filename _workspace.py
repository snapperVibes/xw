from ortools.sat.python import cp_model

model = cp_model.CpModel()
solver = cp_model.CpSolver()

word_1 = [model.NewIntVar(0, 25, "0"), model.NewIntVar(0, 25, "1"), model.NewIntVar(0, 25, "2")]
word_2 = [model.NewIntVar(0, 25, "0"), model.NewIntVar(0, 25, "1"), model.NewIntVar(0, 25, "2")]

model.AddAllowedAssignments(
    word_1,
    [
        (0, 1, 2),
        (3, 1, 4)
    ]
)
model.AddAllowedAssignments(
    word_2,
    [
        (0, 1, 2),
        (3, 1, 4)
    ]
)
# model.AddBoolAnd(not [ x == y for x, y in zip(word_1, word_2)])

expr = [x == y for x, y in zip(word_1, word_2)]
variables = [model.NewBoolVar(f"words_not_equal_{i}") for i, _ in enumerate([word_1, word_2])]
model.Add(expr).OnlyEnforceIf(b.Not())

class WorkspaceSolutionCallback(cp_model.CpSolverSolutionCallback):
    def __init__(self, word, word2):
        super().__init__()
        self._words = word
        self.word2 = word2

    def on_solution_callback(self):
        print(self.Value(self._words[0]), self.Value(self._words[1]), self.Value(self._words[2]))
        print(self.Value(self.word2[0]), self.Value(self.word2[1]), self.Value(self.word2[2]))
        print("---")


print("yee")

workspace_callback = WorkspaceSolutionCallback(word_1, word_2)
result = solver.Solve(model, workspace_callback)

if result == cp_model.FEASIBLE:
    print("FEASIBLE")
if result == cp_model.INFEASIBLE:
    print("INFEASIBLE")
if result == cp_model.OPTIMAL:
    print("OPTIMAL")
else:
    print("OTHER")