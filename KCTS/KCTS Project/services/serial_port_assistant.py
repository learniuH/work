import serial
import serial.tools.list_ports

from PyQt5.QtWidgets import QComboBox, QPushButton, QRadioButton, QStackedWidget, QLineEdit
from PyQt5.QtCore import pyqtSignal, QObject
from serial.serialutil import SerialException

from widget.constant import SerialAsstConstant
from config.validators import Validators
from services.network import  SerialAssistant
from services.package_send import PackageToLora

class SerialPortAsst:
    ''' 串口助手 '''

    def __init__(self, ashining_radiobutton: QRadioButton,
                 ebyte_radiobutton: QRadioButton,
                 lora_config_pushButton: QPushButton,
                 com_comboBox: QComboBox,
                 baud_rate_comboBox: QComboBox,
                 data_bits_comboBox: QComboBox,
                 parity_comboBox: QComboBox,
                 stop_bits_comboBox: QComboBox,
                 com_port_open_pushButton: QPushButton,
                 stackedWidget: QStackedWidget,
                 ebyte_channel_lineEdit: QLineEdit,
                 ):

        self.ashining_radiobutton = ashining_radiobutton            # 泽耀 Lora
        self.ebyte_radiobutton = ebyte_radiobutton                  # 亿佰特 Lora
        self.lora_config_pushButton = lora_config_pushButton        # 配置 Lora
        self.com_comboBox = com_comboBox                            # 获取 COM 口
        self.baud_rate_comboBox = baud_rate_comboBox                # 获取 波特率
        self.data_bits_comboBox = data_bits_comboBox                # 获取 数据位
        self.parity_comboBox = parity_comboBox                      # 获取 奇偶校验
        self.stop_bits_comboBox = stop_bits_comboBox                # 获取 停止位
        self.com_port_open_pushButton = com_port_open_pushButton    # 打开/关闭 串口
        self.stackedWidget = stackedWidget                          # stackedWidget 界面

        self.ebyte_channel_lineEdit = ebyte_channel_lineEdit        # 亿佰特信道

        self.serial_asst_manager = SerialAssistant()                # 串口接收线程管理器

        self.signal_bind()                                          # pyqtSignal 绑定
        self.setup_validators()                                     # lineEdit 输入验证器

    def signal_bind(self):
        ''' 数据包接收完成发送 pyqtSignal 信号 '''
        self.serial_asst_manager.ebyte_config_received_signal.connect(self.ebyte_config_package_parse)

    def setup_validators(self):
        ''' 设置 lineEdit 输入验证器 '''
        self.ebyte_channel_lineEdit.setValidator(Validators.ebyte_channel_validator())

    @staticmethod
    def update_com_ports(comboBox: QComboBox):
        ''' 将电脑当前可用的串口号更新到 comboBox '''
        available_port = [port.device for port in serial.tools.list_ports.comports()]

        # 更新串口列表
        comboBox.clear()
        if available_port:
            comboBox.addItems(available_port)

    def back_to_mainwindow(self):
        ''' 点击返回箭头, 返回串口助手主界面 '''
        self.stackedWidget.setCurrentIndex(SerialAsstConstant.SERIAL_ASST_PAGE)

    def update_baud_rate(self, index: int):
        ''' comboBox Index 变化 更新串口助手波特率 '''
        if self.serial_asst_manager.serial.is_open:
            self.serial_asst_manager.serial.baudrate = SerialAsstConstant.BAUD_RATE[index]

    def update_byte_size(self, index: int):
        ''' comboBox Index 变化 更新串口助手数据位'''
        if self.serial_asst_manager.serial.is_open:
            self.serial_asst_manager.serial.bytesize = SerialAsstConstant.DATA_BIT[index]

    def update_parity(self, index: int):
        ''' comboBox Index 变化 更新串口助手优先级 '''
        if self.serial_asst_manager.serial.is_open:
            self.serial_asst_manager.serial.parity = SerialAsstConstant.PARITY[index]

    def update_stop_bits(self, index: int):
        ''' comboBox Index 变化 更新串口助手停止位 '''
        try:
            if self.serial_asst_manager.serial.is_open:
                self.serial_asst_manager.serial.stopbits = SerialAsstConstant.STOP_BIT[index]
        except SerialException as e:
            print(f'停止位参数配置错误: {e}')

    def open_serial_port(self):
        ''' 打开/关闭 串口/线程 '''

        # 没有端口号就不做处理
        if self.com_comboBox.currentText() == '':
            return

        if self.com_port_open_pushButton.text() == '打开串口':
            # 打开串口, 启动接收数据线程
            self.serial_asst_manager.start_recv_serial(port=self.com_comboBox.currentText(),
                                                       baudrate=SerialAsstConstant.BAUD_RATE[self.baud_rate_comboBox.currentIndex()],
                                                       bytesize=SerialAsstConstant.DATA_BIT[self.data_bits_comboBox.currentIndex()],
                                                       parity=SerialAsstConstant.PARITY[self.parity_comboBox.currentIndex()],
                                                       stopbits=SerialAsstConstant.STOP_BIT[self.stop_bits_comboBox.currentIndex()],
                                                       )
            if self.serial_asst_manager.serial.is_open:         # 串口对象创建成功
                # 禁用端口选择的 comboBox
                self.com_comboBox.setDisabled(True)
                # Lora 配置的按键使能
                self.lora_config_pushButton.setEnabled(True)
                self.com_port_open_pushButton.setText('关闭串口')

        else:
            # 关闭串口, 停止发送数据线程
            self.serial_asst_manager.stop_receiving_serial()

            self.com_comboBox.setEnabled(True)                  # 端口选择的 comboBox 使能
            self.lora_config_pushButton.setDisabled(True)       # 禁用 Lora 配置的按键
            self.com_port_open_pushButton.setText('打开串口')

    def parameter_init_Ebyte(self):
        ''' 配置 EByte Lora 的串口参数
            serial 波特率 9600 (EByte Lora 参数配置波特率)
            serial 数据位 8    (EByte Lora 参数配置数据位)
            serial 奇偶校验 无  (EByte Lora 参数配置奇偶校验)
            serial 停止位 1    (EByte Lora 参数配置停止位)
        '''
        self.serial_asst_manager.serial.baudrate = SerialAsstConstant.BAUD_RATE_EBYTE_CONFIG
        self.baud_rate_comboBox.setCurrentIndex(SerialAsstConstant.BAUD_RATE_9600_INDEX)
        self.serial_asst_manager.serial.bytesize = SerialAsstConstant.DATA_BIT_EBYTE_CONFIG
        self.data_bits_comboBox.setCurrentIndex(SerialAsstConstant.BYTE_SIZE_EIGHTBITS_INDEX)
        self.serial_asst_manager.serial.parity = SerialAsstConstant.PARITY_EBYTE_CONFIG
        self.parity_comboBox.setCurrentIndex(SerialAsstConstant.PARITY_NONE_INDEX)
        self.serial_asst_manager.serial.stopbits = SerialAsstConstant.STOP_BIT_EBYTE_CONFIG
        self.stop_bits_comboBox.setCurrentIndex(SerialAsstConstant.STOPBITS_ONE_INDEX)

    def lora_config(self):
        ''' 点击 Lora 配置, 切换到相应的 Lora 型号配置界面 '''

        # 进入 泽耀Lora 配置界面
        if self.ashining_radiobutton.isChecked() and self.stackedWidget.currentIndex() != SerialAsstConstant.ASHING_CONFIG_PAGE:
            self.stackedWidget.setCurrentIndex(SerialAsstConstant.ASHING_CONFIG_PAGE)

        # 进入 亿佰特Lora 配置界面
        if self.ebyte_radiobutton.isChecked() and self.stackedWidget.currentIndex() != SerialAsstConstant.EBYTE_CONFIG_PAGE:
            self.stackedWidget.setCurrentIndex(SerialAsstConstant.EBYTE_CONFIG_PAGE)
            # 串口参数更新
            self.parameter_init_Ebyte()
            # 发送获取参数的 AT 指令
            self.get_ebyte_config()


    def get_ebyte_config(self):
        ''' 点击 Lora配置, 发送 AT 指令, 以获取亿佰特 Lora 配置 '''
        # 发送 AT 指令 - 获取信道
        self.serial_asst_manager.serial.write(PackageToLora.GET_EBYTE_CHANNEL)


    def ebyte_config_package_parse(self, config_package: list):
        ''' 接收 pyqtSignal 信号, 解析亿佰特数据包, 获取信道 '''
        pass

    def update_ebyte_channel(self):
        ''' 信道的 lineEdit text changed 时, 发送 AT 指令, 修改 Lora 信道 '''
        # print(f'当前的信道是{self.ebyte_channel_lineEdit.text()}')
        # 通过 lineEdit 修改信道
        PackageToLora.update_ebyte_channel(self.ebyte_channel_lineEdit.text())
        # 发动 AT 指令
        self.serial_asst_manager.serial.write(PackageToLora.CHANGE_EBYTE_CHANNEL)

        # # 测试
        # buffer = [0xC1, 0x00, 0x04]
        # self.serial_asst_manager.serial.write(buffer)
