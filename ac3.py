# Remeber: Delete from the TAIL!
from collections import defaultdict

def AC3(csp,queue,removals=defaultdict(set)):
    # queue is for constraints
    # law el constraints khelset abl ma el domains te5las yeb2a keda i satisfied them
    # law el domains 5elset el awal raga3 false we backtrack
    while queue:
        # Xt --> Xh Delete from domain of Xt
        (Xt, Xh) = queue.pop()
        if remove_inconsistent_values(csp, Xt, Xh, removals):
            if (Xt == (0,0)):
                print(csp.domains[Xt])
            if not csp.domains[Xt]:
                return False
            elif len(csp.domains[Xt]) > 1:
                continue
            for X in csp.adjList[Xt]:
                if X != Xt:
                    queue.append((X, Xt))
    return True

def remove_inconsistent_values(csp, Xt, Xh, removals):
    # Return True if we remove a value
    revised = False
    # If Xt=x conflicts with Xh=y for every possible y, eliminate Xt=x
    for x in csp.domains[Xt].copy():
        for y in csp.domains[Xh]:
            if not csp.conflicts(*Xt, x, *Xh, y):
                break
            else:
                csp.domains[Xt].remove(x)
                removals[Xt].add(x)
                revised = True
    return revised

def makeArcQue(csp, Xs):
    return [(Xt, Xh) for Xh in Xs for Xt in csp.adjList[Xh]]
