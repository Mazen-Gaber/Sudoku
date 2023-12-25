import pygame
import sys
from gui_widgets import *
from gui_utils import *
from sudoku_utils import *
#from sudoku_class import *
import numpy as np
import argparse
import time
from AC3MRVLCVSudokuSolver import AC3MRVLCVSudokuSolver

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
solver = AC3MRVLCVSudokuSolver()
pygame.display.set_caption("Sudoku Solver")
font = pygame.font.SysFont("Arial Black", 25)
font_board = pygame.font.SysFont("Arial", 25)

initial_board = [[0 for _ in range(9)] for _ in range(9)]

def draw_game_page (player, mode):

    screen.fill(LIGHT_GREY)
    bold_underline_font = pygame.font.Font(None, 34)
    bold_underline_font.set_underline(True)
    
    # Start game button
    if mode == "normal":
        pygame.draw.rect(screen, CRIMSON, start_game_button_rect, border_radius=5)
        start_text = font.render("RANDOMIZE", True, BLACK)
        start_text_rect = start_text.get_rect(center=start_game_button_rect.center)
        screen.blit(start_text, start_text_rect)

        # Hovering
        if start_game_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, DARK_GRAY, start_game_button_rect, border_radius=5, width=3)
        
    pygame.draw.rect(screen, CRIMSON, begin_solving_button_rect, border_radius=5)
    begin_text = font.render("SOLVE PUZZLE", True, BLACK)
    begin_text_rect = begin_text.get_rect(center=begin_solving_button_rect.center)
    screen.blit(begin_text, begin_text_rect)
    
    # Hovering
    if begin_solving_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, DARK_GRAY, begin_solving_button_rect, border_radius=5, width=3)
        
    if mode == "interactive":
        pygame.draw.rect(screen, CRIMSON, clear_board_button_rect, border_radius=5)
        clear_text = font.render("CLEAR PUZZLE", True, BLACK)
        clear_text_rect = begin_text.get_rect(center=clear_board_button_rect.center)
        screen.blit(clear_text, clear_text_rect)
    
        # Hovering
        if clear_board_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, DARK_GRAY, clear_board_button_rect, border_radius=5, width=3)
    
    draw_grid()
    pygame.display.update()
    

def draw_grid(): # Function to draw the grid outline of the sudoku board
    grid_background_rect = pygame.Rect(grid_x, grid_y, GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
    pygame.draw.rect(screen, WHITE, grid_background_rect)
    
    for i in range(GRID_SIZE + 1):
        if i % 3 == 0:
            thickness = 4
        else:
            thickness = 1
        pygame.draw.line(screen, BLACK, (grid_x + i * CELL_SIZE, grid_y), (grid_x + i * CELL_SIZE, grid_y + GRID_SIZE * CELL_SIZE), thickness)
        pygame.draw.line(screen, BLACK, (grid_x, grid_y + i * CELL_SIZE), (grid_x + GRID_SIZE * CELL_SIZE, grid_y + i * CELL_SIZE), thickness)

def draw_numbers(grid): # Function to draw numbers on the sudoku board
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] != 0:
                number = font_board.render(str(grid[i][j]), True, BLACK)
                screen.blit(number, (grid_x + j * CELL_SIZE + 25, grid_y + i * CELL_SIZE + 20))
                
                
