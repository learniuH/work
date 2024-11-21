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
        KCTS.resize(1064, 690)
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
        self.navigation_list.setMinimumSize(QtCore.QSize(90, 0))
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
        self.label.setGeometry(QtCore.QRect(70, 20, 141, 41))
        self.label.setObjectName("label")
        self.gridLayoutWidget = QtWidgets.QWidget(self.device_status_page)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(80, 60, 691, 536))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.kc_ts_send_tu_port_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.kc_ts_send_tu_port_lineEdit.setStyleSheet("QLineEdit {\n"
"        min-width: 150px;    /* 最小宽度 */\n"
"        max-width: 200px;    /* 最大宽度 */\n"
"        height: 40px;        /* 高度 */\n"
"        font-size: 16px;     /* 字体大小 */\n"
"        border: 2px solid gray;  /* 边框 */\n"
"        border-radius: 5px;      /* 圆角 */\n"
"        padding: 5px;            /* 内边距 */\n"
"}")
        self.kc_ts_send_tu_port_lineEdit.setObjectName("kc_ts_send_tu_port_lineEdit")
        self.gridLayout_2.addWidget(self.kc_ts_send_tu_port_lineEdit, 3, 1, 1, 1)
        self.kc_ts_send_tu_port_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.kc_ts_send_tu_port_label.setMaximumSize(QtCore.QSize(200, 16777215))
        self.kc_ts_send_tu_port_label.setStyleSheet("QLabel {\n"
"    border: 0px solid #298DFF; /* 无边框 */\n"
"    border-radius: 3px; /* 边框圆角 */\n"
"    background-color: ; /* 背景颜色 */\n"
"    color: #298DFF; /* 文本颜色 */\n"
"    font-family: \"Microsoft YaHei\"; /* 文本字体族 */\n"
"    font-size: 10pt; /* 文本字体大小 */\n"
"}")
        self.kc_ts_send_tu_port_label.setAlignment(QtCore.Qt.AlignCenter)
        self.kc_ts_send_tu_port_label.setObjectName("kc_ts_send_tu_port_label")
        self.gridLayout_2.addWidget(self.kc_ts_send_tu_port_label, 3, 0, 1, 1)
        self.kc_ts_send_mu_port_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.kc_ts_send_mu_port_label.setMaximumSize(QtCore.QSize(200, 16777215))
        self.kc_ts_send_mu_port_label.setStyleSheet("QLabel {\n"
"    border: 0px solid #298DFF; /* 无边框 */\n"
"    border-radius: 3px; /* 边框圆角 */\n"
"    background-color: ; /* 背景颜色 */\n"
"    color: #298DFF; /* 文本颜色 */\n"
"    font-family: \"Microsoft YaHei\"; /* 文本字体族 */\n"
"    font-size: 10pt; /* 文本字体大小 */\n"
"}")
        self.kc_ts_send_mu_port_label.setAlignment(QtCore.Qt.AlignCenter)
        self.kc_ts_send_mu_port_label.setObjectName("kc_ts_send_mu_port_label")
        self.gridLayout_2.addWidget(self.kc_ts_send_mu_port_label, 4, 0, 1, 1)
        self.kc_ts_recv_tu_port_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.kc_ts_recv_tu_port_lineEdit.setStyleSheet("QLineEdit {\n"
"        min-width: 150px;    /* 最小宽度 */\n"
"        max-width: 200px;    /* 最大宽度 */\n"
"        height: 40px;        /* 高度 */\n"
"        font-size: 16px;     /* 字体大小 */\n"
"        border: 2px solid gray;  /* 边框 */\n"
"        border-radius: 5px;      /* 圆角 */\n"
"        padding: 5px;            /* 内边距 */\n"
"}")
        self.kc_ts_recv_tu_port_lineEdit.setObjectName("kc_ts_recv_tu_port_lineEdit")
        self.gridLayout_2.addWidget(self.kc_ts_recv_tu_port_lineEdit, 1, 1, 1, 1)
        self.kc_ts_recv_ou_port_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.kc_ts_recv_ou_port_lineEdit.setStyleSheet("QLineEdit {\n"
"        min-width: 150px;    /* 最小宽度 */\n"
"        max-width: 200px;    /* 最大宽度 */\n"
"        height: 40px;        /* 高度 */\n"
"        font-size: 16px;     /* 字体大小 */\n"
"        border: 2px solid gray;  /* 边框 */\n"
"        border-radius: 5px;      /* 圆角 */\n"
"        padding: 5px;            /* 内边距 */\n"
"}")
        self.kc_ts_recv_ou_port_lineEdit.setObjectName("kc_ts_recv_ou_port_lineEdit")
        self.gridLayout_2.addWidget(self.kc_ts_recv_ou_port_lineEdit, 2, 1, 1, 1)
        self.kc_ts_ip_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.kc_ts_ip_lineEdit.setStyleSheet("QLineEdit {\n"
"        min-width: 150px;    /* 最小宽度 */\n"
"        max-width: 200px;    /* 最大宽度 */\n"
"        height: 40px;        /* 高度 */\n"
"        font-size: 16px;     /* 字体大小 */\n"
"        border: 2px solid gray;  /* 边框 */\n"
"        border-radius: 5px;      /* 圆角 */\n"
"        padding: 5px;            /* 内边距 */\n"
"}")
        self.kc_ts_ip_lineEdit.setReadOnly(True)
        self.kc_ts_ip_lineEdit.setObjectName("kc_ts_ip_lineEdit")
        self.gridLayout_2.addWidget(self.kc_ts_ip_lineEdit, 0, 1, 1, 1)
        self.kc_ts_send_mu_port_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.kc_ts_send_mu_port_lineEdit.setStyleSheet("QLineEdit {\n"
"        min-width: 150px;    /* 最小宽度 */\n"
"        max-width: 200px;    /* 最大宽度 */\n"
"        height: 40px;        /* 高度 */\n"
"        font-size: 16px;     /* 字体大小 */\n"
"        border: 2px solid gray;  /* 边框 */\n"
"        border-radius: 5px;      /* 圆角 */\n"
"        padding: 5px;            /* 内边距 */\n"
"}")
        self.kc_ts_send_mu_port_lineEdit.setObjectName("kc_ts_send_mu_port_lineEdit")
        self.gridLayout_2.addWidget(self.kc_ts_send_mu_port_lineEdit, 4, 1, 1, 1)
        self.kc_ts_recv_port_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.kc_ts_recv_port_label.setMaximumSize(QtCore.QSize(200, 16777215))
        self.kc_ts_recv_port_label.setStyleSheet("QLabel {\n"
"    border: 0px solid #298DFF; /* 无边框 */\n"
"    border-radius: 3px; /* 边框圆角 */\n"
"    background-color: ; /* 背景颜色 */\n"
"    color: #298DFF; /* 文本颜色 */\n"
"    font-family: \"Microsoft YaHei\"; /* 文本字体族 */\n"
"    font-size: 10pt; /* 文本字体大小 */\n"
"}")
        self.kc_ts_recv_port_label.setAlignment(QtCore.Qt.AlignCenter)
        self.kc_ts_recv_port_label.setObjectName("kc_ts_recv_port_label")
        self.gridLayout_2.addWidget(self.kc_ts_recv_port_label, 1, 0, 1, 1)
        self.kc_ts_ip_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.kc_ts_ip_label.setStyleSheet("QLabel {\n"
"    border: 0px solid #298DFF; /* 无边框 */\n"
"    border-radius: 3px; /* 边框圆角 */\n"
"    background-color: ; /* 背景颜色 */\n"
"    color: #298DFF; /* 文本颜色 */\n"
"    font-family: \"Microsoft YaHei\"; /* 文本字体族 */\n"
"    font-size: 10pt; /* 文本字体大小 */\n"
"}")
        self.kc_ts_ip_label.setAlignment(QtCore.Qt.AlignCenter)
        self.kc_ts_ip_label.setObjectName("kc_ts_ip_label")
        self.gridLayout_2.addWidget(self.kc_ts_ip_label, 0, 0, 1, 1)
        self.mu_ip_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.mu_ip_label.setMaximumSize(QtCore.QSize(150, 16777215))
        self.mu_ip_label.setStyleSheet("QLabel {\n"
"    border: 0px solid #298DFF; /* 无边框 */\n"
"    border-radius: 3px; /* 边框圆角 */\n"
"    background-color: ; /* 背景颜色 */\n"
"    color: #298DFF; /* 文本颜色 */\n"
"    font-family: \"Microsoft YaHei\"; /* 文本字体族 */\n"
"    font-size: 10pt; /* 文本字体大小 */\n"
"}")
        self.mu_ip_label.setAlignment(QtCore.Qt.AlignCenter)
        self.mu_ip_label.setObjectName("mu_ip_label")
        self.gridLayout_2.addWidget(self.mu_ip_label, 0, 2, 1, 1)
        self.recv_ou_port_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.recv_ou_port_label.setMaximumSize(QtCore.QSize(150, 16777215))
        self.recv_ou_port_label.setStyleSheet("QLabel {\n"
"    border: 0px solid #298DFF; /* 无边框 */\n"
"    border-radius: 3px; /* 边框圆角 */\n"
"    background-color: ; /* 背景颜色 */\n"
"    color: #298DFF; /* 文本颜色 */\n"
"    font-family: \"Microsoft YaHei\"; /* 文本字体族 */\n"
"    font-size: 10pt; /* 文本字体大小 */\n"
"}")
        self.recv_ou_port_label.setAlignment(QtCore.Qt.AlignCenter)
        self.recv_ou_port_label.setObjectName("recv_ou_port_label")
        self.gridLayout_2.addWidget(self.recv_ou_port_label, 2, 0, 1, 1)
        self.mu_ip_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.mu_ip_lineEdit.setStyleSheet("QLineEdit {\n"
"        min-width: 150px;    /* 最小宽度 */\n"
"        max-width: 200px;    /* 最大宽度 */\n"
"        height: 40px;        /* 高度 */\n"
"        font-size: 16px;     /* 字体大小 */\n"
"        border: 2px solid gray;  /* 边框 */\n"
"        border-radius: 5px;      /* 圆角 */\n"
"        padding: 5px;            /* 内边距 */\n"
"}")
        self.mu_ip_lineEdit.setObjectName("mu_ip_lineEdit")
        self.gridLayout_2.addWidget(self.mu_ip_lineEdit, 0, 3, 1, 1)
        self.mu_recv_port_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.mu_recv_port_label.setMaximumSize(QtCore.QSize(150, 16777215))
        self.mu_recv_port_label.setStyleSheet("QLabel {\n"
"    border: 0px solid #298DFF; /* 无边框 */\n"
"    border-radius: 3px; /* 边框圆角 */\n"
"    background-color: ; /* 背景颜色 */\n"
"    color: #298DFF; /* 文本颜色 */\n"
"    font-family: \"Microsoft YaHei\"; /* 文本字体族 */\n"
"    font-size: 10pt; /* 文本字体大小 */\n"
"}")
        self.mu_recv_port_label.setAlignment(QtCore.Qt.AlignCenter)
        self.mu_recv_port_label.setObjectName("mu_recv_port_label")
        self.gridLayout_2.addWidget(self.mu_recv_port_label, 1, 2, 1, 1)
        self.mu_recv_port_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.mu_recv_port_lineEdit.setStyleSheet("QLineEdit {\n"
"        min-width: 150px;    /* 最小宽度 */\n"
"        max-width: 200px;    /* 最大宽度 */\n"
"        height: 40px;        /* 高度 */\n"
"        font-size: 16px;     /* 字体大小 */\n"
"        border: 2px solid gray;  /* 边框 */\n"
"        border-radius: 5px;      /* 圆角 */\n"
"        padding: 5px;            /* 内边距 */\n"
"}")
        self.mu_recv_port_lineEdit.setObjectName("mu_recv_port_lineEdit")
        self.gridLayout_2.addWidget(self.mu_recv_port_lineEdit, 1, 3, 1, 1)
        self.kc_tu_ip_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.kc_tu_ip_label.setMaximumSize(QtCore.QSize(150, 16777215))
        self.kc_tu_ip_label.setStyleSheet("QLabel {\n"
"    border: 0px solid #298DFF; /* 无边框 */\n"
"    border-radius: 3px; /* 边框圆角 */\n"
"    background-color: ; /* 背景颜色 */\n"
"    color: #298DFF; /* 文本颜色 */\n"
"    font-family: \"Microsoft YaHei\"; /* 文本字体族 */\n"
"    font-size: 10pt; /* 文本字体大小 */\n"
"}")
        self.kc_tu_ip_label.setAlignment(QtCore.Qt.AlignCenter)
        self.kc_tu_ip_label.setObjectName("kc_tu_ip_label")
        self.gridLayout_2.addWidget(self.kc_tu_ip_label, 2, 2, 1, 1)
        self.kc_tu_ip_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.kc_tu_ip_lineEdit.setStyleSheet("QLineEdit {\n"
"        min-width: 150px;    /* 最小宽度 */\n"
"        max-width: 200px;    /* 最大宽度 */\n"
"        height: 40px;        /* 高度 */\n"
"        font-size: 16px;     /* 字体大小 */\n"
"        border: 2px solid gray;  /* 边框 */\n"
"        border-radius: 5px;      /* 圆角 */\n"
"        padding: 5px;            /* 内边距 */\n"
"}")
        self.kc_tu_ip_lineEdit.setObjectName("kc_tu_ip_lineEdit")
        self.gridLayout_2.addWidget(self.kc_tu_ip_lineEdit, 2, 3, 1, 1)
        self.kc_tu_recv_port_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.kc_tu_recv_port_label.setMaximumSize(QtCore.QSize(150, 16777215))
        self.kc_tu_recv_port_label.setStyleSheet("QLabel {\n"
"    border: 0px solid #298DFF; /* 无边框 */\n"
"    border-radius: 3px; /* 边框圆角 */\n"
"    background-color: ; /* 背景颜色 */\n"
"    color: #298DFF; /* 文本颜色 */\n"
"    font-family: \"Microsoft YaHei\"; /* 文本字体族 */\n"
"    font-size: 10pt; /* 文本字体大小 */\n"
"}")
        self.kc_tu_recv_port_label.setAlignment(QtCore.Qt.AlignCenter)
        self.kc_tu_recv_port_label.setObjectName("kc_tu_recv_port_label")
        self.gridLayout_2.addWidget(self.kc_tu_recv_port_label, 3, 2, 1, 1)
        self.kc_tu_recv_port_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.kc_tu_recv_port_lineEdit.setStyleSheet("QLineEdit {\n"
"        min-width: 150px;    /* 最小宽度 */\n"
"        max-width: 200px;    /* 最大宽度 */\n"
"        height: 40px;        /* 高度 */\n"
"        font-size: 16px;     /* 字体大小 */\n"
"        border: 2px solid gray;  /* 边框 */\n"
"        border-radius: 5px;      /* 圆角 */\n"
"        padding: 5px;            /* 内边距 */\n"
"}")
        self.kc_tu_recv_port_lineEdit.setObjectName("kc_tu_recv_port_lineEdit")
        self.gridLayout_2.addWidget(self.kc_tu_recv_port_lineEdit, 3, 3, 1, 1)
        self.apply_pushButton = QtWidgets.QPushButton(self.device_status_page)
        self.apply_pushButton.setGeometry(QtCore.QRect(800, 490, 131, 61))
        self.apply_pushButton.setObjectName("apply_pushButton")
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
        self.tabWidget = QtWidgets.QTabWidget(self.analysis_page)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.real_time_analysis_tab = QtWidgets.QWidget()
        self.real_time_analysis_tab.setObjectName("real_time_analysis_tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.real_time_analysis_tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget = QtWidgets.QWidget(self.real_time_analysis_tab)
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.PWM15_progressBar = QtWidgets.QProgressBar(self.widget)
        self.PWM15_progressBar.setMaximum(24)
        self.PWM15_progressBar.setProperty("value", 24)
        self.PWM15_progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.PWM15_progressBar.setTextVisible(True)
        self.PWM15_progressBar.setObjectName("PWM15_progressBar")
        self.gridLayout.addWidget(self.PWM15_progressBar, 3, 7, 1, 1)
        self.PWM7_progressBar = QtWidgets.QProgressBar(self.widget)
        self.PWM7_progressBar.setMaximum(24)
        self.PWM7_progressBar.setProperty("value", 24)
        self.PWM7_progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.PWM7_progressBar.setTextVisible(True)
        self.PWM7_progressBar.setObjectName("PWM7_progressBar")
        self.gridLayout.addWidget(self.PWM7_progressBar, 0, 6, 1, 1)
        self.PWM2_progressBar = QtWidgets.QProgressBar(self.widget)
        self.PWM2_progressBar.setMaximum(24)
        self.PWM2_progressBar.setProperty("value", 24)
        self.PWM2_progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.PWM2_progressBar.setTextVisible(True)
        self.PWM2_progressBar.setObjectName("PWM2_progressBar")
        self.gridLayout.addWidget(self.PWM2_progressBar, 0, 5, 1, 1)
        self.PWM10_progressBar = QtWidgets.QProgressBar(self.widget)
        self.PWM10_progressBar.setMaximum(24)
        self.PWM10_progressBar.setProperty("value", 24)
        self.PWM10_progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.PWM10_progressBar.setTextVisible(True)
        self.PWM10_progressBar.setObjectName("PWM10_progressBar")
        self.gridLayout.addWidget(self.PWM10_progressBar, 3, 6, 1, 1)
        self.PWM6_progressBar = QtWidgets.QProgressBar(self.widget)
        self.PWM6_progressBar.setMaximum(24)
        self.PWM6_progressBar.setProperty("value", 24)
        self.PWM6_progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.PWM6_progressBar.setTextVisible(True)
        self.PWM6_progressBar.setObjectName("PWM6_progressBar")
        self.gridLayout.addWidget(self.PWM6_progressBar, 4, 5, 1, 1)
        self.PWM3_progressBar = QtWidgets.QProgressBar(self.widget)
        self.PWM3_progressBar.setMaximum(24)
        self.PWM3_progressBar.setProperty("value", 24)
        self.PWM3_progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.PWM3_progressBar.setTextVisible(True)
        self.PWM3_progressBar.setObjectName("PWM3_progressBar")
        self.gridLayout.addWidget(self.PWM3_progressBar, 1, 5, 1, 1)
        self.PWM8_progressBar = QtWidgets.QProgressBar(self.widget)
        self.PWM8_progressBar.setMaximum(24)
        self.PWM8_progressBar.setProperty("value", 24)
        self.PWM8_progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.PWM8_progressBar.setTextVisible(True)
        self.PWM8_progressBar.setObjectName("PWM8_progressBar")
        self.gridLayout.addWidget(self.PWM8_progressBar, 1, 6, 1, 1)
        self.PWM13_progressBar = QtWidgets.QProgressBar(self.widget)
        self.PWM13_progressBar.setMaximum(24)
        self.PWM13_progressBar.setProperty("value", 24)
        self.PWM13_progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.PWM13_progressBar.setTextVisible(True)
        self.PWM13_progressBar.setObjectName("PWM13_progressBar")
        self.gridLayout.addWidget(self.PWM13_progressBar, 1, 7, 1, 1)
        self.PWM1_progressBar = QtWidgets.QProgressBar(self.widget)
        self.PWM1_progressBar.setMaximum(24)
        self.PWM1_progressBar.setProperty("value", 24)
        self.PWM1_progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.PWM1_progressBar.setTextVisible(True)
        self.PWM1_progressBar.setObjectName("PWM1_progressBar")
        self.gridLayout.addWidget(self.PWM1_progressBar, 4, 4, 1, 1)
        self.PWM14_progressBar = QtWidgets.QProgressBar(self.widget)
        self.PWM14_progressBar.setMaximum(24)
        self.PWM14_progressBar.setProperty("value", 24)
        self.PWM14_progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.PWM14_progressBar.setTextVisible(True)
        self.PWM14_progressBar.setObjectName("PWM14_progressBar")
        self.gridLayout.addWidget(self.PWM14_progressBar, 2, 7, 1, 1)
        self.PWM5_progressBar = QtWidgets.QProgressBar(self.widget)
        self.PWM5_progressBar.setMaximum(24)
        self.PWM5_progressBar.setProperty("value", 24)
        self.PWM5_progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.PWM5_progressBar.setTextVisible(True)
        self.PWM5_progressBar.setObjectName("PWM5_progressBar")
        self.gridLayout.addWidget(self.PWM5_progressBar, 3, 5, 1, 1)
        self.PWM4_progressBar = QtWidgets.QProgressBar(self.widget)
        self.PWM4_progressBar.setMaximum(24)
        self.PWM4_progressBar.setProperty("value", 24)
        self.PWM4_progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.PWM4_progressBar.setTextVisible(True)
        self.PWM4_progressBar.setObjectName("PWM4_progressBar")
        self.gridLayout.addWidget(self.PWM4_progressBar, 2, 5, 1, 1)
        self.DO1_label = QtWidgets.QLabel(self.widget)
        self.DO1_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO1_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO1_label.setObjectName("DO1_label")
        self.gridLayout.addWidget(self.DO1_label, 0, 0, 1, 1)
        self.PWM11_progressBar = QtWidgets.QProgressBar(self.widget)
        self.PWM11_progressBar.setMaximum(24)
        self.PWM11_progressBar.setProperty("value", 24)
        self.PWM11_progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.PWM11_progressBar.setTextVisible(True)
        self.PWM11_progressBar.setObjectName("PWM11_progressBar")
        self.gridLayout.addWidget(self.PWM11_progressBar, 4, 6, 1, 1)
        self.PWM12_progressBar = QtWidgets.QProgressBar(self.widget)
        self.PWM12_progressBar.setMaximum(24)
        self.PWM12_progressBar.setProperty("value", 24)
        self.PWM12_progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.PWM12_progressBar.setTextVisible(True)
        self.PWM12_progressBar.setObjectName("PWM12_progressBar")
        self.gridLayout.addWidget(self.PWM12_progressBar, 0, 7, 1, 1)
        self.PWM9_progressBar = QtWidgets.QProgressBar(self.widget)
        self.PWM9_progressBar.setMaximum(24)
        self.PWM9_progressBar.setProperty("value", 24)
        self.PWM9_progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.PWM9_progressBar.setTextVisible(True)
        self.PWM9_progressBar.setObjectName("PWM9_progressBar")
        self.gridLayout.addWidget(self.PWM9_progressBar, 2, 6, 1, 1)
        self.PWM16_progressBar = QtWidgets.QProgressBar(self.widget)
        self.PWM16_progressBar.setMaximum(24)
        self.PWM16_progressBar.setProperty("value", 24)
        self.PWM16_progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.PWM16_progressBar.setTextVisible(True)
        self.PWM16_progressBar.setObjectName("PWM16_progressBar")
        self.gridLayout.addWidget(self.PWM16_progressBar, 4, 7, 1, 1)
        self.DO2_label = QtWidgets.QLabel(self.widget)
        self.DO2_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO2_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO2_label.setObjectName("DO2_label")
        self.gridLayout.addWidget(self.DO2_label, 1, 0, 1, 1)
        self.DO3_label = QtWidgets.QLabel(self.widget)
        self.DO3_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO3_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO3_label.setObjectName("DO3_label")
        self.gridLayout.addWidget(self.DO3_label, 2, 0, 1, 1)
        self.DO4_label = QtWidgets.QLabel(self.widget)
        self.DO4_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO4_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO4_label.setObjectName("DO4_label")
        self.gridLayout.addWidget(self.DO4_label, 3, 0, 1, 1)
        self.DO5_label = QtWidgets.QLabel(self.widget)
        self.DO5_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO5_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO5_label.setObjectName("DO5_label")
        self.gridLayout.addWidget(self.DO5_label, 4, 0, 1, 1)
        self.DO6_label = QtWidgets.QLabel(self.widget)
        self.DO6_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO6_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO6_label.setObjectName("DO6_label")
        self.gridLayout.addWidget(self.DO6_label, 0, 1, 1, 1)
        self.DO8_label = QtWidgets.QLabel(self.widget)
        self.DO8_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO8_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO8_label.setObjectName("DO8_label")
        self.gridLayout.addWidget(self.DO8_label, 2, 1, 1, 1)
        self.DO7_label = QtWidgets.QLabel(self.widget)
        self.DO7_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO7_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO7_label.setObjectName("DO7_label")
        self.gridLayout.addWidget(self.DO7_label, 1, 1, 1, 1)
        self.DO9_label = QtWidgets.QLabel(self.widget)
        self.DO9_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO9_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO9_label.setObjectName("DO9_label")
        self.gridLayout.addWidget(self.DO9_label, 3, 1, 1, 1)
        self.DO10_label = QtWidgets.QLabel(self.widget)
        self.DO10_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO10_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO10_label.setObjectName("DO10_label")
        self.gridLayout.addWidget(self.DO10_label, 4, 1, 1, 1)
        self.DO11_label = QtWidgets.QLabel(self.widget)
        self.DO11_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO11_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO11_label.setObjectName("DO11_label")
        self.gridLayout.addWidget(self.DO11_label, 0, 2, 1, 1)
        self.DO12_label = QtWidgets.QLabel(self.widget)
        self.DO12_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO12_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO12_label.setObjectName("DO12_label")
        self.gridLayout.addWidget(self.DO12_label, 1, 2, 1, 1)
        self.DO13_label = QtWidgets.QLabel(self.widget)
        self.DO13_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO13_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO13_label.setObjectName("DO13_label")
        self.gridLayout.addWidget(self.DO13_label, 2, 2, 1, 1)
        self.DO14_label = QtWidgets.QLabel(self.widget)
        self.DO14_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO14_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO14_label.setObjectName("DO14_label")
        self.gridLayout.addWidget(self.DO14_label, 3, 2, 1, 1)
        self.DO15_label = QtWidgets.QLabel(self.widget)
        self.DO15_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO15_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO15_label.setObjectName("DO15_label")
        self.gridLayout.addWidget(self.DO15_label, 4, 2, 1, 1)
        self.DO16_label = QtWidgets.QLabel(self.widget)
        self.DO16_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO16_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO16_label.setObjectName("DO16_label")
        self.gridLayout.addWidget(self.DO16_label, 0, 3, 1, 1)
        self.DO18_label = QtWidgets.QLabel(self.widget)
        self.DO18_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO18_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO18_label.setObjectName("DO18_label")
        self.gridLayout.addWidget(self.DO18_label, 2, 3, 1, 1)
        self.DO17_label = QtWidgets.QLabel(self.widget)
        self.DO17_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO17_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO17_label.setObjectName("DO17_label")
        self.gridLayout.addWidget(self.DO17_label, 1, 3, 1, 1)
        self.DO19_label = QtWidgets.QLabel(self.widget)
        self.DO19_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO19_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO19_label.setObjectName("DO19_label")
        self.gridLayout.addWidget(self.DO19_label, 3, 3, 1, 1)
        self.DO20_label = QtWidgets.QLabel(self.widget)
        self.DO20_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO20_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO20_label.setObjectName("DO20_label")
        self.gridLayout.addWidget(self.DO20_label, 4, 3, 1, 1)
        self.DO21_label = QtWidgets.QLabel(self.widget)
        self.DO21_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO21_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO21_label.setObjectName("DO21_label")
        self.gridLayout.addWidget(self.DO21_label, 0, 4, 1, 1)
        self.DO23_label = QtWidgets.QLabel(self.widget)
        self.DO23_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO23_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO23_label.setObjectName("DO23_label")
        self.gridLayout.addWidget(self.DO23_label, 2, 4, 1, 1)
        self.DO24_label = QtWidgets.QLabel(self.widget)
        self.DO24_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO24_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO24_label.setObjectName("DO24_label")
        self.gridLayout.addWidget(self.DO24_label, 3, 4, 1, 1)
        self.DO22_label = QtWidgets.QLabel(self.widget)
        self.DO22_label.setTextFormat(QtCore.Qt.PlainText)
        self.DO22_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DO22_label.setObjectName("DO22_label")
        self.gridLayout.addWidget(self.DO22_label, 1, 4, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.verticalLayout_4.addWidget(self.widget)
        self.ou_analysis_send_stacked = QtWidgets.QStackedWidget(self.real_time_analysis_tab)
        self.ou_analysis_send_stacked.setObjectName("ou_analysis_send_stacked")
        self.ou_analysis_page = QtWidgets.QWidget()
        self.ou_analysis_page.setObjectName("ou_analysis_page")
        self.label_3 = QtWidgets.QLabel(self.ou_analysis_page)
        self.label_3.setGeometry(QtCore.QRect(320, 170, 191, 51))
        self.label_3.setObjectName("label_3")
        self.ou_analysis_send_stacked.addWidget(self.ou_analysis_page)
        self.ou_simulator_page = QtWidgets.QWidget()
        self.ou_simulator_page.setObjectName("ou_simulator_page")
        self.label_4 = QtWidgets.QLabel(self.ou_simulator_page)
        self.label_4.setGeometry(QtCore.QRect(320, 150, 331, 101))
        self.label_4.setObjectName("label_4")
        self.ou_analysis_send_stacked.addWidget(self.ou_simulator_page)
        self.verticalLayout_4.addWidget(self.ou_analysis_send_stacked)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.IOQuery_pushButton = QtWidgets.QPushButton(self.real_time_analysis_tab)
        self.IOQuery_pushButton.setEnabled(False)
        self.IOQuery_pushButton.setMinimumSize(QtCore.QSize(0, 35))
        self.IOQuery_pushButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.IOQuery_pushButton.setObjectName("IOQuery_pushButton")
        self.horizontalLayout_3.addWidget(self.IOQuery_pushButton)
        self.send_package_pushButton = QtWidgets.QPushButton(self.real_time_analysis_tab)
        self.send_package_pushButton.setMinimumSize(QtCore.QSize(0, 35))
        self.send_package_pushButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.send_package_pushButton.setObjectName("send_package_pushButton")
        self.horizontalLayout_3.addWidget(self.send_package_pushButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.real_time_analysis_tab, "")
        self.history_tab = QtWidgets.QWidget()
        self.history_tab.setObjectName("history_tab")
        self.tabWidget.addTab(self.history_tab, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.sub_interface_stacked.addWidget(self.analysis_page)
        self.horizontalLayout_2.addWidget(self.sub_interface_stacked)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 15)
        self.verticalLayout.addWidget(self.Body)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 15)
        KCTS.setCentralWidget(self.Window)

        self.retranslateUi(KCTS)
        self.sub_interface_stacked.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(KCTS)

    def retranslateUi(self, KCTS):
        _translate = QtCore.QCoreApplication.translate
        KCTS.setWindowTitle(_translate("KCTS", "KCTS"))
        self.system_label.setText(_translate("KCTS", "KCTS"))
        self.pushButton.setText(_translate("KCTS", "选择项目"))
        self.pushButton_2.setText(_translate("KCTS", "生成报告"))
        self.pushButton_3.setText(_translate("KCTS", "……"))
        self.label.setText(_translate("KCTS", "这是设备状态界面"))
        self.kc_ts_send_tu_port_label.setText(_translate("KCTS", "send_tu_port :"))
        self.kc_ts_send_mu_port_label.setText(_translate("KCTS", "send_mu_port :"))
        self.kc_ts_recv_port_label.setText(_translate("KCTS", "recv_TU_port :"))
        self.kc_ts_ip_label.setText(_translate("KCTS", "KC-TS IP:"))
        self.mu_ip_label.setText(_translate("KCTS", "MU IP :"))
        self.recv_ou_port_label.setText(_translate("KCTS", "recv_OU_prot :"))
        self.mu_recv_port_label.setText(_translate("KCTS", "MU recv_port :"))
        self.kc_tu_ip_label.setText(_translate("KCTS", "KC-TU IP :"))
        self.kc_tu_recv_port_label.setText(_translate("KCTS", "KC-TU recv_port :"))
        self.apply_pushButton.setText(_translate("KCTS", "应用"))
        self.label_2.setText(_translate("KCTS", "这是自动化测试界面"))
        self.PWM15_progressBar.setFormat(_translate("KCTS", "PWM15{%vV}"))
        self.PWM7_progressBar.setFormat(_translate("KCTS", "PWM7{%vV}"))
        self.PWM2_progressBar.setFormat(_translate("KCTS", "PWM2{%vV}"))
        self.PWM10_progressBar.setFormat(_translate("KCTS", "PWM10{%vV}"))
        self.PWM6_progressBar.setFormat(_translate("KCTS", "PWM6{%vV}"))
        self.PWM3_progressBar.setFormat(_translate("KCTS", "PWM3{%vV}"))
        self.PWM8_progressBar.setFormat(_translate("KCTS", "PWM8{%vV}"))
        self.PWM13_progressBar.setFormat(_translate("KCTS", "PWM13{%vV}"))
        self.PWM1_progressBar.setFormat(_translate("KCTS", "PWM1{%vV}"))
        self.PWM14_progressBar.setFormat(_translate("KCTS", "PWM14{%vV}"))
        self.PWM5_progressBar.setFormat(_translate("KCTS", "PWM5{%vV}"))
        self.PWM4_progressBar.setFormat(_translate("KCTS", "PWM4{%vV}"))
        self.DO1_label.setText(_translate("KCTS", "DO1"))
        self.PWM11_progressBar.setFormat(_translate("KCTS", "PWM11{%vV}"))
        self.PWM12_progressBar.setFormat(_translate("KCTS", "PWM12{%vV}"))
        self.PWM9_progressBar.setFormat(_translate("KCTS", "PWM9{%vV}"))
        self.PWM16_progressBar.setFormat(_translate("KCTS", "PWM16{%vV}"))
        self.DO2_label.setText(_translate("KCTS", "DO2"))
        self.DO3_label.setText(_translate("KCTS", "DO3"))
        self.DO4_label.setText(_translate("KCTS", "DO4"))
        self.DO5_label.setText(_translate("KCTS", "DO5"))
        self.DO6_label.setText(_translate("KCTS", "DO6"))
        self.DO8_label.setText(_translate("KCTS", "DO8"))
        self.DO7_label.setText(_translate("KCTS", "DO7"))
        self.DO9_label.setText(_translate("KCTS", "DO9"))
        self.DO10_label.setText(_translate("KCTS", "DO10"))
        self.DO11_label.setText(_translate("KCTS", "DO11"))
        self.DO12_label.setText(_translate("KCTS", "DO12"))
        self.DO13_label.setText(_translate("KCTS", "DO13"))
        self.DO14_label.setText(_translate("KCTS", "DO14"))
        self.DO15_label.setText(_translate("KCTS", "DO15"))
        self.DO16_label.setText(_translate("KCTS", "DO16"))
        self.DO18_label.setText(_translate("KCTS", "DO18"))
        self.DO17_label.setText(_translate("KCTS", "DO17"))
        self.DO19_label.setText(_translate("KCTS", "DO19"))
        self.DO20_label.setText(_translate("KCTS", "DO20"))
        self.DO21_label.setText(_translate("KCTS", "DO21"))
        self.DO23_label.setText(_translate("KCTS", "DO23"))
        self.DO24_label.setText(_translate("KCTS", "DO24"))
        self.DO22_label.setText(_translate("KCTS", "DO22"))
        self.label_3.setText(_translate("KCTS", "这是OU解析的界面"))
        self.label_4.setText(_translate("KCTS", "这是OU模拟器的界面"))
        self.IOQuery_pushButton.setText(_translate("KCTS", "IO查询"))
        self.send_package_pushButton.setText(_translate("KCTS", "模拟发包"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.real_time_analysis_tab), _translate("KCTS", "实时解析"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.history_tab), _translate("KCTS", "历史记录"))
