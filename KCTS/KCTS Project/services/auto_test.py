from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QTableWidget, QPushButton, QLineEdit, QLabel

class AutoTest:
    """ 自动化测试类 """

    def __init__(self, widget: dict):
        """ 界面子控件初始化 """
        self.tableWidget_test_case: QTableWidget        =   widget['tableWidget_test_case']
        self.pushButton_insert_case: QPushButton        =   widget['pushButton_insert_case']
        self.pushButton_start_test: QPushButton         =   widget['pushButton_start_test']
        self.pushButton_stop_test: QPushButton          =   widget['pushButton_stop_test']
        self.pushButton_previous_page: QPushButton      =   widget['pushButton_previous_page']
        self.pushButton_next_page: QPushButton          =   widget['pushButton_next_page']
        self.lineEdit_current_page: QLineEdit           =   widget['lineEdit_current_page']
        self.label_total_pages: QLabel                  =   widget['label_total_pages']

        self.slot_connect()

    def slot_connect(self):
        """ 自动化测试界面子控件槽链接 """
        self.pushButton_insert_case.clicked.connect(lambda: self.open_dialog())
        # self.pushButton_start_test.clicked.connect(lambda: )
        # self.pushButton_stop_test.clicked.connect(lambda: )
        # self.pushButton_previous_page.clicked.connect()
        # self.pushButton_next_page.clicked.connect()
        # self.lineEdit_current_page.textChanged.connect()

    def open_dialog(self):
        """ 点击导入用例, 打开文件对话框 """
        file_path = QFileDialog.getOpenFileName(
            None, '选择测试用例', '', 'Excel Files (*.xlsx *xls);;All Files (*)'
        )