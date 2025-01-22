import serial
import serial.tools.list_ports

from PyQt5.QtWidgets import QComboBox, QPushButton, QRadioButton, QStackedWidget, QLineEdit
from PyQt5.QtCore import pyqtSignal, QObject
from serial.serialutil import SerialException

from widget.constant import SerialAsstConstant, SendCycle
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
                 ebyte_addr_lineEdit: QLineEdit,
                 ebyte_channel_lineEdit: QLineEdit,
                 ebyte_baud_comboBox: QComboBox,
                 ebyte_parity_comboBox: QComboBox,
                 ebyte_airspeed_comboBox: QComboBox,
                 ):

        self.ashining_radiobutton       = ashining_radiobutton              # 泽耀 Lora
        self.ebyte_radiobutton          = ebyte_radiobutton                 # 亿佰特 Lora
        self.lora_config_pushButton     = lora_config_pushButton            # 配置 Lora
        self.com_comboBox               = com_comboBox                      # 获取 COM 口
        self.baud_rate_comboBox         = baud_rate_comboBox                # 获取 波特率
        self.data_bits_comboBox         = data_bits_comboBox                # 获取 数据位
        self.parity_comboBox            = parity_comboBox                   # 获取 奇偶校验
        self.stop_bits_comboBox         = stop_bits_comboBox                # 获取 停止位
        self.com_port_open_pushButton   = com_port_open_pushButton          # 打开/关闭 串口
        self.stackedWidget              = stackedWidget                     # stackedWidget 界面

        self.ebyte_addr_lineEdit        = ebyte_addr_lineEdit               # 亿佰特模块地址
        self.ebyte_channel_lineEdit     = ebyte_channel_lineEdit            # 亿佰特信道
        self.ebyte_baud_comboBox        = ebyte_baud_comboBox               # 亿佰特波特率
        self.ebyte_parity_comboBox      = ebyte_parity_comboBox             # 亿佰特奇偶校验
        self.ebyte_airspeed_comboBox    = ebyte_airspeed_comboBox           # 亿佰特空中速率

        self.serial_asst_manager        = SerialAssistant()                # 串口接收线程管理器

        self.signal_bind()                                          # pyqtSignal 绑定
        self.setup_validators()                                     # lineEdit 输入验证器

    def signal_bind(self):
        ''' 数据包接收完成发送 pyqtSignal 信号 '''
        self.serial_asst_manager.ebyte_config_received_signal.connect(self.ebyte_config_package_parse)

    def setup_validators(self):
        ''' 设置 lineEdit 输入验证器 '''
        self.ebyte_channel_lineEdit.setValidator(Validators.ebyte_channel_validator())
        self.ebyte_addr_lineEdit.setValidator(Validators.ebyte_addr_vallidator())

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
        if self.serial_asst_manager.serial:
            self.serial_asst_manager.serial.baudrate = SerialAsstConstant.BAUD_RATE[index]

    def update_byte_size(self, index: int):
        ''' comboBox Index 变化 更新串口助手数据位'''
        if self.serial_asst_manager.serial:
            self.serial_asst_manager.serial.bytesize = SerialAsstConstant.DATA_BIT[index]

    def update_parity(self, index: int):
        ''' comboBox Index 变化 更新串口助手校验位 '''
        if self.serial_asst_manager.serial:
            self.serial_asst_manager.serial.parity = SerialAsstConstant.PARITY[index]

    def update_stop_bits(self, index: int):
        ''' comboBox Index 变化 更新串口助手停止位 '''
        try:
            if self.serial_asst_manager.serial:
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
            if self.serial_asst_manager.serial:         # 串口对象创建成功
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
        self.serial_asst_manager.start_write_serial(SendCycle.CYCLE, is_loop=False)

    def ebyte_channel(self, channel: bytes):
        ''' 点击Lora配置后, 根据数据包更新界面上 亿佰特的信道 '''
        self.ebyte_channel_lineEdit.blockSignals(True)
        self.ebyte_channel_lineEdit.setText(f'{str(int(channel[0]))}')
        self.ebyte_channel_lineEdit.blockSignals(False)

    def ebyte_addr(self, addr: bytes):
        ''' 点击Lora配置后, 根据数据包更新界面上 亿佰特的模块地址 '''
        self.ebyte_addr_lineEdit.blockSignals(True)
        # 将Lora返回的地址存入要发送的包中
        PackageToLora.EBYTE_ADDRH = int(hex(addr[0]), 16)
        PackageToLora.EBYTE_ADDRL = int(hex(addr[1]), 16)

        addr = ' '.join(f'{byte:02X}' for byte in addr)
        self.ebyte_addr_lineEdit.setText(addr)
        self.ebyte_addr_lineEdit.blockSignals(False)

    def ebyte_serial_config(self, serial_config: bytes):
        ''' 点击Lora配置后, 根据数据包更新界面上 亿佰特的串口相关参数 '''
        self.ebyte_baud_comboBox.blockSignals(True)
        self.ebyte_parity_comboBox.blockSignals(True)
        self.ebyte_airspeed_comboBox.blockSignals(True)
        # 将 Lora 返回的串口参数存入要发送的包中
        PackageToLora.CHANGE_EBYTE_SERIAL[3] = serial_config[0]

        ebyte_config_list = []
        for i in range(8):
            ebyte_config_list.append((int(str(serial_config[0])) >> i) & 1)
        # 串口波特率
        if ebyte_config_list[5] == 1:
            if ebyte_config_list[6] == 1:
                if ebyte_config_list[7] == 1:
                    self.ebyte_baud_comboBox.setCurrentIndex(SerialAsstConstant.EBYTE_BAUD_RATE_115200_INDEX)
                    print('波特率115200')
                else:
                    self.ebyte_baud_comboBox.setCurrentIndex(SerialAsstConstant.EBYTE_BAUD_RATE_9600_INDEX)
                    print('波特率9600')
            else:
                if ebyte_config_list[7] == 1:
                    self.ebyte_baud_comboBox.setCurrentIndex(SerialAsstConstant.EBYTE_BAUD_RATE_38400_INDEX)
                    print('波特率38400')
                else:
                    self.ebyte_baud_comboBox.setCurrentIndex(SerialAsstConstant.EBYTE_BAUD_RATE_2400_INDEX)
                    print('波特率2400')
        else:
            if ebyte_config_list[6] == 1:
                if ebyte_config_list[7] == 1:
                    self.ebyte_baud_comboBox.setCurrentIndex(SerialAsstConstant.EBYTE_BAUD_RATE_57600_INDEX)
                    print('波特率57600')
                else:
                    self.ebyte_baud_comboBox.setCurrentIndex(SerialAsstConstant.EBYTE_BAUD_RATE_4800_INDEX)
                    print('波特率4800')
            else:
                if ebyte_config_list[7] == 1:
                    self.ebyte_baud_comboBox.setCurrentIndex(SerialAsstConstant.EBYTE_BAUD_RATE_19200_INDEX)
                    print('波特率19200')
                else:
                    self.ebyte_baud_comboBox.setCurrentIndex(SerialAsstConstant.EBYTE_BAUD_RATE_1200_INDEX)
                    print('波特率1200')

        # 校验位
        if ebyte_config_list[3] == 1:
            if ebyte_config_list[4] == 1:
                self.ebyte_parity_comboBox.setCurrentIndex(SerialAsstConstant.EBYTE_PARITY_8N1_INDEX)
                print('8N1')
            else:
                self.ebyte_parity_comboBox.setCurrentIndex(SerialAsstConstant.EBYTE_PARITY_8O1_INDEX)
                print('8o1')
        else:
            if ebyte_config_list[4] == 1:
                self.ebyte_parity_comboBox.setCurrentIndex(SerialAsstConstant.EBYTE_PARITY_8E1_INDEX)
                print('8E1')
            else:
                self.ebyte_parity_comboBox.setCurrentIndex(SerialAsstConstant.EBYTE_PARITY_8N1_INDEX)
                print('8N1')

        # 空中速率
        if ebyte_config_list[0] == 1:
            if ebyte_config_list[1] == 1:
                if ebyte_config_list[2] == 1:
                    self.ebyte_airspeed_comboBox.setCurrentIndex(SerialAsstConstant.EBYTE_AIRSPEED_625_INDEX)
                    print('空中速率62.5K')
                else:
                    self.ebyte_airspeed_comboBox.setCurrentIndex(SerialAsstConstant.EBYTE_AIRSPEED_48_INDEX)
                    print('空中速率4.8K')
            else:
                if ebyte_config_list[2] == 1:
                    self.ebyte_airspeed_comboBox.setCurrentIndex(SerialAsstConstant.EBYTE_AIRSPEED_192_INDEX)
                    print('空中速率19.2k')
                else:
                    self.ebyte_airspeed_comboBox.setCurrentIndex(SerialAsstConstant.EBYTE_AIRSPEED_24_INDEX)
                    print('空中速率2.4K')
        else:
            if ebyte_config_list[1] == 1:
                if ebyte_config_list[2] == 1:
                    self.ebyte_airspeed_comboBox.setCurrentIndex(SerialAsstConstant.EBYTE_AIRSPEED_384_INDEX)
                    print('空中速率38.4kK')
                else:
                    self.ebyte_airspeed_comboBox.setCurrentIndex(SerialAsstConstant.EBYTE_AIRSPEED_24_INDEX)
                    print('空中速率2.4K')
            else:
                if ebyte_config_list[2] == 1:
                    self.ebyte_airspeed_comboBox.setCurrentIndex(SerialAsstConstant.EBYTE_AIRSPEED_96_INDEX)
                    print('空中速率9.6k')
                else:
                    self.ebyte_airspeed_comboBox.setCurrentIndex(SerialAsstConstant.EBYTE_AIRSPEED_24_INDEX)
                    print('空中速率2.4K')

        self.ebyte_baud_comboBox.blockSignals(False)
        self.ebyte_parity_comboBox.blockSignals(False)
        self.ebyte_airspeed_comboBox.blockSignals(False)


    def ebyte_config_package_parse(self, config_package: list):
        ''' 接收 pyqtSignal 信号, 解析亿佰特数据包, 获取信道 '''
        # 亿佰特寄存器定义
        ebyte_register_define = {
            0x00: self.ebyte_addr,
            0x03: self.ebyte_serial_config,
            0x05: self.ebyte_channel,
        }
        if config_package[1] in ebyte_register_define:
            # 对于已定义的寄存器, 调用对应的函数进行处理
            ebyte_register_define[config_package[1]](config_package[3:])

    def update_ebyte_channel(self):
        ''' 信道的 lineEdit text changed 时, 发送 AT 指令, 修改 Lora 信道 '''
        # print(f'当前的信道是{self.ebyte_channel_lineEdit.text()}')
        # 通过 lineEdit 修改信道
        PackageToLora.update_ebyte_channel(self.ebyte_channel_lineEdit.text())
        # 发送 AT 指令
        self.serial_asst_manager.serial.write(PackageToLora.CHANGE_EBYTE_CHANNEL)

    def update_ebyte_addr(self):
        ''' 模块地址的 lineEdit text changed 时, 发送 AT 指令, 修改 Lora 模块地址 '''
        # 通过 lineEdit 修改模块地址
        if PackageToLora.update_ebyte_addr(self.ebyte_addr_lineEdit.text()):
            # 返回True, 允许发送 AT 指令
            self.serial_asst_manager.serial.write(PackageToLora.CHANGE_EBYTE_ADDR)

    def update_ebyte_baud(self, index: int):
        """ 亿佰特波特率 comboBox Index 变化, 发送 AT 指令, 修改 亿佰特波特率 """
        # 更新 AT 指令
        start_bit = 5
        PackageToLora.update_ebyte_serial(index, start_bit)
        # 发送 AT 指令
        self.serial_asst_manager.serial.write(PackageToLora.CHANGE_EBYTE_SERIAL)

    def update_ebyte_parity(self, index: int):
        """ 亿佰特奇偶检验 comboBox Index 变化, 发送 AT 指令, 修改亿佰特奇偶校验 """
        # 更新 AT 指令
        start_bit = 3
        PackageToLora.update_ebyte_serial(index, start_bit)
        # 发送 AT 指令
        self.serial_asst_manager.serial.write(PackageToLora.CHANGE_EBYTE_SERIAL)

    def update_ebyte_airSpeed(self, index: int):
        """ 亿佰特空中速率 comboBox Index 变化, 发送 AT 指令, 修改亿佰特空中速率 """
        # 更新 AT 指令
        start_bit = 0
        PackageToLora.update_ebyte_serial(index, start_bit)
        # 发送 AT 指令
        self.serial_asst_manager.serial.write(PackageToLora.CHANGE_EBYTE_SERIAL)