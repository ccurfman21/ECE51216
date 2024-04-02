"""
Authors: Cory Curfman, ccurfman@purdue.edu
         Jacob Martel, martel0@purdue.edu

Course: ECE 51216 -  Digital Systems Design Automation

Professor: Dr. Anand Raghunathan, araghu@purdue.edu
       TA: Sujay Pandit, pandit8@purdue.edu
         
Assignment: ECE51216 Course Project - Option 1

Due Date: 05/03/2024

Description:
    Implementing a SAT solver based on DPLL backtracking algoriumthm using two advanced 
    heuristics
   
"""

# Imports
import os
"import pandas"
"import numpy"
import timeit
import sys 
import random

# Functions

#____ Unit Propagation ____
"""
    The algorithm starts by simplifying the formula using unit propagation. A unit clause is a clause with only one literal. 
    When a unit clause is found, it forces the truth value of the corresponding variable, and the clause is satisfied. This process 
    continues recursively until no more unit clauses can be found
"""


#____ Pure Literal Elimination ____
""" 
    Next, the algorithm identifies and assigns truth values to pure literals. A pure literal is a variable that always appears with the same polarity 
    (either always positive or always negative) in the formula. Assigning truth values to pure literals cannot cause conflicts with the remaining clauses.
"""


#____ Branching ____
"""
      If the formula still cannot be simplified, the algorithm chooses an unassigned variable and assigns it a truth value (either true or false). 
      This choice is arbitrary and can be made based on a heuristic, such as choosing the variable that appears most frequently or appears in the fewest number of clauses.  
"""


#____ Backtracking ____
"""
    After assigning a truth value to a variable, the algorithm recursively applies steps 1-3 to the simplified formula. If a conflict arises (i.e., a clause becomes empty), 
    the algorithm backtracks to the most recent decision point (variable assignment) and tries a different truth value. This process continues until either a satisfying assignment 
    is found or all possible assignments have been tried.
"""


#____ Termination ____
"""
    The algorithm terminates when either a satisfying assignment is found (i.e., all clauses are satisfied) or it exhaustively explores all possible assignments without finding a satisfying one.
"""



def parse(cnf_text):
    """ 
    Function that reads a CNF (Conjunctive Normal Form) text file and extracts a list of literals.
    
    Parameters:
        cnf_text (str): The path to the CNF text file.
        
    Returns:
        list: A list of clauses, where each clause is represented as a list of literals.
    """
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

