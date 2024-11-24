from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar
from PyQt5.uic import loadUi

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('test.ui', self)  # 替换为你的 .ui 文件路径

        # 示例：动态设置进度条的值
        self.progressBar.setValue(1200)  # 设置一个示例值，范围应在 minimum 和 maximum 之间
        value = self.progressBar.value() / 100
        self.progressBar.setFormat(f'PWM:{value:.2f}V')

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


