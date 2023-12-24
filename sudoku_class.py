from ac3 import *

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
        arcs = set()
        for var in self.variables:
            row = var // 9
            col = var % 9
            box_row = row // 3
            box_col = col // 3

            # Row arcs
            for i in range(9):
                if i != col:
                    arcs.add((var, row * 9 + i))

            # Column arcs
            for j in range(9):
                if j != row:
                    arcs.add((var, j * 9 + col))

            # 3x3 box arcs
            for i in range(box_row * 3, box_row * 3 + 3):
                for j in range(box_col * 3, box_col * 3 + 3):
                    if i != row and j != col:
                        arcs.add((var, i * 9 + j))
                        
                        
        sorted_arcs = sorted(arcs, key = lambda arc: (arc[0] // 9, arc[0] % 9, arc[1] // 9, arc[1] % 9))
        for arc in sorted_arcs:
            row1, col1 = arc[0] // 9, arc[0] % 9
            row2, col2 = arc[1] // 9, arc[1] % 9
            print("(", row1, ",", col1, ")", "-->", "(", row2, ",", col2, ")")
        return arcs

    def constraint(self, x, y):
        return x != y  # Sudoku constraint: numbers should be different

    def solve(self):
        if not ac3(self):
            return None

        solution = [self.domains[var][0] for var in self.variables]
        return solution