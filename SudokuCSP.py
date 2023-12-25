
class SudokuCSP():
    def __init__(self, variables = [], adjList = {}, domains = {}):
        self.variables = variables
        self.adjList = adjList
        self.domains = domains

    def restore_domains(self, removals):
        for X in removals:
            # union : add removals to domains again
            self.domains[X] |= removals[X]

    # The following methods are used in min_conflict algorithm
    def nconflicts(self, X1, x, assignment):
        def conflict(X2):
            return self.conflicts(X1, x, X2, assignment[X2])
        return sum(conflict(X2) for X2 in self.adjList[X1] if X2 in assignment)

    def conflicted_vars(self, current):
        return [var for var in self.variables
                if self.nconflicts(var, current[var], current) > 0]

    def conflicts(self, i1, j1, x, i2, j2, y):
        k1 = i1 // 3 * 3 + j1 // 3
        k2 = i2 // 3 * 3 + j2 // 3
        return x == y and ( i1 == i2 or j1 == j2 or k1 == k2 )
