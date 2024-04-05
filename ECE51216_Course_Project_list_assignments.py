import timeit
import random

def parse(cnf_text): #parses cnf file into list of lists
    equation = []
    with open(cnf_text, 'r') as cnf: #opens files as read
        for line in cnf:
            clause = []       
            if line.startswith(('c', 'p','%','0','\n')): #skips the lines that pertain to the equation
                continue
            literals = line.split() # gets rid of whitespace and makes list
            for text in literals:
                literal = int(text)
                if literal != 0:
                    clause.append(literal)
                    if clause == '':
                        t = 1
            equation.append(clause)
    cnf.close()    
    return equation
           
def find_count(clauses): #counts literals
    counter = {}
    for clause in clauses:
        for literal in clause:
            if literal in counter:
                counter[literal] += 1
            else:
                counter[literal] = 1
    return counter

def bcps(clauses, literal): #gets rid of satisfied clauses and removes opposite literal in other clauses
    neg_lit = -literal
    new_clauses = []
    for clause in clauses:
        if literal in clause: #don't keep clauses with literal in it (they are SAT already)
            continue
        if neg_lit in clause:  #opposite literal gets removed from clauses
            update_clause = [lit for lit in clause if lit != neg_lit]
            if len(update_clause) == 0:
                return None # Conflict detected (UNSAT), return None
            new_clauses.append(update_clause)
        else:
            new_clauses.append(clause)
    return new_clauses

def bcp(clauses, literal): #gets rid of satisfied clauses and removes opposite literal in other clauses
    new_clauses = []
    for clause in clauses:
        if literal in clause: #don't keep clauses with literal in it (they are SAT already)
            continue
        if -literal in clause:  #opposite literal gets removed from clauses
            update_clause = []
            for lit in clause:
                if lit != -literal:  #creating a new list of the literals that don't contain that negated literal
                    update_clause.append(lit)
            if len(update_clause) == 0:
                return None # Conflict detected (UNSAT), return None
            new_clauses.append(update_clause)
        else:
            new_clauses.append(clause)
    return new_clauses

def backtracking(clauses, assignment=[]): #finds/assigns values to solve cnf

    count = find_count(clauses)
    #print(f'\nCount: {count}')
    
    #print(f'Updated Clause (start): {clauses}')
    
    units = [clause[0] for clause in clauses if len(clause) == 1] #find clauses that only have one literal and save the literal
    #print(f'Unit Clauses: {units}')
    
    pure = [key for key in count.keys() if -key not in count.keys()] #find literals that are a single polarity
    #print(f'Pure Literals: {pure}')
    
    pure_units = list(set(units) | set(pure)) #take union of two list without repeating literals
    #print(f'Combo of Pure and Unit: {pure_units}')
    while len(pure_units) > 0:
        for lit in pure_units: #eliminate all pure and unit literals from clauses
            clauses = bcp(clauses, lit)
            #print(f'Updated Clause (pure): {clauses}') 
            
            if clauses is None :
                #print(f'Updated Clause (pure): {clauses}') 
                return False
        pure = [key for key in count.keys() if -key not in count.keys()]
        units = [clause[0] for clause in clauses if len(clause) == 1]
        pure_units = list(set(units) | set(pure))
        count = find_count(clauses)
        
        new_assignment = [lit for lit in pure_units] #generate assignment
        assignment.extend(new_assignment)
    
    #print(f'Assignment (pure/unit): {assignment}')
    if len(clauses) == 0:
        return True, assignment 
    select_lit = random.choice(list(count.keys())) #select random literal thats remaining
    #select_lit = int(input('Select Lit: '))
    #print(f'Random Literal Selected: {select_lit}')
    
    copy_clauses = clauses.copy()
    clauses = bcp(clauses,select_lit)
    if clauses is None:
        return False
    #print(f'Updated Clause (select): {clauses}')
    
    
    if len(clauses) == 0:
        return True, assignment
    else:
        #print(f'Assignment (first): {assignment}')
        
        #assignment_copy = assignment.copy()
        sol= backtracking(clauses, assignment + [select_lit])
        if not sol: #backtracking last assigned variable failed, swap that variables assignment and try again
        
            copy_clauses = bcp(copy_clauses, -select_lit)
            if copy_clauses is None:
                return False
           # print(f'Assignment (second): {assignment}')
            
            sol = backtracking(copy_clauses, assignment + [-select_lit])
    
    #print(f'Sol: {sol}')
    return sol

def format(assignment): #converts numbers and T/F to letters and 1/0
    formated_list = []
    assignment = list(set(assignment))
    assignment = sorted(assignment, key=abs)
    for ass in assignment:
        if ass < 0:
            formated_list = formated_list + [str(abs(ass)) + '=0']
        else: 
            formated_list = formated_list +[str(ass) + '=1']
    return formated_list

#____ Main ____
def main():
    
    
    test_clauses = parse('uf20-01.cnf')  #cnf2.txt #uf20-01.cnf unsat_cnf.txt aim-50-1_6-yes1-1.cnf
    
    #test_clauses = parse(r'C:\\Users\\ccurf\\OneDrive\\Desktop\\ECE Masters Classes\\ECE 51216 - Digital Design\\cnf2_1.txt ')  #cnf2.txt #uf20-01.cnf
       
    start = timeit.default_timer() #start runtime
    print('Started. Please Wait...')
    sol = backtracking(test_clauses) #solve cnf
    stop = timeit.default_timer() #stop runtime 
    if sol:
        letters =  format(sol[1]) #convert numbers to letters
        print('RESULT: SAT')
        print('ASSIGNMENT:', *letters, sep=' ')
    else:
        print('UNSAT')
    
    
    print('\nTime: ', (stop - start))
   
# Main body
if __name__ == "__main__":
    main()