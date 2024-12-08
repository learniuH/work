import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QCheckBox, QStackedWidget, QWidget, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建主窗口的布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 创建一个复选框
        self.checkbox = QCheckBox("显示第二页")
        layout.addWidget(self.checkbox)

        # 创建一个StackedWidget
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # 添加页面到StackedWidget
        page1 = QWidget()
        page1_layout = QVBoxLayout(page1)
        page1_layout.addWidget(QLabel("这是第一页"))

        page2 = QWidget()
        page2_layout = QVBoxLayout(page2)
        page2_layout.addWidget(QLabel("这是第二页"))

        self.stacked_widget.addWidget(page1)
        self.stacked_widget.addWidget(page2)

        # 默认显示第一页
        self.stacked_widget.setCurrentIndex(0)

        # 连接复选框的状态改变信号
        self.checkbox.stateChanged.connect(self.toggle_page)

    def toggle_page(self, state):
        # 如果复选框被选中，显示第二页，否则显示第一页
        if state == 2:  # 2 表示选中状态
            self.stacked_widget.setCurrentIndex(1)
        else:
            self.stacked_widget.setCurrentIndex(0)


# 程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec_())
