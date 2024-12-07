from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QHBoxLayout
)
from PyQt5.QtCore import QTimer, Qt
import sys


class TopHintApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Top Hint 提示示例")
        self.resize(400, 200)

        # 主部件和布局
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 按钮：触发提示
        file_not_found_button = QPushButton("模拟 FileNotFoundError")
        file_not_found_button.clicked.connect(self.simulate_file_not_found_error)
        layout.addWidget(file_not_found_button)

        value_error_button = QPushButton("模拟 ValueError")
        value_error_button.clicked.connect(self.simulate_value_error)
        layout.addWidget(value_error_button)

        # 初始化提示框
        self.hint_label = QLabel("", self)
        self.hint_label.setAlignment(Qt.AlignCenter)
        self.hint_label.setStyleSheet(
            "background-color: rgba(255, 0, 0, 180);"  # 半透明红色背景
            "color: white;"                           # 白色字体
            "padding: 10px;"                          # 内边距
            "border-radius: 5px;"                     # 圆角边框
            "font-size: 14px;"
        )
        self.hint_label.setFixedWidth(300)
        self.hint_label.setVisible(False)  # 初始隐藏

    def simulate_file_not_found_error(self):
        """模拟 FileNotFoundError 并显示提示"""
        try:
            raise FileNotFoundError("文件不存在：test.txt")
        except FileNotFoundError as e:
            self.show_top_hint(f"错误: {str(e)}")

    def simulate_value_error(self):
        """模拟 ValueError 并显示提示"""
        try:
            raise ValueError("输入值无效！")
        except ValueError as e:
            self.show_top_hint(f"错误: {str(e)}")

    def show_top_hint(self, message):
        """显示顶部提示框"""
        self.hint_label.setText(message)
        self.hint_label.move(
            self.width() // 2 - self.hint_label.width() // 2,
            20  # 距离顶部20像素
        )
        self.hint_label.setVisible(True)

        # 设置定时器，3秒后隐藏提示框
        QTimer.singleShot(3000, lambda: self.hint_label.setVisible(False))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TopHintApp()
    window.show()
    sys.exit(app.exec_())
