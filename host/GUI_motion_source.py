import pygame
import GUI_utilities as ut

# pygame setup
pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
# pygame.mouse.set_cursor(*pygame.cursors.ball)
running = True
dt = 0
PERIOD = 0.7

# tempo dot variables
RADIUS = 200
dot_x = 200
dot_y = 0
dot_center_x = SCREEN_WIDTH / 2
dot_center_y = SCREEN_HEIGHT / 2

# mouse variables
mouse_x = 0
mouse_y = 0
clicked = False

# instructions
font = pygame.font.Font(None, 36)
instructions = [
    "Follow the white dot and match its tempo.",
    "Right-click when ready."
]
surfaces = [
    font.render(line, True, (255, 255, 255))
    for line in instructions
]

tempo_dot = pygame.Vector2(
    dot_center_x + dot_x, 
    dot_center_y + dot_y)

while running:       

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif not clicked and event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    if not clicked:
        for i, surface in enumerate(surfaces):
            screen.blit(surface, (20, 20 + i * 40))
    
    pygame.draw.line(screen, 
                     "blue", 
                     pygame.Vector2(SCREEN_WIDTH / 2, 0),
                     pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT),   # noqa: E501
                     2)
    
    pygame.draw.line(screen, 
                     "blue", 
                     pygame.Vector2(0, SCREEN_HEIGHT / 2),
                     pygame.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT / 2),   # noqa: E501
                     2)
    
    pygame.draw.circle(screen, "white", tempo_dot, 10)

    if clicked:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.circle(screen, "red", pygame.Vector2(mouse_x, mouse_y), 10)

    x, y = ut.calc_cir_pos(dot_x, dot_y, RADIUS, dt, PERIOD)

    tempo_dot = pygame.Vector2(
        dot_center_x + x, 
        dot_center_y + y)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