def sat_solver_DPLL(clauses,assignment={}):
    """ 
    DPLL-based SAT solver algorithm for solving SAT problems.
    
    Parameters:
        clauses (list): A list of clauses, where each clause is represented as a list of literals.
        assignment (dict): A dictionary representing the current variable assignments (default is an empty dictionary).
        
    Returns:
        list: A list containing either the satisfying assignment and 'SAT' or an indication of an unsatisfiable problem.
    """
    def check_empty_clauses(clauses):
        """ Helper function to check for empty clauses. """
        for clause in clauses:
            if len(clause) == 0:
                return True
    
    #check for unit propagation
    def unit_propagation(clauses,assignment):
        """ Helper function for unit propagation. """
        for clause in clauses:
            if len(clause) == 1:
                assignment[abs(clause[0])] = clause[0] > 0
                #if clause[0] > 0:
               #     assignment[abs(clause[0])] = True
                #else:
                 #   assignment[abs(clause[0])] = False

        return assignment
    
    #Counter Function that counts the literals

    def find_count(clauses):
        counter = {}
        for clause in clauses:
            for literal in clause:
                if literal in counter:
                    counter[literal] += 1
                else:
                    counter[literal] = 1
        return counter
    
    # Function that picks the literal based on the total number of apperances 
    def literal_selection(clauses):
        '''counter = find_count(clauses)
        sorted_counter = sorted(counter, key=counter.get, reverse=True)
        if sorted_counter:
            return sorted_counter[0]
        else:
            None'''
        counter = find_count(clauses)
        return random.choice(list(counter.keys()))
    
    #Boolean Constraint Propagation
    def bcp(clauses,assignment):
        updated_clauses = []
        for clause in clauses:
            satisfied = False
            modified_clauses = []
            for literal in clause:
                if literal in assignment: #checks if literal is already assigned
                    if assignment[literal]: #checks if its true
                        satisfied = True
                        break
                elif -literal not in assignment: #checks if the inverse of the literal is assigned
                    modified_clauses.append(literal)
            if not satisfied: # if clause is not satisfied
                if modified_clauses: # checks #checks if there are literals left in the clause
                    updated_clauses.append(modified_clauses)
                else:
                    return -1 # unsatisfiable
            return updated_clauses
    #pure literal 
    def literal_elim(clauses, assignment):
        """ Helper function for literal elimination. """
        checked_literals = []
        for clause in clauses:
            for literal in clause:
                if abs(literal) in checked_literals or abs(literal) in list(assignment.keys()): #skip literal if it already has been checked or has a value
                    continue
                else:
                    same_literals = [lit for cla in clauses for lit in cla if literal == abs(lit)]
                    if -literal not in same_literals: #check if there is a negative value of the current literal
                        assignment[abs(literal)] = literal > 0

                    checked_literals.append(abs(literal))
                abs_literal = abs(literal)
                if abs_literal not in assignment:
                    assignment[abs_literal] = literal > 0
        return assignment
    
    # Backtracking function
    def backtracking(clauses, assignment):
        
        '''#Unit propagation
        unit_assignment = unit_propagation(clauses, assignment)

        #Pure literal
        pure_assignment = literal_elim(clauses, assignment) 

        assignment.update(unit_assignment)
        assignment.update(pure_assignment)
        
        #Boolean constrain propagation
        clauses = bcp(clauses, assignment)
        
        if clauses == -1:
            return False
        #Start with the literal with the most appearances
        lit = literal_selection(clauses)
        if lit is None:
            return False

        solution = backtracking(clauses, assignment + [lit])

        if not solution:
            solution = backtracking(clauses, assignment + [-lit])
        return solution
'''

    # Unit propagation
        unit_assignment = unit_propagation(clauses, assignment)

    # Pure literal elimination
        pure_assignment = literal_elim(clauses, assignment)

        assignment.update(unit_assignment)
        assignment.update(pure_assignment)

    # Boolean constraint propagation
        clauses = bcp(clauses, assignment)

        if clauses == -1:
            return False
    
    # Check if all clauses are satisfied
        if all(len(clause) == 0 for clause in clauses):
            return True

    # Select an unassigned literal
        lit = literal_selection(clauses)
        if lit is None:
            return False

    # Try assigning true to the literal
        assignment[lit] = True
        if backtracking(clauses, assignment):
            return True

    # If assigning true doesn't lead to a solution, try assigning false
        assignment[lit] = False
        if backtracking(clauses, assignment):
            return True

    # If neither true nor false lead to a solution, backtrack
        del assignment[lit]
        return False

    def inner_DPLL_main(clauses, assignment):
        #Runs the main code
        unsat = check_empty_clauses(clauses)
        
        if unsat:
            return ['Empty Clause', 'UNSAT']

        if backtracking(clauses, assignment):
            return [assignment, "SAT"]
        else:
            return[assignment, "UNSAT"]
        
    return inner_DPLL_main(clauses, assignment)

    

def createFileList(directory):
    """ 
    Create a list of '.cnf' files found in the specified directory.
    
    Parameters:
        directory (str): The path to the directory containing the files.
        
    Returns:
        list: A list of filenames ending with '.cnf' found in the directory.
    """
    cnf_file_list = []
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            if file.endswith('.cnf'):
                cnf_file_list.append(file)
    return cnf_file_list



#____ Main ____
def main():
    
    start = timeit.default_timer() #start runtime
    
    test_clauses = parse("cnf.txt")
    #assignment = {4:False, 6:False}
    
    ans = sat_solver_DPLL(test_clauses)
    
    print(ans)

    """
    directory = r'C:\\Users\\Administrator\\Documents\\GitHub\\ECE51216\\'
    file = 'uf20-01.cnf'
    
    #for file in cnf_file_list:
    file_dir = directory + file
    

    parsed_file = parse(file_dir)
    result = sat_solver_DPLL(parsed_file)
    num_elem = len(parsed_file)
    num_lit_in_ele = len(parsed_file[0])
    num_lit = num_lit_in_ele*num_elem
    #print(f"Number of literals:  {num_lit}")
    print(result)
    """
    stop = timeit.default_timer() #stop runtime
    
    print('Time: ', (stop - start))
    #print(f'Total files ran: {len(cnf_file_list)}')
  

# Main body
if __name__ == "__main__":
    main()
