
# Sudoku Solver

This repository contains a Sudoku solver implemented in Python using the Pygame library. The solver uses the AC3 algorithm with Minimum Remaining Values (MRV) and Least Constraining Value (LCV) heuristics to efficiently solve Sudoku puzzles.

## How to Run

To run the Sudoku solver, follow the steps below:

1.  Make sure you have Python installed on your system (Python 3.7 or above is recommended).
    
2.  Install the necessary libraries by running the following command:

```
pip install pygame time

```

3.  Clone this repository to your local machine or download the source code files.
    
4.  Open a terminal or command prompt and navigate to the directory where the source code files are located.
    
5.  Run the  `start_page.py`  file using the following command:
    
```
python start_page.py

```

6.  The Sudoku solver application will open in a new window.

## Dependencies

The following libraries are required to run the Sudoku solver:

-   Python (3.7 or above)
-   Pygame

You can install the necessary libraries using the  `pip`  package manager, as shown in the installation step above.

## Usage

Once you run the  `start_page.py`  file, the Sudoku solver application will open. You can interact with the application using the graphical user interface (GUI). Here are some key features of the application:

-   The Sudoku board will be displayed on the screen, initially empty.
    
-   You can click on a cell to select it, and then use the keyboard to enter a number from 1 to 9.
    
-   The solver will automatically validate the entered number and update the board accordingly.
    
-   To solve the Sudoku puzzle, click the "Solve" button. The solver will attempt to find a solution using the AC3 algorithm with MRV and LCV heuristics.
    
-   If a solution is found, it will be displayed on the board. If no solution is found, an error message will be shown.
    
-   You can clear the board by clicking the "Clear" button.
    
