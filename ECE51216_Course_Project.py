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
import pandas
import numpy
import timeit



# Global Constants




# Classes




# Functions

# ______________________ DO NOT USE DELETE WHEN FINISHED _______________________
"""
def read_file(file_path):
     Read text file 
    if os.path.exists(file_path):
        with open(file_path, "r") as fo:
            for line in fo:
                if "p cnf" in line:
                    file_contents = fo.read()       
        fo.close()
        #print(file_contents)    
        return file_contents
    else:
        return "File Does Not Exist"
    
def parsing_CNF_file(file_string):
    Parse CNF File into list
    cnf = [i for i in file_string.split('\n')]
    try:
        for j in range(len(cnf)): 
            if cnf[j] not in ['','%',' ','0']:
                cnf[j] = [int(x) for x in cnf[j].split()] #convert to integers
                if 0 in cnf[j]:
                    cnf[j].remove(0)
    except ValueError:
        print(cnf[j])
        print("Value Exception Error")
        
    try:
        index = cnf.index('%')
        cnf = cnf[:index]
    except ValueError:
        cnf = cnf

    return cnf
"""       
# ___________________________________________________________________________________________________


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
        if any(len(clause) == 0 for clause in clauses):
            return True
      
    def check_solved(clauses, assignment):
        """ Helper function to check if the problem is solved. """
        count = 0
        not_solved = False
        for clause in clauses:
            for literal in clause:
                cc = clause.index(literal) + 1
                if abs(literal) in assignment: #make sure literal has been assigned a value
                    if  literal > 0:
                        test = True
                    else:
                        test = False       
                    if assignment[abs(literal)] == test: #keep count of how many literals are assigned
                        count += 1
                        break
                    
                #need to add something for UNSAT: if all literals in assignment.keys() --> unsat    
                
                elif (clause.index(literal) + 1) == len(clause): #if we hit the last literal in the clause, it is not solved yet
                        not_solved = True  
            if not_solved: #get out of loop since it is not solved
                break
            elif count == len(clauses): #solved
                return True
        return False

    #check for unit propagation
    def unit_propagation(clauses,assignment):
        """ Helper function for unit propagation. """
        for clause in clauses:
            if len(clause) == 1:
                if clause[0] > 0:
                    assignment[abs(clause[0])] = True
                else:
                    assignment[abs(clause[0])] = False
        return assignment
    
    def literal_elim(clauses, assignment):
        """ Helper function for literal elimination. """
        checked_literals = []
        for clause in clauses:
            for literal in clause:
                if abs(literal) in checked_literals or abs(literal) in list(assignment.keys()): #skip literal if it already has been checked or has a value
                    continue
                else:     
                    if -literal not in [lit for cla in clauses for lit in cla if literal == abs(lit)]: #check if there is a negative value of the current literal
                        if literal > 0:
                            assignment[abs(literal)] = True
                        else:
                            assignment[abs(literal)] = False
                            
                        checked_literals.append(abs(literal))
        return assignment
    
    def inner_DPLL_main(clauses, assignment):
        """ Main function for the inner DPLL algorithm. """
        unsat = check_empty_clauses(clauses)
        
        if unsat:
            return ['Empty Clause', 'UNSAT']
        
        sat = check_solved(clauses, assignment)
        if sat:
            return [assignment, 'SAT']
        
        assignment = unit_propagation(clauses, assignment)
        
        asignment = literal_elim(clauses,assignment)
        
        
        sat = check_solved(clauses, assignment)
        if sat:
            return [assignment, 'SAT']
        else:
            return [assignment, 'UNSAT']
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
    
    test_clauses = [[1,2,3],[1],[-1,-4,-6],[5,3,-4]]
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
