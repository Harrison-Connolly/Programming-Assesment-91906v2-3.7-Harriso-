import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QStackedWidget, QWidget, QVBoxLayout, QLabel, QMessageBox

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

    def initUI(self):
        self.setWindowTitle("Whack a Mole Game")
        self.setGeometry(100, 100, 400, 400)

        # First page with the buttons to switch game modes.
        self.page1 = QWidget()
        page1_layout = QVBoxLayout()
        self.switch_button = QPushButton("3X3 layout",)
        self.switch_button.move(100, 100)
        self.switch_button.clicked.connect(self.show_grid_page)
        page1_layout.addWidget(self.switch_button)
        self.page1.setLayout(page1_layout)

        #second page with the 3x3 grid layout.
        self.page2 = QWidget()
        grid_layout = QGridLayout()
        self.buttons = []
        for row in range (3):
            row_buttons = []
            for col in range(3):
                button = QPushButton(f"({row}, {col})")
                grid_layout.addWidget(button, row, col)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    this_window = MyWindow()
    this_window.show()
    sys.exit(app.exec())

