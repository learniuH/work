import serial
import serial.tools.list_ports

from PyQt5.QtWidgets import QComboBox


class SerialPortAsst:
    ''' 串口助手 '''

    @staticmethod
    def update_com_ports(comboBox: QComboBox):
        ''' 将电脑当前可用的串口号更新到 comboBox '''
        available_port = [port.device for port in serial.tools.list_ports.comports()]

        # 更新串口列表
        comboBox.clear()
        if available_port:
            comboBox.addItems(available_port)


