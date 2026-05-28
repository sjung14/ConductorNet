import math
angle = 0

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TEMP_DOT_PERIOD = 0.7
TEMP_DOT_RADIUS = 200    # temp dot orbit radius
COUNTDOWN_PERIOD = 1.5


def calc_cir_pos(x, y, dt):
    global angle
    if dt == 0:
        return x, y
    
    omega = 2 * math.pi / TEMP_DOT_PERIOD
    angle += omega * dt
    x = TEMP_DOT_RADIUS * math.cos(angle)
    y = TEMP_DOT_RADIUS * math.sin(angle)

    if angle > 2 * math.pi:
        angle = 0
    
    return x, y