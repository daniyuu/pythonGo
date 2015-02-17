#!/usr/bin/python
# -*- coding: cp936 -*-

import wx
from Defines import *
import os
import  time

class DragShape:
    def __init__(self, bmp):
        self.bmp = bmp
        self.pos = (0,0)
        self.shown = True
        self.text = None
        self.fullscreen = False

    def HitTest(self, pt):
        rect = self.GetRect()
        return rect.InsideXY(pt.x, pt.y)

    def GetRect(self):
        return wx.Rect(self.pos[0], self.pos[1],
                      self.bmp.GetWidth(), self.bmp.GetHeight())

    def Draw(self, dc, op = wx.COPY):
        if self.bmp.Ok():
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.bmp)

            dc.Blit(self.pos[0], self.pos[1],
                    self.bmp.GetWidth(), self.bmp.GetHeight(),
                    memDC, 0, 0, op, True)

            return True
        else:
            return False

#---------------------------------------------------------------------------
class MainWindow(wx.Frame):
    def __init__(self,parent,id,title):
        self.dirname=''
        wx.Frame.__init__(self, parent, -1, title, size = (600+5,537+46),
                          style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)

#        self.SetSizeHints(600,537)
        self.CentreOnScreen()
        self.SetMaxSize([600+5,537+46])
        #---------------------------------------------------------------------------
        #定义和初始化一些全局的变量
        self.InitValues()
        #---------------------------------------------------------------------------
        #建立菜单
        self.BuildMenu()
        #---------------------------------------------------------------------------
        #建立定时器
        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(200)
        self.Notify()
        #---------------------------------------------------------------------------
        #消息绑定
        self.Bind(wx.EVT_MENU, self.OnNew, id=ID_NEW)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=ID_HELP_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnExit, id=ID_EXIT)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLButtonDown)

        self.Show(1)

    def BuildMenu(self) :
        #---------------------------------------------------------------------------
        #编排一个"游戏"单列菜单的所有项目
        FileMenu = wx.Menu()#建立"游戏"菜单项
        j = 0
        for Item in FileMenuNameList :
            i = FileMenuNameList.index(Item)
            if Item[0] == '' :
                FileMenu.AppendSeparator()
                j = j - 1
            else :
                FileMenu.Append(ID_NEW+i+j,Item[0],Item[1])

        #增加一个能包含整列菜单的菜单栏
        menuBar = wx.MenuBar()
        menuBar.Append(FileMenu,"游戏")
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        #---------------------------------------------------------------------------
        #编排一个单列"帮助"菜单的所有项目
        ToolMenu = wx.Menu()#建立"帮助"菜单项
        j = 0
        for Item in ToolMenuNameList :
            i = ToolMenuNameList.index(Item)
            if Item[0] == '' :
                ToolMenu.AppendSeparator()
                j = j - 1
            else :
                ToolMenu.Append(ID_HELP_ABOUT+i+j,Item[0],Item[1])

        #增加一个能包含整列菜单的菜单栏
        menuBar.Append(ToolMenu,"帮助") # 增加一个"帮助"菜单到菜单栏
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

    def InitValues(self) :
        #------------------cyy---------------------
        self.board = [0 for x in range(15*15)]                 #棋盘状态
        self.last_move_pos = (-1,-1)    #上一步的位置
        self.strings = [0 for x in range(15*15)]               #存储棋盘上的棋串 i->index
        self.string_color = [0 for x in range(15*15)]          #棋串颜色
        self.string_num = [0 for x in range(15*15)]            #棋串上棋子的个数
        self.string_index = [-1 for x in range(15*15)]          #棋串的Index

        #------------------cyy---------------------
        self.m_PpLastPos = (-1,-1)      #玩家走的前一步棋
        self.m_PcLastPos = (-1,-1)      #计算机走的前一步棋
        self.m_bWhoFirst = False        #谁先走，1为电脑先走，0为玩家先走
        self.m_bInit = False            #判断游戏是否是处于刚开始阶段
        self.m_bPlayerWin = False       #判断是否玩家赢
        self.m_bComputerWin = False     #判断是否计算机赢
        self.m_bCTable = []             #棋盘状态记录，原代码中是一个三维数组[15][15][572]
        self.m_iWin = []                #原代码中是一个二维数组[2][572]
        self.m_bPTable = []             #原代码中是一个三维数组[15][15][572]
        self.m_bStart = True            #记录是否开始
        self.m_bPlayer = False          #记录是否轮到玩家
        self.m_bComputer = False        #记录是否轮到计算机
        self.m_iBoard = []
        self.m_BmpBoard = wx.Bitmap('res/board.bmp')                #棋盘背景
        self.m_Bmplastwhitechess = wx.Bitmap('res/lastwhite.bmp')   #白色落子图片
        self.m_Bmplastblackchess = wx.Bitmap('res/lastblack.bmp')   #黑色落子图片
        self.m_Bmpblack = wx.Bitmap('res/black.bmp')
        self.m_Bmpwhitechess = wx.Bitmap('res/whitechess.bmp')      #白色执手图片
        self.m_Bmpblackchess = wx.Bitmap('res/blackchess.bmp')      #黑色执手图片
        #----------------------------------------------------------------
        #判断哪方先开始
        if self.m_bWhoFirst :
            self.m_bPlayer = False
            self.m_bComputer = True
        else :
            self.m_bPlayer = True
            self.m_bComputer = False
        #----------------------------------------------------------------
        #初始化计算机和玩家的获胜组合情况
        self.m_bPTable = [ [ [False] * 572 for x in range(15) ] for x in range(15) ]
        self.m_bCTable = [ [ [False] * 572 for x in range(15) ] for x in range(15) ]
        self.m_iWin = [ [0] * 572 for x in range(2) ]
        self.m_iBoard = [ [2] * 15 for x in range(15) ]

        count = 0
        for i in range(15) :
            for j in range(11) :
                for k in range(5) :
                    self.m_bPTable[j+k][i][count]=True
                    self.m_bCTable[j+k][i][count]=True
                    k+=1
                count += 1

        for i in range(15) :
            for j in range(11) :
                for k in range(5) :
                    self.m_bPTable[i][j+k][count]=True
                    self.m_bCTable[i][j+k][count]=True
                    k+=1
                count += 1

        for i in range(11) :
            for j in range(11) :
                for k in range(5) :
                    self.m_bPTable[j+k][i+k][count]=True
                    self.m_bCTable[j+k][i+k][count]=True
                    k+=1
                count += 1

        for i in range(11) :
            j = 14
            while j >= 4 :
                for k in range(5) :
                    self.m_bPTable[j-k][i+k][count]=True
                    self.m_bCTable[j-k][i+k][count]=True
                    k+=1
                count += 1
                j-=1

    def OnLButtonDown(self,event) :
        if self.m_bPlayer and event.m_x <= 535 and event.m_y <= 535 :     #判断是否在有效区域
            tx=x=event.m_x-24
            ty=y=event.m_y-25
            while tx >= 36 :
                tx-=36
            while ty >= 36 :
                ty-=36
            tx+=x/36
            ty+=y/36
            if tx > 18 :
                x=x/36+1
            else :
                x=x/36
            if ty > 18 :
                y=y/36+1
            else :
                y=y/36
            if self.m_iBoard[x][y] == 2 :
                self.m_iBoard[x][y]=0                #设为玩家的棋子
                if self.m_PpLastPos[0] != -1 and self.m_PpLastPos[1] != -1 :
                    if not self.m_bWhoFirst :
                        self.DrawWhiteChess(self.m_PpLastPos[0],self.m_PpLastPos[1])
                    else :
                        self.DrawBlackChess(self.m_PpLastPos[0],self.m_PpLastPos[1])
                if not self.m_bWhoFirst :
                    self.DrawNowWhite(x,y)
                else :
                    self.DrawNowBlack(x,y)
                self.m_PpLastPos = (x,y)
                i = 0
                while i < 572 :         #修改玩家下子后棋盘状态的变化
                    if i == 80 :
                        i = 80
                    if self.m_bPTable[x][y][i] and self.m_iWin[0][i] != 7 :
                        self.m_iWin[0][i] += 1
                    if self.m_bCTable[x][y][i] :
                        self.m_bCTable[x][y][i] = False
                        self.m_iWin[1][i]=7
                    i+=1
                self.m_bPlayer = False
                self.m_bComputer = True

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.TileBackground(dc)
        for i in range(15) :
            for j in range(15) :
                if self.m_iBoard[i][j] == 0 :#玩家的棋子
                    if self.m_PpLastPos[0] == i and self.m_PpLastPos[1] == j :
                        if not self.m_bWhoFirst :
                            self.DrawNowWhite(self.m_PpLastPos[0],self.m_PpLastPos[1])
                        else :
                            self.DrawNowBlack(self.m_PpLastPos[0],self.m_PpLastPos[1])
                        continue
                    if not self.m_bWhoFirst :
                        self.DrawWhiteChess(i,j)
                    else :
                        self.DrawBlackChess(i,j)

                if self.m_iBoard[i][j] == 1 :#计算机的棋子
                    if self.m_PcLastPos[0] == i and self.m_PcLastPos[1] == j :
                        if not self.m_bWhoFirst :
                            self.DrawNowBlack(self.m_PcLastPos[0],self.m_PcLastPos[1])
                        else :
                            self.DrawNowWhite(self.m_PcLastPos[0],self.m_PcLastPos[1])
                        continue

                    if not self.m_bWhoFirst :
                        self.DrawBlackChess(i,j);
                    else :
                        self.DrawWhiteChess(i,j);

    def TileBackground(self, dc):
        sz = self.GetClientSize()
        w = self.m_BmpBoard.GetWidth()
        h = self.m_BmpBoard.GetHeight()

        x = 0

        while x < sz.width:
            y = 0

            while y < sz.height:
                dc.DrawBitmap(self.m_BmpBoard, x, y)
                y = y + h

            x = x + w

    def IsWin(self) :
        for i in range(572) :
            if self.m_iWin[0][i] == 5 :
                self.m_bPlayerWin = True
                break
            if self.m_iWin[1][i] == 5 :
                self.m_bComputer = True
                break

    def Notify(self):
        self.IsWin()
        if self.m_bPlayerWin :
            time.Stop()
            d = wx.MessageDialog(self,"恭喜，您真厉害!","惊讶中……",wx.OK)
            d.ShowModal()
            d.Destroy()
            self.m_bPlayerWin = False
            self.m_bComputer = False
            self.m_bInit = True
        elif self.m_bComputerWin :
            time.Stop()
            d = wx.MessageDialog(self,"啊哈！您输了!","开心中……",wx.OK)
            d.ShowModal()
            d.Destroy()
            self.m_bPlayerWin = False
            self.m_bComputer = False
            self.m_bInit = True
        else :
            if self.m_bComputer :
                self.ComTurn()

    def SearchBlank(self,Nowboard,List=None) :
        for x in range(15):
            for y in range(15):
                if Nowboard[x][y] == 2:
                    List[0] = x
                    List[1] = y
                    return 1
        return 0

    def ComTurn(self) :
        temp1 = [-1]*20
        temp2 = [-1]*20
        tmpList = [0,0]
        cscore=-10000
        ctempboard = [[0]*15 for x in range(15)]
        ptempboard = [[0]*15 for x in range(15)]
        if self.m_bStart :
            if self.m_iBoard[7][7] == 2 :
                bestx=7
                besty=7
            else :
                bestx=8
                besty=8
            self.m_bStart = False
        else :#寻找最佳位置
            for i in range(15) :
                for j in range(15) :
                    ctempboard[i][j]=self.m_iBoard[i][j]

            while self.SearchBlank(ctempboard,tmpList) == True:
                i = tmpList[0]
                j = tmpList[1]
                n=0
                pscore=10
                for k in range(15) :
                    for l in range(15) :
                        ptempboard[k][l]=self.m_iBoard[k][l]
                ctempboard[i][j] = 3      #标记已被查找
                ctemp = self.GiveScore(1,i,j)
                for m in range(572) : #暂时更改玩家信息
                    if self.m_bPTable[i][j][m] :
                        temp1[n]=m
                        self.m_bPTable[i][j][m] = False
                        temp2[n]=self.m_iWin[0][m]
                        self.m_iWin[0][m]=7
                        n+=1
