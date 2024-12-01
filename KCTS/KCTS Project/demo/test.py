# from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QPushButton, QVBoxLayout, QWidget, QTableWidgetItem
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("Dynamic Row Addition with Vertical Header")
#         self.resize(400, 300)
#
#         # 初始化 tableWidget
#         self.tableWidget = QTableWidget(0, 3)  # 初始0行3列
#         self.tableWidget.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])
#
#         # 添加按钮
#         self.button = QPushButton("Add Row")
#         self.button.clicked.connect(self.add_row)
#
#         # 布局设置
#         layout = QVBoxLayout()
#         layout.addWidget(self.tableWidget)
#         layout.addWidget(self.button)
#
#         container = QWidget()
#         container.setLayout(layout)
#         self.setCentralWidget(container)
#
#         # 初始化点击计数
#         self.click_count = 0
#
#     def add_row(self):
#         # 记录点击次数
#         self.click_count += 1
#
#         # 添加新行
#         current_row_count = self.tableWidget.rowCount()
#         self.tableWidget.insertRow(current_row_count)
#
#         # 更新对应的行号为 "点击了n次按钮"
#         self.tableWidget.setVerticalHeaderItem(current_row_count, QTableWidgetItem(f"点击了{self.click_count}次按钮"))
#
# if __name__ == "__main__":
#     app = QApplication([])
#     window = MainWindow()
#     window.show()
#     app.exec_()



from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QProgressBar, QLabel, QWidget
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Centered ProgressBar and Label")
        self.resize(400, 300)

        # 创建垂直方向的 ProgressBar
        self.progressBar = QProgressBar()
        self.progressBar.setOrientation(Qt.Vertical)  # 设置为垂直方向
        self.progressBar.setValue(50)  # 设置进度值

        # 创建 QLabel
        self.label = QLabel("Progress")
        self.label.setAlignment(Qt.AlignCenter)  # 设置文本居中

        # 创建布局
        layout = QGridLayout()
        layout.addWidget(self.progressBar, 0, 0, alignment=Qt.AlignCenter)  # 进度条居中
        layout.addWidget(self.label, 1, 0, alignment=Qt.AlignCenter)  # 标签居中

        # 设置中心窗口小部件
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

