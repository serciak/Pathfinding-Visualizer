import PySide6.QtGui
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel,
                               QLineEdit, QPushButton, QComboBox)
from PySide6.QtCore import Qt, QEvent, QRectF, QSize
from PySide6.QtGui import QPen, QBrush, QIcon, QColor, QPixmap
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

        self.__make_central_layout()
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)


    def __make_central_layout(self):
        self.central_layout.addWidget(QLabel('PATHFINDING VISUALIZER'))

        buttons_layout = QHBoxLayout()
        start_button = QPushButton('START')
        start_button.setMinimumSize(120, 50)
        start_button.clicked.connect(self.__open_path_finding_visualizer)

        self.board_options = QComboBox()
        self.board_options.setMinimumSize(120, 50)
        self.board_options.addItems(['Small', 'Medium', 'Large'])
        self.board_options.setCurrentIndex(1)

        buttons_layout.addWidget(start_button)
        buttons_layout.addWidget(self.board_options)

        self.central_layout.addLayout(buttons_layout)


    def __open_path_finding_visualizer(self):
        board_sizes = {'Small': (23, 33), 'Medium': (41, 51), 'Large': (65, 79)}
        self.pfv_view = PathfindingVisualizer(*board_sizes[self.board_options.currentText()])
        
        self.pfv_view.show()
        self.close()
        



if __name__ == '__main__':
    app = QApplication()
    view = MenuView()
    view.show()
    app.exec()

