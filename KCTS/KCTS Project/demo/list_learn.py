from PyQt5.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt

app = QApplication([])

window = QWidget()
layout = QVBoxLayout()

lineEdit = QLineEdit()
lineEdit.setPlaceholderText("请输入内容")

# 使用 QPalette 设置 placeholderText 的颜色
palette = lineEdit.palette()
palette.setColor(QPalette.PlaceholderText, Qt.black)
lineEdit.setPalette(palette)

layout.addWidget(lineEdit)
window.setLayout(layout)
window.show()

app.exec()
