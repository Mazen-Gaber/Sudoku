import pygame
import random, sys
from gui_widgets import *
from game_page import *
#from sudoku_class import *
import numpy as np

def generate_sudoku_board(difficulty):
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
    board[0][0] = random.randint(1,9)
    solve(board)

    # Remove some numbers to create the puzzle
    if difficulty == "hard": # Adjust the range based on difficulty <- mohemaaa do we need to apply difficulities ?
        empty_cells = random.randint(30, 40)
    elif difficulty == "medium":
        empty_cells = random.randint(40, 50)
    else:
        empty_cells = random.randint(50, 60)
        
    # empty_cells = random.randint(40, 55)  
    
    for _ in range(empty_cells):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        board[row][col] = 0
    return board

def generate_user_board(screen): # Interactive board
    board = [[0 for _ in range(9)] for _ in range(9)]
    selected_cell = None
    begin = False

    while not begin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                selected_cell = get_selected_cell(mouse_x, mouse_y)

                if selected_cell is not None:
                    board[selected_cell[0]][selected_cell[1]] = (board[selected_cell[0]][selected_cell[1]] + 1) % 10
                    
                if clear_board_button_rect.collidepoint(event.pos):
                    screen.fill(LIGHT_GREY)
                    draw_game_page("ai", "interactive")
                    draw_grid()
                    board = [[0 for _ in range(9)] for _ in range(9)]
                    selected_cell = None
                    pygame.display.update()
                    
                if start_game_button_rect.collidepoint(event.pos):
                    begin = True
                    print("begin ", begin)
                    
                        
                        
        draw_grid()
        draw_numbers(board)
        pygame.display.update()
        
    return board

def get_selected_cell(mouse_x, mouse_y):
    if grid_x <= mouse_x < grid_x + GRID_SIZE * CELL_SIZE and grid_y <= mouse_y < grid_y + GRID_SIZE * CELL_SIZE:
        cell_x = int((mouse_x - grid_x) // CELL_SIZE)
        cell_y = int((mouse_y - grid_y) // CELL_SIZE)
        return cell_y, cell_x
    return None

def is_valid(board, row, col):
    number = board[row][col]
    for i in range(9):
        if i != col and board[row][i] == number:
            return False
    for i in range(9):
        if i != row and board[i][col] == number:
            return False
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if (box_row + i != row or box_col + j != col) and board[box_row + i][box_col + j] == number:
                return False
    return True
