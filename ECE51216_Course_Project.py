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



# Global Constants




# Classes




# Functions

def read_file(file_path):
    """ Read text file """
    if os.path.exists(file_path):
        with open(file_path, "r") as fo:
            for line in fo:
                if "p cnf" in line:
                    file_contents = fo.read()       
        fo.close()    
        return file_contents
    else:
        return "File Does Not Exist"
    
def parsing_CNF_file(file_string):
    """ Parse CNF File into list"""
    cnf = []
    cnf = [i for i in file_string.split('\n')]

    for j in range(len(cnf)): 
        if cnf[j] not in ['','%',' ','0']:
            cnf[j] = [int(x) for x in cnf[j].split()] #convert to integers
            if 0 in cnf[j]:
                cnf[j].remove(0)
    try:
        index = cnf.index('%')
        cnf = cnf[:index]
    except ValueError:
        cnf = cnf

    return cnf
        

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


#____ Main ____
def main():
    raw_file = read_file(r'C:\Users\Administrator\Documents\GitHub\ECE51216\aim-50-1_6-no-1.cnf')
    #print(raw_file)
    parsed_file = parsing_CNF_file(raw_file)
    print(parsed_file)
  

# Main body
if __name__ == "__main__":
    main()
