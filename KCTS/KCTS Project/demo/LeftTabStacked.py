from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建 QTableWidget
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(3)
        self.tableWidget.setColumnCount(3)

        # 设置字体以适应长文本显示
        font = QFont("Arial", 10)

        # 创建长文本并插入第一个单元格
        long_text = "This is a very long text that should wrap around within the cell. " \
                    "It should automatically go to the next line when it reaches the end of the cell."
        item1 = QTableWidgetItem(long_text)
        item1.setFont(font)
        item1.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)  # 左上对齐
        item1.setText(item1.text())  # 启用自动换行
        self.tableWidget.setItem(0, 0, item1)

        # 设置第二列的内容（多行文本）
        long_text2 = "Here is another long text. The cell should resize automatically to fit the content."
        item2 = QTableWidgetItem(long_text2)
        item2.setFont(font)
        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)  # 左上对齐
        item2.setText(item2.text())  # 启用自动换行
        self.tableWidget.setItem(1, 1, item2)

        # 设置每行的高度，确保有足够空间显示多行文本
        self.tableWidget.setRowHeight(0, 60)  # 设置第一行高度
        self.tableWidget.setRowHeight(1, 60)  # 设置第二行高度
        self.tableWidget.setRowHeight(2, 60)  # 设置第三行高度

        # 设置列宽，确保文本能完全显示
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 250)

        # 创建布局并添加到主窗口
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.resize(500, 300)
    window.show()
    app.exec_()
