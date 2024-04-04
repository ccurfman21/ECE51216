import timeit
import random
from collections import OrderedDict

def parse(cnf_text): #parses cnf file into list of lists
    equation = []
    try:
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
    
    except FileNotFoundError:
        print("File not found")
        return []
        
def find_count(clauses): #counts literals
    counter = {}
    for clause in clauses:
        for literal in clause:
            if literal in counter:
                counter[literal] += 1
            else:
                counter[literal] = 1
    return counter

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

def backtracking(clauses, assignment={}): #finds/assigns values to solve cnf

    count = find_count(clauses)
    print(f'\nCount: {count}')
    
    print(f'Updated Clause (start): {clauses}')
    
    units = [clause[0] for clause in clauses if len(clause) == 1] #find clauses that only have one literal and save the literal
    print(f'Unit Clauses: {units}')
    
    pure = [key for key in count.keys() if -key not in count.keys()] #find literals that are a single polarity
    print(f'Pure Literals: {pure}')
    
    pure_units = list(set(units) | set(pure)) #take union of two list without repeating literals
    print(f'Combo of Pure and Unit: {pure_units}')
    
    for lit in pure_units: #eliminate all pure and unit literals from clauses
        clauses = bcp(clauses, lit)
        print(f'Updated Clause (pure): {clauses}')
        
        if clauses is None :
            return False
        
    new_assignment = {abs(lit): lit > 0 for lit in pure_units} #generate assignment
    assignment.update(new_assignment)
    print(f'Assignment (pure/unit): {assignment}')
        
    select_lit = random.choice(list(count.keys())) #select random literal thats remaining
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
        if not sol: #backtracking last assigned variable failed, swap that variables assignment and try again
            assignment[abs(select_lit)] = select_lit < 0
            copy_clauses = bcp(copy_clauses, -select_lit)
            if copy_clauses is None:
                return False
            print(f'Assignment (second): {assignment}')
            
            sol = backtracking(copy_clauses, assignment)
        
    return sol

def make_letters(dict): #converts numbers and T/F to letters and 1/0
    letter_dict = {}
    for key, value in dict.items():
        letter = chr(key + ord('a') - 1)  #make number a letter
        letter_dict[letter] = 1 if value else 0  #change T/F to 1/0
    return letter_dict

#____ Main ____
def main():
    start = timeit.default_timer() #start runtime 
    
    test_clauses = parse(r'C:\\Users\\Administrator\\Documents\\GitHub\\ECE51216\\uf20-01.cnf')  #cnf2.txt #uf20-01.cnf unsat_cnf.txt
    #test_clauses = parse(r'C:\\Users\\ccurf\\OneDrive\\Desktop\\ECE Masters Classes\\ECE 51216 - Digital Design\\cnf2_1.txt ')  #cnf2.txt #uf20-01.cnf
    
    sol = backtracking(test_clauses) #solve cnf

    if sol:
        letters =  make_letters(sol[1]) #convert numbers to letters
        print('RESULT: SAT')
        print('ASSIGNMENT: ',end=' ')
        for key in letters.keys(): #print assignment dict
            print(f'{key}={letters[key]}', end=' ' )
    else:
        print('UNSAT')
       
    stop = timeit.default_timer() #stop runtime   
    print('\nTime: ', (stop - start))

# Main body
if __name__ == "__main__":
    main()