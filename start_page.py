import pygame, sys, os, subprocess
from gui_widgets import *

pygame.init()
clock = pygame.time.Clock()

WINDOW_SIZE = (1000, 2000/3)
WIDTH = 1000
HEIGHT = 2000/3
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Start Page")

font = pygame.font.SysFont("Arial", 25)

background = pygame.image.load(os.path.join("assets", "start_page_background.png"))
background = pygame.transform.scale(background, WINDOW_SIZE)
start_button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 200, 150, 50)

def draw_start_page():
    
    background_path = os.path.join("assets", "start_page_background2.png")
    background_image = pygame.image.load(background_path)
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    screen.blit(background_image, (0, 0))
    
    pygame.draw.rect(screen, CRIMSON, start_button_rect, border_radius=10)
    font = pygame.font.Font(None, 32)
    start_text = font.render("Start", True, BLACK)
    start_text_rect = start_text.get_rect(center=start_button_rect.center)
    screen.blit(start_text, start_text_rect)

    # Hovering
    if start_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, DARK_GRAY, start_button_rect, border_radius=10, width=3)
        
    pygame.display.flip()

def game_page():
    pygame.quit()  # Close the Pygame window
    # FOR LINUX USERS (HASSAN) CHANGE python WITH python3
    subprocess.call(["python", "game_page.py"])
    sys.exit()  # Exit the current Python script

def main():
    start = True
    
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    start = False

        draw_start_page()
        clock.tick(60)

    # draw_game_page()

if __name__ == "__main__":
    main()