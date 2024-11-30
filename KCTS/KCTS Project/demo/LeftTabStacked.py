from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QHeaderView

app = QApplication([])
table_widget = QTableWidget()

# 添加表头和数据
table_widget.setColumnCount(3)
table_widget.setRowCount(4)
table_widget.setHorizontalHeaderLabels(['Column 1', 'Column 2', 'Column 3'])

data = [
    ['Row 1, Column 1', 'Row 1, Column 2', 'Row 1, Column 3'],
    ['Row 2, Column 1', 'Row 2, Column 2', 'Row 2, Column 3'],
    ['Row 3, Column 1', 'Row 3, Column 2', 'Row 3, Column 3'],
    ['Row 4, Column 1', 'Row 4, Column 2', 'Row 4, Column 3']
]

for i, row in enumerate(data):
    for j, item in enumerate(row):
        table_widget.setItem(i, j, QTableWidgetItem(item))

# 调整列宽最大化
header = table_widget.horizontalHeader()
header.setSectionResizeMode(QHeaderView.Stretch)

table_widget.show()
app.exec()
