import itertools
import sys

rows = "123456789"
cols = "ABCDEFGHI"

class Sudoku:
    def __init__(self, grid):
        game = list(grid)
        # generation of all the coords of the grid
        self.cells = list()
        self.cells = self.generate_variables()

        # generation of all the possibilities for each one of these coords
        self.domain = dict()
        self.domain = self.generate_domain(grid)
        # generation of the line / row / square constraints
        rule_constraints = self.generate_constraints()

        # convertion of these constraints to binary constraints
        self.binary_constraints = list()
        self.binary_constraints = self.generate_binary_constraints(rule_constraints)

        # generating all constraint-related cells for each of them
        self.neighbours = dict()
        self.neighbours = self.generate_neighbours()
        #prune
        self.pruned = dict()
        self.pruned = {v: list() if grid[i] == '0' else [int(grid[i])] for i, v in enumerate(self.cells)}
        
    def generate_variables(self):
        neighbours = []

        # for A,B,C, ... ,H,I
        for col in cols:
            #for 1,2,3 ,... ,8,9
            for row in rows:
                # A1, A2, A3, ... , H8, H9
                new_coords = col + row
                neighbours.append(new_coords)

        return neighbours
    
    def generate_domain(self, grid):
        grid_as_list = list(grid)
        domain = dict()
        for index, coords in enumerate(self.cells):
            # if value is 0, then the cell can have any value in [1, 9]
            if grid_as_list[index] == "0":
                domain[coords] = list(range(1,10))
            # else value is already defined, possibilities is this value
            else:
                domain[coords] = [int(grid_as_list[index])]
        return domain

    def generate_constraints(self):
        
        row_constraints = []
        column_constraints = []
        square_constraints = []

        # get rows constraints
        for row in rows:
            row_constraints.append([col + row for col in cols])

        # get columns constraints
        for col in cols:
            column_constraints.append([col + row for row in rows])
            
        rows_square_neighbours = (cols[i:i+3] for i in range(0, len(rows), 3))
        rows_square_neighbours = list(rows_square_neighbours)

        cols_square_neighbours = (rows[i:i+3] for i in range(0, len(cols), 3))
        cols_square_neighbours = list(cols_square_neighbours)

        # for each square
        for row in rows_square_neighbours:
            for col in cols_square_neighbours:

                current_square_constraints = []
                
                # and for each value in this square
                for x in row:
                    for y in col:
                        current_square_constraints.append(x + y)

                square_constraints.append(current_square_constraints)

        # all constraints is the sum of these 3 rules
        return row_constraints + column_constraints + square_constraints

    def generate_binary_constraints(self, rule_constraints):
        generated_binary_constraints = list()
        # for each set of constraints
        for constraint_set in rule_constraints:
            binary_constraints = list()
            # 2 because we want binary constraints            
            #for tuple_of_constraint in itertools.combinations(constraint_set, 2):
            for tuple_of_constraint in itertools.permutations(constraint_set, 2):
                binary_constraints.append(tuple_of_constraint)
            # for each of these binary constraints
            for constraint in binary_constraints:
                # check if we already have this constraint saved
                # = check if already exists
                constraint_as_list = list(constraint)
                if(constraint_as_list not in generated_binary_constraints):
                    generated_binary_constraints.append([constraint[0], constraint[1]])
        return generated_binary_constraints

    def generate_neighbours(self):
        related_cells = dict()
        #for each one of the 81 cells
        for cell in self.cells:
            related_cells[cell] = list()
            # related cells are the ones that current cell has constraints with
            for constraint in self.binary_constraints:
                if cell == constraint[0]:
                    related_cells[cell].append(constraint[1])

        return related_cells

    def isFinished(self):
        for coords, possibilities in self.domain.items():
            if len(possibilities) > 1:
                return False
        return True
    
    def __str__(self):
        output = ""
        count = 1
        # for each cell, print its value
        for cell in self.cells:
            # trick to get the right print in case of an AC3-finished sudoku
            value = str(self.domain[cell])
            if type(self.domain[cell]) == list:
                value = str(self.domain[cell][0])
            output += "[" + value + "]"
            # if we reach the end of the line,
            # make a new line on display
            if count >= 9:
                count = 0
                output += "\n"
            count += 1
        return output
