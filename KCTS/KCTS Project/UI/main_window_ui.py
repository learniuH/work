# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\main_window_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_KCTS(object):
    def setupUi(self, KCTS):
        KCTS.setObjectName("KCTS")
        KCTS.resize(920, 617)
        self.Window = QtWidgets.QWidget(KCTS)
        self.Window.setObjectName("Window")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.Window)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Menu = QtWidgets.QWidget(self.Window)
        self.Menu.setMaximumSize(QtCore.QSize(16777215, 100))
        self.Menu.setStyleSheet("background-color: rgb(125, 125, 125);")
        self.Menu.setObjectName("Menu")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.Menu)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(120, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.system_label = QtWidgets.QLabel(self.Menu)
        self.system_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.system_label.setSizeIncrement(QtCore.QSize(0, 0))
        self.system_label.setStyleSheet("font: 20pt \"幼圆\";")
        self.system_label.setAlignment(QtCore.Qt.AlignCenter)
        self.system_label.setObjectName("system_label")
        self.horizontalLayout.addWidget(self.system_label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton = QtWidgets.QPushButton(self.Menu)
        self.pushButton.setMaximumSize(QtCore.QSize(80, 40))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.Menu)
        self.pushButton_2.setMaximumSize(QtCore.QSize(80, 40))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.Menu)
        self.pushButton_3.setMaximumSize(QtCore.QSize(40, 40))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.verticalLayout.addWidget(self.Menu)
        self.Body = QtWidgets.QWidget(self.Window)
        self.Body.setStyleSheet("background-color: rgb(211, 211, 211);")
        self.Body.setObjectName("Body")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.Body)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.navigation_list = QtWidgets.QListWidget(self.Body)
        self.navigation_list.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.navigation_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.navigation_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.navigation_list.setItemAlignment(QtCore.Qt.AlignCenter)
        self.navigation_list.setObjectName("navigation_list")
        self.horizontalLayout_2.addWidget(self.navigation_list)
        self.sub_interface_stacked = QtWidgets.QStackedWidget(self.Body)
        self.sub_interface_stacked.setObjectName("sub_interface_stacked")
        self.device_status_page = QtWidgets.QWidget()
        self.device_status_page.setObjectName("device_status_page")
        self.label = QtWidgets.QLabel(self.device_status_page)
        self.label.setGeometry(QtCore.QRect(290, 90, 141, 41))
        self.label.setObjectName("label")
        self.sub_interface_stacked.addWidget(self.device_status_page)
        self.auto_test_page = QtWidgets.QWidget()
        self.auto_test_page.setObjectName("auto_test_page")
        self.label_2 = QtWidgets.QLabel(self.auto_test_page)
        self.label_2.setGeometry(QtCore.QRect(290, 180, 151, 41))
        self.label_2.setObjectName("label_2")
        self.sub_interface_stacked.addWidget(self.auto_test_page)
        self.analysis_page = QtWidgets.QWidget()
        self.analysis_page.setObjectName("analysis_page")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.analysis_page)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.real_time_analysis_pushButton = QtWidgets.QPushButton(self.analysis_page)
        self.real_time_analysis_pushButton.setObjectName("real_time_analysis_pushButton")
        self.horizontalLayout_3.addWidget(self.real_time_analysis_pushButton)
        self.history_pushButton = QtWidgets.QPushButton(self.analysis_page)
        self.history_pushButton.setObjectName("history_pushButton")
        self.horizontalLayout_3.addWidget(self.history_pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.analysis_stackedWidget = QtWidgets.QStackedWidget(self.analysis_page)
        self.analysis_stackedWidget.setObjectName("analysis_stackedWidget")
        self.real_time_analysis_page = QtWidgets.QWidget()
        self.real_time_analysis_page.setObjectName("real_time_analysis_page")
        self.gridLayoutWidget = QtWidgets.QWidget(self.real_time_analysis_page)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 100, 832, 166))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 0, 0, 1, 1)
        self.pushButton_11 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_11.setObjectName("pushButton_11")
        self.gridLayout.addWidget(self.pushButton_11, 0, 3, 1, 1)
        self.pushButton_12 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_12.setObjectName("pushButton_12")
        self.gridLayout.addWidget(self.pushButton_12, 0, 4, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 2, 0, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout.addWidget(self.pushButton_9, 0, 1, 1, 1)
        self.pushButton_10 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout.addWidget(self.pushButton_10, 0, 2, 1, 1)
        self.pushButton_14 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_14.setObjectName("pushButton_14")
        self.gridLayout.addWidget(self.pushButton_14, 0, 6, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout.addWidget(self.pushButton_7, 3, 0, 1, 1)
        self.pushButton_13 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_13.setObjectName("pushButton_13")
        self.gridLayout.addWidget(self.pushButton_13, 0, 5, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 1, 0, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout.addWidget(self.pushButton_8, 4, 0, 1, 1)
        self.pushButton_15 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_15.setObjectName("pushButton_15")
        self.gridLayout.addWidget(self.pushButton_15, 0, 7, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.gridLayoutWidget)
        self.progressBar.setMaximum(24)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 2, 5, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)
        self.analysis_stackedWidget.addWidget(self.real_time_analysis_page)
        self.history_page = QtWidgets.QWidget()
        self.history_page.setObjectName("history_page")
        self.label_5 = QtWidgets.QLabel(self.history_page)
        self.label_5.setGeometry(QtCore.QRect(360, 200, 211, 121))
        self.label_5.setObjectName("label_5")
        self.analysis_stackedWidget.addWidget(self.history_page)
        self.verticalLayout_2.addWidget(self.analysis_stackedWidget)
        self.sub_interface_stacked.addWidget(self.analysis_page)
        self.configuration_page = QtWidgets.QWidget()
        self.configuration_page.setObjectName("configuration_page")
        self.label_4 = QtWidgets.QLabel(self.configuration_page)
        self.label_4.setGeometry(QtCore.QRect(240, 150, 201, 71))
        self.label_4.setObjectName("label_4")
        self.sub_interface_stacked.addWidget(self.configuration_page)
        self.horizontalLayout_2.addWidget(self.sub_interface_stacked)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 15)
        self.verticalLayout.addWidget(self.Body)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 15)
        KCTS.setCentralWidget(self.Window)

        self.retranslateUi(KCTS)
        QtCore.QMetaObject.connectSlotsByName(KCTS)

    def retranslateUi(self, KCTS):
        _translate = QtCore.QCoreApplication.translate
        KCTS.setWindowTitle(_translate("KCTS", "KCTS"))
        self.system_label.setText(_translate("KCTS", "KCTS"))
        self.pushButton.setText(_translate("KCTS", "选择项目"))
        self.pushButton_2.setText(_translate("KCTS", "生成报告"))
        self.pushButton_3.setText(_translate("KCTS", "……"))
        self.label.setText(_translate("KCTS", "这是设备状态界面"))
        self.label_2.setText(_translate("KCTS", "这是自动化测试界面"))
        self.real_time_analysis_pushButton.setText(_translate("KCTS", "实时解析"))
        self.history_pushButton.setText(_translate("KCTS", "历史记录"))
        self.pushButton_4.setText(_translate("KCTS", "PushButton"))
        self.pushButton_11.setText(_translate("KCTS", "PushButton"))
        self.pushButton_12.setText(_translate("KCTS", "PushButton"))
        self.pushButton_6.setText(_translate("KCTS", "PushButton"))
        self.pushButton_9.setText(_translate("KCTS", "PushButton"))
        self.pushButton_10.setText(_translate("KCTS", "PushButton"))
        self.pushButton_14.setText(_translate("KCTS", "PushButton"))
        self.pushButton_7.setText(_translate("KCTS", "PushButton"))
        self.pushButton_13.setText(_translate("KCTS", "PushButton"))
        self.pushButton_5.setText(_translate("KCTS", "PushButton"))
        self.pushButton_8.setText(_translate("KCTS", "PushButton"))
        self.pushButton_15.setText(_translate("KCTS", "PushButton"))
        self.progressBar.setFormat(_translate("KCTS", "%vV"))
        self.label_5.setText(_translate("KCTS", "这是历史记录界面"))
        self.label_4.setText(_translate("KCTS", "这是配置管理界面"))
