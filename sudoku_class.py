
from ac3 import *
import copy

class SudokuCSP:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.variables = [i for i in range(81)]  # Variables are the cells of the Sudoku grid
        self.domains = {var: list(range(1, 10)) if puzzle[var] == 0 else [puzzle[var]] for var in self.variables}
        self.constraints = self.get_constraints()
        self.neighbours = self.get_neighbours()
        self.arcs = self.get_arcs()

    def get_constraints(self):
        constraints = set()
        for var in self.variables:
            row = var // 9
            col = var % 9
            box_row = row // 3
            box_col = col // 3

            # Row constraints
            for i in range(9):
                if i != col:
                    constraints.add((var, row * 9 + i))

            # Column constraints
            for j in range(9):
                if j != row:
                    constraints.add((var, j * 9 + col))

            # 3x3 box constraints
            for i in range(box_row * 3, box_row * 3 + 3):
                for j in range(box_col * 3, box_col * 3 + 3):
                    if i != row and j != col:
                        constraints.add((var, i * 9 + j))

        return constraints

    def get_neighbours(self):
        neighbours = {var: set() for var in self.variables}
        for var1, var2 in self.constraints:
            neighbours[var1].add(var2)
            neighbours[var2].add(var1)
        return neighbours

    def get_arcs(self):
        arcs = self.constraints.copy()
        sorted_arcs = sorted(arcs, key=lambda arc: (arc[0] // 9, arc[0] % 9, arc[1] // 9, arc[1] % 9))
        for arc in sorted_arcs:
            row1, col1 = arc[0] // 9, arc[0] % 9
            row2, col2 = arc[1] // 9, arc[1] % 9
            # print("(", row1, ",", col1, ")", "-->", "(", row2, ",", col2, ")")
        return arcs

    def constraint(self, x, y):
        return x != y  # Sudoku constraint: numbers should be different

    def solve(self):
        if not ac3(self, None):
            return None

        return self.backtrack()

    def backtrack(self):
        if self.is_complete():
            return [self.domains[var][0] for var in self.variables]

        var = self.select_unassigned_variable()
        for value in self.order_domain_values(var):
            if self.is_consistent(var, value):
                self.assign_value(var, value)
                result = self.backtrack()
                if result is not None:
                    return result
                self.remove_assignment(var)

        return None

    def is_complete(self):
        for var in self.variables:
            if len(self.domains[var]) != 1:
                return False
        return True

    def select_unassigned_variable(self):
        for var in self.variables:
            if len(self.domains[var]) != 1:
                return var

    def order_domain_values(self, var):
        return self.domains[var]

    def is_consistent(self, var, value):
        for neighbour in self.neighbours[var]:
            if len(self.domains[neighbour]) == 1 and self.domains[neighbour][0] == value:
                return False
        return True

    def assign_value(self, var, value):
        self.domains[var] = [value]

    def remove_assignment(self, var):
        self.domains[var] = list(range(1, 10)) if self.puzzle[var] == 0 else [self.puzzle[var]]