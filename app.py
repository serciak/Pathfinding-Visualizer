import PySide6.QtGui
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QGridLayout, QVBoxLayout, QLabel,
                               QLineEdit, QPushButton, QFileDialog, QAbstractItemView, QListWidget,
                               QMessageBox, QGraphicsView, QGraphicsScene, QComboBox, QSpacerItem)
from PySide6.QtCore import Qt, QEvent, QRectF, QTimer, QSize
from PySide6.QtGui import QPen, QBrush, QIcon
import numpy as np
import algorithms
from maze_generator import MazeGenerator
import time
import math



class PathfindingVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pathfinding Visualizer")
        self.setMinimumSize(930, 635)
        self.resize(1200, 800)
        self.setWindowIcon(QIcon('./icons/path_icon.png'))

        self.rows = 41
        self.cols = 51
        self.board = np.zeros((self.cols, self.rows))
        self.visualization_nodes = np.zeros((self.cols, self.rows))
        self.start_point = None
        self.end_point = None

        self.maze_generator = MazeGenerator(self.board.shape)

        self.central_widget = QWidget()
        central_layout = QHBoxLayout()
        
        self.__init_graphics_view()
        central_layout.addWidget(self.__menu_widget())
        central_layout.addWidget(self.graphics_view)

        self.central_widget.setLayout(central_layout)
        self.setCentralWidget(self.central_widget)


    def __menu_widget(self):
        self.menu_widget = QWidget()
        self.menu_layout = QVBoxLayout()

        self.start_button = QPushButton(icon=QIcon('./icons/start_icon.png'))
        self.start_button.setMinimumSize(120, 50)
        self.start_button.setIconSize(QSize(30, 30))

        self.node_types = QComboBox()
        self.node_types.setMinimumSize(120, 50)
        self.node_types.addItems(['Start point', 'End point', 'Wall'])

        self.node_types.setItemIcon(0, QIcon('./icons/start_point_icon.png'))
        self.node_types.setItemIcon(1, QIcon('./icons/finish_icon.png'))
        self.node_types.setItemIcon(2, QIcon('./icons/wall_icon.png'))
        self.node_types.setIconSize(QSize(20,20))


        self.clear_board_button = QPushButton(icon=QIcon('./icons/bin_icon.png'), text='Clear board')
        self.clear_board_button.setMinimumSize(120, 50)
        self.clear_board_button.setIconSize(QSize(30, 30))

        self.clear_vis_button = QPushButton(icon=QIcon('./icons/broom_icon.png'), text='Clear\nvisualization')
        self.clear_vis_button.setMinimumSize(120, 50)
        self.clear_vis_button.setIconSize(QSize(30, 30))

        self.maze_button = QPushButton(icon=QIcon('./icons/maze_icon.png'))
        self.maze_button.setMinimumSize(120, 50)
        self.maze_button.setIconSize(QSize(30, 30))

        self.start_button.clicked.connect(self.__visualize)
        self.maze_button.clicked.connect(self.__generate_maze)
        self.clear_vis_button.clicked.connect(self.__clear_visualization)
        self.clear_board_button.clicked.connect(self.__clear_board)

        self.menu_layout.addWidget(self.start_button, alignment=Qt.AlignHCenter)
        self.menu_layout.addWidget(self.node_types, alignment=Qt.AlignHCenter)
        self.menu_layout.addWidget(self.clear_board_button, alignment=Qt.AlignHCenter)
        self.menu_layout.addWidget(self.clear_vis_button, alignment=Qt.AlignHCenter)
        self.menu_layout.addWidget(self.maze_button, alignment=Qt.AlignHCenter)

        self.menu_widget.setLayout(self.menu_layout)
        self.menu_widget.setMaximumWidth(250)

        return self.menu_widget
    

    def __generate_maze(self):
        self.__clear_board()
        self.board, history = self.maze_generator.generate()
        self.__maze_generation_visualization(history)

    
    def __maze_generation_visualization(self, history):
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        border = QPen(Qt.black)
        for node in history:
            x, y = node
            color = Qt.white if self.board[x, y] == 0 else Qt.black
            self.__draw_visualization_node(x, y, color, border, brush)
            QApplication.processEvents()
            time.sleep(0)
    

    def __visualize(self):
        self.visualization_nodes = np.zeros((self.cols, self.rows))
        self.__reload_graphic_view()

        try:
            visited, path = algorithms.dijkstra_shortest_path(self.board, self.start_point, self.end_point)
        except Exception as e:
            QMessageBox.information(self, 'Visualization error', str(e))
            return

        border = QPen(Qt.black)

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)

        for node in visited:
            x, y = node
            if (x, y) not in [self.start_point, self.end_point]:
                self.visualization_nodes[x, y] = 4
                self.__draw_visualization_node(x, y, Qt.cyan, border, brush)
                QApplication.processEvents()
                time.sleep(0)

        for node in path:
            x, y = np.unravel_index(node, self.board.shape)
            if (x, y) not in [self.start_point, self.end_point]:
                self.visualization_nodes[x, y] = 5
                self.__draw_visualization_node(x, y, Qt.yellow, border, brush)
                QApplication.processEvents()
                time.sleep(0.01)


    def __draw_visualization_node(self, x, y, color, border, brush):
        step = self.__calculate_row_col_step()
        brush.setColor(color)
        self.graphics_scene.addRect(QRectF(x * step[0], y * step[1], step[0], step[1]), border, brush)

    
    def __clear_visualization(self):
        self.visualization_nodes = np.zeros((self.cols, self.rows))
        self.__reload_graphic_view()


    def __init_graphics_view(self):
        self.graphics_view = QGraphicsView(self.central_widget)
        self.graphics_scene = QGraphicsScene()

        gwidth, gheight = self.__calculate_graphics_view_size()
        self.graphics_view.setFixedSize(gwidth, gheight)

        self.graphics_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.graphics_scene.setBackgroundBrush(Qt.white)

        self.__draw_grid()

        self.graphics_view.setScene(self.graphics_scene)
        self.graphics_view.viewport().installEventFilter(self)
        self.graphics_view.setAlignment(Qt.AlignCenter)

    
    def __clear_board(self):
        self.board = np.zeros((self.cols, self.rows))
        self.__clear_visualization()

        self.start_point = None
        self.end_point = None
        
        self.__reload_graphic_view()


    def __draw_grid(self):
        gwidth, gheight = self.__calculate_graphics_view_size()
        step = self.__calculate_row_col_step()

        for x in range(0, gwidth, step[0]):
            self.graphics_scene.addLine(x, 0, x, gheight, QPen(Qt.black))

        for y in range(0, gheight, step[1]):
            self.graphics_scene.addLine(0, y, gwidth, y, QPen(Qt.black))


    def __reload_graphic_view(self, include_visualization=False):
        gwidth, gheight = self.__calculate_graphics_view_size()
        self.graphics_scene.clear()
        self.graphics_view.setFixedSize(gwidth, gheight)
        print('GV: ', self.graphics_view.width(), self.graphics_view.height())
        print('Window: ', self.width(), self.height())

        self.__draw_grid()
        self.__add_existing_nodes(include_visualization)

