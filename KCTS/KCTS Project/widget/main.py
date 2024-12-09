from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from checkbox import LearniuHCheckBox
from pushbutton import LearniuHPushButton

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        checkBox = LearniuHCheckBox(12)
        button = LearniuHPushButton('nihao',12)
        self.layout.addWidget(button)



if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
