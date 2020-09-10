# NYT-Sudoku-Solver

## About

This is a simple project I made to as part of a friendly competition with my father. A self-proclaimed New York Times Sudoku whiz, my father put me up to the challenge of completing all 3 of the daily new York Times Sudoku puzzles before he could. Luckily, there was no mention of using a programmative aid in our competion, and hence this project was born

## Technologies

- Python 3.8

This project uses Python Selenium and Chrome Webdriver to read the puzzle board, input the solutions into the website itself, and navigate between all three daily puzzles.
This program implements a forward-checking MRV backtracking algorithm to solve the puzzle.

## Launch
In order to run on your own machine, only the `main.py` and `sudokuLog.txt` files are necessary...the rest were unit tests I had implemented seperately that eventually were all compiled together in `main.py`. By running the "main" method
in `main.py`, the program will initiate a sentient Chrome tab that directs to the "Easy" puzzle of the day, read in the board, solve the board, input the solution to the board on the puzzle website, then navigate to the next hardest puzzle in terms of listed difficulty.
Upon solving all three daily puzzles, the Chrome tab will quit and information will be logged to `sudokuLog.txt`. This information includes:

- A heading with the current date 
- The original, unsolved board of each difficulty
- The solved board of each difficulty
- The time taken to solve each puzzle according to the in-website timer*

*Note: The current `sudokuLog.txt` found in this repo has past trials as an example of formatting. If you intend to use this txt file on your own, feel free to clear the file on your own machine*