#                print ctempboard
                ptempboard[i][j]=1
                pi=i
                pj=j
                while self.SearchBlank(ptempboard,tmpList) == True:
                    i = tmpList[0]
                    j = tmpList[1]
#                    print ('i=%d j=%d n=%d' % (i,j,n))
                    ptempboard[i][j]=3          #标记已被查找
                    ptemp=self.GiveScore(0,i,j)
#                    print ptempboard
                    if pscore > ptemp : #此时为玩家下子，运用极小极大法时应选取最小值
                        pscore=ptemp
                for m in range(n) :    #恢复玩家信息
                    self.m_bPTable[pi][pj][temp1[m]] = True
                    self.m_iWin[0][temp1[m]] = temp2[m]
                if ctemp+pscore > cscore :  #此时为计算机下子，运用极小极大法时应选取最最大值
                    cscore=ctemp+pscore
#                    print ('%f,%f,%f' %(ctemp,pscore,cscore))
                    bestx=pi
                    besty=pj

        self.m_iBoard[bestx][besty]=1
        if self.m_PcLastPos[0] != -1 and self.m_PcLastPos[1] != -1 :    #画前一棋子
            if not self.m_bWhoFirst :
                self.DrawBlackChess(self.m_PcLastPos[0],self.m_PcLastPos[1])
            else :
                self.DrawWhiteChess(self.m_PcLastPos[0],self.m_PcLastPos[1])

        if not self.m_bWhoFirst :
            self.DrawNowBlack(bestx,besty)
        else :
            self.DrawNowWhite(bestx,besty)
        self.m_PcLastPos = (bestx,besty)
        for i in range(572) :   #修改计算机下子后，棋盘的变化状况
            if self.m_bCTable[bestx][besty][i] and self.m_iWin[1][i] != 7 :
                self.m_iWin[1][i] += 1
            if self.m_bPTable[bestx][besty][i] :
                self.m_bPTable[bestx][besty][i]=False
                self.m_iWin[0][i]=7
        self.m_bComputer = False
        self.m_bPlayer = True

    def GiveScore(self,type,x,y) :
        score = 0
        for i in range(572) :#计算机下
            if type == 1 :
                if self.m_bCTable[x][y][i] :
                    if self.m_iWin[1][i] == 1 :
                        score+=5
                    elif self.m_iWin[1][i] == 2 :
                        score+=50
                    elif self.m_iWin[1][i] == 3 :
                        score+=100
                    elif self.m_iWin[1][i] == 4 :
                        score+=10000
            else:#人下
                if self.m_bPTable[x][y][i] :
                    if self.m_iWin[0][i] == 1 :
                        score-=5
                    elif self.m_iWin[0][i] == 2 :
                        score-=50
                    elif self.m_iWin[0][i] == 3 :
                        score-=500
                    elif self.m_iWin[0][i] == 4 :
                        score-=5000
        return score

    def DrawNowWhite(self,x,y,dc=None) :
        if dc == None :
            dc = wx.ClientDC(self)

        memDC = wx.MemoryDC()
        memDC.SelectObject(self.m_Bmpblack)
        dc.Blit(24+x*36-x-18,25+y*36-y-18,33,33,memDC, 0, 0, wx.OR_INVERT, True)
        memDC.SelectObject(self.m_Bmplastwhitechess)
        dc.Blit(24+x*36-x-18,25+y*36-y-18,33,33,memDC, 0, 0, wx.AND, True)

    def DrawNowBlack(self,x,y,dc=None) :
        if dc == None :
            dc = wx.ClientDC(self)

        memDC = wx.MemoryDC()
        memDC.SelectObject(self.m_Bmpblack)
        dc.Blit(24+x*36-x-18,25+y*36-y-18,33,33,memDC, 0, 0, wx.OR_INVERT, True)
        memDC.SelectObject(self.m_Bmplastblackchess)
        dc.Blit(24+x*36-x-18,25+y*36-y-18,33,33,memDC, 0, 0, wx.AND, True)

    def DrawWhiteChess(self,x,y,dc=None) :
        if dc == None :
            dc = wx.ClientDC(self)

        memDC = wx.MemoryDC()
        memDC.SelectObject(self.m_Bmpblack)
        dc.Blit(24+x*36-x-18,25+y*36-y-18,33,33,memDC, 0, 0, wx.OR_INVERT, True)
        memDC.SelectObject(self.m_Bmpwhitechess)
        dc.Blit(24+x*36-x-18,25+y*36-y-18,33,33,memDC, 0, 0, wx.AND, True)

    def DrawBlackChess(self,x,y,dc=None) :
        if dc == None :
            dc = wx.ClientDC(self)

        memDC = wx.MemoryDC()
        memDC.SelectObject(self.m_Bmpblack)
        dc.Blit(24+x*36-x-18,25+y*36-y-18,33,33,memDC, 0, 0, wx.OR_INVERT, True)
        memDC.SelectObject(self.m_Bmpblackchess)
        dc.Blit(24+x*36-x-18,25+y*36-y-18,33,33,memDC, 0, 0, wx.AND, True)

    def OnNew(self,e):
        self.InitValues()
        self.Refresh()

    def OnAbout(self,e):
        d= wx.MessageDialog( self, "参考：一个网络上用VC编写的开源五子棋程序。\n移植：jawbreaker \nEmail：jawbreaker@163.com","关于Python开源版的简易五子棋", wx.OK)
                            # Create a message dialog box
        d.ShowModal() # Shows it
        d.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close()  # Close the frame.

#---------------------------------------------------------------------------


#---------------------------------------------------------------------------

def main():
    app = wx.PySimpleApp()
    frame = MainWindow(None, -1, "简易五子棋")
    frame.Show(1)
    app.MainLoop()


#---------------------------------------------------------------------------

#----------------------------------------------------------------------------

if __name__ == '__main__':
    main()

#----------------------------------------------------------------------------
