import pygame
import GUI_utilities as ut
from GUI_motion2control import Control
from audio_control import AudioControl

# pygame setup
pygame.init()
screen = pygame.display.set_mode((ut.SCREEN_WIDTH, ut.SCREEN_HEIGHT))
clock = pygame.time.Clock()
# pygame.mouse.set_cursor(*pygame.cursors.ball)
running = True
dt = 0
control = Control()
audio_control = AudioControl()
music_playing = False

# tempo dot variables
dot_x = 200
dot_y = 0
dot_center_x = ut.SCREEN_WIDTH / 2
dot_center_y = ut.SCREEN_HEIGHT / 2

# mouse variables
mouse_x = 0
mouse_y = 0
clicked = False
mouse_text_x = "X: "
mouse_text_y = "    Y: "
mouse_text_motion = "   Mov: "
center_x = '*'
center_y = '*'


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
state = 3
countdown_text = "Music plays in ... "
countdown_time = ut.COUNTDOWN_PERIOD

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
            control.set_prev_pos(pygame.mouse.get_pos())

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # Print center of mouse motion & motion energy
    center_x, center_y = control.center(mouse_x, mouse_y)
    # x
    surface_mouse = font.render(mouse_text_x + str(center_x), True, (255, 255, 255))  # noqa: E501
    screen.blit(surface_mouse, (20, ut.SCREEN_HEIGHT - 30))
    # y
    surface_mouse = font.render(mouse_text_y + str(center_y), True, (255, 255, 255))  # noqa: E501
    screen.blit(surface_mouse, (400, ut.SCREEN_HEIGHT - 30))
    # Motion energy
    motion_energy = control.get_samplerate(mouse_x, mouse_y, dt)
    surface_mouse = font.render(mouse_text_motion + str(motion_energy), True, (255, 255, 255))     # noqa: E501
    screen.blit(surface_mouse, (800, ut.SCREEN_HEIGHT - 30))

    if not clicked:
        for i, surface in enumerate(surfaces):
            screen.blit(surface, (20, 20 + i * 40))
    
    pygame.draw.line(screen, 
                     "blue", 
                     pygame.Vector2(ut.SCREEN_WIDTH / 2, 0),
                     pygame.Vector2(ut.SCREEN_WIDTH / 2, ut.SCREEN_HEIGHT),   # noqa: E501
                     2)
    
    pygame.draw.line(screen, 
                     "blue", 
                     pygame.Vector2(0, ut.SCREEN_HEIGHT / 2),
                     pygame.Vector2(ut.SCREEN_WIDTH, ut.SCREEN_HEIGHT / 2),   # noqa: E501
                     2)
    
    pygame.draw.circle(screen, "white", tempo_dot, 10)

    if clicked:
        if state != 0 and countdown_time > 0:
            surface = font.render(countdown_text + str(state), True, (255, 255, 255))   # noqa: E501
            screen.blit(surface, (20, 20))
            countdown_time -= dt
            if countdown_time <= 0:
                state -= 1
                countdown_time = ut.COUNTDOWN_PERIOD
        if not music_playing and state == 0:
            audio_control.start()
            music_playing = True

        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.circle(screen, "red", pygame.Vector2(mouse_x, mouse_y), 10)

    x, y = ut.calc_cir_pos(dot_x, dot_y, dt)

    if state == 0:
        audio_control.change_speed(motion_energy)

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
