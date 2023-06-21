from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, 
                               QPushButton, QMessageBox, QGraphicsView, QGraphicsScene, QComboBox)
from PySide6.QtCore import Qt, QEvent, QRectF, QSize, Signal
from PySide6.QtGui import QPen, QBrush, QIcon, QColor, QPixmap
import numpy as np
from pathfinding_algorithms import PathfindingAlgorithms
from maze_generator import MazeGenerator
from board_saving import BoardSaver
from board_saving_window import BoardSavingWindow
import time
import math



class PathfindingVisualizer(QMainWindow):
    go_back = Signal()

    def __init__(self, rows, cols, size):
        super().__init__()
        self.setWindowTitle("Pathfinding Visualizer")
        self.setMinimumSize(930, 635)
        self.resize(1200, 800)
        self.setWindowIcon(QIcon('./icons/path_icon.png'))

        self.rows = rows
        self.cols = cols
        self.board = np.zeros((self.cols, self.rows))
        self.visualization_nodes = np.zeros((self.cols, self.rows))
        self.start_point = None
        self.end_point = None
        self.colors = {'Start point': QColor(52, 168, 83, 255), 
                       'End point': QColor(234, 67, 53, 255), 
                       'Wall': QColor(5, 5, 5, 255),
                       'Visualization': QColor(66, 133, 244, 255),
                       'Path': QColor(251, 188, 5, 255),
                       'Empty': Qt.white}
        self.speed_levels = {'Fast': 0, 'Average': 0.001, 'Slow': 0.0025}

        self.maze_generator = MazeGenerator(self.board.shape)
        self.pf_algorithms = PathfindingAlgorithms()
        self.board_saver = BoardSaver(size)

        self.central_widget = QWidget()
        central_layout = QHBoxLayout()
        
        self.__init_graphics_view()
        central_layout.addWidget(self.__menu_widget())
        central_layout.addWidget(self.graphics_view, alignment=Qt.AlignCenter)

        self.central_widget.setLayout(central_layout)
        self.setCentralWidget(self.central_widget)


    def __menu_widget(self):
        self.menu_widget = QWidget()
        self.menu_layout = QVBoxLayout()

        self.start_button = QPushButton(icon=QIcon('./icons/start_icon.png'))
        self.start_button.setMinimumSize(120, 50)
        self.start_button.setIconSize(QSize(30, 30))
        self.start_button.setToolTip('Start visualization')

        self.algorithms_list = QComboBox()
        self.algorithms_list.setMinimumSize(120, 50)
        self.algorithms_list.addItems(['Dijkstra\'s Algorithm', 'A* Search', 'Depth-First Search'])
        self.algorithms_list.setToolTip('Choose algorithm to visualize')

        self.speed = QComboBox()
        self.speed.setMinimumSize(120, 50)
        self.speed.addItems(self.speed_levels.keys())
        self.speed.setCurrentIndex(0)
        self.speed.setToolTip('Choose speed of visualization')

        self.node_types = QComboBox()
        self.node_types.setMinimumSize(120, 50)
        self.node_types.addItems(['Start point', 'End point', 'Wall'])

        self.node_types.setItemIcon(0, QIcon('./icons/start_point_icon.png'))
        self.node_types.setItemIcon(1, QIcon('./icons/finish_icon.png'))
        self.node_types.setItemIcon(2, QIcon('./icons/wall_icon.png'))
        self.node_types.setIconSize(QSize(20,20))
        self.node_types.setToolTip('Choose node to draw')


        self.clear_board_button = QPushButton(icon=QIcon('./icons/bin_icon.png'), text='Clear board')
        self.clear_board_button.setMinimumSize(120, 50)
        self.clear_board_button.setIconSize(QSize(30, 30))

        self.clear_vis_button = QPushButton(icon=QIcon('./icons/broom_icon.png'), text='Clear\nvisualization')
        self.clear_vis_button.setMinimumSize(120, 50)
        self.clear_vis_button.setIconSize(QSize(30, 30))

        self.maze_button = QPushButton(icon=QIcon('./icons/maze_icon.png'))
        self.maze_button.setMinimumSize(120, 50)
        self.maze_button.setIconSize(QSize(30, 30))
        self.maze_button.setToolTip('Generate maze')

        load_layout = QHBoxLayout()

        self.saved_boards = QComboBox()
        self.saved_boards.setMinimumSize(50, 50)
        self.__update_saved_boards_list()
        self.saved_boards.setCurrentIndex(0)
        self.saved_boards.setToolTip('Choose board to load')

        load_button = QPushButton(icon=QIcon('./icons/load_icon.png'))
        load_button.setMinimumSize(50, 50)
        load_button.setIconSize(QSize(30, 30))
        load_button.setToolTip('Load board')

        load_layout.addWidget(load_button)
        load_layout.addWidget(self.saved_boards)

        save_button = QPushButton(icon=QIcon('./icons/save_icon.png'))
        save_button.setMinimumSize(120, 50)
        save_button.setIconSize(QSize(30, 30))
        save_button.setToolTip('Save current board')

        self.back_button = QPushButton(icon=QIcon('./icons/back_icon.png'))
        self.back_button.setMinimumSize(120, 50)
        self.back_button.setIconSize(QSize(30, 30))
        self.back_button.setToolTip('Go back to menu')

        self.start_button.clicked.connect(self.__visualize)
        self.maze_button.clicked.connect(self.__generate_maze)
        self.clear_vis_button.clicked.connect(self.__clear_visualization)
        self.clear_board_button.clicked.connect(self.__clear_board)
        self.back_button.clicked.connect(self.__on_back_button)
        save_button.clicked.connect(self.__display_board_saving_window)
        load_button.clicked.connect(self.__on_load_button)

        self.menu_layout.addWidget(self.algorithms_list)
        self.menu_layout.addWidget(self.start_button)
        self.menu_layout.addWidget(self.speed)
        self.menu_layout.addWidget(self.node_types)
        self.menu_layout.addWidget(self.clear_board_button)
        self.menu_layout.addWidget(self.clear_vis_button)
        self.menu_layout.addWidget(self.maze_button)
        self.menu_layout.addWidget(save_button)
        self.menu_layout.addLayout(load_layout)
        self.menu_layout.addWidget(self.back_button)

        self.menu_widget.setLayout(self.menu_layout)
        self.menu_widget.setMaximumWidth(250)

        return self.menu_widget
    

    def __update_saved_boards_list(self):
        self.saved_boards.clear()

        boards_list = ['']
        boards_list.extend(self.board_saver.get_boards_names())
        self.saved_boards.addItems(boards_list)


    def __on_back_button(self):
        self.close()
        self.go_back.emit()


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
            color = self.colors['Empty'] if self.board[x, y] == 0 else self.colors['Wall']
            self.__draw_visualization_node(x, y, color, border, brush)
            QApplication.processEvents()
            time.sleep(self.speed_levels[self.speed.currentText()])
    

    def __visualize(self):
        self.algorithm_types = {'Dijkstra\'s Algorithm': self.pf_algorithms.dijkstra_shortest_path, 
                                'A* Search': self.pf_algorithms.astar_shortest_path,
                                'Depth-First Search': self.pf_algorithms.dfs_shortest_path}

        self.visualization_nodes = np.zeros((self.cols, self.rows))
        self.__reload_graphic_view()

        try:
            algorithm = self.algorithm_types[self.algorithms_list.currentText()]
            visited, path = algorithm(self.board, self.start_point, self.end_point)
        except Exception as e:
            self.__display_warning('Visualization error', str(e))
            return

        border = QPen(self.colors['Wall'])

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)

        for node in visited:
            x, y = node
            if (x, y) not in [self.start_point, self.end_point]:
                self.visualization_nodes[x, y] = 4
                self.__draw_visualization_node(x, y, self.colors['Visualization'], border, brush)
                QApplication.processEvents()
                time.sleep(self.speed_levels[self.speed.currentText()])

        for node in path:
            x, y = np.unravel_index(node, self.board.shape)
            if (x, y) not in [self.start_point, self.end_point]:
                self.visualization_nodes[x, y] = 5
                self.__draw_visualization_node(x, y, self.colors['Path'], border, brush)
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
        self.graphics_view.horizontalScrollBar().blockSignals(True)
        self.graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphics_view.verticalScrollBar().blockSignals(True)

        self.graphics_scene.setBackgroundBrush(Qt.white)

        self.__draw_grid()

        self.graphics_view.setScene(self.graphics_scene)
        self.graphics_view.viewport().installEventFilter(self)

    
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

        self.__draw_grid()
        self.__add_existing_nodes(include_visualization)


    def __calculate_graphics_view_size(self):
        cell_size = int(math.floor(self.height() / self.rows))
        new_width = cell_size * self.cols
        new_height = cell_size * self.rows

        return new_width, new_height
    

    def __add_existing_nodes(self, include_visualization):
        node_types = {0: 'Empty', 1: 'Wall', 2: 'Start point', 3: 'End point', 4: 'Visualization', 5: 'Path'}
        step = self.__calculate_row_col_step()

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)

        for i, row in enumerate(self.board):
            for j, node in enumerate(row):
                if include_visualization:
                    node_type = node_types[self.visualization_nodes[i, j]]
                    brush.setColor(self.colors[node_type])
                    self.graphics_scene.addRect(QRectF(i * step[0], j * step[1], step[0], step[1]), QPen(Qt.black), brush)

                if node != 0:
                    node_type = node_types[node]
                    brush.setColor(self.colors[node_type])
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

        if color == self.colors['Empty']:
            self.board[x, y] = 0
            if (x, y) == self.start_point:
                self.start_point = None
            if (x, y) == self.end_point:
                self.end_point = None
            return True
        elif self.board[x, y] == 0:
            if color == self.colors['Wall']:
                self.board[x, y] = 1
                return True
            if color == self.colors['Start point'] and not self.start_point:
                self.board[x, y] = 2
                self.start_point = (x, y)
                return True
            if color == self.colors['End point'] and not self.end_point:
                self.board[x, y] = 3
                self.end_point = (x, y)
                return True

        return False


    def eventFilter(self, watched, event):
        gwidth, gheight = self.__calculate_graphics_view_size()
        step = self.__calculate_row_col_step()

        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)

        border = QPen(Qt.black)
        color = self.colors[self.node_types.currentText()]

        if event.type() == QEvent.MouseButtonPress and watched is self.graphics_view.viewport():
            pos = event.position()
            x = pos.x() - (pos.x() % step[0])
            y = pos.y() - (pos.y() % step[1])

            if event.button() == Qt.LeftButton and self.__update_board_matrix(x, y, color):
                brush.setColor(color)
                self.graphics_scene.addRect(QRectF(x, y, step[0], step[1]), border, brush)

            elif event.button() == Qt.RightButton and self.__update_board_matrix(x, y, self.colors['Empty']):
                brush.setColor(self.colors['Empty'])
                self.graphics_scene.addRect(QRectF(x, y, step[0], step[1]), border, brush)

            self.last = event.button()

        if event.type() == QEvent.MouseMove and watched is self.graphics_view.viewport() and not (self.last == Qt.LeftButton and color in [self.colors['Start point'], self.colors['End point']]):
            pos = event.position()
            x = pos.x() - (pos.x() % step[0])
            y = pos.y() - (pos.y() % step[1])
            in_board = x <= gwidth or y <= gheight
            brush.setColor(color) if self.last == Qt.LeftButton else brush.setColor(self.colors['Empty'])

            if in_board:
                if self.__update_board_matrix(x, y, brush.color()):
                    self.graphics_scene.addRect(QRectF(x, y, step[0], step[1]), border, brush)

        return QWidget.eventFilter(self, watched, event)
    

    def __set_new_minimum_width(self):
        ratio = self.cols / self.rows
        new_min_width = int(round(self.height() * ratio, 0))
        self.setMinimumWidth(new_min_width + 135)


    def resizeEvent(self, event):
        self.__reload_graphic_view(include_visualization=True)
        self.__set_new_minimum_width()


    def __display_warning(self, title, text):
        warn_box = QMessageBox(self)
        warn_box.setIconPixmap(QPixmap('./icons/warning_icon.png'))
        warn_box.setWindowIcon(QIcon('./icons/warning_icon.png'))
        warn_box.setWindowTitle(title)
        warn_box.setText(text)
        warn_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        warn_box.exec()


    def __display_board_saving_window(self):
        self.board_saving_window = BoardSavingWindow()

        self.board_saving_window.save_clicked.connect(self.__on_save_button)

        self.board_saving_window.show()


    def __on_save_button(self):
        name = self.board_saving_window.name_input.text()
        self.board_saver.save_board(name, self.board)
        self.board_saving_window.close()
        self.__update_saved_boards_list()
        self.__reload_graphic_view()


    def __on_load_button(self):
        name = self.saved_boards.currentText()

        if name == '':
            self.__display_warning('Load error', 'Board to load wasn\'t choosen!')
            return
        
        self.__clear_board()
        self.board = self.board_saver.load_board(name)
        self.__reload_graphic_view()