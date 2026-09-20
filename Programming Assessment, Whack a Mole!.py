from ast import While
import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QStackedWidget, QWidget, QVBoxLayout, QLabel, QMessageBox

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.value = 3  # default grid size
        self.buttons = []
        self.mole_row = None
        self.mole_col = None

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
        self.switch_button.clicked.connect(lambda: self.start_game(3))
        self.switch_button2.clicked.connect(lambda: self.start_game(5))
        print("3X3 layout button created") 
        page1_layout.addWidget(self.switch_button)
        page1_layout.addWidget(self.switch_button2)
        self.page1.setLayout(page1_layout)        

        self.page2 = QWidget()
        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)

    def start_game(self, size):
        self.value = size
        self.show_grid_page
        print(f"{size}X{size} layout button clicked")
        self.build_grid()
        self.stack.setCurrentWidget(self.page2)
        self.placemole()

    def build_grid(self):
    # removes buttons from the previous game.
        old_layout = self.page2.layout()
        if old_layout is not None:
            while old_layout.count():
                item = old_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            QWidget().setLayout(old_layout)

 #second page with the 3x3 grid layout.q
        grid_layout = QGridLayout()
        self.buttons = []
        for row in range ({self.value}):
            for col in range({self.value}):
                button = QPushButton(f"(Empty) {row},{col}")
                grid_layout.addWidget(button, row, col)
                button.clicked.connect(lambda clicked, r=row, c=col: self.button_click(r, c))
                self.buttons.append(button)
        self.page2.setLayout(grid_layout)
    def get_button(self, row, col):
        return self.buttons[row * self.value + col]

    def placemole(self):
        for button in self.buttons:
            button.setText("Empty")
    While True:
        self.mole_row = random.randint(0, self.value - 1)
        self.mole_col = random.randint(0, self.value - 1)
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    this_window = MyWindow()
    this_window.show()
    sys.exit(app.exec())

