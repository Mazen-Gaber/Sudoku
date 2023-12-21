import random

def backtracking(csp,assignment = {}):
    return backtrack(assignment, csp)

def backtrack(assignment, csp):
    if is_complete(assignment, csp):
        return assignment
    # if csp.solved():
    #     return assignment
    
    var = select_unassigned_variable(assignment, csp)
    for value in order_domain_values(var, csp):
        if is_consistent(var, value, assignment, csp):
            
            # assigning
            assignment[var] = value
            if csp.domain:
                forward_check(csp, var, value, assignment)

            result = backtrack(assignment, csp)
            if result:
                return result
            
            #unassigning
            if var in assignment:
                for (neighbour, value) in csp.pruned[var]:
                    csp.domain[var].append(value)
                    
                csp.pruned[var] = []
                del assignment[var]
    return False

def is_consistent(var, value, assignment, csp):
    consistent = True
    
    for current_var, current_value in assignment.items():
        if current_value == value and current_var in csp.neighbours[var]:
            consistent = False
            
    return consistent

def is_complete(assignment, csp):
    return len(assignment) == len(csp.cells)

def select_unassigned_variable(assignment, csp):
    unassigned_variables = [var for var in csp.cells if var not in assignment]
    mini = min(unassigned_variables, key = lambda var: len(csp.domain[var]))        
    return mini

def number_of_conflicts(csp, var, value):
    count = 0
    # for each of the cells that can be in conflict with cell
    for neighbour in csp.neighbours[var]:
        # if the value of related_c is not found yet AND the value we look for exists in its possibilities
        if len(csp.domain[neighbour]) > 1 and value in csp.domain[neighbour]:
            # then a conflict exists
            count += 1
    return count

def order_domain_values(var, csp):
    if len(csp.domain[var]) == 1:
        return csp.domain[var]
    
    return sorted(csp.domain[var], key = lambda value: number_of_conflicts(csp, var, value))

def forward_check(csp, var, value, assignment):
    for neighbour in csp.neighbours[var]:
        if neighbour not in assignment:
            if value in csp.domain[neighbour]:
                csp.domain[neighbour].remove(value)
                csp.pruned[var].append((neighbour, value))


def check_initial_assignment(assignment, csp):
    for var, value in assignment.items():
        if not is_consistent(var, value, assignment, csp):
            return False
    return True


class CSP:
    def __init__(self):
        self.cells = []
        self.cells = ['A1','A2','A3','A4','B1','B2','B3','B4','C1','C2','C3','C4','D1','D2','D3','D4']  # List of variables

        self.domain = {}
        for cell in self.cells:
            self.domain[cell] = [1,2,3,4,5,6,7,8,9]

        # Neighbors for each variable
        self.neighbours = {
            'A1': ['A2', 'A3', 'A4', 'B1', 'B2','C1','C3'],
            'A2': ['A1', 'A3', 'A4','B1', 'B2','C2','C4'],
            'A3': ['A1', 'A2', 'A4','B3', 'B4','C1','C3'],
            'A4': ['A1', 'A2', 'A3','B3', 'B4','C2','C4'],
            'B1': ['A1', 'A2', 'B2','B3','B4','D1','D3'],
            'B2': ['A1', 'A2', 'B1','B3','B4','D2','D4'],
            'B3': ['A3', 'A4', 'B1','B2','B4','D1','D3'],
            'B4': ['A3', 'A4', 'B1','B2','B3','D2','D4'],
            'C1': ['A1', 'A3', 'C2','C3','C4','D1','D2'],
            'C2': ['A2', 'A4', 'C1','C3','C4','D1','D2'],
            'C3': ['A1', 'A3', 'C1','C2','C4','D3','D4'],
            'C4': ['A2', 'A4', 'C1','C2','C3','D3','D4'],
            'D1': ['B1', 'B3', 'C1','C2','D3','D4','D2'],
            'D2': ['B2', 'B4', 'C1','C2','D3','D4','D1'],
            'D3': ['B1', 'B3', 'C3','C4','D1','D2','D4'],
            'D4': ['B2', 'B4', 'C3','C4','D1','D2','D3']
        }
        
        # Additional data structure for pruning during forward checking
        self.pruned = {var: [] for var in self.cells}

    def solved(self):
	    return not any(len(self.domain[var])!=1 for var in self.cells)

# Creating an instance of the CSP
if __name__ == "__main__":        
    csp_instance = CSP()
    assignment = {}
    selected_items = random.sample(csp_instance.cells,5)
    for item in selected_items:
        assignment[item] = random.randint(1,9)
    print(f"random assignment = {assignment}")
    print("Is soduku solvable correct?", check_initial_assignment(assignment, csp_instance))
    solution = backtracking(csp_instance,assignment=assignment)
    print("Solution found by backtracking:", solution)

