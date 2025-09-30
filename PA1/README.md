# Blocksworld A* Search – CSCE 420 PA1

Author: Joey Lim  
File: `blocksworld.py`  
Language: Python 3


## Overview

This program solves the Blocksworld problem using A* search. It reads a `.bwp` file containing an initial and goal block configuration and outputs the sequence to solve it with a heuristic.


## How to Run

```bash
python blocksworld.py <filename> [-H H0|H1|Hbest|H2] [-MAX_ITERS N]
<use H1 or Hbest for my own heuristic>

Limitations
	•	For the heuristic it may over penalise if multiple misplaced characters are in their correct stack but wrong positions
	•	Solves problems up to moderate difficulty; hard problems may fail if MAX_ITERS is exceeded.
	•	Uses Python’s built-in heapq for the priority queue.
