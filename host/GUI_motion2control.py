'''
1. motion energy (ax^2 + ay^2 + az^2) -> sample rate
2. position on screen
    right -> louder volume, left -> smaller volume
    higher -> high pass filter, lower -> low pass filter
'''


class Control:
    def __init__(self):
        self.prev_x = 0
        self.prev_y = 0
        self.N = 100
        self.buffer = [(0.0, 0.0)] * self.N
        self.head = 0
        self.sum_x = 0  # will be used to calculate center_x
        self.sum_y = 0  # will be used to calculate center_y
        self.buf_filled = False
        self.center_x = 0   # will be used for filter stabilization
        self.center_y = 0   # will be used for filter stabilization

    def set_prev_pos(x, y, self):
        self.prev_x = x
        self.prev_y = y

    def get_samplerate(x, y, dt, self):
        return ((x - self.prev_x) / dt)**2 + ((y - self.prev_y) / dt)**2
    
    '''
    The GUI will instruct users to draw a perfect circle with fixed tempo to introduce default sound setting
    We need to update center so that ...
    TODO: fill this up hahaha
    '''
    def update_center(x, y, self):
        if self.buf_filled:
            # Update sum 
            self.sum_x -= self.buffer[self.head][0]
            self.sum_y -= self.buffer[self.head][1]
            self.sum_x += x
            self.sum_y += y

            # Update buffer
            self.buffer[self.head] = (x, y)
            head = (head + 1) % self.N
            
            # Update center of movement
            self.center_x = self.sum_x / self.N
            self.center_y = self.sum_y / self.N
        else:
            # Update sum
            self.sum_x += x
            self.sum_y += y

            # Update buffer
            self.buffer[self.head] = (x, y)
            head = (head + 1) % self.N
            if head == 0:
                self.buf_filled = True


    def get_filter(x, y, self):
        
