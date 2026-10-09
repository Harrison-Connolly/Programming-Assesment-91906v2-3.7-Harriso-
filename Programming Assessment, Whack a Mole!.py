import sys
import random
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QPushButton, QGridLayout, QSizePolicy, QStackedWidget, QWidget, QVBoxLayout, QLabel, QMessageBox
from PyQt6.QtCore import Qt, QTimer

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
        self.time_left = 30
        self.mole_timer = QTimer(self)
        self.mole_timer.timeout.connect(self.placemole)   # mole will move on its own depending on time
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.tick)

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
        self.time_left = 30
        print(f"{size}X{size} layout button clicked")
        self.build_grid()
        self.stack.setCurrentWidget(self.page2)
        self.placemole()
        self.mole_timer.start(2500)   # mole moves every "X" miliseconds (1000 = 1 second)
        self.game_timer.start(1000)   # Changes how fast the timer ticks down in miliseconds

    def tick(self):
        self.time_left -= 1
        self.time_label.setText(f"Time: {self.time_left}")
        if self.time_left <= 0:
            self.end_game()

    def end_game(self):
        self.mole_timer.stop()
        self.game_timer.stop()
        QMessageBox.information(self, "Game over", f"Final score: {self.score}")
        self.stack.setCurrentWidget(self.page1) 

    def build_grid(self):
        # Clears the previous grid and makes a new one based on size.
        self.stack.removeWidget(self.page2)
        self.page2.deleteLater()
        self.page2 = QWidget()
        self.stack.addWidget(self.page2)

        page2_layout = QVBoxLayout()

        self.score_label = QLabel(f"Score: {self.score}")
        self.score_label.setStyleSheet(
            "color: black; font-size: 14px; font-weight: bold; "
            "background-color: white; padding: 4px 8px; border: 1px solid black; border-radius: 4px;"
        )
        self.score_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.score_label.adjustSize()
        self.time_label = QLabel(f"Time: {self.time_left}")
        self.time_label.setStyleSheet(
            "color: black; font-size: 14px; font-weight: bold; "
            "background-color: white; padding: 4px 8px; border: 1px solid black; border-radius: 4px;"
        )
        self.time_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        score_bar = QHBoxLayout()
        score_bar.addWidget(self.time_label)    # time on the left
        score_bar.addStretch()                  # pushes the score to the right
        score_bar.addWidget(self.score_label)
        page2_layout.addLayout(score_bar)

        # --- Grid of buttons added AFTER the score bar ---
        grid_layout = QGridLayout()
        self.buttons = []
        for row in range(self.value):
            for col in range(self.value):
                button = QPushButton(f"(Empty) {row},{col}")
                button.setFixedHeight(80)   # change 80 to whatever height you want
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
            button.setText(".")
        while True:
            r = random.randint(0, self.value - 1)
            c = random.randint(0, self.value - 1)
            if (r, c) != (self.mole_row, self.mole_col):
                break
        self.mole_row, self.mole_col = r, c
        self.get_button(r, c).setText("Mole")

    #Scoreboard that will go up in value when the mole is hit.
    def button_click(self, row, col):
        if row == self.mole_row and col == self.mole_col:
            print("HIT!")
            self.score += 1
            self.score_label.setText(f"Score: {self.score}")
            print(f"Score: {self.score}")
            self.placemole()  # Place a new mole
            self.mole_timer.start(1000)
        else:
            print("MISS!", self.score)
            self.score_label.setText(f"Score: {self.score}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    this_window = MyWindow()
    this_window.show()
    sys.exit(app.exec())

