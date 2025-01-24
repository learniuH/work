import sys

from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QRegExp
from test_ui import Ui_Form

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.set_up_validator()

    def set_up_validator(self):
        """ 初始化 lineEdit, 使用正则表达式匹配 lineEdit 内容"""
        self.ui.lineEdit_2.setValidator(self.get_addr_validator())


    def get_addr_validator(self) -> QRegExpValidator:
        """ 亿佰特 Lora 模块地址验证器 """
        addr_regex = QRegExp(r'^[0-9A-Fa-f]{2} ([1-9A-Fa-f][0-9A-Fa-f]|0[0-9A-Fa-f]{2,3})$')
        # addr_regex = QRegExp(r'^[0-9A-Fa-f]{2} (?:[1-9A-Fa-f]{2}|0[0-9A-Fa-f]{2,3})$')
        return QRegExpValidator(addr_regex)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())