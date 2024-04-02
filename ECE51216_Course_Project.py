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


""" 
DPLL-based SAT solver algorithm for solving SAT problems.

Parameters:
    clauses (list): A list of clauses, where each clause is represented as a list of literals.
    assignment (dict): A dictionary representing the current variable assignments (default is an empty dictionary).
    
Returns:
    list: A list containing either the satisfying assignment and 'SAT' or an indication of an unsatisfiable problem.
"""
def check_empty_clauses(clauses):
    """ Checks for empty clauses that will make everything UNSAT """
    for clause in clauses:
        if len(clause) == 0:
            return True

#check for unit propagation
def unit_propagation(clauses,assignment):
    """ Finds clauses with a single literal and assigns it to satisfy that clause """
    for clause in clauses:
        if len(clause) == 1:
            assignment[abs(clause[0])] = clause[0] > 0

    return assignment

#Counter Function that counts the literals

def find_count(clauses):
    """ Counts how many of each literal there are for selection"""
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
    counter = find_count(clauses)
    return random.choice(list(counter.keys()))

#Boolean Constraint Propagation
def bcp(clauses,assignment):
    """ Removes clauses that are already satisfied and and opposite polarity variables from the other clauses"""
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
    """ Finds literals that are the same polarity and defines them """
    checked_literals = []
    for clause in clauses:
        for literal in clause:
            abs_lit = abs(literal)
            if abs_lit in checked_literals or abs_lit in list(assignment.keys()): #skip literal if it already has been checked or has a value
                continue
            else:
                same_literals = [lit for cla in clauses for lit in cla if literal == abs(lit)]
                if -literal not in same_literals: #check if there is a negative value of the current literal
                    assignment[abs_lit] = literal > 0

            checked_literals.append(abs_lit)
                
    return assignment

# Backtracking function
def backtracking(clauses, assignment={}):
    """ Checks clauses and assigns literals to make the function SAT"""
    
# Unit propagation
    unit_assignment = unit_propagation(clauses, assignment)

# Pure literal elimination
    pure_assignment = literal_elim(clauses, assignment)

    assignment.update(unit_assignment)
    assignment.update(pure_assignment)

# Boolean constraint propagation
    clauses = bcp(clauses, assignment)

    if clauses == -1:
        return ['UNSAT', assignment]

# Check if all clauses are satisfied
    if all(len(clause) == 0 for clause in clauses):
        return ['SAT', assignment]

# Select an unassigned literal
    lit = literal_selection(clauses)
    if lit is None:
        return ['UNSAT', assignment]

# Try assigning true to the literal
    assignment[lit] = True
    if backtracking(clauses, assignment):
        return ['SAT', assignment]

# If assigning true doesn't lead to a solution, try assigning false
    assignment[lit] = False
    if backtracking(clauses, assignment):
        return ['SAT', assignment]

# If neither true nor false lead to a solution, backtrack
    del assignment[lit]
    return ['UNSAT', assignment]
 
#____ Main ____
def main():
    
    start = timeit.default_timer() #start runtime 
    test_clauses = parse(r'C:\\Users\\Administrator\\Documents\\GitHub\\ECE51216\\cnf2.txt')  
    ans = backtracking(test_clauses) 
    print(ans)
    
    stop = timeit.default_timer() #stop runtime   
    print('Time: ', (stop - start))

# Main body
if __name__ == "__main__":
    main()
