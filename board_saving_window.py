from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import Qt, Signal, QRegularExpression


class BoardSavingWindow(QWidget):
    save_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 200)
        self.setWindowTitle('Save current board')
        bs_layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Enter board name')
        regex = QRegularExpression('[A-Z-a-z-0-9_-]+')
        self.name_input.setValidator(QRegularExpressionValidator(regex))
        self.name_input.setMaxLength(15)
        
        self.save_button = QPushButton('Save')
        self.save_button.setFixedSize(85, 30)
        self.save_button.setEnabled(False)

        bs_layout.addWidget(self.name_input)
        bs_layout.addWidget(self.save_button, alignment=Qt.AlignCenter)

        bs_layout.setContentsMargins(30, 50, 30, 30)
        self.setLayout(bs_layout)

        self.name_input.textChanged.connect(self.__on_text_change)
        self.save_button.clicked.connect(self.__on_save_button)


    def __on_text_change(self):
        name = self.name_input.text()
        self.save_button.setEnabled(bool(name))


    def __on_save_button(self):
        self.save_clicked.emit()
