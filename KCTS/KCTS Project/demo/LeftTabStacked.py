# import sys
# import math
# from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton,
#                              QDesktopWidget, QVBoxLayout, QScrollArea)
# from PyQt5.QtCore import Qt, QSize
#
#
# class HeightAdaptiveGridLayout(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.total_buttons = 20
#         self.button_height = 50  # 每个按钮的高度
#         self.button_width = 100  # 每个按钮的宽度
#         self.vertical_spacing = 10  # 垂直间距
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('Height-Adaptive Grid Layout')
#
#         # 主布局
#         main_layout = QVBoxLayout()
#
#         # 滚动区域
#         self.scroll_area = QScrollArea()
#         self.scroll_widget = QWidget()
#         self.grid_layout = QGridLayout(self.scroll_widget)
#
#         # 设置布局间距
#         self.grid_layout.setVerticalSpacing(self.vertical_spacing)
#         self.grid_layout.setHorizontalSpacing(10)
#
#         # 初始化按钮
#         self.update_grid_layout()
#
#         self.scroll_area.setWidget(self.scroll_widget)
#         self.scroll_area.setWidgetResizable(True)
#
#         main_layout.addWidget(self.scroll_area)
#         self.setLayout(main_layout)
#
#         # 设置初始窗口大小
#         self.resize(800, 600)
#         self.center()
#
#         # 连接窗口大小改变事件
#         self.resizeEvent = self.on_resize
#
#     def calculate_buttons_per_column(self, total_height):
#         # 计算每列可以放置的按钮数量
#         # 考虑按钮高度和垂直间距
#         buttons_height = self.button_height
#         buttons_spacing = self.vertical_spacing
#         single_button_total_height = buttons_height + buttons_spacing
#
#         # 计算可以放置的按钮数量
#         buttons_per_column = max(1, int(total_height // single_button_total_height))
#         return buttons_per_column
#
#     def update_grid_layout(self):
#         # 清除旧的布局
#         for i in reversed(range(self.grid_layout.count())):
#             widget = self.grid_layout.itemAt(i).widget()
#             if widget is not None:
#                 widget.deleteLater()
#
#         # 计算每列可以放置的按钮数量
#         scroll_height = self.scroll_area.height()
#         buttons_per_column = self.calculate_buttons_per_column(scroll_height)
#
#         # 计算需要的列数
#         total_columns = math.ceil(self.total_buttons / buttons_per_column)
#
#         # 添加按钮
#         for i in range(self.total_buttons):
#             row = i % buttons_per_column
#             col = i // buttons_per_column
#             btn = QPushButton(f'Button {i + 1}')
#             btn.setFixedSize(self.button_width, self.button_height)
#             self.grid_layout.addWidget(btn, row, col)
#
#     def on_resize(self, event):
#         # 窗口大小改变时更新布局
#         self.update_grid_layout()
#
#     def center(self):
#         # 窗口居中
#         qr = self.frameGeometry()
#         cp = QDesktopWidget().availableGeometry().center()
#         qr.moveCenter(cp)
#         self.move(qr.topLeft())
#
#
# def main():
#     app = QApplication(sys.argv)
#     ex = HeightAdaptiveGridLayout()
#     ex.show()
#     sys.exit(app.exec_())
#
#
# if __name__ == '__main__':
#     main()


from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from PyQt5.QtCore import Qt


class DynamicGridLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)  # 设置控件之间的间距
        self.setLayout(self.grid_layout)

        self.widgets = []
        self.populate_widgets(20)  # 添加20个控件

        self.setMinimumSize(200, 100)  # 设置窗口的最小尺寸

    def populate_widgets(self, count):
        """创建控件"""
        for i in range(count):
            btn = QPushButton(f"Button {i + 1}")
            btn.setMinimumSize(50, 30)  # 设置控件的最小尺寸
            self.widgets.append(btn)

        self.adjust_grid_layout()

    def adjust_grid_layout(self):
        """动态调整网格布局"""
        # 清空布局中的控件
        while self.grid_layout.count() > 0:
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        grid_width = self.width()
        widget_width = 60  # 每个控件的理想宽度，包括间距
        widgets_per_row = max(1, grid_width // widget_width)  # 计算每行控件数量

        for idx, widget in enumerate(self.widgets):
            row = idx // widgets_per_row
            col = idx % widgets_per_row
            self.grid_layout.addWidget(widget, row, col, alignment=Qt.AlignCenter)

    def resizeEvent(self, event):
        """重写resizeEvent，窗口大小改变时动态调整布局"""
        self.adjust_grid_layout()
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    window = DynamicGridLayout()
    window.resize(400, 300)  # 设置初始窗口大小
    window.show()
    app.exec_()

