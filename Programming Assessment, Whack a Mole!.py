import sys
from PyQt6.QtWidgets import QApplication, QMainWindow

class MyWindow(QMainWindow):
   def __init__(self):
       super().__init__()
       self.initUI()

   def initUI(self):
       self.setWindowTitle("This is a window")
       self.setGeometry(100, 100, 400, 200)

if __name__ == '__main__':
   app = QApplication(sys.argv)
   this_window = MyWindow()
   this_window.show()
   sys.exit(app.exec())

