import pygame
import os

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (29, 29, 29)
CRIMSON = (213, 61, 68)
LIGHT_GREY = (237, 232, 226)

WIDTH = 1000
HEIGHT = 2000/3

# Define the grid size
GRID_SIZE = 9
CELL_SIZE = 60

BACKGROUND_IMAGE_PATH = os.path.join("assets", "game_background.png")

# font = pygame.font.SysFont("Arial", 25)

grid_x = (WIDTH - GRID_SIZE * CELL_SIZE) // 2 + 160 
grid_y = (HEIGHT - GRID_SIZE * CELL_SIZE) // 2

strategy_label_x = 50
strategy_label_y = 200

board_x = WIDTH // 2 + 20
board_y = HEIGHT // 2

radiobutton_x = 50
radiobutton_y = strategy_label_y + 40
radiobutton2_y = radiobutton_y + 60

radiobutton_checked_image = pygame.image.load("assets/radiobutton_checked.png")
radiobutton_unchecked_image = pygame.image.load("assets/radiobutton_unchecked.png")
radiobutton_image = radiobutton_unchecked_image
radiobutton2_image = radiobutton_unchecked_image

start_game_button_rect = pygame.Rect(65, radiobutton2_y + 80, 250, 50)
begin_solving_button_rect = pygame.Rect(65, (radiobutton2_y + 80 + 50) + 20, 250, 50)
clear_board_button_rect = pygame.Rect(65, (radiobutton2_y + 80 + 100 + 20) + 20, 250, 50)