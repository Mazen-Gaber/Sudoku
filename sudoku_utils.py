def backtracking(csp):
    return backtrack({}, csp)

def backtrack(assignment, csp):
    if is_complete(assignment, csp):
        return assignment
    
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
    return min(unassigned_variables, key = lambda var: len(csp.domain[var]))

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

