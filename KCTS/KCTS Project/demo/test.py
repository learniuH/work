from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QStackedWidget, QVBoxLayout, QWidget
import sys


# 子界面1
class Page1(QWidget):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.label.setText("这是界面1")


# 子界面2
class Page2(QWidget):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.label.setText("这是界面2")


# 子界面3
class Page3(QWidget):
    def __init__(self, parent=None):
        super(Page3, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.label.setText("这是界面3")


# 主窗口
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("ListWidget 和 StackedWidget 切换")
        self.resize(800, 600)

        # 主部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # 左侧的 ListWidget 作为导航栏
        self.list_widget = QListWidget()
        self.list_widget.addItem("界面1")
        self.list_widget.addItem("界面2")
        self.list_widget.addItem("界面3")
        self.list_widget.currentRowChanged.connect(self.switch_page)  # 绑定切换方法
        layout.addWidget(self.list_widget)

        # 右侧的 StackedWidget
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(Page2())  # 添加子界面1
        self.stacked_widget.addWidget(Page1())  # 添加子界面2
        self.stacked_widget.addWidget(Page3())  # 添加子界面3
        layout.addWidget(self.stacked_widget)

    def switch_page(self, index):
        """切换 stackedWidget 的子界面"""
        self.stacked_widget.setCurrentIndex(index)


# 子界面类由 Qt Designer 生成
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(387, 297)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(210, 140, 72, 15))
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "这是界面1"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
