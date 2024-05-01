# DPLL SAT Solver w/ Heuristics
This code was originally written as the final project to ECE 51216 at Purdue University. DPLL is a method to solve logical formulas expressed in conjunctive normal form (CNF) implemented. In this program, two heuristics were added: Dynamic Largest Individual Sum (DLIS) and Watched Literals.

## Algorithm
This code was originally written in Python 3.9.1, which might not be compatible with previous versions. Pseudo code of the main backtracking algorithm is below:

```python
FUNCTION backtracking(clauses, assignment=[]):
    pure_units = ['a']
    WHILE length of pure_units > 0:
        count = find_count(clauses)
        pure = [key for key in count.keys() IF -key is not in count.keys()]
        units = [clause[0] for clause in clauses IF length of clause == 1]
        pure_units = UNIQUE COMBINATION of units and pure
        FOR EACH lit IN pure_units:
            clauses = bcp(clauses, lit)
            IF clauses is None:
                RETURN False
        new_assignment = COPY OF pure_units
        APPEND new_assignment to assignment
    IF length of clauses == 0:
        RETURN True and assignment
    select_lit = MAXIMUM count value in count
    IF select_lit in assignment:
        select_lit = RANDOM SELECTED literal from count keys
    copy_clauses = COPY OF clauses
    clauses = watched_lit_bcp(clauses, select_lit)
    IF clauses is None:
        RETURN False
    IF length of clauses == 0:
        RETURN True and assignment
    ELSE:
        sol = backtracking(clauses, assignment + [select_lit])
        IF sol is False:
            copy_clauses = bcp(copy_clauses, -select_lit)
            IF copy_clauses is None:
                RETURN False
            sol = backtracking(copy_clauses, assignment + [-select_lit])
    RETURN sol
```

## File Syntax
Each clause is written in a single line containing literals from 1 to N that ends with a 0. The negative sign "-" is used to define a negated literal. An example of a valid file is below. 

```bash
c FILE: aim-50-1_6-no-2.cnf
c
c SOURCE: Kazuo Iwama, Eiji Miyano (miyano@cscu.kyushu-u.ac.jp),
c          and Yuichi Asahiro
c
c DESCRIPTION: Artifical instances from generator by source.  Generators
c              and more information in sat/contributed/iwama.
c
c NOTE: Not Satisfiable
c
p cnf 50 80
5 17 37 0
24 28 37 0
24 -28 40 0
4 -28 -40 0
4 -24 29 0
13 -24 -29 0
-13 -24 -29 0
-4 10 -17 0
-4 -10 -17 0
26 33 -37 0
5 -26 34 0
33 -34 48 0
    ...
```

*Note: the "..." is showing a continuation of the file. They are not permitted inside the file.

## Usage
To test this code, save a CNF file, in the formatted above, into the same directory as the python file. "mySAT.py" can be replaced by the python file name. "benchmark.cnf" can be replaced with any CNF formatted file name.

```bask
python3 mySAT.py benchmark.cnf
```
The program will output the following if it is SATISFACTORY:
```bash
RESULT: SAT
ASSIGNMENT: 1=1 2=0 3=0 4=1 ...
```
The program will output the following if it is UNSATISFACTORY:
```bash
RESULT: UNSAT
```
## Authors and Acknowledgment
Written by: Cory Curfman and Jacob Martel \
Date: May 2024