#TODO
    def __calculate_graphics_view_size(self):
        #size_param = self.height() if self.graphics_view.height() < self.width() - 200 else self.width() - 200
        #ratio_param = self.rows if self.graphics_view.height() < self.width() - 200 else self.cols

        cell_size = int(math.floor(self.height() / self.rows))
        new_width = cell_size * self.cols
        new_height = cell_size * self.rows

        return new_width, new_height
    

    def __add_existing_nodes(self, include_visualization):
        colors = {0: Qt.white, 1: Qt.black, 2: Qt.green, 3: Qt.red, 4: Qt.cyan, 5: Qt.yellow}
        step = self.__calculate_row_col_step()

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)

        for i, row in enumerate(self.board):
            for j, node in enumerate(row):
                if include_visualization:
                    brush.setColor(colors[self.visualization_nodes[i, j]])
                    self.graphics_scene.addRect(QRectF(i * step[0], j * step[1], step[0], step[1]), QPen(Qt.black), brush)

                if node != 0:
                    brush.setColor(colors[node])
                    self.graphics_scene.addRect(QRectF(i * step[0], j * step[1], step[0], step[1]), QPen(Qt.black), brush)


    def __calculate_row_col_step(self):
        gwidth, gheight = self.__calculate_graphics_view_size()
        w_step = round(gwidth / self.cols, 0)
        h_step = round(gheight / self.rows, 0)

        return (int(w_step), int(h_step))


    def __update_board_matrix(self, x, y, color):
        step = self.__calculate_row_col_step()
        x = int(x / step[0])
        y = int(y / step[1])

        if x >= self.cols or y >= self.rows:
            return False

        if color == Qt.white:
            self.board[x, y] = 0
            if (x, y) == self.start_point:
                self.start_point = None
            if (x, y) == self.end_point:
                self.end_point = None
            return True
        elif self.board[x, y] == 0:
            if color == Qt.black:
                self.board[x, y] = 1
                return True
            if color == Qt.green and not self.start_point:
                self.board[x, y] = 2
                self.start_point = (x, y)
                return True
            if color == Qt.red and not self.end_point:
                self.board[x, y] = 3
                self.end_point = (x, y)
                return True

        return False


    def eventFilter(self, watched, event):
        colors = {'Start point': Qt.green, 'End point': Qt.red, 'Wall': Qt.black}
        gwidth, gheight = self.__calculate_graphics_view_size()
        step = self.__calculate_row_col_step()

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)

        border = QPen(Qt.black)
        color = colors[self.node_types.currentText()]

        if event.type() == QEvent.MouseButtonPress and watched is self.graphics_view.viewport():
            pos = event.position()
            x = pos.x() - (pos.x() % step[0])
            y = pos.y() - (pos.y() % step[1])

            if event.button() == Qt.LeftButton and self.__update_board_matrix(x, y, color):
                brush.setColor(color)
                self.graphics_scene.addRect(QRectF(x, y, step[0], step[1]), border, brush)

            elif event.button() == Qt.RightButton and self.__update_board_matrix(x, y, Qt.white):
                brush.setColor(Qt.white)
                self.graphics_scene.addRect(QRectF(x, y, step[0], step[1]), border, brush)

            self.last = event.button()

        if event.type() == QEvent.MouseMove and watched is self.graphics_view.viewport() and not (self.last == Qt.LeftButton and color in [Qt.green, Qt.red]):
            pos = event.position()
            x = pos.x() - (pos.x() % step[0])
            y = pos.y() - (pos.y() % step[1])
            in_board = x <= gwidth or y <= gheight
            brush.setColor(color) if self.last == Qt.LeftButton else brush.setColor(Qt.white)

            if in_board:
                if self.__update_board_matrix(x, y, brush.color()):
                    self.graphics_scene.addRect(QRectF(x, y, step[0], step[1]), border, brush)

        return QWidget.eventFilter(self, watched, event)
    

    def resizeEvent(self, event):
        self.__reload_graphic_view(include_visualization=True)


if __name__ == '__main__':
    app = QApplication()
    view = PathfindingVisualizer()
    view.show()
    app.exec()


