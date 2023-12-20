import pygame
import sys
from gui_widgets import *
from gui_utils import *
from sudoku_utils import *
from sudoku_solver import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Sudoku Solver")
font = pygame.font.SysFont("Arial", 25)

initial_board = [[0 for _ in range(9)] for _ in range(9)]

def draw_game_page (interactive_mode):

    bold_underline_font = pygame.font.Font(None, 34)
    bold_underline_font.set_underline(True)

    
    strategy_label = bold_underline_font.render("Game Mode: ", True, BLACK)
    screen.blit(strategy_label, (strategy_label_x, strategy_label_y))
    
    # Radiobuttons
    screen.blit(radiobutton_image, (radiobutton_x, radiobutton_y))
    radiobutton_label1 = font.render("Normal Mode", True, BLACK)
    radiobutton1_label_x = radiobutton_x + radiobutton_image.get_width() + 5
    radiobutton1_label_y = radiobutton_y - (radiobutton_label1.get_height() - radiobutton_image.get_height()) // 2
    screen.blit(radiobutton_label1, (radiobutton1_label_x, radiobutton1_label_y))
    
    screen.blit(radiobutton2_image, (radiobutton_x, radiobutton2_y))
    radiobutton_label2 = font.render("Interactive Mode", True, BLACK)
    radiobutton2_label_x = radiobutton_x + radiobutton2_image.get_width() + 5
    radiobutton2_label_y = (radiobutton2_y) - (radiobutton_label2.get_height() - radiobutton2_image.get_height()) // 2
    screen.blit(radiobutton_label2, (radiobutton2_label_x, radiobutton2_label_y))
    
    # Start game button
    pygame.draw.rect(screen, CRIMSON, start_game_button_rect, border_radius=5)
    start_text = font.render("Start Game", True, BLACK)
    start_text_rect = start_text.get_rect(center=start_game_button_rect.center)
    screen.blit(start_text, start_text_rect)

    # Hovering
    if start_game_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, DARK_GRAY, start_game_button_rect, border_radius=5, width=3)
    
    if interactive_mode: # Show a begin button in interactive mode
        pygame.draw.rect(screen, CRIMSON, begin_solving_button_rect, border_radius=5)
        begin_text = font.render("Solve", True, BLACK)
        begin_text_rect = begin_text.get_rect(center=begin_solving_button_rect.center)
        screen.blit(begin_text, begin_text_rect)

        # Hovering
        if begin_solving_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, DARK_GRAY, begin_solving_button_rect, border_radius=5, width=3)
    
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
                number = font.render(str(grid[i][j]), True, BLACK)
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
                    
                if begin_solving_button_rect.collidepoint(event.pos):
                    begin = True
                    print("begin ", begin)

        draw_grid()
        draw_numbers(board)
        pygame.display.update()
        
    return board

def main():
    start_game = False
    game_over = False
    normal_mode = False
    interactive_mode = False
    global radiobutton_image, radiobutton2_image
    
    screen.fill(LIGHT_GREY)
    draw_game_page(interactive_mode)
    
    while not start_game: # Waiting for the user to choose the mode
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 
            
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mouse_x, _ = pygame.mouse.get_pos()
                        
                    # if radiobutton1 is clicked
                    if radiobutton_x <= mouse_x < radiobutton_x + radiobutton_image.get_width() and radiobutton_y <= mouse_y < radiobutton_y + radiobutton_image.get_height():
                        normal_mode = not normal_mode
                        print("Normal mode: ", normal_mode)
                        radiobutton_image = radiobutton_checked_image if normal_mode else radiobutton_unchecked_image
                        
                        if interactive_mode == True :
                            interactive_mode = not interactive_mode
                            print("Interactive mode: ", interactive_mode)
                            radiobutton2_image = radiobutton_checked_image if interactive_mode else radiobutton_unchecked_image
                        
                        pygame.display.update()  
                        
                    # if radiobutton2 is clicked
                    if radiobutton_x <= mouse_x < radiobutton_x + radiobutton2_image.get_width() and radiobutton2_y <= mouse_y < radiobutton2_y + radiobutton2_image.get_height():
                        interactive_mode = not interactive_mode
                        print("Interactive mode: ", interactive_mode)
                        radiobutton2_image = radiobutton_checked_image if interactive_mode else radiobutton_unchecked_image
                        
                        pygame.display.update() 
                        
                        if  normal_mode == True :
                            normal_mode = not normal_mode
                            print("Normal mode: ", normal_mode)
                            radiobutton_image = radiobutton_checked_image if normal_mode else radiobutton_unchecked_image
                        
                        pygame.display.update()
                        
                    if start_game_button_rect.collidepoint(event.pos):
                        start_game = True
                        
        # background image
        # background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
        # background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        
        # screen.blit(background_image, (0, 0))
        screen.fill(LIGHT_GREY)
        draw_game_page(interactive_mode)
        pygame.display.flip()
        
    if normal_mode:
        board = generate_sudoku_board()
    elif interactive_mode:
        board = generate_user_board()
        solution = solver(board)
        if solution:
            print("Puzzle is SOLVABLE!")
            draw
        else:
            print("Puzzle is NOT SOLVABLE!")
        print(board)
        
    screen.fill(LIGHT_GREY)
    draw_game_page(interactive_mode)
    pygame.display.flip()
    
    while not game_over: # Game starts
        # Implementations here:
        # 1. Call AI algorithm to solve the board
        # 2. Interactive mode: check after each user insertion if the number inserted violates any of the constraints
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mouse_x, _ = pygame.mouse.get_pos()
                    
                        
        # background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
        # background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        # screen.blit(background_image, (0, 0))
        #screen.fill(LIGHT_GREY)
        #draw_game_page(normal_mode, interactive_mode)
        draw_grid()
        draw_numbers(board)

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