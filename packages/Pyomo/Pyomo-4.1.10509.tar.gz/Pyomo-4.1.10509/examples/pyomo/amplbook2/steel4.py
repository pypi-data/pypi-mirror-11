#  _________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright (c) 2014 Sandia Corporation.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  This software is distributed under the BSD License.
#  _________________________________________________________________________

#
# Imports
#
from pyomo.core import *

#
# Setup
#

model = AbstractModel()

model.PROD = Set()

model.STAGE = Set()

model.rate = Param(model.PROD, model.STAGE, within=PositiveReals)

model.avail = Param(model.STAGE, within=NonNegativeReals)

model.profit = Param(model.PROD)

model.commit = Param(model.PROD, within=NonNegativeReals)

model.market = Param(model.PROD, within=NonNegativeReals)

def Make_bounds(model,i):
    return (model.commit[i],model.market[i])
model.Make = Var(model.PROD, bounds=Make_bounds)

def Objective_rule (model):
    return summation(model.profit, model.Make)
model.Total_Profit = Objective(rule=Objective_rule, sense=maximize)

def Timelim_rule(model, s):
    timeexpr = 0
    for p in model.PROD:
        timeexpr = timeexpr + (1.0/model.rate[p,s]) * model.Make[p]
    return timeexpr < model.avail[s]
model.Time = Constraint(model.STAGE, rule=Timelim_rule)
