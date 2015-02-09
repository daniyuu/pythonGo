# encoding:utf-8
#-------------------------------------------------------------------------------
# Name:        chessboard.py
# Purpose:     definiton of chessboard
#
# Author:      daniyuu
#
# Created:     03/02/2015
# Copyright:   (c) daniyuu 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#定义一些常量
#和铺的图有关系
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
        #设置字体
        #TODO:字体没有被改变显示中文有问题
        self.font = pygame.font.SysFont("testfront.ttf", 40)
        #显示文字 内容|是否开启锯齿|字体颜色|背景色
        self.reset_btn_surface = self.font.render(u'Reset', True, (0,0,0), (155, 155, 155))
        #文字显示位置
        self.reset_btn_location = (10, 10)

    #重启游戏
    def reset(self):
        pass

    #判断(x,y)这个位置是否在棋盘上
    def _judge_range(self, x, y):
        if x < LEFT - 10 or y > RIGHT + 10:
            return False
        if y < TOP - 10 or y > BOTTOM + 10:
            return False
        return True

    #screen.blit(a, loc) 讲a显示在loc的位置上
    def draw(self, screen):
        screen.blit(self.reset_btn_surface, self.reset_btn_location)

    #检测鼠标所指（px,py）是否在reset按钮的有效范围内
    def in_range_reset_btn(self, px, py):
        if 0 < px - self.reset_btn_location[0] < self.reset_btn_surface.get_width()\
           and 0 < py - self.reset_btn_location[1] < self.reset_btn_surface.get_height():
            return True
        return False

    #获取下子位置(rx,ry)
    def get_stone_index(self, x, y):
        #判断合法性
        if not self._judge_range(x, y):
            return None, None

        tx = x - LEFT
        ty = y - TOP
        #print "tx==" + str(tx)
        #print "ty==" + str(ty)
        if tx % GRID_INTERVAL > 10:
            rx = tx / GRID_INTERVAL + 1
        else:
            rx = tx / GRID_INTERVAL
        if ty % GRID_INTERVAL > 10:
            ry = ty / GRID_INTERVAL + 1
        else:
            ry = ty / GRID_INTERVAL

        #print "rx==" + str(rx)
        #print "ry==" + str(ry)
        return rx, ry

    #获取游戏界面的pos 是实时都在刷新的值
    #TODO:函数意义不明
    def get_pos(self, ix, iy):
        #判断合法性
        #print "ix == " + str(ix)
        #print "iy == " + str(iy)
        if ix >= GRID_SIZE or iy >= GRID_SIZE:
            return None,None

        px = LEFT + ix * GRID_INTERVAL
        py = TOP + iy * GRID_INTERVAL

        return px, py