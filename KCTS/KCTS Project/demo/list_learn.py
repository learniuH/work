from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QListView, QStackedWidget, \
    QLabel, QListWidget, QListWidgetItem
from PyQt5.QtCore import QSize, Qt
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ListView + StackedWidget Demo")
        self.setGeometry(100, 100, 800, 600)

        # 主窗口布局
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # 左侧导航栏 (QListView 或 QListWidget)
        self.list_view = QListWidget()
        self.list_view.setFixedWidth(200)
        self.list_view.setSpacing(10)
        self.list_view.setStyleSheet("background-color: #f0f0f0;")  # 设置背景色

        # 添加导航项
        for i in range(1, 4):
            item = QListWidgetItem(f"Page {i}")
            item.setSizeHint(QSize(180, 40))  # 设置项目高度
            item.setTextAlignment(Qt.AlignCenter)
            self.list_view.addItem(item)

        # 右侧内容区域 (QStackedWidget)
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #ffffff;")

        # 添加页面到 QStackedWidget
        for i in range(1, 4):
            page = QLabel(f"Content for Page {i}")
            page.setAlignment(Qt.AlignCenter)
            page.setStyleSheet("font-size: 20px; color: #333333;")
            self.stacked_widget.addWidget(page)

        # 将 ListView 和 StackedWidget 添加到主布局
        main_layout.addWidget(self.list_view)
        main_layout.addWidget(self.stacked_widget)

        # 连接 ListView 的点击事件到切换页面的槽函数
        self.list_view.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())