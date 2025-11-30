
Author: Joey Lim
Class: CSCE 420 
Programming Assignment PA2

## overview
This project implements a Boolean satisfiability solver using the DPLL algorithm.
The solver reads a propositional knowledge base in CNF (Conjunctive Normal Form) and does:
DPLL recursive search
Unit Clause heuristic
Backtracking search

and returns:
A satisfying model or “unsatisfiable” if no model exists

The program is used to solve:
1.	The Australia Map Coloring problem
2.	The 6-Queens problem
3.	A Wumpus World inference scenario

### how to run
python3 DPLL.py <KB_filename> <literal>*

<KB_filename> → your .cnf file
<literal>* → optional literals to add as unit clauses

Examples

python DPLL.py mapcolor.cnf > transcript.mapcolor.txt
python DPLL.py mapcolor.cnf -NTR -NSWR TR > transcript.mapcolor2.txt

python DPLL.py 6queens.cnf > transcript.6queens.A.txt
python DPLL.py 6queens.cnf Q14 > transcript.6queens.B.txt

python DPLL.py wumpus.cnf -B12 -S12 B21 -S21 > transcript.wumpus.txt

# assumptions
Symbol order is by first appearance in the CNF file
No randomness is used hence results are deterministic
Command-line literals are treated as unit clauses

# model representation
1 = True
-1 = False
0 = Unknown
The program stores truth assignments as a dictionary e.g. model = { symbol: value }

# CNF Format
The CNF files use the simplified ASCII CNF format described in PA2:
Each line represents one clause
Literals are separated by spaces
Clauses are implicitly ORs
The file is an implicit AND of all clauses
A literal beginning with - means NOT
Blank lines and comment lines starting with # are ignored

### DPLL algorithm
	1.	Check clauses
	2.	Unit clause heuristic
	3.	Choose unassigned symbol
	4.	Branch true then false
	5.	Backtrack

Unit Clause Heuristic
If a clause has exactly one unassigned literal that literal must be true.
Symbol Selection Strategy
The solver chooses the next unassigned symbol by scanning for:
The first clause that is unsatisfied and not false
The first unassigned literal in that clause
This reduces early contradictions and improves consistency of results.
