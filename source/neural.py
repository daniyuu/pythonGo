# encoding:utf-8
class Neural(object):
    """description of class"""
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.mat = []
        for i in range(w * h):
            self.mat.append(0)

    def reset(self):
        for i in range(self.width * self.height):
            self.mat[i] = 0

    def set_value(self, x, y, value):
        t = self.mat[self.width * y + x]
        if t == 0:
            self.mat[self.width * y + x] = value
            return True
        else:
            return False

    def get_value(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        return self.mat[self.width * y + x]

    def _count(self, last_func, next_func, x, y, value):
        result = 1
        pos = [x,y]
        while self._judge_next_connected(pos, value, last_func):
            result+=1
        pos = [x,y]
        while self._judge_next_connected(pos, value, next_func):
            result+=1
        return result

    def _get_left_pos(self, pos):
        if pos[0] == 0:
            return None
        return [pos[0] - 1, pos[1]]

    def _get_right_pos(self, pos):
        if pos[0] == self.width:
            return None
        return [pos[0] + 1, pos[1]]

    def _get_up_pos(self, pos):
        if pos[1] == 0:
            return None
        return [pos[0], pos[1] - 1]

    def _get_down_pos(self, pos):
        if pos[1] == self.height:
            return None
        return [pos[0], pos[1] + 1]

    def _get_up_left_pos(self, pos):
        pos = self._get_left_pos(pos)
        if pos is None:
            return None
        return self._get_up_pos(pos)

    def _get_up_right_pos(self, pos):
        pos = self._get_right_pos(pos)
        if pos is None:
            return None
        return self._get_up_pos(pos)

    def _get_down_left_pos(self, pos):
        pos = self._get_left_pos(pos)
        if pos is None:
            return None
        return self._get_down_pos(pos)

    def _get_down_right_pos(self, pos):
        pos = self._get_right_pos(pos)
        if pos is None:
            return None
        return self._get_down_pos(pos)

    def _judge_next_connected(self, pos, value, get_next_pos):
        ''' 判断下一个是否连上了，如果连上了，将当前位置改为下一个的位置。'''
        if not pos:
            return False
        left = get_next_pos(pos)
        if not left:
            return False
        if self.get_value(left[0], left[1]) == value:
            pos[0], pos[1] = left[0], left[1]
            return True
        else:
            return False


    def get_connected_count(self, x, y, direction):
        ''' direction:
            1: left<->right
            2: up<->down
            3: right-up
            4: right-down
        '''
        value = self.get_value(x, y)
        if not value:
            return 0
        if direction == 1:
            last_get_pos_func = self._get_left_pos
            next_get_pos_func = self._get_right_pos
        elif direction == 2:
            last_get_pos_func = self._get_up_pos
            next_get_pos_func = self._get_down_pos
        elif direction == 3:
            last_get_pos_func = self._get_up_right_pos
            next_get_pos_func = self._get_down_left_pos
        elif direction == 4:
            last_get_pos_func = self._get_up_left_pos
            next_get_pos_func = self._get_down_right_pos
        else:
            return 0
        return self._count(last_get_pos_func, next_get_pos_func, x, y, value)
