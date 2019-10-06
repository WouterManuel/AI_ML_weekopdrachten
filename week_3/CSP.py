# class constructies afkomstig uit "AIPython Code for AIFCA" - https://artint.info/AIPython/aipython/cspProblem.py
class Constraint(object):
    def __init__(self, scope, condition):
        self.scope = scope
        self.condition = condition
    
    def __repr__(self):
        return str(self.condition.__name__ + str(self.scope))
    
    def holds(self, assignment):
        # * unpacks the tuple given
        return self.condition(*tuple(assignment[v] for v in self.scope))

class CSP(object):
    def __init__(self, domains, constraints):
        self.variables = set(domains)
        self.domains = domains
        self.constraints = constraints
        self.var_to_const = {var: set() for var in self.variables}
        for con in constraints: 
            for var in con.scope:
                self.var_to_const[var].add(con)
    
    def __str__(self):
        return str(self.domains)
    
    def __repr__(self):
        return "CSP("+str(self.domains)+", "+str([str(c) for c in self.constraints])+")"
    
    def consistent(self, assignment):
        return all(con.holds(assignment) 
                   for con in self.constraints
                   if all(v in assignment for v in con.scope))
    
    def backtracking_search(self, assignment): 
        if len(assignment) == len(self.variables):
            return assignment
        
        unassigned = [v for v in self.variables if v not in assignment]

        first = unassigned[0]

        for value in self.domains[first]: 
            local_assignment = assignment.copy()
            local_assignment[first] = value

            if self.consistent(first, local_assignment):
                result = self.backtracking_search(local_assignment)

                if result is not None:
                    return result
                    
        return None