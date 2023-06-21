import os
import numpy as np
import json

class BoardSaver:
    def __init__(self, board_size):
        self.boards_path = f'./saved_boards/{board_size.lower()}'
        self.__make_boards_path_dirs()


    def __make_boards_path_dirs(self):
        if not os.path.exists(self.boards_path):
            os.makedirs(self.boards_path)


    def get_boards_names(self):
        boards_names = []

        for filename in os.listdir(self.boards_path):
            board_name = os.path.splitext(filename)[0]
            boards_names.append(board_name)

        return boards_names
    

    def save_board(self, name, board):
        board_path = os.path.join(self.boards_path, name + '.json')

        board[board > 1] = 0

        with open(board_path, 'w') as file:
            json.dump(board.tolist(), file)


    def load_board(self, name):
        board_path = os.path.join(self.boards_path, name + '.json')

        with open(board_path, 'r') as file:
            board = json.load(file)

        return np.array(board)