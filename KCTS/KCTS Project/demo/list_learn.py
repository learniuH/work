from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox
from PyQt5.Qt import Qt


class CustomWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 主布局
        main_layout = QVBoxLayout(self)

        # 创建一个 QGridLayout
        self.grid_layout = QGridLayout()
        main_layout.addLayout(self.grid_layout)

        # 在 GridLayout 中添加控件
        self.line_edits = []  # 存储所有 QLineEdit
        for i in range(5):
            line_edit = QLineEdit()
            self.grid_layout.addWidget(line_edit, i, 0)
            self.line_edits.append(line_edit)

            button = QPushButton(f"Button {i + 1}")
            self.grid_layout.addWidget(button, i, 1)
            button.pressed.connect(self.disable_line_edit_focus)
            button.released.connect(self.enable_line_edit_focus)

            checkbox = QCheckBox(f"Check {i + 1}")
            self.grid_layout.addWidget(checkbox, i, 2)

        # 在主布局中添加 GridLayout 外部的控件
        self.outside_label = QLabel("Prevent focus on QLineEdit when button pressed")
        self.outside_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.outside_label)

    def disable_line_edit_focus(self):
        """禁用所有 QLineEdit 的焦点策略"""
        for line_edit in self.line_edits:
            line_edit.setFocusPolicy(Qt.NoFocus)

    def enable_line_edit_focus(self):
        """恢复所有 QLineEdit 的焦点策略"""
        for line_edit in self.line_edits:
            line_edit.setFocusPolicy(Qt.StrongFocus)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    window = CustomWidget()
    window.resize(400, 300)
    window.show()

    sys.exit(app.exec_())
