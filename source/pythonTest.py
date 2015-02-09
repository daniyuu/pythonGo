# encoding:utf-8
#-------------------------------------------------------------------------------
# Name:        pythonTest.py
# Purpose:     definiton of chessboard
#
# Author:      daniyuu
#
# Created:     03/02/2015
# Copyright:   (c) daniyuu 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from gameflow import GameFlow

background_image_filename = r'image/Go.jpg'
black_image_filename = r'image/Black.png'
white_image_filename = r'image/White.png'
#指定图像文件名称

import random
import pygame
#导入pygame库
from pygame.locals import *
#导入一些常用的函数和常量
from sys import exit
#向sys模块借一个exit函数用来退出程序

pygame.init()
#初始化pygame,为使用硬件做准备

screen = pygame.display.set_mode((650, 406), 0, 32)
#创建了一个窗口
pygame.display.set_caption("pythonGo")
#设置窗口标题

background = pygame.image.load(background_image_filename).convert()
black_stone = pygame.image.load(black_image_filename).convert_alpha()
white_stone = pygame.image.load(white_image_filename).convert_alpha()
#加载并转换图像

flow = GameFlow(black_stone, white_stone)
mouse_cursor = flow.get_mouse_cursor()
font = pygame.font.SysFont("testfront.ttf", 40)

while True:
#游戏主循环
    flag = False

    for event in pygame.event.get():
        if event.type == QUIT:
            #接收到退出事件后退出程序
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                flow.update(event.pos)
                #print event.pos
                mouse_cursor = flow.get_mouse_cursor()
                flag = True

    screen.blit(background, (0,0))
    #将背景图画上去

    flow.draw(screen)
    x, y = pygame.mouse.get_pos()
    #获得鼠标位置
    x-= mouse_cursor.get_width() / 2
    y-= mouse_cursor.get_height() / 2
    #计算光标的左上角位置
    screen.blit(mouse_cursor, (x, y))
    #把光标画上去

    if flow.winner:
        screen.blit(flow.win_text_surface, (screen.get_width()/2 - flow.win_text_surface.get_width()/2, screen.get_height()/2 - flow.win_text_surface.get_height()/2))

    pygame.display.update()
    #刷新一下画面



    if(flag):
        ix = random.randrange(0,19,1)
        iy = random.randrange(0,19,1)
        flow.play_move(ix,iy)


        mouse_cursor = flow.get_mouse_cursor()

        screen.blit(background, (0,0))
        #将背景图画上去

        flow.draw(screen)
        x, y = pygame.mouse.get_pos()
        #获得鼠标位置
        x-= mouse_cursor.get_width() / 2
        y-= mouse_cursor.get_height() / 2
        #计算光标的左上角位置
        screen.blit(mouse_cursor, (x, y))
        #把光标画上去

        if flow.winner:
            screen.blit(flow.win_text_surface, (screen.get_width()/2 - flow.win_text_surface.get_width()/2, screen.get_height()/2 - flow.win_text_surface.get_height()/2))

        pygame.display.update()
        #刷新一下画面
        flag = False