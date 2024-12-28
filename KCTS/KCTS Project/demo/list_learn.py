from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QRadioButton, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建主窗口
        self.setWindowTitle("RadioButton Example")
        self.setGeometry(100, 100, 300, 200)

        # 创建中央小部件和布局
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        # 创建两个 RadioButton
        self.radio_button1 = QRadioButton("Option 1", self)
        self.radio_button2 = QRadioButton("Option 2", self)

        # 创建按钮
        self.button = QPushButton("Print Value", self)
        self.button.clicked.connect(self.print_value)

        # 添加控件到布局
        layout.addWidget(self.radio_button1)
        layout.addWidget(self.radio_button2)
        layout.addWidget(self.button)

        # 设置中央小部件
        self.setCentralWidget(central_widget)

    def print_value(self):
        # 判断哪个 RadioButton 被选中
        if self.radio_button1.isChecked():
            print(1)
        elif self.radio_button2.isChecked():
            print(2)
        else:
            print("No option selected")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
