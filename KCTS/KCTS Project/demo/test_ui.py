# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\test.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1211, 485)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(10, 0, 191, 71))
        self.tabWidget.setStyleSheet("QTabWidget::pane { /* The tab widget frame */\n"
"    border-top: 2px solid #C2C7CB;\n"
"}\n"
"\n"
"QTabWidget::tab-bar {\n"
"    left: 5px; /* move to the right by 5px */\n"
"}\n"
"\n"
"/* Style the tab using the tab sub-control. Note that\n"
"    it reads QTabBar _not_ QTabWidget */\n"
"QTabBar::tab {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"    border: 2px solid #C4C4C3;\n"
"    border-bottom-color: #C2C7CB; /* same as the pane color */\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"    min-width: 8ex;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"QTabBar::tab:selected, QTabBar::tab:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #fafafa, stop: 0.4 #f4f4f4,\n"
"                                stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    border-color: #9B9B9B;\n"
"    border-bottom-color: #C2C7CB; /* same as pane color */\n"
"}\n"
"\n"
"QTabBar::tab:!selected {\n"
"    margin-top: 2px; /* make non-selected tabs look smaller */\n"
"}")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setGeometry(QtCore.QRect(810, 300, 118, 23))
        self.progressBar.setStyleSheet("QProgressBar {\n"
"    border: 2px solid #204789;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: #05B8CC;\n"
"    width: 100px;\n"
"}")
        self.progressBar.setMaximum(2499)
        self.progressBar.setProperty("value", 23)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(220, 0, 91, 51))
        self.label.setStyleSheet("QLabel {\n"
"    border: 2px solid green;\n"
"    border-radius: 10px;\n"
"    padding: 2px;\n"
"    background-color: #f3f3f3;\n"
"}")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(320, 0, 111, 51))
        self.pushButton.setStyleSheet("QPushButton {\n"
"    border: 2px solid #8f8f91;\n"
"    border-radius: 6px;\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #f6f7fa, stop: 1 #dadbde);\n"
"    min-width: 80px;\n"
"    \n"
"    font: 9pt \"幼圆\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #dadbde, stop: 1 #f6f7fa);\n"
"}\n"
"\n"
"QPushButton:flat {\n"
"    border: none; /* no border for a flat push button */\n"
"}\n"
"\n"
"QPushButton:default {\n"
"    border-color: navy; /* make the default button prominent */\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(0, 60, 431, 281))
        self.textEdit.setStyleSheet("/* radial gradient */\n"
"QTextEdit {\n"
"    background-color: qlineargradient(x1: 1, y1: 0, x2: 0, y2: 0,\n"
"                                      stop: 0 #404959, stop: 1 #f0f0f0);\n"
"}")
        self.textEdit.setObjectName("textEdit")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(440, 30, 93, 28))
        self.pushButton_2.setStyleSheet("QPushButton {\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b78e6, stop:1 #0f5fd7);\n"
"    border-radius: 5px;\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    padding: 5px 15px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #60a3f7, stop:1 #3b78e6);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f5fd7, stop:1 #3b78e6);\n"
"}\n"
"")
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(590, 0, 113, 21))
        self.lineEdit.setStyleSheet("QLineEdit {\n"
"    background: transparent;\n"
"    border-width: 1;\n"
"    border-style: outset;\n"
"}")
        self.lineEdit.setObjectName("lineEdit")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(1000, 20, 131, 31))
        self.comboBox.setStyleSheet("QComboBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 3px;\n"
"    padding: 1px 18px 1px 3px;\n"
"    min-width: 6em;\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:!editable, QComboBox::drop-down:editable {\n"
"     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"}\n"
"\n"
"/* QComboBox gets the \"on\" state when the popup is open */\n"
"QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,\n"
"                                stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(/usr/share/icons/crystalsvg/16x16/actions/1downarrow.png);\n"
"}\n"
"\n"
"QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}")
        self.comboBox.setEditable(False)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox_2 = QtWidgets.QComboBox(Form)
        self.comboBox_2.setGeometry(QtCore.QRect(820, 80, 102, 22))
        self.comboBox_2.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.comboBox_2.setStyleSheet("/* 设置滚动条整体样式 */\n"
"QComboBox QScrollBar:vertical {\n"
"    border: 1px solid #dcdcdc; /* 滚动条边框颜色 */\n"
"    background: #f5f5f5;       /* 滚动条背景颜色 */\n"
"    width: 12px;               /* 滚动条宽度 */\n"
"}\n"
"\n"
"/* 设置滚动条滑块样式 */\n"
"QComboBox QScrollBar::handle:vertical {\n"
"    background: #cccccc;       /* 滑块颜色 */\n"
"    border-radius: 6px;        /* 滑块圆角 */\n"
"    min-height: 20px;          /* 滑块最小高度 */\n"
"}\n"
"\n"
"/* 设置滑块在鼠标悬停时的样式 */\n"
"QComboBox QScrollBar::handle:vertical:hover {\n"
"    background: #aaaaaa;       /* 滑块悬停颜色 */\n"
"}\n"
"\n"
"/* 设置滚动条上箭头和下箭头按钮样式 */\n"
"QComboBox QScrollBar::sub-line,\n"
"QComboBox QScrollBar::add-line {\n"
"    border: 1px solid #dcdcdc; /* 按钮边框颜色 */\n"
"    background: #f5f5f5;       /* 按钮背景颜色 */\n"
"    height: 12px;              /* 按钮高度 */\n"
"    subcontrol-origin: margin; /* 按钮对齐方式 */\n"
"}\n"
"\n"
"\n"
"\n"
"/* 设置滚动条轨道样式 */\n"
"QComboBox QScrollBar::add-page,\n"
"QComboBox QScrollBar::sub-page {\n"
"    background: #eaeaea; /* 滚动条轨道颜色 */\n"
"}\n"
"")
        self.comboBox_2.setMaxVisibleItems(5)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(10, 350, 289, 99))
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tableWidget.setStyleSheet("    QHeaderView::section {\n"
"            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #f6f7fa, stop: 1 #dadbde);\n"
"    }\n"
"QTableWidget::item {\n"
"            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #408a99, stop: 1 #dadbde);\n"
"    }")
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setAutoScrollMargin(16)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(50)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setDefaultSectionSize(60)
        self.tableWidget.verticalHeader().setMinimumSectionSize(40)
        self.tableWidget_2 = QtWidgets.QTableWidget(Form)
        self.tableWidget_2.setGeometry(QtCore.QRect(450, 60, 311, 111))
        self.tableWidget_2.setStyleSheet("/*表头背景颜色*/\n"
"QHeaderView::section {\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #f6f7fa, stop: 1 #dadbde);\n"
"}\n"
"\n"
"/*单元格背景颜色*/\n"
"QTableWidget::item {\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #408a99, stop: 1 #dadbde);\n"
"}\n"
"/*选中单元格的背景颜色*/\n"
"QTableWidget::item:selected {\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #408a99, stop: 1 #20505e);\n"
"}\n"
"/*设置字体*/\n"
"QTableWidget::item {\n"
"    font-size: 12pt;\n"
"    font-family: \"微软雅黑\";\n"
"}")
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        self.progressBar_2 = QtWidgets.QProgressBar(Form)
        self.progressBar_2.setGeometry(QtCore.QRect(740, 20, 118, 23))
        self.progressBar_2.setStyleSheet("QProgressBar {\n"
"    border: 3px solid grey;\n"
"    border-radius: 10px;\n"
"    text-align: center;\n"
"    border-color: #44909f;\n"
"    font: 9pt \"微软雅黑\";\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #f6f7fa, stop: 1 #dadbde);\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: #e77060;\n"
"    width: 20px;\n"
"}")
        self.progressBar_2.setProperty("value", 24)
        self.progressBar_2.setObjectName("progressBar_2")
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setGeometry(QtCore.QRect(440, 170, 171, 61))
        self.checkBox.setStyleSheet("QCheckBox::indicator {\n"
"    width: 85px;\n"
"    height: 45px;\n"
"}\n"
"\n"
"QCheckBox::indicator:unckecked {\n"
"    image: url(:/checkBox/img/toggle_switch_unchecked.png);\n"
"}\n"
"\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    image: url(:/checkBox/img/toggle_switch_checked.png);\n"
"}")
        self.checkBox.setObjectName("checkBox")
        self.checkBox_3 = QtWidgets.QCheckBox(Form)
        self.checkBox_3.setGeometry(QtCore.QRect(440, 230, 221, 71))
        self.checkBox_3.setStyleSheet("QCheckBox {\n"
"    spacing: 0px;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 85px;\n"
"    height: 35px;\n"
"}\n"
"\n"
"QCheckBox::indicator:unckecked {\n"
"    image: url(:/checkBox/img/padlock.png);\n"
"}\n"
"\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    image: url(:/checkBox/img/padlock (1).png);\n"
"}")
        self.checkBox_3.setObjectName("checkBox_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setEnabled(True)
        self.lineEdit_2.setGeometry(QtCore.QRect(620, 200, 113, 20))
        self.lineEdit_2.setStyleSheet("QLineEdit {\n"
"        font-size: 16px;          /* 正常状态下的字体大小 */\n"
"        color: black;             /* 正常状态下输入文本的颜色 */\n"
"        background-color: white;  /* 正常状态下的背景颜色 */\n"
"    }\n"
"    QLineEdit:disabled {\n"
"        color: gray;              /* 禁用状态下的文本颜色 */\n"
"        background-color: #f0f0f0; /* 禁用状态下的背景颜色 */\n"
"        border: 1px solid #d3d3d3; /* 禁用状态下的边框样式 */\n"
"    }")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalSlider = QtWidgets.QSlider(Form)
        self.horizontalSlider.setGeometry(QtCore.QRect(460, 330, 160, 22))
        self.horizontalSlider.setStyleSheet("QSlider::groove:horizontal {\n"
"    background: transparent;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"    border: 2px solid qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #f6f7fa, stop: 1 #dadbde);\n"
"    border-radius: 5px;\n"
"    width: 2px;\n"
"    margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */\n"
"\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"    background: transparent;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"    border: 1px solid #204789;\n"
"    border-radius: 5px;\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,\n"
"                                      stop: 0 #05b8cc, stop: 1 #06dcf4);\n"
"}")
        self.horizontalSlider.setSliderPosition(0)
        self.horizontalSlider.setTracking(True)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setInvertedAppearance(False)
        self.horizontalSlider.setInvertedControls(False)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.horizontalSlider.setTickInterval(0)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.dial = QtWidgets.QDial(Form)
        self.dial.setGeometry(QtCore.QRect(930, 290, 41, 41))
        self.dial.setStyleSheet("")
        self.dial.setPageStep(10)
        self.dial.setProperty("value", 0)
        self.dial.setOrientation(QtCore.Qt.Horizontal)
        self.dial.setWrapping(False)
        self.dial.setNotchTarget(11.0)
        self.dial.setNotchesVisible(True)
        self.dial.setObjectName("dial")
        self.horizontalSlider_2 = QtWidgets.QSlider(Form)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(460, 300, 160, 20))
        self.horizontalSlider_2.setStyleSheet("/*滑块的样式*/\n"
"QSlider::groove:horizontal {\n"
"    border: 1px solid #00B0AE;\n"
"    background: #00B0AE;\n"
"    height: 2px;\n"
"    border-radius: 1px;\n"
"    padding-left:0px;\n"
"    padding-right:0px;\n"
"}\n"
" \n"
"/*滑块经过的颜色:前面的颜色*/\n"
"QSlider::sub-page:horizontal {\n"
"    background: #00B0AE;\n"
"    border: 1px solid #00B0AE;\n"
"    height: 2px;\n"
"    border-radius: 2px;\n"
"}\n"
" \n"
"QSlider::add-page:horizontal {\n"
"background: #EAEAEA;\n"
"border: 0px solid #EAEAEA;\n"
"height: 2px;\n"
"border-radius: 2px;\n"
"}\n"
"QSlider::handle:horizontal \n"
"{\n"
"    background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, \n"
"    stop:0.6 #00B0AE,stop:0.98409 rgba(255, 255, 255, 255));\n"
" \n"
"    width: 15px;\n"
"    margin-top: -6px;\n"
"    margin-bottom: -6px;\n"
"    border-radius: 5px;\n"
"}\n"
" \n"
"QSlider::handle:horizontal:hover {\n"
"    background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, \n"
"    stop:0.6 #00B0AE,stop:0.98409 rgba(255, 255, 255, 255));\n"
" \n"
"    width: 15px;\n"
"    margin-top: -6px;\n"
"    margin-bottom: -6px;\n"
"    border-radius: 5px;\n"
"}")
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "实时解析"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "历史记录"))
        self.progressBar.setFormat(_translate("Form", "%v%"))
        self.label.setText(_translate("Form", "TextLabel"))
        self.pushButton.setText(_translate("Form", "PushButton"))
        self.pushButton_2.setText(_translate("Form", "PushButton"))
        self.comboBox.setItemText(0, _translate("Form", "1"))
        self.comboBox.setItemText(1, _translate("Form", "2"))
        self.comboBox_2.setItemText(0, _translate("Form", "1"))
        self.comboBox_2.setItemText(1, _translate("Form", "新建项目"))
        self.comboBox_2.setItemText(2, _translate("Form", "新建项目"))
        self.comboBox_2.setItemText(3, _translate("Form", "新建项目"))
        self.comboBox_2.setItemText(4, _translate("Form", "新建项目"))
        self.comboBox_2.setItemText(5, _translate("Form", "1"))
        self.comboBox_2.setItemText(6, _translate("Form", "1"))
        self.comboBox_2.setItemText(7, _translate("Form", "1"))
        self.comboBox_2.setItemText(8, _translate("Form", "1"))
        self.comboBox_2.setItemText(9, _translate("Form", "1"))
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Form", "OU ANAL"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "bit7"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "bit6"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "bit5"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "bit4"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "bit3"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "bit2"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Form", "bit1"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Form", "bit0"))
        item = self.tableWidget_2.verticalHeaderItem(0)
        item.setText(_translate("Form", "新建行"))
        item = self.tableWidget_2.verticalHeaderItem(1)
        item.setText(_translate("Form", "新建行"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("Form", "新建列"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("Form", "新建列"))
        self.checkBox.setText(_translate("Form", "去重"))
        self.checkBox_3.setText(_translate("Form", "checkBox"))
import resource_rc
