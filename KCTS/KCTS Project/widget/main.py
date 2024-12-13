from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QProgressBar, QSpacerItem, QSizePolicy
from checkbox import LearniuHCheckBox
from pushbutton import LearniuHPushButton
from lineedit import LearniuHLineEdit
from progressbar import LearniuHProgressBar
from slider import LearniuHSlider
from spacer import LearniuHSpacer

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout(self)
        checkBox = LearniuHCheckBox(12)
        button = LearniuHPushButton('急停',12)
        lineedit = LearniuHLineEdit(12)
        progressbar = LearniuHProgressBar(12)
        slider = LearniuHSlider(12)
        spacer = LearniuHSpacer()

        self.layout.addWidget(checkBox, 0, 0)
        self.layout.addWidget(button, 0, 1)
        self.layout.addWidget(lineedit, 0, 2)
        self.layout.addItem(spacer, 0, 3)
        self.layout.addWidget(progressbar, 0, 4)
        self.layout.addWidget(slider, 0, 5)

        horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(horizontal_spacer, 0, 6)



if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
