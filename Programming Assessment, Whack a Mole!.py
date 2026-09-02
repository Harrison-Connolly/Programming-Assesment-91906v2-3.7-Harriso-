import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("This is a window")
        self.setGeometry(100, 100, 400, 200)

        self.button1_name = QPushButton("Button 1", self)
        self.button1_name.move(50, 50)
        self.button1_name.clicked.connect(self.button1_click)

    def button1_click(self):
        print("Button 1 was clicked!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    this_window = MyWindow()
    this_window.show()
    sys.exit(app.exec())

