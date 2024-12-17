from PyQt5.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QWidget

app = QApplication([])

# 主窗口
window = QWidget()
layout = QVBoxLayout(window)

# QLineEdit 控件
lineEdit = QLineEdit()
lineEdit.setPlaceholderText("请输入内容...")
lineEdit.setDisabled(True)  # 设置为 disabled 状态

# 设置 QSS 样式
lineEdit.setStyleSheet("""
    QLineEdit {
        font-size: 16px;          /* 正常状态下的字体大小 */
        color: black;             /* 正常状态下输入文本的颜色 */
        background-color: white;  /* 正常状态下的背景颜色 */
    }
    QLineEdit:disabled {
        color: gray;              /* 禁用状态下的文本颜色 */
        background-color: #f0f0f0; /* 禁用状态下的背景颜色 */
        border: 1px solid #d3d3d3; /* 禁用状态下的边框样式 */
    }
    QLineEdit::placeholderText:disabled {
        color: red;         /* 禁用状态下的 placeholder 颜色 */
    }
""")

layout.addWidget(lineEdit)
window.setLayout(layout)
window.show()

app.exec()
