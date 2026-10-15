import sys
import random
import os
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLineEdit, QMainWindow, QPushButton, QGridLayout, QSizePolicy, QStackedWidget, QWidget, QVBoxLayout, QLabel, QMessageBox
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QIcon, QIntValidator, QPixmap

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
        image_path = os.path.join(os.path.dirname(os.fspath(__file__)), "photo", "mole.jpg")
        self.mole_icon = QIcon(image_path)
        self.empty_icon = QIcon()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Whack a Mole Game")
        self.setGeometry(100, 100, 600, 600)
        

        # First page with the buttons to switch game modes.
        self.page1 = QWidget()
        page1_layout = QVBoxLayout()
        self.switch_button = QPushButton("3X3 layout",)
        self.switch_button2 = QPushButton("4X4 layout")
        self.switch_button.clicked.connect(lambda: self.start_game(3))
        self.switch_button2.clicked.connect(lambda: self.start_game(4))

        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("Enter time in seconds")
        self.time_input.setValidator(QIntValidator(1, 300))  

        page1_layout.addWidget(self.time_input)
        page1_layout.addWidget(self.switch_button)
        page1_layout.addWidget(self.switch_button2)
        
        self.page1.setLayout(page1_layout)        
        self.page1.setStyleSheet("background-color: lightblue;")  # Set background color for page1
        self.switch_button.setStyleSheet("background-color: rgb(50, 205, 50); font-size: 16px; padding: 10px; border: 3px solid black;")
        self.switch_button2.setStyleSheet("background-color: rgb(50, 205, 50); font-size: 16px; padding: 10px; border: 3px solid black;")
        self.time_input.setStyleSheet("background-color: rgb(50, 205, 50); font-size: 16px; padding: 10px; border: 3px solid black;")

        # Second page with grid layout for the game.
        self.page2 = QWidget()
        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)


    def start_game(self, size):
        self.value = size
        self.score = 0
        text = self.time_input.text().strip()
        self.time_left = int(text) if text.isdigit() and int(text) > 0 else 30
        print(f"{size}X{size} layout button clicked")
        self.build_grid()
        self.stack.setCurrentWidget(self.page2)
        self.placemole()
        self.mole_timer.start(2500)   # mole moves every "X" miliseconds (1000 = 1 second)
        self.game_timer.start(1000)   # Changes how fast the timer ticks down in miliseconds, base 1000

    def tick(self):
        self.time_left -= 1
        self.time_label.setText(f"Time: {self.time_left}")
        if self.time_left <= 0:
            self.endgame() 

    def build_grid(self):
        # Clears the previous grid and makes a new one based on selected size.
        self.stack.removeWidget(self.page2)
        self.page2.deleteLater()
        self.page2 = QWidget()
        self.stack.addWidget(self.page2)

        page2_layout = QVBoxLayout()

        self.score_label = QLabel(f"Score: {self.score}")
        self.score_label.setStyleSheet(
            "color: black; font-size: 14px; font-weight: bold; "
            "background-color: rgb(50, 205, 50); padding: 4px 8px; border: 3px solid black; border-radius: 4px;"
        )
        self.score_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.score_label.adjustSize()
        self.time_label = QLabel(f"Time: {self.time_left}")
        self.time_label.setStyleSheet(
            "color: black; font-size: 14px; font-weight: bold; "
            "background-color: rgb(50, 205, 50); padding: 4px 8px; border: 3px solid black; border-radius: 4px;"
        )
        self.time_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # back button code
        self.back_button = QPushButton("End Game")
        self.back_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.back_button.clicked.connect(self.back_home)
        self.back_button.setStyleSheet(
            "color: black; font-size: 14px; font-weight: bold; "
            "background-color: rgb(50, 205, 50); padding: 4px 8px; border: 3px solid black; border-radius: 4px;"
        )

        score_bar = QHBoxLayout()
        score_bar.addWidget(self.time_label)    # time on the left
        score_bar.addStretch()                  # pushes the back button to the middle
        score_bar.addWidget(self.back_button)   # time in middle
        score_bar.addStretch()                  # pushes the score to the right
        score_bar.addWidget(self.score_label)   # score on right
        page2_layout.addLayout(score_bar)

        # Creates the grid of buttons based on the selected size (3x3 or 5x5).
        grid_layout = QGridLayout()
        self.buttons = []
        for row in range(self.value):
            for col in range(self.value):
                button = QPushButton(f"(Empty) {row},{col}")
                button.setFixedHeight(80)
                grid_layout.addWidget(button, row, col)
                button.clicked.connect(lambda clicked, r=row, c=col: self.button_click(r, c))
                self.buttons.append(button)
                self.page2.setStyleSheet("background-color: lightgreen;")  # Set background color for page2
                button.setStyleSheet("background-color: lightgreen; font-size: 16px; padding: 10px; border: 3px solid black;")
                self.buttons[-1].setStyleSheet("background-color: rgb(119, 63, 26); font-size: 16px; padding: 10px; border: 3px solid black;")

        page2_layout.addLayout(grid_layout)
        self.page2.setLayout(page2_layout)


    def get_button(self, row, col):
        return self.buttons[row * self.value + col]

    #Code that will determine where the mole is randomly placed in the grid.
    def placemole(self):
        for button in self.buttons:
            button.setText("")
            button.setIcon(self.empty_icon) #No image for the empty button so its just blank
        while True:
            r = random.randint(0, self.value - 1)
            c = random.randint(0, self.value - 1)
            if (r, c) != (self.mole_row, self.mole_col):
                break
        self.mole_row, self.mole_col = r, c
        mole_button = self.get_button(r, c)
        mole_button.setIcon(self.mole_icon)  # Set the mole icon for the button
        mole_button.setIconSize(QSize(64, 64))  # Set the size of the mole icon

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
    def stop_game(self):
        self.mole_timer.stop()
        self.game_timer.stop()
        self.stack.setCurrentWidget(self.page1)

    def endgame(self):
        self.mole_timer.stop()
        self.game_timer.stop()
        QMessageBox.information(self, "Game over", f"Final score: {self.score}")
        self.stack.setCurrentWidget(self.page1)

    def back_home(self):
        self.stop_game()

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    this_window = MyWindow()
    this_window.show()
    sys.exit(app.exec())

