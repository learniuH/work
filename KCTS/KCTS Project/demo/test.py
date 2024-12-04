# from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QTextEdit, QPushButton
#
# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("QTextEdit 续写内容")
#         self.resize(400, 300)
#
#         # 创建控件
#         self.text_edit = QTextEdit(self)
#         self.text_edit.setPlaceholderText("这里是 QTextEdit...")
#         self.button = QPushButton("添加 '你好'", self)
#         self.button_1 = QPushButton(self)
#
#         # 布局
#         layout = QVBoxLayout()
#         layout.addWidget(self.text_edit)
#         layout.addWidget(self.button)
#         self.setLayout(layout)
#
#         # 信号与槽连接
#         self.button.clicked.connect(self.append_text)
#         self.button.clicked.connect(self.print1)
#         self.button_1.clicked.connect(self.print1)
#
#     def print1(self):
#         print(1)
#
#     def append_text(self):
#         # 在 QTextEdit 末尾添加文本
#         self.text_edit.append("你好")
#
# # 应用程序
# app = QApplication([])
# window = MainWindow()
# window.show()
# app.exec_()
a = None
a[1] = 'a'
print(a)