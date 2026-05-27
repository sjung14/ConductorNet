import math
angle = 0


def calc_cir_pos(x, y, radius, dt, period):
    global angle
    if dt == 0:
        return x, y
    
    omega = 2 * math.pi / period
    angle += omega * dt
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)

    if angle > 2 * math.pi:
        angle = 0
    
    return x, y