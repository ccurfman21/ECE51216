import random
import sys

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
           
def find_count(clauses): #counts literals favoring shorter clauses
    counter = {}
    for clause in clauses:
        for literal in clause:
            if literal in counter:
                counter[literal] += 2 ** -len(clause)
            else:
                counter[literal] = 2 ** -len(clause)
    return counter

def bcp(clauses, literal): #gets rid of satisfied clauses and removes opposite literal in other clauses
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

def watched_lit_bcp(clauses, literal):
    watched_literals = [[clau[0], clau[1]] for clau in clauses if len(clau) > 1]
    for watched_lit in watched_literals:
        if literal in watched_lit:
            return bcp(clauses, literal)
        elif -literal in watched_lit:
            index = watched_literals.index(watched_lit)
            if len(clauses[index]) > 2:
                watched_literals[index] = [clauses[index][1], clauses[index][2]]
            elif len(clauses[index]) <= 2:
                return bcp(clauses, literal)
    
    return clauses
            
def backtracking(clauses, assignment=[]): #finds/assigns values to solve cnf

    pure_units = ['a']
    while len(pure_units) > 0:
        count = find_count(clauses)
        pure = [key for key in count.keys() if -key not in count.keys()]
        units = [clause[0] for clause in clauses if len(clause) == 1]
        pure_units = list(set(units) | set(pure))
   
        for lit in pure_units: #eliminate all pure and unit literals from clauses
            clauses = bcp(clauses, lit)           
            if clauses is None :
                return False
        
        new_assignment = [lit for lit in pure_units] #generate assignment
        assignment.extend(new_assignment)
    
    if len(clauses) == 0:
        return True, assignment 

    select_lit = max(count, key = count.get)
    if select_lit in assignment:
        select_lit = random.choice(list(count.keys())) #select random literal thats remaining
    
    copy_clauses = clauses.copy()
    clauses = watched_lit_bcp(clauses, select_lit)
    #clauses = bcp(clauses, select_lit)
    if clauses is None:
        return False
    
    if len(clauses) == 0:
        return True, assignment
    else:
        sol= backtracking(clauses, assignment + [select_lit])
        if not sol: #backtracking last assigned variable failed, swap that variables assignment and try again
        
            copy_clauses = bcp(copy_clauses, -select_lit)
            if copy_clauses is None:
                return False
            
            sol = backtracking(copy_clauses, assignment + [-select_lit])
    
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

    if len(sys.argv) != 2:
        print("Usage: python3 mySAT.py <cnf_file>")
        return
    
    cnf_file = sys.argv[1]
    test_clauses = parse(cnf_file)  #cnf2.txt #uf20-01.cnf unsat_cnf.txt aim-50-1_6-yes1-1.cnf
         
    sol = backtracking(test_clauses) #solve cnf

    if sol:
        letters =  format(sol[1]) #convert numbers to letters
        print('RESULT: SAT')
        print('ASSIGNMENT:', *letters, sep=' ')
    else:
        print('RESULT: UNSAT')
    
   
# Main body
if __name__ == "__main__":
    main()