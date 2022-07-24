import itertools

from ortools.sat.python import cp_model

model = cp_model.CpModel()
solver = cp_model.CpSolver()

base10_domain = cp_model.Domain(0, 9)

a = model.NewIntVarFromDomain(base10_domain, "a")
b = model.NewIntVarFromDomain(base10_domain, "b")
c = model.NewIntVarFromDomain(base10_domain, "c")


x = model.NewIntVarFromDomain(base10_domain, "x")
y = model.NewIntVarFromDomain(base10_domain, "y")
z = model.NewIntVarFromDomain(base10_domain, "z")

counter = itertools.count(0)

def var_from_array(elements: list[cp_model.IntVar], base):
    var = model.NewIntVar(0, cp_model.INT32_MAX, str(counter.__next__()))
    expr = var.Sum([elem * (base ** i) for i, elem in enumerate(elements)])
    # print("expr:", expr)
    # model.AddLinearConstraint(expr, 0, cp_model.INT_MAX)
    # breakpoint()
    model.Add(var == expr)
    return var

abc_list = [a, b, c]
xyz_list = [x, y, z]

abc_var = var_from_array(abc_list, 10)
xyz_var = var_from_array(xyz_list, 10)

variables = []
variables.extend(abc_list)
variables.extend(xyz_list)
variables.extend((abc_var, xyz_var))

model.Add(a == 1)
model.Add(b == 2)
model.Add(c == 3)

model.Add(x == 1)
model.Add(y == 2)
model.Add(z >= 3)

expr = abc_var != xyz_var
model.Add(expr)

model.Minimize(
    a + b + c + x + y + z
)



class WorkspaceSolutionCallback(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        super().__init__()
        self._variables = variables

    def on_solution_callback(self):
        print("Solution:")
        for var in self._variables:
            print(var.Name(), self.Value(var))
        print("---")


solution_callback = WorkspaceSolutionCallback(variables)
result = solver.Solve(model, solution_callback)

if result == cp_model.FEASIBLE:
    print("FEASIBLE")
elif result == cp_model.INFEASIBLE:
    print("INFEASIBLE")
elif result == cp_model.OPTIMAL:
    print("OPTIMAL")
elif result == cp_model.MODEL_INVALID:
    print("MODEL INVALID")
else:
    print("OTHER", result)
