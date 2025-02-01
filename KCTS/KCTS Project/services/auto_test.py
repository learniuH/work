from PyQt5.QtWidgets import QFileDialog, QTableWidget, QPushButton, QLineEdit, QLabel, QComboBox

import pandas as pd
import numpy as np


class AutoTest:
    """ 自动化测试类 """

    def __init__(self, widget: dict):
        """ 界面子控件初始化 """
        self.tableWidget_test_case: QTableWidget        =   widget['tableWidget_test_case']
        self.comboBox_case_sheet_names: QComboBox       =   widget['comboBox_case_sheet_names']
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
        self.comboBox_case_sheet_names.currentIndexChanged.connect(lambda: self.excel_case_parse())
        # self.pushButton_start_test.clicked.connect(lambda: )
        # self.pushButton_stop_test.clicked.connect(lambda: )
        # self.pushButton_previous_page.clicked.connect()
        # self.pushButton_next_page.clicked.connect()
        # self.lineEdit_current_page.textChanged.connect()

    def open_dialog(self):
        """ 点击导入用例, 打开文件对话框 """
        file_path, _ = QFileDialog.getOpenFileName(
            parent= None,
            caption= "选择测试用例",
            filter= "ExcelFile (*.xlsx *.xls)",
        )
        if file_path:
            # 获取用例 Excel 的表单列表
            sheet_names = self.get_sheet_names(file_path)
            # 将表单名更新到 comboBox
            self.update_comboBox_items(sheet_names)

    def get_sheet_names(self, file_path: str) -> list:
        """
        根据测试用例路径, 解析Excel表单列表
        :param file_path:  测试用例Excel的路径
        :return: 测试用例Excel的表单列表
        """
        excel_file = pd.ExcelFile(file_path)
        sheet_names: list = excel_file.sheet_names
        return sheet_names

    def update_comboBox_items(self, sheet_names: list):
        """ 根据表单名列表更新 comboBox 的 items """
        self.comboBox_case_sheet_names.blockSignals(True)
        self.comboBox_case_sheet_names.addItems(sheet_names)
        self.comboBox_case_sheet_names.setCurrentIndex(-1)
        self.comboBox_case_sheet_names.blockSignals(False)

    def excel_case_parse(self):
        """ 根据测试用例的路径, 解析Excel内容 """
        print(1)