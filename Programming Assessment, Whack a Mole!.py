import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QStackedWidget, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.value = 3  # default grid size
        self.score = 0
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

        # Second page with grid layout for the game.
        self.page2 = QWidget()
        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)

    def start_game(self, size):
        self.value = size
        self.score = 0
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

        page2_layout = QVBoxLayout()
        
        self.score_label = QLabel(f"Score: {self.score}")
        page2_layout.addWidget(self.score_label) 
        self.score_label.setStyleSheet("width: 25%; height: 20px; color: black; font-size: 18px; font-weight: bold; background-color: white; border: 1px solid black;")
        page2_layout.addWidget(self.score_label, alignment=Qt.AlignmentFlag.AlignRight)

 #second page with the alternating grid layout.
        grid_layout = QGridLayout()
        self.buttons = []
        for row in range (self.value):
            for col in range(self.value):
                button = QPushButton(f"(Empty) {row},{col}")
                grid_layout.addWidget(button, row, col)
                button.clicked.connect(lambda clicked, r=row, c=col: self.button_click(r, c))
                self.buttons.append(button)

            page2_layout.addLayout(grid_layout)
            self.page2.setLayout(page2_layout)

    def get_button(self, row, col):
        return self.buttons[row * self.value + col]

    #Code that will determine where the mole is randomly placed in the grid.
    def placemole(self):
        for button in self.buttons:
            button.setText("Empty")

        self.mole_row = random.randint(0, self.value - 1)
        self.mole_col = random.randint(0, self.value - 1)
        self.get_button(self.mole_row, self.mole_col).setText("Mole")

    #Scoreboard that will go up in value when the mole is hit.
    def button_click(self, row, col):
        if row == self.mole_row and col == self.mole_col:
            print("HIT!")
            self.score += 1
            self.score_label.setText(f"Score: {self.score}")
            print(f"Score: {self.score}")
            self.placemole()  # Place a new mole
        else:
            print("MISS!", self.score)
            self.score_label.setText(f"Score: {self.score}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    this_window = MyWindow()
    this_window.show()
    sys.exit(app.exec())

