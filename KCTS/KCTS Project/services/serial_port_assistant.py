import serial
import serial.tools.list_ports

from PyQt5.QtWidgets import QComboBox, QPushButton, QRadioButton, QStackedWidget

from widget.constant import ConstantText

class SerialPortAsst:
    ''' 串口助手 '''

    def __init__(self, ashining_radiobutton: QRadioButton,
                 ebyte_radiobutton: QRadioButton,
                 com_comboBox: QComboBox,
                 baud_rate_comboBox: QComboBox,
                 data_bits_comboBox: QComboBox,
                 parity_comboBox: QComboBox,
                 stop_bits_comboBox: QComboBox,
                 com_port_open_pushButton: QPushButton,
                 stackedWidget: QStackedWidget
                 ):

        self.ashining_radiobutton = ashining_radiobutton            # 泽耀 Lora
        self.ebyte_radiobutton = ebyte_radiobutton                  # 亿佰特 Lora
        self.com_comboBox = com_comboBox                            # 获取 COM 口
        self.baud_rate_comboBox = baud_rate_comboBox                # 获取 波特率
        self.data_bits_comboBox = data_bits_comboBox                # 获取 数据位
        self.parity_comboBox = parity_comboBox                      # 获取 奇偶校验
        self.stop_bits_comboBox = stop_bits_comboBox                # 获取 停止位
        self.com_port_open_pushButton = com_port_open_pushButton    # 打开/关闭 串口
        self.stackedWidget = stackedWidget                          # stackedWidget 界面

    @staticmethod
    def update_com_ports(comboBox: QComboBox):
        ''' 将电脑当前可用的串口号更新到 comboBox '''
        available_port = [port.device for port in serial.tools.list_ports.comports()]

        # 更新串口列表
        comboBox.clear()
        if available_port:
            comboBox.addItems(available_port)

    def open_serial_port(self):
        ''' 点击打开串口 '''
        if self.stackedWidget.currentIndex() != ConstantText.SERIAL_ASST_PAGE:
            self.stackedWidget.setCurrentIndex(ConstantText.SERIAL_ASST_PAGE)
        if self.com_port_open_pushButton.text() == '打开串口':
            self.com_comboBox.setDisabled(True)
            self.com_port_open_pushButton.setText('关闭串口')
        else:
            # 按钮的文字是关闭串口
            self.com_comboBox.setEnabled(True)
            self.com_port_open_pushButton.setText('打开串口')

    def lora_config(self):
        ''' 点击 Lora 配置, 切换到相应的 Lora 型号配置界面 '''

        # 根据 radio button, 切换到相应的 Lora 配置界面
        if self.ashining_radiobutton.isChecked() and self.stackedWidget.currentIndex() != ConstantText.ASHING_CONFIG_PAGE:
            self.stackedWidget.setCurrentIndex(ConstantText.ASHING_CONFIG_PAGE)
        if self.ebyte_radiobutton.isChecked() and self.stackedWidget.currentIndex() != ConstantText.EBYTE_CONFIG_PAGE:
            self.stackedWidget.setCurrentIndex(ConstantText.EBYTE_CONFIG_PAGE)

