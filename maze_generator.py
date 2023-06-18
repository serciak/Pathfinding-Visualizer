import random
import numpy as np



class MazeGenerator:
    def __init__(self, board_shape):
        self.rows, self.cols = board_shape

    def generate(self):
        self.history = []

        self.board = np.ones((self.rows, self.cols))
        self.board[1:-1,1:-1] = 0

        print(self.cols, self.rows)
        top_border = [(i, 0) for i in range(self.rows)]
        right_border = [(self.rows-1, i) for i in range(self.cols)]
        bottom_border = [(i, self.cols-1) for i in range(self.rows)]
        left_border = [(0, i) for i in range(self.cols)]
        
        self.history.extend(top_border)
        self.history.extend(right_border)
        self.history.extend(reversed(bottom_border))
        self.history.extend(reversed(left_border))
        
        self.divide(0, 0, self.cols, self.rows)

        return self.board, self.history

    def divide(self, x, y, cols, rows):
        random_generator = random.Random()

        orientation = 0
        new_wall = 0
        new_hole = 0
        new_rows = 0
        new_cols = 0
        y_pair = 0
        x_pair = 0
        new_rows_pair = 0
        new_cols_pair = 0

        if cols < rows:
            orientation = 0
        elif cols > rows:
            orientation = 1
        else:
            orientation = random_generator.randint(0, 1)

        if orientation == 0:
            if rows < 5:
                return

            new_wall = y + (random_generator.randint(2, rows - 3) // 2) * 2
            new_hole = x + (random_generator.randint(1, cols - 2) // 2) * 2 + 1

            for i in range(x, x + cols - 1):
                self.board[new_wall, i] = 1
                self.history.append((new_wall, i))
            self.board[new_wall, new_hole] = 0
            self.history.append((new_wall, new_hole))

            new_rows = new_wall - y + 1
            new_cols = cols

            y_pair = new_wall
            x_pair = x
            new_rows_pair = y + rows - new_wall
            new_cols_pair = cols
        elif orientation == 1:
            if cols < 5:
                return

            new_wall = x + (random_generator.randint(2, cols - 3) // 2) * 2
            new_hole = y + (random_generator.randint(1, rows - 2) // 2) * 2 + 1
            for i in range(y, y + rows - 1):
                self.board[i, new_wall] = 1
                self.history.append((i, new_wall))
            self.board[new_hole][new_wall] = 0
            self.history.append((new_hole, new_wall))

            new_rows = rows
            new_cols = new_wall - x + 1

            y_pair = y
            x_pair = new_wall
            new_rows_pair = rows
            new_cols_pair = x + cols - new_wall

        self.divide(x, y, new_cols, new_rows)
        self.divide(x_pair, y_pair, new_cols_pair, new_rows_pair)