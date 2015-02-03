# encoding:utf-8
LEFT = 155
TOP = 33
GRID_SIZE = 19
GRID_INTERVAL = 19
WIDTH = 19 * 18
RIGHT = LEFT + WIDTH
BOTTOM = TOP + WIDTH


import pygame


class Chessboard(object):
    """description of class"""
    def __init__(self):
        self.font = pygame.font.SysFont("simsunnsimsun", 40)
        self.reset_btn_surface = self.font.render(u'Reset', True, (0,0,0), (155, 155, 155))
        self.reset_btn_location = (10, 10)
        

    def reset(self):
        pass

    def _judge_range(self, x, y):
        if x < LEFT - 10 or y > RIGHT + 10:
            return False
        if y < TOP - 10 or y > BOTTOM + 10:
            return False

        return True
    def draw(self, screen):
        screen.blit(self.reset_btn_surface, self.reset_btn_location)

    def in_range_reset_btn(self, px, py):
        if 0 < px - self.reset_btn_location[0] < self.reset_btn_surface.get_width()\
           and 0 < py - self.reset_btn_location[1] < self.reset_btn_surface.get_height():
            return True
        return False

    def get_stone_index(self, x, y):
        if not self._judge_range(x, y):
            return None, None
        tx = x - LEFT
        ty = y - TOP
        if tx % GRID_INTERVAL > 10:
            rx = tx / GRID_INTERVAL + 1
        else:
            rx = tx / GRID_INTERVAL
        if ty % GRID_INTERVAL > 10:
            ry = ty / GRID_INTERVAL + 1
        else:
            ry = ty / GRID_INTERVAL
        return rx, ry

    def get_pos(self, ix, iy):
        if ix >= GRID_SIZE or iy >= GRID_SIZE:
            return None,None
        px = LEFT + ix * GRID_INTERVAL
        py = TOP + iy * GRID_INTERVAL
        return px, py