import itertools

floors = ['L', 'M', 'N', 'E', 'J']

# variable domains
L = set(0,1,2,3)

for i in list(itertools.permutations(floors)):
    if (i[4] != 'L' 
        and i[0] != 'M' 
        and i[0] != 'N' 
        and i.index('E') > i.index('M') 
        and (i.index('J') - i.index('N') >= 2 or i.index('J') - i. index('N') <= -2) 
        and (i.index('N') - i.index('M') >= 2 or i.index('N') - i.index('M') <= -2)):
            print(i)

class Constraint(object):
    def __init__(self, scope, condition):
        self.scope = scope
        self.condition = condition
    
    def __repr__(self):
        return str(self.condition.__name__ + str(self.scope))
    
    def holds(self, assignement):
        return self.condition(*tuple(assignement[v] for v in self.scope))

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
        return (all(con.holds(assignment) for con in self.constraints if all(v in assignment for v con.scope)))
