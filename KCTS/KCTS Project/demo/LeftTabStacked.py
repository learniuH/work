from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QStyledItemDelegate
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

class SelectionBorderDelegate(QStyledItemDelegate):
    """ 自定义委托，仅在选区外圈绘制边框 """
    def paint(self, painter, option, index):
        super().paint(painter, option, index)

        table = option.widget
        selection_model = table.selectionModel()
        if not selection_model.isSelected(index):
            return

        # 获取所有选中的索引
        selected_indexes = selection_model.selectedIndexes()
        if not selected_indexes:
            return

        # 计算选区的最小/最大行列
        min_row = min(index.row() for index in selected_indexes)
        max_row = max(index.row() for index in selected_indexes)
        min_col = min(index.column() for index in selected_indexes)
        max_col = max(index.column() for index in selected_indexes)

        # 仅在选区外圈绘制边框
        if index.row() == min_row or index.row() == max_row or \
           index.column() == min_col or index.column() == max_col:
            pen = QPen(Qt.green, 2)  # 绿色边框，宽度2px
            painter.setPen(pen)
            painter.drawRect(option.rect)

# 创建应用程序
app = QApplication([])

# 创建表格
table = QTableWidget(5, 5)
table.setItemDelegate(SelectionBorderDelegate(table))

# 填充数据
for row in range(5):
    for col in range(5):
        table.setItem(row, col, QTableWidgetItem(f"{row},{col}"))

table.resize(400, 300)
table.show()
app.exec_()
