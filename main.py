from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from menu_view import MenuView


if __name__ == '__main__':
    app = QApplication()
    app.setWindowIcon(QIcon('./icons/path_icon.png'))
    app.setStyle('Fusion')
    view = MenuView()
    view.show()
    app.exec()