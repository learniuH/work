from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("动态调整行数的 TableWidget")
        self.resize(600, 400)

        # 初始化 TableWidget
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(3)  # 假设有 3 列
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Name", "Age"])

        # 模拟 Excel 数据
        self.excel_data = [
            ["1", "Alice", "23"],
            ["2", "Bob", "30"],
            ["3", "Charlie", "25"],
            ["4", "David", "28"],
            ["5", "Eve", "22"],
            ["6", "Frank", "35"],
            ["7", "Grace", "27"],
            ["8", "Hank", "32"],
            ["9", "Ivy", "29"],
            ["10", "Jack", "26"]
        ]

        # 当前页数和每页行数
        self.current_page = 0
        self.rows_per_page = 0

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 初始化显示
        self.update_table()

    def resizeEvent(self, event):
        """窗口大小变化时触发"""
        super().resizeEvent(event)
        self.update_table()

    def update_table(self):
        """更新表格显示"""
        # 计算适合显示的行数
        table_height = self.tableWidget.viewport().height()  # 表格可视区域高度
        row_height = self.tableWidget.rowHeight(0) if self.tableWidget.rowCount() > 0 else 30  # 默认行高
        header_height = self.tableWidget.horizontalHeader().height()  # 表头高度
        self.rows_per_page = max(1, (table_height - header_height) // row_height)

        # 清空表格
        self.tableWidget.setRowCount(0)

        # 加载当前页数据
        start_row = self.current_page * self.rows_per_page
        end_row = start_row + self.rows_per_page
        for row in range(start_row, min(end_row, len(self.excel_data))):
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            for col, value in enumerate(self.excel_data[row]):
                self.tableWidget.setItem(row - start_row, col, QTableWidgetItem(value))

    def keyPressEvent(self, event):
        """键盘翻页"""
        if event.key() == Qt.Key_Left:  # 上一页
            self.current_page = max(0, self.current_page - 1)
            self.update_table()
        elif event.key() == Qt.Key_Right:  # 下一页
            self.current_page = min((len(self.excel_data) - 1) // self.rows_per_page, self.current_page + 1)
            self.update_table()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()