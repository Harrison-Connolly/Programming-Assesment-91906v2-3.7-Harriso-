import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QStackedWidget, QWidget, QVBoxLayout, QLabel, QMessageBox

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Whack a Mole Game")
        self.setGeometry(100, 100, 400, 400)

        # First page with the buttons to switch game modes.
        self.page1 = QWidget()
        page1_layout = QVBoxLayout()
        self.switch_button = QPushButton("3X3 layout",)
        self.switch_button.move(100, 100)
        self.switch_button.clicked.connect(self.show_grid_page)
        print("3X3 layout button created")
        page1_layout.addWidget(self.switch_button)
        self.page1.setLayout(page1_layout)

        #second page with the 3x3 grid layout.
        self.page2 = QWidget()
        grid_layout = QGridLayout()
        self.buttons = []
        for row in range (3):
            for col in range(3):
                btn = QPushButton(f"(Empty) {row},{col}")
                grid_layout.addWidget(btn, row, col)
                btn.clicked.connect(lambda clicked, r=row, c=col: self.button_click(r, c))
        print("3X3 grid layout created")
        self.buttons.append(btn)
        self.page2.setLayout(grid_layout)

        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)

    def show_grid_page(self):
        self.stack.setCurrentWidget(self.page2)

    def button_click(self, row, col):
        print(f"Button clicked at {row}, {col}")
        mole = (random_row, random_col)
        random_row = random.randint(0, 2)
        random_col = random.randint(0, 2)
        if row == random_row and col == random_col:
            QMessageBox.information(self, "Hit!", f"You hit the mole at {row}, {col}!")
        else:
            QMessageBox.information(self, "Miss!", f"You missed! The mole was at {random_row}, {random_col}.")
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    this_window = MyWindow()
    this_window.show()
    sys.exit(app.exec())

