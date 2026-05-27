'''
1. motion energy (ax^2 + ay^2 + az^2) -> sample rate
2. position on screen
    right -> louder volume, left -> smaller volume
    higher -> high pass filter, lower -> low pass filter
'''
import math
import GUI_utilities as ut


class Control:
    def __init__(self):
        self.__prev_x = 0
        self.__prev_y = 0
        self.__N = 100
        self.__buffer = [(0.0, 0.0)] * self.__N
        self.__head = 0
        self.__sum_x = 0  # will be used to calculate center_x
        self.__sum_y = 0  # will be used to calculate center_y
        self.__buf_filled = False
        self.__center_x = '*'   # will be used for filter stabilization
        self.__center_y = '*'   # will be used for filter stabilization

    def set_prev_pos(self, mouse_pos):
        self.__prev_x, self.__prev_y = mouse_pos

    def get_samplerate(self, x, y, dt):
        if dt == 0:
            return 0
        return math.sqrt(((x - self.__prev_x) / dt)**2 + ((y - self.__prev_y) / dt)**2)     # noqa: E501
    
    '''
    The GUI will instruct users to draw a perfect circle with fixed tempo to introduce default sound setting    # noqa: E501
    We __Need to update center so that ...
    TODO: fill this up hahaha
    '''
    def center(self, x, y):
        if self.__buf_filled:
            # Update sum 
            self.__sum_x -= self.__buffer[self.__head][0]
            self.__sum_y -= self.__buffer[self.__head][1]
            self.__sum_x += x
            self.__sum_y += y
            
            # Update center of movement
            self.__center_x = self.__sum_x / self.__N - ut.SCREEN_WIDTH / 2
            self.__center_y = self.__sum_y / self.__N - ut.SCREEN_HEIGHT / 2
        else:
            # Update sum
            self.__sum_x += x
            self.__sum_y += y

            if self.__head == 0:
                self.__buf_filled = True

        # Update __buffer
        self.__buffer[self.__head] = (x, y)
        self.__head = (self.__head + 1) % self.__N
        return self.__center_x, self.__center_y
        