def draw_number_with_color(number, row, col, color):
    if number != 0:
        number_text = font_board.render(str(number), True, color)
        number_rect = number_text.get_rect()
        number_rect.center = (grid_x + col * CELL_SIZE + CELL_SIZE // 2, grid_y + row * CELL_SIZE + CELL_SIZE // 2)
        screen.blit(number_text, number_rect)
        
def draw_numbers_with_colors(board, aux_board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == 0 and aux_board [i][j] == 0:
                continue
            if board[i][j] != 0 and board[i][j] == aux_board [i][j]:
                draw_number_with_color(aux_board[i][j], i, j, BLACK)
            elif board[i][j] == 0:
                if is_valid(aux_board, i, j):
                    draw_number_with_color(aux_board[i][j], i, j, VIOLET)
                else:
                    draw_number_with_color(aux_board[i][j], i, j, RED)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("player")
    parser.add_argument("difficulty")
    parser.add_argument("mode")
    parser.add_argument("speed")
    args = parser.parse_args()
    print(args.player)
    print(args.difficulty)
    print(args.mode)
    print(args.speed)

    start_game = False
    game_over = False
    
    screen.fill(LIGHT_GREY)
    draw_game_page(args.player, args.mode)
    
    if args.mode == "normal":
        # list
        board = generate_sudoku_board(args.difficulty)
        board = np.array(board).ravel()
    
    elif args.mode == "interactive":
        # list
        board = generate_user_board(screen)
        board = np.array(board).ravel()
        print("board = ", board)
        
    screen.fill(LIGHT_GREY)
    draw_game_page(args.player, args.mode)
    draw_grid()
    draw_numbers(np.array(board).reshape(9,9))
    pygame.display.flip()
    
    while not start_game: # Waiting for the user to start the game
        if args.mode == "interactive":
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 
            
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mouse_x, _ = pygame.mouse.get_pos()
                        
                    if start_game_button_rect.collidepoint(event.pos):
                        board = generate_sudoku_board(args.difficulty)
                        board = np.array(board).ravel()
                        screen.fill(LIGHT_GREY)
                        draw_game_page(args.player, args.mode)
                        draw_grid()
                        draw_numbers(np.array(board).reshape(9,9))
                        pygame.display.flip()
                        
                    if begin_solving_button_rect.collidepoint(event.pos):
                        start_game = True
    
    pygame.display.flip()
    aux_board = np.array(board).reshape(9,9)
    if args.player == "user":
        board = np.array(board).reshape(9,9)
        
    while not game_over: # Game starts
        # Implementations here:
        # 1. Call AI algorithm to solve the board
        # 2. User player : check after each user insertion if the number inserted violates any of the constraints
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    selected_cell = get_selected_cell(mouse_x, mouse_y)
                    
                    if args.player == "user" and selected_cell is not None and board[selected_cell[0]][selected_cell[1]] == 0:
                        aux_board[selected_cell[0]][selected_cell[1]] = (aux_board[selected_cell[0]][selected_cell[1]] + 1) % 10
                        number = aux_board[selected_cell[0]][selected_cell[1]]
                        screen.fill(LIGHT_GREY)
                        draw_game_page(args.player, args.mode)
                        draw_grid()
                        draw_numbers_with_colors(board, aux_board)
                        aux_board_copy = aux_board.reshape(9,9).tolist()
                        solution = solver.solveSudoku(aux_board_copy)
                        if solution:
                            unsolvable1_text = font.render("Solvable Puzzle", True, VIOLET)
                            screen.blit(unsolvable1_text, (60, 180))
                            pygame.display.update()
                        else:
                            unsolvable1_text = font.render("Unsolvable Puzzle", True, RED)
                            screen.blit(unsolvable1_text, (60, 180))
                            pygame.display.update()
                        
        
                # draw_grid()
                # draw_numbers(np.array(aux_board).reshape(9,9))
                pygame.display.update()
                # el modees
                if args.player == "ai" :
                    init_board = board.copy()
                    aux_board = init_board.copy()
                    
                    board = board.reshape(9,9).tolist()
                    
                    start_time = time.time()
                    solution = solver.solveSudoku(board)
                    end_time = time.time()
                    #print("Time taken: " + str(end_time - start_time) * 100)
                    time_text = font.render("Time taken: " + str(end_time - start_time) + " ms", True, DARK_GRAY)
                    screen.blit(time_text, (50, 250))
                    pygame.display.update()
                    
                    board = np.array(board).ravel()
                    # raga3 el board min hina 1d array of ints
                    draw_grid()
                    draw_numbers(np.array(init_board).reshape(9,9))
                    # sudoku variables 
                    # boar
                    if solution:
                        # board_copy = board.copy()
                        # sudoku variables
                        unsolvable1_text = font.render("Puzzle is solvable", True, RED)
                        screen.blit(unsolvable1_text, (50, 180))
                        pygame.display.update()
                        

                        # board awalaneya 1d np array : init_board 81
                        # board gedeeda 1d np array : board 81

                        for i in range(81):
                            screen.fill(LIGHT_GREY)
                            draw_game_page(args.player, args.mode)
                            unsolvable1_text = font.render("Puzzle is solvable", True, RED)
                            screen.blit(unsolvable1_text, (50, 180))
                            pygame.display.update()
                            time_text = font.render("Time taken: {:.3f} ms".format((end_time - start_time) * 1000), True, DARK_GRAY)
                            screen.blit(time_text, (50, 250))
                            pygame.display.update()
                            draw_grid()
                            # draw_numbers(np.array(aux_board).reshape(9,9))
                            draw_numbers_with_colors(np.array(init_board).reshape(9,9), np.array(aux_board).reshape(9,9))
                            if board[i] == init_board[i]:
                                continue
                            aux_board[i] = board[i]
                            draw_number_with_color(aux_board[i], i // 9, i % 9, VIOLET)
                            # draw_numbers_with_colors(np.array(aux_board).reshape(9,9), np.array(board).reshape(9,9))
                            pygame.display.update()
                            pygame.display.flip()
                            time.sleep(int(args.speed)/10)
                            
                        game_over = True
                        # visualize_arcs(sudoku.arcs)
                    else:
                        # no solution
                        print("puzzle is unsolvable")
                        unsolvable_text = font.render("Puzzle is unsolvable!", True, RED)
                        screen.blit(unsolvable_text, (50, 150))
                        game_over = True
                        
        pygame.display.set_caption("Sudoku")
        pygame.display.update()
        pygame.display.flip()
        
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
if __name__ == "__main__":
    main()