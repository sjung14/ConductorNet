'''
1. motion energy (ax^2 + ay^2 + az^2) -> sample rate
2. position on screen
    right -> louder volume, left -> smaller volume
    higher -> high pass filter, lower -> low pass filter
'''
import GUI_utilities as ut
import math


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
        self.AVG_ENERGY = (ut.TEMP_DOT_RADIUS
                           * (2 * math.pi / ut.TEMP_DOT_PERIOD)) ** 2

    def set_prev_pos(self, mouse_pos):
        self.__prev_x, self.__prev_y = mouse_pos

    def get_speed(self, x, y, dt):
        '''
        Get sample rate
        Also updates __prev_x & __prev_y
        Minimum 0.5 and Maximum 2.0
        '''
        if dt == 0:
            return 1
        old_x = self.__prev_x
        old_y = self.__prev_y
        self.set_prev_pos((x, y))
        speed = (((x - old_x) / dt)**2 + ((y - old_y) / dt)**2) / self.AVG_ENERGY    # noqa: E501
        return max(0.5, min(speed, 2.0))
    
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
            self.__center_y = ut.SCREEN_HEIGHT / 2 - self.__sum_y / self.__N
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
        

