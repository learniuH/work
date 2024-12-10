from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QProgressBar, QSpacerItem, QSizePolicy
from checkbox import LearniuHCheckBox
from pushbutton import LearniuHPushButton
from lineedit import LearniuHLineEdit

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout(self)
        checkBox = LearniuHCheckBox(12)
        button = LearniuHPushButton('急停',12)
        lineedit = LearniuHLineEdit(12)

        self.layout.addWidget(checkBox, 0, 0)
        self.layout.addWidget(button, 0, 1)
        self.layout.addWidget(lineedit, 0, 2)

        horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(horizontal_spacer, 0, 3)



if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
