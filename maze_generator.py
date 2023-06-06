import random
import numpy as np



class MazeGenerator:
    def __init__(self, board_shape):
        self.h, self.w = board_shape

    def generate(self):
        self.history = []

        self.board = np.ones((self.h, self.w))
        self.board[1:-1,1:-1] = 0

        print(self.w, self.h)
        top_border = [(i, 0) for i in range(self.h)]
        right_border = [(self.h-1, i) for i in range(self.w)]
        bottom_border = [(i, self.w-1) for i in range(self.h)]
        left_border = [(0, i) for i in range(self.w)]
        
        self.history.extend(top_border)
        self.history.extend(right_border)
        self.history.extend(reversed(bottom_border))
        self.history.extend(reversed(left_border))
        
        self.divide(0, 0, self.w, self.h)

        return self.board, self.history

    def divide(self, x, y, w, h):
        random_generator = random.Random()

        orientation = 0
        new_wall = 0
        new_hole = 0
        new_h = 0
        new_w = 0
        y_pair = 0
        x_pair = 0
        new_h_pair = 0
        new_w_pair = 0

        if w < h:
            orientation = 0
        elif w > h:
            orientation = 1
        else:
            orientation = random_generator.randint(0, 1)

        if orientation == 0:
            if h < 5:
                return

            new_wall = y + (random_generator.randint(2, h - 3) // 2) * 2
            new_hole = x + (random_generator.randint(1, w - 2) // 2) * 2 + 1

            for i in range(x, x + w - 1):
                self.board[new_wall, i] = 1
                self.history.append((new_wall, i))
            self.board[new_wall, new_hole] = 0
            self.history.append((new_wall, new_hole))

            new_h = new_wall - y + 1
            new_w = w

            y_pair = new_wall
            x_pair = x
            new_h_pair = y + h - new_wall
            new_w_pair = w
        elif orientation == 1:
            if w < 5:
                return

            new_wall = x + (random_generator.randint(2, w - 3) // 2) * 2
            new_hole = y + (random_generator.randint(1, h - 2) // 2) * 2 + 1
            for i in range(y, y + h - 1):
                self.board[i, new_wall] = 1
                self.history.append((i, new_wall))
            self.board[new_hole][new_wall] = 0
            self.history.append((new_hole, new_wall))

            new_h = h
            new_w = new_wall - x + 1

            y_pair = y
            x_pair = new_wall
            new_h_pair = h
            new_w_pair = x + w - new_wall

        self.divide(x, y, new_w, new_h)
        self.divide(x_pair, y_pair, new_w_pair, new_h_pair)