#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:
#
# Author:      alven
#
# Created:     23/09/2015
# Copyright:   (c) alven 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from pulp import *
prob = LpProblem('lptest', LpMaximize)

x1 = LpVariable('x1', lowBound = 0)
x2 = LpVariable('x2', lowBound = 0)

prob += 2 * x1 + 5 * x2

prob += 2 * x1 - x2 <= 4
prob += x1 + 2 * x2 <= 9
prob += -x1 + x2 <= 3

GLPK().solve(prob)

for v in prob.variables():
    print(v.name, '=', v.varValue)

print('objective =', value(prob.objective))


