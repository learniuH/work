# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'KCTS.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Window(object):
    def setupUi(self, Window):
        Window.setObjectName("Window")
        Window.resize(518, 399)
        self.ip_editText = QtWidgets.QTextEdit(Window)
        self.ip_editText.setGeometry(QtCore.QRect(110, 80, 256, 41))
        self.ip_editText.setObjectName("ip_editText")
        self.port_editText = QtWidgets.QTextEdit(Window)
        self.port_editText.setGeometry(QtCore.QRect(110, 140, 256, 41))
        self.port_editText.setObjectName("port_editText")
        self.targetIp_label = QtWidgets.QLabel(Window)
        self.targetIp_label.setGeometry(QtCore.QRect(10, 100, 72, 15))
        self.targetIp_label.setObjectName("targetIp_label")
        self.targetPort_label = QtWidgets.QLabel(Window)
        self.targetPort_label.setGeometry(QtCore.QRect(10, 160, 91, 16))
        self.targetPort_label.setObjectName("targetPort_label")
        self.connect_pushButton = QtWidgets.QPushButton(Window)
        self.connect_pushButton.setGeometry(QtCore.QRect(400, 110, 93, 28))
        self.connect_pushButton.setObjectName("connect_pushButton")
        self.openFile_pushButton = QtWidgets.QPushButton(Window)
        self.openFile_pushButton.setGeometry(QtCore.QRect(230, 30, 93, 28))
        self.openFile_pushButton.setObjectName("openFile_pushButton")

        self.retranslateUi(Window)
        QtCore.QMetaObject.connectSlotsByName(Window)

    def retranslateUi(self, Window):
        _translate = QtCore.QCoreApplication.translate
        Window.setWindowTitle(_translate("Window", "Form"))
        self.targetIp_label.setText(_translate("Window", "Target_IP"))
        self.targetPort_label.setText(_translate("Window", "Target_Port"))
        self.connect_pushButton.setText(_translate("Window", "连接"))
        self.openFile_pushButton.setText(_translate("Window", "打开文件"))
