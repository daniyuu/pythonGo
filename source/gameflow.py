# encoding:utf-8
from chessboard import Chessboard
from neural import Neural
BLACK_PLAYER = 1
WHITE_PLAYER = 2
class GameFlow(object):
    """description of class"""
    def __init__(self, black_stone_img, white_stone_img):
        self.chessboard = Chessboard()
        self.neural = Neural(19, 19)
        self.player = BLACK_PLAYER
        self.black_stone_img = black_stone_img
        self.white_stone_img = white_stone_img
        self.winner = None
        self.win_text_surface = None

    def reset(self):
        self.chessboard.reset()
        self.neural.reset()
        self.player = BLACK_PLAYER
        self.winner = None
        self.win_text_surface = None

    def _change_player(self):
        if self.player == BLACK_PLAYER:
            self.player = WHITE_PLAYER
        elif self.player == WHITE_PLAYER:
            self.player = BLACK_PLAYER
        else:
            assert(False)
            self.player = BLACK_PLAYER
            
    def get_player_name(self):
        if self.player == BLACK_PLAYER:
            return 'Black'
        elif self.player == WHITE_PLAYER:
            return 'White'
        else:
            return 'Unknown'

    def _is_win(self, x, y):
        for dir in range(1,5):
            if self.neural.get_connected_count(x,y,dir) >= 5:
                return True
        return False
        
    def update(self, pos):
        px, py = pos
        # update button
        if self.chessboard.in_range_reset_btn(px, py):
            # reset
            self.reset()
            return

        # update go
        if self.winner:
            return
        ix, iy = self.chessboard.get_stone_index(px, py)
        if ix is None or iy is None:
            return
        if self.neural.set_value(ix, iy, self.player):
            if self._is_win(ix, iy):
                self.winner = self.player
                msg = u'%s is winner!' % self.get_player_name()
                self.win_text_surface = self.chessboard.font.render(msg, True, (0,0,0), (255, 255, 255))
            self._change_player()
        

    def _get_img(self, player):
        if player == BLACK_PLAYER:
            return self.black_stone_img
        elif player == WHITE_PLAYER:
            return self.white_stone_img
        else:
            assert(False)
            return None
        
    def get_mouse_cursor(self):
        return self._get_img(self.player)

    def draw(self, screen):
        for w in range(self.neural.width):
            for h in range(self.neural.height):
                value = self.neural.get_value(w,h)
                if not value:
                    continue
                play_img = self._get_img(value)
                x, y = self.chessboard.get_pos(w,h)
                if x is None or y is None:
                    continue

                x-= play_img.get_width() / 2
                y-= play_img.get_height() / 2
                #计算光标的左上角位置
                screen.blit(play_img, (x, y))

        self.chessboard.draw(screen)