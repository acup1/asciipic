import pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
font = pygame.font.Font(pygame.font.get_default_font(), 36)

# Render the text without using keyword arguments
text_surface = font.render('Hello world', True, (255, 0, 0))  # antialias=True, color=(0, 0, 0)
screen.blit(text_surface, (0, 0))

pygame.display.flip()  # Update the display to show the rendered text

# Keep the window open until it is closed by the user
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
