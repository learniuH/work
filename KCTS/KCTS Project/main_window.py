from PyQt5.QtCore import Qt, QSettings, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QListView, QHeaderView, QTableWidgetItem, \
    QProgressBar, QLabel, QSpacerItem, QSizePolicy, QTextEdit, QGridLayout, QSlider, QLineEdit

from UI.main_window_ui import Ui_KCTS

from config.validators import Validators
from config.qss import QLabelStyleSheet, AnalogStyleSheet
from services.network import NetworkManager
from services.read_excel import ExcelRead
from services.ou_simulator import OUSimulator
from services.package_send import PackageToMu
from services.serial_port_assistant import SerialPortAsst

from widget.checkbox import LearniuHCheckBox
from widget.combobox import LearniuHComboBox
from widget.pushbutton import LearniuHPushButton
from widget.lineedit import LearniuHLineEdit
from widget.slider import LearniuHSlider
from widget.spacer import LearniuHSpacer
from widget.constant import ConstantText, SendCycle

import sys
import socket
import copy
from datetime import datetime
from typing import Union


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_window_ui = Ui_KCTS()     # 主界面的 UI 实例
        self.main_window_ui.setupUi(self)   # 将 UI 加载到 MainWindow 上

        self.load_last_content()            # 加载上一次运行时的配置

        self.network_manager = NetworkManager()     # 初始化网络管理器

        self.function_definition: dict = None       # 线号与UI控件绑定
        self.previous_ou_parsed: dict = None        # 记录上一帧OU解析的结果
        self.previous_mu_parsed: dict = None        # 记录上一帧MU解析的结果

        self.excel_reader = None                    # 读取Excel文件实例
        self.serial_port_asst = None                # 串口助手

        self.main_window_init()     # 窗口界面初始化
        self.serial_port_init()     # 初始化串口助手

        self.setup_validators()     # 正则表达式匹配 IP 端口 信息
        self.setup_connections()    # 控件信号连接绑定
        self.signal_bind()          # pyqtSignal 信号绑定, 控件与线号连接

    def load_last_content(self):
        ''' 加载上一次程序运行时的相关配置 '''
        settings = QSettings('KCTS', 'CONFIGURE')
        self.main_window_ui.kc_ts_recv_tu_port_lineEdit.setText(settings.value('KCTS_recv_tu_port_content', ''))
        self.main_window_ui.kc_ts_send_tu_port_lineEdit.setText(settings.value('KCTS_send_tu_port_content', ''))
        self.main_window_ui.kc_ts_recv_ou_port_lineEdit.setText(settings.value('KCTS_recv_ou_port_content', ''))
        self.main_window_ui.kc_ts_send_mu_port_lineEdit.setText(settings.value('KCTS_send_mu_port_content', ''))
        self.main_window_ui.mu_ip_lineEdit.setText(settings.value('MU_IP_content', ''))
        self.main_window_ui.mu_recv_port_lineEdit.setText(settings.value('MU_recv_port_content', ''))
        self.main_window_ui.kc_tu_ip_lineEdit.setText(settings.value('KCTU_IP_content', ''))
        self.main_window_ui.kc_tu_recv_port_lineEdit.setText(settings.value('KCTU_recv_port_content', ''))
        self.main_window_ui.lineEdit_package_header.setText(settings.value('OU_simulator_package_head', ''))

    def setup_validators(self):
        ''' 设置输入验证器 '''
        self.main_window_ui.kc_ts_ip_lineEdit.setValidator(Validators.get_ipv4_validator())             # KCTS IP 验证器
        self.main_window_ui.kc_ts_recv_tu_port_lineEdit.setValidator(Validators.get_port_validator())   # KCTS 接收端口验证器
        self.main_window_ui.kc_ts_send_tu_port_lineEdit.setValidator(Validators.get_port_validator())   # KCTS 发送端口验证器
        self.main_window_ui.kc_ts_recv_ou_port_lineEdit.setValidator(Validators.get_port_validator())   # KCTS 接收端口验证器
        self.main_window_ui.kc_ts_send_mu_port_lineEdit.setValidator(Validators.get_port_validator())   # KCTS 发送端口验证器
        self.main_window_ui.mu_ip_lineEdit.setValidator(Validators.get_ipv4_validator())            # MU IP 验证器
        self.main_window_ui.mu_recv_port_lineEdit.setValidator(Validators.get_port_validator())     # MU 接收端口验证器
        self.main_window_ui.kc_tu_ip_lineEdit.setValidator(Validators.get_ipv4_validator())         # KCTU IP 验证器
        self.main_window_ui.kc_tu_recv_port_lineEdit.setValidator(Validators.get_port_validator())  # KCTU 接收端口验证器
        self.main_window_ui.lineEdit_package_header.setValidator(Validators.get_hex_validator())    # 十六进制组合验证器

    def setup_connections(self):
        ''' 设置信号连接 '''
        # 通过 QlistWidget 当前的 item 变化来切换 QStackedWidget 中的序号
        self.main_window_ui.navigation_list.currentRowChanged.connect(self.switch_sub_interface_stacked_page)

        self.main_window_ui.apply_pushButton.clicked.connect(self.apply_current_configuration)
        self.main_window_ui.IOQuery_pushButton.clicked.connect(lambda: self.switch_ou_analysis_send_stacked_page(index=0))
        self.main_window_ui.send_package_pushButton.clicked.connect(lambda: self.switch_ou_analysis_send_stacked_page(index=1))

        # 点击导入协议, 打开选择对话框
        self.main_window_ui.import_protocol_pushButton.clicked.connect(self.open_file_dialog)
        # comboBox 的 index 改变时, 解析表单
        self.main_window_ui.sheet_name_list_comboBox.currentIndexChanged.connect(self.parse_excel)

        # header lineEdit 改变时, 改变发给MU包的包头
        self.main_window_ui.lineEdit_package_header.textChanged.connect(lambda: PackageToMu.update_package_header(self.main_window_ui.lineEdit_package_header))

        # checkBox 的状态改变时, 切换去重和不去重两个界面
        self.main_window_ui.deduplication_checkBox.stateChanged.connect(self.history_interface_switch)

        self.main_window_ui.clear_record_pushButton.clicked.connect(self.clear_history_record)


    def signal_bind(self):
        ''' 绑定 pyqtSignal 到对应事件与按键 '''
        self.network_manager.tu_package_receiver.update_do_signal.connect(self.update_do_label_status)          # 用于更新MU数据显示区
        self.network_manager.tu_package_receiver.update_pwm_signal.connect(self.update_pwm_progressBar_status)  # 用于更新MU数据显示区
        self.network_manager.tu_package_receiver.mu_output_record_signal.connect(self.update_mu_history_record) # 更新历史记录中MU的输出
        self.network_manager.program_exception_signal.connect(self.top_hint_display)                            # 更新提示

        # 将 DO PWM 信号与UI控件绑定
        self.function_definition = {
            'DO1':   self.main_window_ui.DO1_label,
            'DO2':   self.main_window_ui.DO2_label,
            'DO3':   self.main_window_ui.DO3_label,
            'DO4':   self.main_window_ui.DO4_label,
            'DO5':   self.main_window_ui.DO5_label,
            'DO6':   self.main_window_ui.DO6_label,
            'DO7':   self.main_window_ui.DO7_label,
            'DO8':   self.main_window_ui.DO8_label,
            'DO9':   self.main_window_ui.DO9_label,
            'DO10':  self.main_window_ui.DO10_label,
            'DO11':  self.main_window_ui.DO11_label,
            'DO12':  self.main_window_ui.DO12_label,
            'DO13':  self.main_window_ui.DO13_label,
            'DO14':  self.main_window_ui.DO14_label,
            'DO15':  self.main_window_ui.DO15_label,
            'DO16':  self.main_window_ui.DO16_label,
            'DO17':  self.main_window_ui.DO17_label,
            'DO18':  self.main_window_ui.DO18_label,
            'DO19':  self.main_window_ui.DO19_label,
            'DO20':  self.main_window_ui.DO20_label,
            'DO21':  self.main_window_ui.DO21_label,
            'DO22':  self.main_window_ui.DO22_label,
            'DO23':  self.main_window_ui.DO23_label,
            'DO24':  self.main_window_ui.DO24_label,
            'PWM1':  self.main_window_ui.PWM1_progressBar,
            'PWM2':  self.main_window_ui.PWM2_progressBar,
            'PWM3':  self.main_window_ui.PWM3_progressBar,
            'PWM4':  self.main_window_ui.PWM4_progressBar,
            'PWM5':  self.main_window_ui.PWM5_progressBar,
            'PWM6':  self.main_window_ui.PWM6_progressBar,
            'PWM7':  self.main_window_ui.PWM7_progressBar,
            'PWM8':  self.main_window_ui.PWM8_progressBar,
            'PWM9':  self.main_window_ui.PWM9_progressBar,
            'PWM10': self.main_window_ui.PWM10_progressBar,
            'PWM11': self.main_window_ui.PWM11_progressBar,
            'PWM12': self.main_window_ui.PWM12_progressBar,
            'PWM13': self.main_window_ui.PWM13_progressBar,
            'PWM14': self.main_window_ui.PWM14_progressBar,
            'PWM15': self.main_window_ui.PWM15_progressBar,
            'PWM16': self.main_window_ui.PWM16_progressBar
        }

    def update_do_label_status(self, do_num: str, do_status: bool):
        ''' 接收来自 pyqtSignal 的信号, 更新 QLabel 状态 '''
        do_label = self.function_definition[do_num]
        # DO 输出时, label 会显示橙色, DO 为0时, 显示白色
        if do_status is True:
            do_label.setStyleSheet(QLabelStyleSheet.LABEL_QSS_HIGHLIGHT)
        else:
            do_label.setStyleSheet(QLabelStyleSheet.LABEL_QSS_NORMAL)

    def update_pwm_progressBar_status(self, pwm_num: str, pwm_value: int):
        ''' 接收来自 pyqtSignal 的信号, 更新 QLabel 状态 '''
        pwm_progressBar = self.function_definition[pwm_num]
        value = pwm_value / 100
        # 进度条显示 PWM 值, 保留两位小数
        pwm_progressBar.setValue(value)
        pwm_progressBar.setFormat(f'{pwm_num}: {value:.2f}V')


    def main_window_init(self):
        ''' 主程序启动时, 启动监听OU数据和TU数据的线程 '''
        self.listening_ou_thread_init()
        self.listening_tu_thread_init()

        # comboBox 初始化 使QSS的配置生效
        self.main_window_ui.sheet_name_list_comboBox.setView(QListView())

        # tableWidget item 宽度自适应窗口宽度
        self.main_window_ui.ou_analysis_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 禁用中文输入法, 解决点击 lineEdit 为中文输入法的问题
        self.main_window_ui.lineEdit_package_header.setAttribute(Qt.WA_InputMethodEnabled, False)

        # 隐藏顶部的top hint 提示
        self.main_window_ui.top_hint_label.setVisible(False)

    def listening_ou_thread_init(self):
        # 启动监听OU数据的线程
        current_configuration = self.update_current_configuration()
        self.network_manager.start_receiving_ou(current_configuration['local_ip'],
                                                current_configuration['recv_ou_port'],
                                                current_configuration['mu_ip'],
                                                current_configuration['mu_recv_port']
                                                )

    def listening_tu_thread_init(self):
        current_configuration = self.update_current_configuration()
        # 启动监听TU数据的线程
        self.network_manager.start_receiving_tu(current_configuration['local_ip'],
                                                current_configuration['recv_tu_port']
                                                )

    def update_current_configuration(self):
        ''' 获取当前设备状态页文本框的内容 '''
        # 更新当前电脑的 IP
        local_ip = socket.gethostbyname(socket.gethostname())
        self.main_window_ui.kc_ts_ip_lineEdit.setText(local_ip)

        # 获取当前文本框中的配置
        recv_tu_port = self.main_window_ui.kc_ts_recv_tu_port_lineEdit.text()
        send_tu_port = self.main_window_ui.kc_ts_send_tu_port_lineEdit.text()
        recv_ou_port = self.main_window_ui.kc_ts_recv_ou_port_lineEdit.text()
        send_mu_port = self.main_window_ui.kc_ts_send_mu_port_lineEdit.text()

        mu_ip = self.main_window_ui.mu_ip_lineEdit.text()
        mu_recv_port = self.main_window_ui.mu_recv_port_lineEdit.text()

        kctu_ip = self.main_window_ui.kc_tu_ip_lineEdit.text()
        kctu_recv_port = self.main_window_ui.kc_tu_recv_port_lineEdit.text()

        current_configuration = {
            'local_ip': local_ip,
            'recv_tu_port': recv_tu_port,
            'send_tu_port': send_tu_port,
            'recv_ou_port': recv_ou_port,
            'send_mu_port': send_mu_port,
            'mu_ip': mu_ip,
            'mu_recv_port': mu_recv_port,
            'kctu_ip': kctu_ip,
            'kctu_recv_port': kctu_recv_port
        }
        return current_configuration


    def switch_sub_interface_stacked_page(self, index: int):
        ''' listWidget 的 item 切换 stackedWidget 的子界面 '''
        self.main_window_ui.sub_interface_stacked.setCurrentIndex(index)

        # 切换到输出查询界面, index == 2(输出查询页面)时, 往TU一直发包采集MU状态
        if index == 2:
            self.sending_tu_thread_init()   # 开始往TU发包

            # 同时在OU模拟器界面, 暂停接收OU的数据, 开启往MU发包
            if self.main_window_ui.ou_analysis_send_stacked.currentIndex() == 1:
                self.network_manager.stop_receiving_ou()
                self.sending_mu_thread_init()

        # 切换到非输出查询界面, 停止给TU发包
        else:
            self.network_manager.stop_sending_tu()
            # 如果同时在主动给MU发包, 就关闭给MU发数据的线程, 恢复监听OU的线程
            if self.network_manager.is_sending_mu:
                self.network_manager.stop_sending_mu()
                self.listening_ou_thread_init()

    def apply_current_configuration(self):
        ''' 点击应用, 停止所有收发的线程, 更新配置后重新启用 '''
        self.network_manager.stop_receiving_ou()
        self.network_manager.stop_receiving_tu()

        # 启动两个监听的线程
        self.listening_ou_thread_init()
        self.listening_tu_thread_init()

    def sending_tu_thread_init(self):
        ''' 初始化给TU发送数据的线程 '''
        current_configuration = self.update_current_configuration()
        self.network_manager.start_sending_tu(current_configuration['local_ip'],
                                              current_configuration['send_tu_port'],
                                              current_configuration['kctu_ip'],
                                              current_configuration['kctu_recv_port'],
                                              SendCycle.CYCLE
                                              )

    def sending_mu_thread_init(self):
        ''' 初始化给MU发送数据的线程 '''
        current_configuration = self.update_current_configuration()
        self.network_manager.start_sending_mu(current_configuration['local_ip'],
                                              current_configuration['send_mu_port'],
                                              current_configuration['mu_ip'],
                                              current_configuration['mu_recv_port'],
                                              SendCycle.CYCLE
                                              )

    def switch_ou_analysis_send_stacked_page(self, index: int):
        ''' 点击 pushButton 切换 OU 解析界面和发包界面 '''
        self.main_window_ui.ou_analysis_send_stacked.setCurrentIndex(index)

        # OU 解析界面, IO查询禁用, 模拟发包使能, 关闭往MU发包的线程, 启动接收OU数据线程
        if index == 0:
            self.network_manager.stop_sending_mu()
            self.listening_ou_thread_init()
            self.main_window_ui.IOQuery_pushButton.setDisabled(True)
            self.main_window_ui.send_package_pushButton.setEnabled(True)
            # 隐藏 OU 模拟器的包头 lineEdit
            self.main_window_ui.lineEdit_package_header.setDisabled(True)


        # 模拟发包界面, IO查询使能, 模拟发包禁用, 关闭接收OU数据的线程, 启动往MU发包线程
        elif index == 1:# and not self.network_manager.is_sending_mu:
            self.network_manager.stop_receiving_ou()
            self.sending_mu_thread_init()
            self.main_window_ui.IOQuery_pushButton.setEnabled(True)
            self.main_window_ui.send_package_pushButton.setDisabled(True)
            # 展示 OU 模拟器的包头 lineEdit
            self.main_window_ui.lineEdit_package_header.setEnabled(True)

    def open_file_dialog(self):
        ''' 打开文件选择对话框, 只显示 Excel 文件 '''
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择项目通信协议', '', 'Excel Files (*.xlsx *xls);;All Files (*)'
        )
        if file_path:
            # 暂时屏蔽信号, 避免清除 items 和 添加 items 的时候误触发函数
            self.main_window_ui.sheet_name_list_comboBox.blockSignals(True)

            self.main_window_ui.sheet_name_list_comboBox.clear()    # 清除所有items
            # 读取 Excel 中的所有表单显示在 comboBox 上
            self.excel_reader = ExcelRead(file_path)
            # 绑定程序异常信号到函数, 用于显示错误提示信息
            self.excel_reader.program_exception_signal.connect(self.top_hint_display)

            sheet_list = self.excel_reader.read_sheet_name()
            # 添加excel里面的表单
            self.main_window_ui.sheet_name_list_comboBox.addItems(sheet_list)

            # 恢复信号
            self.main_window_ui.sheet_name_list_comboBox.blockSignals(False)

    def parse_excel(self, index: int):
        ''' comboBox 的 item 变化时, 会解析当前选择的表单 '''
        # 获取所选择表单(comboBox item)的名字
        sheet_name = self.main_window_ui.sheet_name_list_comboBox.currentText()
        # 解析所选表单的Excel
        protocol, protocol_length = self.excel_reader.read_file(sheet_name)

        # 
        if protocol != {}:
            # 实例化解析OU包的类
            self.network_manager.ou_package_receiver_inst(protocol)

            # 将信号 PackageFromOU 解析后的包发出的 pyqtSignal 信号绑定到函数
            self.network_manager.ou_package_receiver.update_switch_signal.connect(self.update_ou_analysis_interface)    # 更新OU解析界面
            self.network_manager.ou_package_receiver.update_switch_signal.connect(self.update_history_record)   # 更新历史记录


            # 表单解析完成后 模拟器按钮使能
            self.main_window_ui.send_package_pushButton.setEnabled(True)
            # 更新 OU 模拟器 UI
            self.update_ou_simulator(protocol)
            OUSimulator.key_button = {}
            # OU模拟器组包
            PackageToMu.generate_package(protocol_length)
            # 实例化后创建 OU 模拟器, 更新 lineEdit 里面的包头
            PackageToMu.update_package_header(self.main_window_ui.lineEdit_package_header)

    def switch_quantity_generation(self, byte_num: int, bit_index: Union[int, str], description: str, row: int):
        ''' 开关量区域: checkBox pushButton lineEdit '''
        col = 0
        if row // ConstantText.WIDGET_PER_COL >= 1:  # 每列最多 13 个开关
            col += (row // ConstantText.WIDGET_PER_COL) * (3 + 1)
            if row % ConstantText.WIDGET_PER_COL == 0:
                # 换行时, 在换行的左边一列的首行添加 spacer 作为间隔
                spacer = LearniuHSpacer()
                self.main_window_ui.gridLayout_switch.addItem(spacer, row % ConstantText.WIDGET_PER_COL, col - 1)
        row %= ConstantText.WIDGET_PER_COL

        checkBox = LearniuHCheckBox(byte_num, bit_index)
        self.main_window_ui.gridLayout_switch.addWidget(checkBox, row, col)

        pushButton = LearniuHPushButton(description, byte_num, bit_index)
        self.main_window_ui.gridLayout_switch.addWidget(pushButton, row, col + 1)

        lineEdit = LearniuHLineEdit(byte_num, bit_index)
        self.main_window_ui.gridLayout_switch.addWidget(lineEdit, row, col + 2)
        lineEdit.setAttribute(Qt.WA_InputMethodEnabled, False)      # 禁用中文输入法

        # 控件绑定事件函数
        checkBox.stateChanged.connect(lambda: OUSimulator.checkBox_status_changed(checkBox, pushButton))

        pushButton.pressed.connect(lambda: OUSimulator.switch_pushButton_pressed(pushButton))
        pushButton.released.connect(lambda: OUSimulator.switch_pushButton_released(pushButton))

        lineEdit.setValidator(Validators.get_key_validator())
        lineEdit.textChanged.connect(lambda: OUSimulator.lineEdit_text_changed(lineEdit, pushButton, checkBox=checkBox))

    def analog_quantity_generation(self, byte_num: Union[int, str], description: str, row: int):
        ''' 模拟量区域: pushButton lineEdit slider '''
        col = 0
        if row // ConstantText.WIDGET_PER_COL >= 1:      # 每列最多 13 个开关
            col += (row // ConstantText.WIDGET_PER_COL) * (3 + 1)
            if row % ConstantText.WIDGET_PER_COL == 0:
                # 换行时, 在换行的左边一列的首行添加 spacer 作为间隔
                spacer = LearniuHSpacer()
                self.main_window_ui.gridLayout_analog.addItem(spacer, row % ConstantText.WIDGET_PER_COL, col - 1)
        row %= ConstantText.WIDGET_PER_COL

        pushButton = LearniuHPushButton(description, byte_num)
        self.main_window_ui.gridLayout_analog.addWidget(pushButton, row, col)

        lineEdit = LearniuHLineEdit(byte_num)
        self.main_window_ui.gridLayout_analog.addWidget(lineEdit, row, col + 1)
        lineEdit.setAttribute(Qt.WA_InputMethodEnabled, False)

        slider = LearniuHSlider(byte_num)
        self.main_window_ui.gridLayout_analog.addWidget(slider, row, col + 2)

        # 将控件绑定事件函数
        pushButton.pressed.connect(lambda: OUSimulator.analog_pushButton_pressed(pushButton))
        pushButton.released.connect(lambda: OUSimulator.analog_pushButton_released(pushButton))

        pushButton.timer_increase.timeout.connect(lambda: OUSimulator.slider_value_increase(pushButton.timer_increase, slider))
        pushButton.timer_decrease.timeout.connect(lambda: OUSimulator.slider_value_decrease(pushButton.timer_decrease, slider))

        lineEdit.setValidator(Validators.get_key_validator())
        lineEdit.textChanged.connect(lambda: OUSimulator.lineEdit_text_changed(lineEdit, pushButton,slider=slider))

        slider.valueChanged.connect(lambda: OUSimulator.slider_value_changed(slider))

        # slider.slider_overflow_signal.connect(self.top_hint_display)

    def update_ou_simulator(self, protocol: dict):
        ''' 更新 OU 模拟器的 UI '''
        self.clear_analogGrid_layout(self.main_window_ui.gridLayout_switch)
        self.clear_analogGrid_layout(self.main_window_ui.gridLayout_analog)
        switch_row, analog_row = 0, 0   # 在 gridLayout 中的行号
        for byte_num in protocol:
            # 开关量
            if isinstance(protocol[byte_num], dict):
                for bit_index, description in protocol[byte_num].items():
                    # 生成自定义控件
                    self.switch_quantity_generation(byte_num, bit_index, description, switch_row)
                    switch_row += 1
            # 模拟量
            else:
                self.analog_quantity_generation(byte_num, protocol[byte_num], analog_row)
                analog_row += 1

    def top_hint_display(self, tips: str):
        ''' 接收来自 read_file 函数(解析Excel表单) 的报错, 将提示信息在主界面显示2S '''
        self.main_window_ui.top_hint_label.setVisible(True)
        self.main_window_ui.top_hint_label.setText(tips)

        # 2S后将提示信息隐藏
        QTimer.singleShot(2000, lambda: self.main_window_ui.top_hint_label.setVisible(False))


    def update_ou_analysis_interface(self, package_parsed: dict):
        ''' 接收 pyqtSignal 信号, 对解析界面的 tableWidget 和 模拟量区域进行状态更新 '''
        self.main_window_ui.ou_analysis_table.setRowCount(0)   # 设置tableWidget行数为0 清空所有行
        self.clear_analogGrid_layout(self.main_window_ui.analog_gridlayout)      # 清除模拟量解析区的所有控件
        gridLayout_col = 0  # 模拟量解析区的列号
        for byte_num in package_parsed:
            # 如果字典的值是字典, 就是开关量, 更新tableWidget
            if isinstance(package_parsed.get(byte_num), dict):
                # 在tableWidget当前行后面添加一个空行, 垂直表头是 byte_num
                row_position = self.main_window_ui.ou_analysis_table.rowCount()
                self.main_window_ui.ou_analysis_table.insertRow(row_position)
                self.main_window_ui.ou_analysis_table.setVerticalHeaderItem(row_position, QTableWidgetItem(f'Byte{byte_num}'))

                for bit_index in package_parsed[byte_num]:
                    # bit_index 是数字, 就是一位为一个开关
                    if isinstance(bit_index, int):
                        # 将内容添加到当前行, 居中填充
                        item = QTableWidgetItem(package_parsed[byte_num][bit_index])
                        item.setTextAlignment(Qt.AlignCenter)
                        self.main_window_ui.ou_analysis_table.setItem(row_position, 7 - bit_index, item)

                    # bit_index 是字符串, 就是多位为一个开关
                    else:
                        bit_index_start, bit_index_end = bit_index.split('-')
                        index_start, index_end = int(bit_index_start), int(bit_index_end)
                        # 合并单元格: 四个参数 (起始行, 起始列, 行跨度, 列跨度)
                        self.main_window_ui.ou_analysis_table.setSpan(row_position, 7 - index_end, 1, index_end - index_start + 1)
                        # 居中填入内容
                        item = QTableWidgetItem(package_parsed[byte_num][bit_index])
                        item.setTextAlignment(Qt.AlignCenter)
                        self.main_window_ui.ou_analysis_table.setItem(row_position, 7 - index_end, item)

            # 如果字典的值是列表, 就是模拟量, 更新progressBar
            else:
                # 单个字节的模拟量
                if isinstance(byte_num, int):
                    # 创建垂直居中在gridLayout中的进度条
                    progressBar = QProgressBar()
                    progressBar.setOrientation(Qt.Vertical)
                    progressBar.setValue(package_parsed[byte_num][1])   # 进度条范围默认0-100
                    progressBar.setTextVisible(False)
                    progressBar.setStyleSheet(AnalogStyleSheet.ProgressBar_QSS)

                    # 创建居中在gridLayout中的label
                    label = QLabel(f'Byte{byte_num}: {package_parsed[byte_num][1]}\n{package_parsed[byte_num][0]}')
                    label.setAlignment(Qt.AlignCenter)
                    label.setStyleSheet(AnalogStyleSheet.Label_QSS)

                    # 进度条居中放在gridLayout第一行
                    self.main_window_ui.analog_gridlayout.addWidget(progressBar, 0, gridLayout_col,
                                                                    alignment=Qt.AlignCenter)
                    # 标签居中放在gridLayout第二行
                    self.main_window_ui.analog_gridlayout.addWidget(label, 1, gridLayout_col, alignment=Qt.AlignCenter)

                    # 列号每个字节结束加1
                    gridLayout_col += 1
                # 多个字节的模拟量
                else:
                    # 创建垂直居中在gridLayout的进度条
                    progressBar = QProgressBar()
                    progressBar.setOrientation(Qt.Vertical)
                    start_byte, end_byte = byte_num.split('-')
                    start_byte_num, end_byte_num = int(start_byte), int(end_byte)
                    maximum = 0    # 进度条的最大值
                    for i in range(0, end_byte_num - start_byte_num + 1):
                        maximum = (maximum << 8) + 0xFF
                    progressBar.setRange(0, maximum)
                    progressBar.setValue(package_parsed[byte_num][1])
                    progressBar.setTextVisible(False)
                    progressBar.setStyleSheet(AnalogStyleSheet.ProgressBar_QSS)

                    # 创建居中在gridLayout中的label
                    label = QLabel(f'Byte{byte_num}: {package_parsed[byte_num][1]}\n{package_parsed[byte_num][0]}')
                    label.setAlignment(Qt.AlignCenter)
                    label.setStyleSheet(AnalogStyleSheet.Label_QSS)

                    # 进度条居中放在gridLayout第一行
                    self.main_window_ui.analog_gridlayout.addWidget(progressBar, 0, gridLayout_col,
                                                                    alignment=Qt.AlignCenter)
                    # 标签居中放在gridLayout第二行
                    self.main_window_ui.analog_gridlayout.addWidget(label, 1, gridLayout_col, alignment=Qt.AlignCenter)

                    # 列号每个字节结束加1
                    gridLayout_col += 1

        # 所有数据添加到界面上后, 在gridLayout的两行加上两个水平弹簧
        for row in range(0,2):
            horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.main_window_ui.analog_gridlayout.addItem(horizontal_spacer, row, gridLayout_col)

    def clear_analogGrid_layout(self, grid_layout: QGridLayout):
        ''' 删除 gridLayout 里的所有控件 '''
        # 如果布局中还有控件
        while grid_layout.count():
            # 获取第一个控件项
            item = grid_layout.takeAt(0)
            widget = item.widget()      # 获取控件
            if widget is not None:
                widget.deleteLater()    # 删除控件

    def history_interface_switch(self, state):
        ''' 点击 checkBox 时, 切换stacked界面 '''
        if state == 2: # ckeckBox 选中时, state == 2
            self.main_window_ui.history_record_stacked.setCurrentIndex(1)
        else:
            self.main_window_ui.history_record_stacked.setCurrentIndex(0)

    def insert_ou_parsed_result(self, textEdit: QTextEdit, package_parsed: dict):
        ''' 填入解析后的OU的数据到textEdit '''
        # 打印系统当前的时间, 2024-12-03 14:30:45.123, 精确到 ms
        current_time = datetime.now()  # 获取系统当前的时间, ms精确到小数点后6位
        textEdit.append(current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

        # 先添加OU的包
        ou_package = 'OU Data: ' + f'  '.join(f'{byte:02X}' for byte in self.network_manager.ou_package_recv)
        textEdit.append(ou_package)  # 添加OU_package自动换行

        # OU包解析结果
        for byte_num in package_parsed:
            textEdit.append(f'Byte{byte_num}: ')
            # 字典就是开关量
            if isinstance(package_parsed.get(byte_num), dict):
                for bit_index in package_parsed[byte_num]:
                    textEdit.insertPlainText(
                        f'bit{bit_index} - {package_parsed[byte_num][bit_index]}    ')
            # 列表就是模拟量
            else:
                textEdit.insertPlainText(
                    f'{package_parsed[byte_num][0]}  {package_parsed[byte_num][1]}')

        textEdit.insertPlainText(f'\n')  # 每一包内容结束之后换行

    def update_history_record(self, package_parsed: dict):
        ''' OU包每一次解析完成后, 更新历史纪录, 并将不同的解析结果, 添加到去重界面 '''
        self.insert_ou_parsed_result(self.main_window_ui.history_record_textEdit, package_parsed)
        # 与上一帧不同时, 添加到去重界面
        if package_parsed != self.previous_ou_parsed:
            self.insert_ou_parsed_result(self.main_window_ui.deduplication_textEdit, package_parsed)

            # 更新上一帧解析的结果
            self.previous_ou_parsed = package_parsed    # package_parsed 会在解析OU包的类里重新赋值(指向新的字典)

    def insert_mu_parsed_result(self, textEdit: QTextEdit, mu_output: dict):
        ''' 填入解析后的MU数据到textEdit '''
        # 显示当前系统时间
        current_time = datetime.now()  # 获取系统当前的时间, ms精确到小数点后6位
        textEdit.append(current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        textEdit.append('MU Output:\n')

        for line_num in mu_output:
            # 开关量
            if isinstance(mu_output[line_num], bool):
                if mu_output[line_num] is True:
                    textEdit.insertPlainText(f'{line_num}:  1\t')
                else:
                    textEdit.insertPlainText(f'{line_num}:  0\t')
            # 模拟量: 字典的值是正数
            else:
                textEdit.insertPlainText(f'{line_num}:  {mu_output[line_num] / 100}V\t')

        textEdit.insertPlainText(f'\n')  # 每一包内容结束之后换行

    def update_mu_history_record(self, mu_output: dict):
        ''' 历史记录中更新MU的输出 '''
        self.insert_mu_parsed_result(self.main_window_ui.history_record_textEdit, mu_output)
        # 与上一帧不同时, 添加到去重界面
        if mu_output != self.previous_mu_parsed:
            self.insert_mu_parsed_result(self.main_window_ui.deduplication_textEdit, mu_output)

            # 更新上一帧解析的结果, 使用深拷贝, 创建新的对象副本
            self.previous_mu_parsed = copy.deepcopy(mu_output)      # mu_output 的修改不影响 previous_mu_parsed, 与OU的insert写法不同, 值得思考

    def clear_history_record(self):
        ''' 清除历史记录里所有内容 '''
        self.main_window_ui.history_record_textEdit.clear()
        self.main_window_ui.deduplication_textEdit.clear()

    def serial_port_init(self):
        ''' UI界面添加串口 comboBox 创建串口助手对象 '''
        com_comboBox = LearniuHComboBox()
        self.main_window_ui.gridLayout_serial_port_info.addWidget(com_comboBox, 1, 2)

        # 实例化串口助手对象
        self.serial_port_asst = SerialPortAsst(self.main_window_ui.radioButton_ashining,        # 泽耀 Lora radioButton
                                               self.main_window_ui.radioButton_ebyte,           # 亿佰特 Lora radioButton
                                               self.main_window_ui.pushButton_lora_config,      # Lora 配置 pushButton
                                               com_comboBox,                                    # 选择串口 comboBox
                                               self.main_window_ui.comboBox_baud_rate,          # 波特率 comboBox
                                               self.main_window_ui.comboBox_data_bits,          # 数据位 comboBox
                                               self.main_window_ui.comboBox_parity,             # 奇偶校验 comboBox
                                               self.main_window_ui.comboBox_stop_bits,          # 停止位 comboBox
                                               self.main_window_ui.pushButton_open_serial_port, # 串口打开/关闭 pushButton
                                               self.main_window_ui.stackedWidget_serial_asst,   # stackedWidget
                                               self.main_window_ui.lineEdit_ebyte_addr,         # 亿佰特 模块地址 lineEdit
                                               self.main_window_ui.lineEdit_ebyte_channel,      # 亿佰特 信道 lineEdit
                                               self.main_window_ui.comboBox_ebyte_baud,         # 亿佰特 波特率 comboBox
                                               self.main_window_ui.comboBox_ebyte_parity,       # 亿佰特 奇偶检验 comboBox
                                               self.main_window_ui.comboBox_ebyte_airspeed,     # 亿佰特 空中速率 comboBox
                                               )

        # 点击串口助手中的 "打开串口"
        self.main_window_ui.pushButton_open_serial_port.clicked.connect(self.serial_port_asst.open_serial_port)
        # 点击串口助手中的 "Lora配置"
        self.main_window_ui.pushButton_lora_config.clicked.connect(self.serial_port_asst.lora_config)
        # 串口助手 comboBox Index 变化
        self.main_window_ui.comboBox_baud_rate.currentIndexChanged.connect(self.serial_port_asst.update_baud_rate)
        self.main_window_ui.comboBox_data_bits.currentIndexChanged.connect(self.serial_port_asst.update_byte_size)
        self.main_window_ui.comboBox_parity.currentIndexChanged.connect(self.serial_port_asst.update_parity)
        self.main_window_ui.comboBox_stop_bits.currentIndexChanged.connect(self.serial_port_asst.update_stop_bits)
        # 点击亿佰特 Lora 配置 返回按钮
        self.main_window_ui.pushButton_ebyte_back.clicked.connect(self.serial_port_asst.back_to_mainwindow)
        # 亿佰特 信道 lineEdit 文本变化
        self.main_window_ui.lineEdit_ebyte_channel.textChanged.connect(self.serial_port_asst.update_ebyte_channel)
        # 点击泽耀 Lora 配置 返回按钮
        self.main_window_ui.pushButton_ashining_back.clicked.connect(self.serial_port_asst.back_to_mainwindow)

    def keyPressEvent(self, event):
        ''' 重写该方法, 用于处理键盘按下时, OU模拟器的按键触发 '''
        key = event.text().upper()

        # 在 OU 模拟器界面上
        if self.main_window_ui.sub_interface_stacked.currentIndex() == 2 \
            and self.main_window_ui.tabWidget.currentIndex() == 0 \
            and self.main_window_ui.ou_analysis_send_stacked.currentIndex() == 1:

            # OU模拟器控件已经生成; 过滤长按键盘重复触发的 keyPressEvent 和 keyReleaseEvent
            if (self.main_window_ui.gridLayout_switch.count() or self.main_window_ui.gridLayout_analog.count()) \
                and not event.isAutoRepeat() and key.isalpha():
                # 遍历已填写字母的 lineEdit
                for lineEdit, key_widget in OUSimulator.key_button.items():
                    if lineEdit.bit_index is not None:
                        # 开关量: 按键与 lineEdit 字母一致; checkBox 没有 checked; pushButton 没有被鼠标点击
                        if key in key_widget \
                            and not key_widget[key][1].isChecked() \
                            and not key_widget[key][0].isDown():

                            OUSimulator.switch_pushButton_pressed(key_widget[key][0])
                            # 禁用 pushButton
                            key_widget[key][0].setDisabled(True)
                            # 禁用 checkBox
                            key_widget[key][1].setDisabled(True)
                            # 禁用 lineEdit
                            lineEdit.setDisabled(True)
                        else:
                            continue

                    else:
                        # 模拟量: 按键与 lineEdit 字母一致; pushButton 没有被鼠标点击; slider 没有被鼠标点击
                        if key in key_widget \
                            and not key_widget[key][0].isDown() \
                            and not key_widget[key][1].isSliderDown():

                            OUSimulator.analog_pushButton_pressed(key_widget[key][0])
                            # 禁用 pushButton
                            key_widget[key][0].setDisabled(True)
                            # 禁用 lineEdit
                            lineEdit.setDisabled(True)
                        else:
                            continue

    def keyReleaseEvent(self, event):
        ''' 重写该方法, 用于处理键盘释放时, OU模拟器的按键释放 '''
        key = event.text().upper()
        focused_widget = QApplication.focusWidget()

        # # 在 OU 模拟器界面上
        # if self.main_window_ui.sub_interface_stacked.currentIndex() == 2 \
        #     and self.main_window_ui.tabWidget.currentIndex() == 0 \
        #     and self.main_window_ui.ou_analysis_send_stacked.currentIndex() == 1:

        # OU模拟器控件已经生成; 过滤长按键盘重复触发的 keyPressEvent 和 keyReleaseEvent; lineEdit 获得焦点不做处理
        if (self.main_window_ui.gridLayout_switch.count() or self.main_window_ui.gridLayout_analog.count()) \
            and not event.isAutoRepeat() and key.isalpha() and not isinstance(focused_widget, QLineEdit):
            # 遍历已填写字母的 lineEdit
            for lineEdit, key_widget in OUSimulator.key_button.items():
                if lineEdit.bit_index is not None:
                    # 开关量: 按键与 lineEdit 字母一致; checkBox 没有 checked
                    if key in key_widget \
                        and not key_widget[key][1].isChecked() \
                        and not key_widget[key][0].isDown():

                        OUSimulator.switch_pushButton_released(key_widget[key][0])
                        # pushButton 使能
                        key_widget[key][0].setEnabled(True)
                        # checkBox 使能
                        key_widget[key][1].setEnabled(True)
                        # lineEdit 使能
                        lineEdit.setEnabled(True)
                    else:
                        continue
                else:
                    # 模拟量: 按键与 lineEdit 字母一致; pushButton 没有被按下; slider 没有被鼠标点击
                    if key in key_widget \
                        and not key_widget[key][0].isDown():
                        # and not key_widget[key][1].isSliderDown():

                        OUSimulator.analog_pushButton_released(key_widget[key][0])
                        # pushButton 使能
                        key_widget[key][0].setEnabled(True)
                        # lineEdit 使能
                        lineEdit.setEnabled(True)
                    else:
                        continue

    def mousePressEvent(self, event):
        ''' 鼠标点击空白区域清除所有控件的焦点 '''
        self.setFocus()
        super().mousePressEvent(event)  # 调用父类的鼠标点击事件处理

    def closeEvent(self, event):
        ''' 主程序关闭时, 保存配置页面的所有配置 '''
        settings = QSettings('KCTS', 'CONFIGURE')
        settings.setValue('KCTS_recv_tu_port_content', self.main_window_ui.kc_ts_recv_tu_port_lineEdit.text())
        settings.setValue('KCTS_send_tu_port_content', self.main_window_ui.kc_ts_send_tu_port_lineEdit.text())
        settings.setValue('KCTS_recv_ou_port_content', self.main_window_ui.kc_ts_recv_ou_port_lineEdit.text())
        settings.setValue('KCTS_send_mu_port_content', self.main_window_ui.kc_ts_send_mu_port_lineEdit.text())
        settings.setValue('MU_IP_content', self.main_window_ui.mu_ip_lineEdit.text())
        settings.setValue('MU_recv_port_content', self.main_window_ui.mu_recv_port_lineEdit.text())
        settings.setValue('KCTU_IP_content', self.main_window_ui.kc_tu_ip_lineEdit.text())
        settings.setValue('KCTU_recv_port_content', self.main_window_ui.kc_tu_recv_port_lineEdit.text())
        settings.setValue('OU_simulator_package_head', self.main_window_ui.lineEdit_package_header.text())
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())