# CISC/CMPE 204 Modelling Project for group 6: Pipe Puzzle

This is a game about connecting pipes in a 3x3 grid where the start is at top-left corner on the left of the grid positioned at 11 and end at bottom right corner on the right of the grid positioned at 33 and they are outside the 3x3 grid. The goal of this game is to connect the starting pipe and the ending pipe together by rotating the pipes on the grid to to from a path from the starting pipe to
the ending pipe. 

## Structure
* `documents/final/modelling_report_final.docx`: This will be the documentation we have for the project
* `run.py`: This file contains all the implementation including proposition, constriant, model exploration
    -There are 4 model exploration. And to test them, please uncomment them in "if __name__ == "__main__":"
    -if there is solution, it will show you the what the grid will look like in the form of '([p] @ loc)'
    -if there is no solution, it will just print 'No solution!!'
* `proof.py`: This is a jape proof file which contains the 3 jape proof we did for this project
* `hard_code.py`: This file contains a failed version of project. It contains the BFS hard code(line 315 to 445) and code to generate random grid_setup(line 223 to 256).
* `test.py`: Run this file to confirm that your submission has everything required. This essentially just means it will check for the right files and sufficient theory size.
