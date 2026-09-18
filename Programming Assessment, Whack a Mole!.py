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
        self.setGeometry(100, 100, 600, 600)

        # First page with the buttons to switch game modes.
        self.page1 = QWidget()
        page1_layout = QVBoxLayout()
        self.switch_button = QPushButton("3X3 layout",)
        self.switch_button2 = QPushButton("5X5 layout")
        self.switch_button.move(100, 100)
        self.switch_button.clicked.connect(self.show_grid_page)
        self.switch_button2.clicked.connect(self.show_grid_page)
        print("3X3 layout button created") 
        page1_layout.addWidget(self.switch_button)
        page1_layout.addWidget(self.switch_button2)
        self.page1.setLayout(page1_layout)

        if self.switch_button.clicked:
            print("3X3 layout button clicked")
            int.value = 3
        elif self.switch_button2.clicked:
            print("5X5 layout button clicked")
            int.value = 5
            print(self.value)

        

        #second page with the 3x3 grid layout.q
        self.page2 = QWidget()
        grid_layout = QGridLayout()
        self.buttons = []
        for row in range ({self.value}):
            for col in range({self.value}):
                button = QPushButton(f"(Empty) {row},{col}")
                grid_layout.addWidget(button, row, col)
                button.clicked.connect(lambda clicked, r=row, c=col: self.button_click(r, c))
                self.buttons.append(button)
        self.page2.setLayout(grid_layout)

        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)
        self.mole_row = None
        self.mole_col = None
    #another page with the 5x5 grid layout

    def show_grid_page(self):
        self.stack.setCurrentWidget(self.page2)
        self.placemole()
    def get_button(self, row, col):
        return self.buttons[row * {self.value} + col]
    def placemole(self):
        for button in self.buttons:
            button.setText("Empty")

        while True:
            new_row = random.randint(0, self.value - 1)
            new_col = random.randint(0, self.value - 1)
            if (new_row, new_col) != (self.mole_row, self.mole_col):
                break
        self.mole_row, self.mole_col = new_row, new_col
        self.get_button(new_row, new_col).setText("Mole")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    this_window = MyWindow()
    this_window.show()
    sys.exit(app.exec())

