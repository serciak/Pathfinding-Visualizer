import PySide6.QtGui
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel,
                               QLineEdit, QPushButton, QFileDialog, QMessageBox, QGraphicsView, QGraphicsScene, QComboBox)
from PySide6.QtCore import Qt, QEvent, QRectF, QSize
from PySide6.QtGui import QPen, QBrush, QIcon, QColor, QPixmap
import numpy as np
import algorithms
from maze_generator import MazeGenerator
import time
import math
from path_finding_visualizer_view import PathfindingVisualizer




class MenuView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pathfinding Visualizer")
        self.setMinimumSize(930, 635)
        self.resize(1200, 800)
        self.setWindowIcon(QIcon('./icons/path_icon.png'))

        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()

        self.central_layout.addWidget(QLabel('PATHFINDING VISUALIZER'))
        self.start_button = QPushButton('START')
        self.start_button.clicked.connect(self.__open_path_finding_visualizer)
        self.central_layout.addWidget(self.start_button)

        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)


    def __open_path_finding_visualizer(self):
        self.pfv_view = PathfindingVisualizer()
        self.close()
        self.pfv_view.show()
        



if __name__ == '__main__':
    app = QApplication()
    view = MenuView()
    view.show()
    app.exec()

