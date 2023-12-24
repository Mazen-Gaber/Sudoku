import pygame
import sys
from gui_widgets import *
from gui_utils import *
from sudoku_utils import *
from sudoku_class import *
import numpy as np
import argparse
import pyautogui
import time

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Sudoku Solver")
font = pygame.font.SysFont("Arial Black", 25)
font_board = pygame.font.SysFont("Arial", 25)

initial_board = [[0 for _ in range(9)] for _ in range(9)]

def draw_game_page (interactive_mode):
    if interactive_mode == "interactive":
        interactive_mode = True

    screen.fill(LIGHT_GREY)
    bold_underline_font = pygame.font.Font(None, 34)
    bold_underline_font.set_underline(True)
    
    # Start game button
    pygame.draw.rect(screen, CRIMSON, start_game_button_rect, border_radius=5)
    start_text = font.render("START", True, BLACK)
    start_text_rect = start_text.get_rect(center=start_game_button_rect.center)
    screen.blit(start_text, start_text_rect)

    # Hovering
    if start_game_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, DARK_GRAY, start_game_button_rect, border_radius=5, width=3)
        pyautogui.alert("You pressed start!")
    
    if interactive_mode: # Show a begin button in interactive mode
        pygame.draw.rect(screen, CRIMSON, begin_solving_button_rect, border_radius=5)
        begin_text = font.render("SOLVE PUZZLE", True, BLACK)
        begin_text_rect = begin_text.get_rect(center=begin_solving_button_rect.center)
        screen.blit(begin_text, begin_text_rect)
        
        # Hovering
        if begin_solving_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, DARK_GRAY, begin_solving_button_rect, border_radius=5, width=3)
            
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

def generate_user_board(): # Interactive board
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
                    draw_game_page("interactive")
                    draw_grid()
                    board = [[0 for _ in range(9)] for _ in range(9)]
                    selected_cell = None
                    pygame.display.update()
                    
                if begin_solving_button_rect.collidepoint(event.pos):
                    begin = True
                    print("begin ", begin)

        draw_grid()
        draw_numbers(board)
        pygame.display.update()
        
    return board

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
    normal_mode = False
    interactive_mode = False
    
    screen.fill(LIGHT_GREY)
    draw_game_page(args.mode)
    
    while not start_game: # Waiting for the user to start the game
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
                        start_game = True
                        
        # background image
        # background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
        # background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        
        # screen.blit(background_image, (0, 0))
        screen.fill(LIGHT_GREY)
        draw_game_page(args.mode)
        pygame.display.flip()
        
    if args.mode == "normal":
        board = generate_sudoku_board(args.difficulty)
        board = np.array(board).ravel()
        
    elif args.mode == "interactive":
        board = generate_user_board()
        board = np.array(board).ravel()
        print("board = ", board)
        # board = [
        #     2, 0, 9, 0, 0, 0, 6, 0, 0,
        #     0, 4, 0, 8, 7, 0, 0, 1, 2,
        #     8, 0, 0, 0, 1, 9, 0, 4, 0,
        #     0, 3, 0, 7, 0, 0, 8, 0, 1,
        #     0, 6, 5, 0, 0, 8, 0, 3, 0,
        #     1, 0, 0, 0, 3, 0, 0, 0, 7,
        #     0, 0, 0, 6, 5, 0, 7, 0, 9,
        #     6, 0, 4, 0, 0, 0, 0, 2, 0,
        #     0, 8, 0, 3, 0, 1, 4, 5, 0,
        # ]
        
    screen.fill(LIGHT_GREY)
    draw_game_page(args.mode)
    draw_grid()
    draw_numbers(np.array(board).reshape(9,9))
    pygame.display.flip()
    time.sleep(2)
    
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
                    mouse_x, _ = pygame.mouse.get_pos()
                    
        
        sudoku = SudokuCSP(board)
        solution = sudoku.solve()
        draw_grid()
        draw_numbers(np.array(board).reshape(9,9))
        
        if solution is not None:
            board_copy = board.copy()
            for var, value in zip(sudoku.variables, solution):
                screen.fill(LIGHT_GREY)
                draw_game_page(args.mode)
                draw_grid()
                if board_copy[var] == value:
                    continue
                board_copy[var] = value
                draw_numbers(np.array(board_copy).reshape(9,9))
                pygame.display.update()
                pygame.display.flip()
                time.sleep(1)
                
            game_over = True
            # visualize_arcs(sudoku.arcs)
        else:
            # display that ac-3 failed 
            # solve using backtracking 
            pass
        # background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
        # background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        # screen.blit(background_image, (0, 0))
        #screen.fill(LIGHT_GREY)
        #draw_game_page(normal_mode, interactive_mode)

        pygame.display.set_caption("Sudoku Solver")
        pygame.display.update()
        pygame.display.flip()
        
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
if __name__ == "__main__":
    main()