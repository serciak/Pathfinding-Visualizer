from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QComboBox)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QFont
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
        font = QFont()
        font.setPointSize(18)

        logo = QLabel()
        logo.setPixmap(QPixmap('./icons/pfv_logo.png'))
        self.central_layout.addWidget(logo, alignment=Qt.AlignCenter)

        buttons_layout = QVBoxLayout()
        start_button = QPushButton('Start')
        start_button.setFont(font)
        start_button.setFixedSize(250, 80)
        start_button.clicked.connect(self.__open_path_finding_visualizer)

        self.board_options = QComboBox()
        self.board_options.setFont(font)
        self.board_options.setFixedSize(250, 80)
        self.board_options.addItems(['Small', 'Medium', 'Large'])
        self.board_options.setItemIcon(0, QIcon('./icons/small_icon.png'))
        self.board_options.setItemIcon(1, QIcon('./icons/mid_icon.png'))
        self.board_options.setItemIcon(2, QIcon('./icons/large_icon.png'))
        self.board_options.setIconSize(QSize(30, 30))
        self.board_options.setCurrentIndex(1)
        self.board_options.setToolTip('Choose board size')
        #self.board_options.setEditable(True)
        #self.board_options.lineEdit().setAlignment(Qt.AlignCenter)
        #self.board_options.lineEdit().setReadOnly(True)

        quit_button = QPushButton('Quit')
        quit_button.setFont(font)
        quit_button.setFixedSize(250, 80)
        quit_button.clicked.connect(self.close)

        buttons_layout.addWidget(start_button, alignment=Qt.AlignCenter)
        buttons_layout.addWidget(self.board_options, alignment=Qt.AlignCenter)
        buttons_layout.addWidget(quit_button, alignment=Qt.AlignCenter)

        buttons_layout.setContentsMargins(0, 50, 0, 50)


        self.central_layout.addLayout(buttons_layout)


    def __open_path_finding_visualizer(self):
        board_sizes = {'Small': (23, 33), 'Medium': (41, 51), 'Large': (65, 79)}
        self.pfv_view = PathfindingVisualizer(*board_sizes[self.board_options.currentText()], self.board_options.currentText())
        self.pfv_view.go_back.connect(self.show)

        self.pfv_view.show()
        self.hide()
