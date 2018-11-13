#/usr/bin/env python3

import cplex
import readfile

# Create an instance of a linear problem to solve
problem = cplex.Cplex()


# We want to find a maximum of our objective function
problem.objective.set_sense(problem.objective.sense.maximize)

# The names of our variables
names = ["x", "y", "z"]

"""
n_vars m_cons optimal solution value
[coefficients p(j)](1,n_vars)
[[the coefficients r(i,j)]](m_cons,n_vars)
[b]^T(1,m_cons)


6 10 3800
 100 600 1200 2400 500 2000
 8 12 13 64 22 41
 8 12 13 75 22 41
 3 6 4 18 6 4
 5 10 8 32 6 12
 5 13 8 42 6 20
 5 13 8 48 6 20
 0 0 0 0 8 0
 3 0 4 0 8 0
 3 2 4 0 8 4
 3 2 4 8 8 4
 80 96 20 36 44 48 10 18 22 24
"""


# The obective function. More precisely, the coefficients of the objective
# function. Note that we are casting to floats.
objective = [5.0, 2.0, -1.0]
#objective = [100 600 1200 2400 500 2000]

# Lower bounds. Since these are all zero, we could simply not pass them in as
# all zeroes is the default.
lower_bounds = [0.0, 0.0, 0.0]

# Upper bounds. The default here would be cplex.infinity, or 1e+20.
upper_bounds = [100, 1000, cplex.infinity]

#problem.variables.add(obj = objective,lb = lower_bounds,ub = upper_bounds,names = names)

# Constraints

# Constraints are entered in two parts, as a left hand part and a right hand
# part. Most times, these will be represented as matrices in your problem. In
# our case, we have "3x + y - z ≤ 75" and "3x + 4y + 4z ≤ 160" which we can
# write as matrices as follows:

# [  3   1  -1 ]   [ x ]   [  75 ]
# [  3   4   4 ]   [ y ] ≤ [ 160 ]
#                  [ z ]

# First, we name the constraints
constraint_names = ["c1", "c2"]

# The actual constraints are now added. Each constraint is actually a list
# consisting of two objects, each of which are themselves lists. The first list
# represents each of the variables in the constraint, and the second list is the
# coefficient of the respective variable. Data is entered in this way as the
# constraints matrix is often sparse.

# The first constraint is entered by referring to each variable by its name
# (which we defined earlier). This then represents "3x + y - z"
first_constraint = [["x", "y", "z"], [3.0, 1.0, -1.0]]
# In this second constraint, we refer to the variables by their indices. Since
# "x" was the first variable we added, "y" the second and "z" the third, this
# then represents 3x + 4y + 4z
second_constraint = [[0, 1, 2], [3.0, 4.0, 4.0]]
constraints = [ first_constraint, second_constraint ]

# So far we haven't added a right hand side, so we do that now. Note that the
# first entry in this list corresponds to the first constraint, and so-on.
rhs = [75.0, 160.0]

# We need to enter the senses of the constraints. That is, we need to tell Cplex
# whether each constrains should be treated as an upper-limit (≤, denoted "L"
# for less-than), a lower limit (≥, denoted "G" for greater than) or an equality
# (=, denoted "E" for equality)
constraint_senses = [ "L", "L" ]

# Note that we can actually set senses as a string. That is, we could also use
#     constraint_senses = "LL"
# to pass in our constraints

objective, lower_bounds, upper_bounds, names, constraints, constraint_senses, rhs, constraint_names = readfile.readfile("teste1.txt")

print(objective)
print(lower_bounds)
print(upper_bounds)
print(names)

print(constraints)
print(constraint_senses)
print(rhs)
print(constraint_names)

problem.variables.add(obj = objective,
                      lb = lower_bounds,
                      ub = upper_bounds,
                      names = names)

for name in names:
    problem.variables.set_types(name, problem.variables.type.binary)

print("done")
# And add the constraints
problem.linear_constraints.add(lin_expr = constraints,
                               senses = constraint_senses,
                               rhs = rhs,
                               names = constraint_names)


print("Done")

problem.set_problem_type(problem.problem_type.MILP)
# Solve the problem
problem.solve()

# And print the solutions
print(problem.solution.get_values())
