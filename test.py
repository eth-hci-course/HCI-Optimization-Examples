# from gurobipy import *
import utils_QAP
import gurobipy

"""'
Taken from: https://github.com/eth-ait/ComputationalInteraction17/tree/master/Anna%20%26%20Antti
"""


def solve(characters, keyslots, bigram_frequency, movement_time, columns):
    # ==== 1. Create the (empty) model ====
    model = gurobipy.Model("keyboard")

    # ==== 2. Add decision variables ======
    x = {}
    # Create one binary variable for each letter-key pair.
    # We give it a meaningful name so we later understand what it means if it is set to 1
    for i in characters:
        for k in keyslots:
            x[(i, k)] = model.addVar(vtype=gurobipy.GRB.BINARY, name="%s_%i" % (i, k))
            # Integrate new variables
    model.update()

    # ==== 3. Specify Objective function ======
    cost = gurobipy.quicksum(
        bigram_frequency[i, j] * movement_time[k, l] * x[(i, k)] * x[(j, l)]
        for l in keyslots
        for k in keyslots
        for i in characters
        for j in characters
    )
    model.setObjective(cost, gurobipy.GRB.MINIMIZE)

    # ====4. Add Constraints ======
    # Add constraints
    # Each letter is only assigned to one keyslot
    for i in characters:
        model.addConstr(
            gurobipy.quicksum(x[(i, k)] for k in keyslots) == 1,
            "uniqueness_constraint_%s" % i,
        )
        # Each element is only assigned to one position
    for k in keyslots:
        model.addConstr(
            gurobipy.quicksum(x[(i, k)] for i in characters) <= 1,
            "uniqueness_constraint_%i" % k,
        )

    model.update()

    # ==== 5. Optimize model ======
    p = model.presolve()
    p.write("presolve.lp")
    model.optimize()

    # ====6. Extract solution ======
    mapping = {}

    for v in model.getVars():
        if v.x == 1:
            character = v.varName.split("_")[0]
            slot = int(v.varName.split("_")[1])
            mapping[character] = slot

    return mapping, model.getObjective().getValue()


# define characters and keyslots
characters = ["a", "c", "s", "r", "e", "f", "t", "h", "i"]
keyslots = list(range(len(characters)))
columns = 3

# obtain cost factors: movement time and bigram frequencies
movement_time = {
    (s1, s2): utils_QAP.fittslawcost(s1, s2, utils_QAP.distance(columns, s1, s2))
    for s1 in keyslots
    for s2 in keyslots
}

bigram_frequency = utils_QAP.get_bigram_frequency(characters)

# solve the problem
mapping, objective = solve(
    characters, keyslots, bigram_frequency, movement_time, columns
)

print("The average WPM of the winning keyboard is %.2f" % utils_QAP.wpm(objective))
