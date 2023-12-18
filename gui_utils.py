import pygame
import random, sys
from gui_widgets import *
from game_page import *

def generate_sudoku_board():
    def is_valid(board, row, col, num):
        # Check if the number is not in the current row, column, and 3x3 box
        return (
            all(board[row][c] != num for c in range(9)) and
            all(board[r][col] != num for r in range(9)) and
            all(board[r][c] != num for r in range(row - row % 3, row - row % 3 + 3) for c in range(col - col % 3, col - col % 3 + 3))
        )

    def solve(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            if solve(board):
                                return True
                            board[row][col] = 0  # Backtrack if the current configuration is not valid
                    return False  # No valid number found for this position
        return True  # All positions filled

    board = [[0 for _ in range(9)] for _ in range(9)]
    solve(board)

    # Remove some numbers to create the puzzle
    empty_cells = random.randint(40, 55)  # Adjust the range based on difficulty <- mohemaaa do we need to apply difficulities ?
    for _ in range(empty_cells):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        board[row][col] = 0

    return board

def get_selected_cell(mouse_x, mouse_y):
    if grid_x <= mouse_x < grid_x + GRID_SIZE * CELL_SIZE and grid_y <= mouse_y < grid_y + GRID_SIZE * CELL_SIZE:
        cell_x = int((mouse_x - grid_x) // CELL_SIZE)
        cell_y = int((mouse_y - grid_y) // CELL_SIZE)
        return cell_y, cell_x
    return None