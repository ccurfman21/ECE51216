import timeit
import random

def parse(cnf_text):
    equation = []
    try:
        with open(cnf_text, 'r') as cnf: 
            for line in cnf:
                clause = []
                "skips the lines that pertain to the equation"
                if line.startswith(('c', 'p','%','0','\n')):
                    continue
                literals = line.split()
                for text in literals:
                    literal = int(text)
                    if literal != 0:
                        clause.append(literal)
                        if clause == '':
                            t = 1

                equation.append(clause)
        cnf.close()    
        return equation 
    except FileNotFoundError:
        print("File not found")
        return []
        
def find_count(clauses):
    counter = {}
    for clause in clauses:
        for literal in clause:
            if literal in counter:
                counter[literal] += 1
            else:
                counter[literal] = 1
    return counter

def bcp(clauses, literal):
    new_clauses = []
    for clause in clauses:
        if literal in clause:  # If the literal is already assigned true (satisfied), don't keep clause
            continue
        if -literal in clause:  # If the negation of the literal is assigned false
            update_clause = []
            for lit in clause:
                if lit != -literal:  # We are creating a new list of the literals that don't contain that negated literal
                    update_clause.append(lit)
            if len(update_clause) == 0:
                return None # Conflict detected, return None
            new_clauses.append(update_clause)
        else:
            new_clauses.append(clause)
    return new_clauses

def backtracking(clauses, assignment={}):
    #if clauses is None:
        #return True, assignment
    #else:
        count = find_count(clauses)
        print(f'\nCount: {count}')
        
        print(f'Updated Clause (start): {clauses}')
        
        units = [clause[0] for clause in clauses if len(clause) == 1] #find clauses that only have one literal and save the literal
        print(f'Unit Clauses: {units}')
        
        pure = [key for key in count.keys() if -key not in count.keys()] #find literals that are a single polarity
        print(f'Pure Literals: {pure}')
        
        pure_units = list(set(units) | set(pure)) #take union of two list without repeating literals
        print(f'Combo of Pure and Unit: {pure_units}')
        
        for lit in pure_units:
            clauses = bcp(clauses, lit)
            print(f'Updated Clause (pure): {clauses}')
            
            if clauses is None :
                return False
        new_assignment = {abs(lit): lit > 0 for lit in pure_units} #generate assignment
        assignment.update(new_assignment)
        print(f'Assignment (pure/unit): {assignment}')
            
        #if len(clauses) == 0:
            #return True
        #else:
        select_lit = random.choice(list(count.keys()))
        #select_lit = int(input('Select Literal: '))
        print(f'Random Literal Selected: {select_lit}')
        copy_clauses = clauses.copy()
        clauses = bcp(clauses,select_lit)
        if clauses is None:
            return False
        print(f'Updated Clause (select): {clauses}')
            

        if len(clauses) == 0:
            return True, assignment
        else:
            assignment[abs(select_lit)] = select_lit > 0
            print(f'Assignment (first): {assignment}')
            sol= backtracking(clauses, assignment)
            if not sol:  
                assignment[abs(select_lit)] = select_lit < 0
                copy_clauses = bcp(copy_clauses, -select_lit)
                if copy_clauses is None:
                    return False
                print(f'Assignment (second): {assignment}')
                sol = backtracking(copy_clauses, assignment)
        
        return sol

#____ Main ____
def main():
    start = timeit.default_timer() #start runtime 
    
    test_clauses = parse(r'C:\\Users\\Administrator\\Documents\\GitHub\\ECE51216\\uf20-01.cnf')  #cnf2.txt #uf20-01.cnf unsat_cnf.txt
    #test_clauses = parse(r'C:\\Users\\ccurf\\OneDrive\\Desktop\\ECE Masters Classes\\ECE 51216 - Digital Design\\cnf2_1.txt ')  #cnf2.txt #uf20-01.cnf
    
    sol = backtracking(test_clauses)

    if sol:
        
        print('RESULT: SAT')
        print(f'ASSIGNMENT: {sol}')
    else:
        print('UNSAT')
    #print(sol, assignment)
       
    stop = timeit.default_timer() #stop runtime   
    print('Time: ', (stop - start))

# Main body
if __name__ == "__main__":
    main()