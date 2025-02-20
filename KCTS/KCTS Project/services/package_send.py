import re
from typing import Union
from PyQt5.QtWidgets import QLineEdit

from widget.constant import SerialAsstConstant

class QueryCollectionStatus:
    ''' 构造采集状态的UDP包 '''
    start_char          =       0x5A        # 起始字符
    data_length         =       0x08        # 包长度(下一个字节开始到CRC之前)
    destination_id      =       0x12        # 目的设备ID
    source_id           =       0x12        # 源设备ID
    sequence_num        =       0x00        # 序列号
    message_type        =       0x01        # 消息类型
    device_type_high    =       0x12        # 设备类型高字节
    device_type_low     =       0x12        # 设备类型低字节
    data_field          =       0x00        # 数据域预留


    @classmethod
    def calculate_crc(cls):
        ''' 计算CRC校验 '''
        check_sum = [
                cls.start_char,
                (cls.data_length >> 8) & 0xFF,
                cls.data_length & 0xFF,
                cls.destination_id,
                cls.source_id,
                (cls.sequence_num >> 8) & 0xFF,
                cls.sequence_num & 0xFF,
                cls.message_type,
                cls.device_type_high,
                cls.device_type_low,
                cls.data_field,
            ]
        return sum(check_sum) & 0xFF

    @classmethod
    def package_send(cls) -> bytearray:
        ''' 组包 0x01 '''
        package = bytearray(
            [
                cls.start_char,
                (cls.data_length >> 8) & 0xFF,
                cls.data_length & 0xFF,
                cls.destination_id,
                cls.source_id,
                (cls.sequence_num >> 8) & 0xFF,
                cls.sequence_num & 0xFF,
                cls.message_type,
                cls.device_type_high,
                cls.device_type_low,
                cls.data_field,
                cls.calculate_crc()
            ]
        )
        cls.sequence_num += 1
        return package

class PackageToMu:
    ''' OU模拟器给MU发的包 '''
    package: bytearray = None           # 要发送的数据包
    package_header_len: int = 0         # 数据包的包头长度

    @classmethod
    def generate_package(cls, package_length: int):
        ''' 主界面的 comboBox indexchanged 后, 生成一个包长确定的包 '''
        cls.package = bytearray(package_length)

    @classmethod
    def update_package_header(cls, lineEdit: QLineEdit):
        ''' 获取主界面 header lineEdit 的文本, 转换为字节值存入数据包包头 '''
        lineEdit_text = lineEdit.text()
        header_array = re.findall(r'[0-9A-Fa-f]+', lineEdit_text)

        if len(header_array) < cls.package_header_len:
            # 将数据包包头变短部分的数置0
            cls.package[len(header_array): cls.package_header_len] = [0] * (cls.package_header_len - len(header_array))

        # 更新包头的长度
        cls.package_header_len = len(header_array)
        # 更新发送的数据包的包头
        for i, element in enumerate(header_array):
            cls.package[i] = int(element, 16)

        # 当数据包发生改变时, 计算 CRC
        cls.package[-1] = sum(cls.package[:-1]) & 0xFF

        # print(' '.join(f'{byte:02X}' for byte in cls.package))

    @classmethod
    def update_data_field(cls, byte_num: Union[int, str], value: int, bit_index: Union[int, str]=None):
        ''' 更新数据包的数据域部分
        Args:
            byte_num : 字节序号
            value    : 如果是开关量, 取 0 1, 如果是模拟量, 取 实际的 value 直接赋值
            bit_index: 位索引, 模拟量默认为 None
        '''
        if bit_index is not None:
            # 开关量, byte_num: int
            if isinstance(bit_index, int):
                # 单位开关量
                if value == 0:
                    # 对应位赋 0
                    cls.package[byte_num - 1] &= ~(1 << bit_index)
                else:
                    # 对应位赋 1
                    cls.package[byte_num - 1] |= (1 << bit_index)

            else:
                # 多位开关量
                bit_index_range = cls.extract_num(bit_index)
                for index in range(bit_index_range[0], bit_index_range[1] + 1):
                    if value == 0:
                        cls.package[byte_num - 1] &= ~(1 << index)
                    else:
                        cls.package[byte_num - 1] |= (1 << index)

        else:
            if isinstance(byte_num, int):
                # 单字节模拟量
                cls.package[byte_num - 1] = value
            else:
                # 多字节模拟量
                byte_num_range = cls.extract_num(byte_num)
                for i, num in enumerate(range(byte_num_range[1], byte_num_range[0] - 1, -1)):
                    # 倒序遍历多字节序号
                    cls.package[num - 1] = ((value >> (i * 8)) & 0xFF)

        # 当数据包发生改变时, 计算 CRC
        cls.package[-1] = sum(cls.package[:-1]) & 0xFF

        # print(' '.join(f'{byte:02X}' for byte in cls.package))

    @classmethod
    def extract_num(cls, value: str) -> list:
        ''' 提取字符串的数字, 返回列表 '''
        return [int(num) for num in value.split('-')]


class PackageToLora:
    ''' 通过串口发送的数据 '''
    EBYTE_CHANNEL: int      = None
    CHANGE_EBYTE_CHANNEL    = [0xC0, 0x05, 0x01, EBYTE_CHANNEL]             # AT指令: 设置 EByte 信道

    EBYTE_ADDRH: int        = None
    EBYTE_ADDRL: int        = None
    CHANGE_EBYTE_ADDR       = [0xC0, 0x00, 0x02, EBYTE_ADDRH, EBYTE_ADDRL]  # AT指令: 设置 EByte 模块地址

    EBYTE_SERIAL: bytes     = None
    CHANGE_EBYTE_SERIAL     = [0xC0, 0x03, 0x01, EBYTE_SERIAL]              # AT指令：设置 EByte 串口参数

    GET_EBYTE_CHANNEL       = [0xC1, 0x05, 0x01]                        # AT指令: 获取 EByte 信道
    GET_EBYTE_ADDR          = [0xC1, 0x00, 0x02]                        # AT指令: 获取 EByte 模块地址
    GET_EBYTE_SERIAL_CONFIG = [0xC1, 0x03, 0x01]                        # AT指令: 获取 EByte 波特率, 校验位, 空中速率
    DATA_LIST               = [bytes(GET_EBYTE_CHANNEL),
                               bytes(GET_EBYTE_ADDR),
                               bytes(GET_EBYTE_SERIAL_CONFIG),
                               ]

    @classmethod
    def update_ebyte_channel(cls, channel: str):
        ''' lineEdit 文本变化时, 更新信道 AT 指令 '''
        if channel != '':
            cls.CHANGE_EBYTE_CHANNEL[3] = int(channel)          # lineEdit 写十进制的数, AT 指令显示的是 十六进制
        else:
            cls.CHANGE_EBYTE_CHANNEL[3] = 0                     # lineEdit 为空, channel 设置为 0

    @classmethod
    def update_ebyte_addr(cls, addr: str) -> bool:
        '''
        lineEdit 文本变化时, 更新模块地址 AT 指令
        :param addr: linEdit 的内容, 格式应该为 FF FF, 两个十六进制字节
        :return: 允许发送 AT, 返回True; 不允许返回False
        '''
        # 提取 lineEdit 里面的两个字节
        addr = [int(byte, 16) for byte in re.findall(r'\d+', addr)]

        if len(addr) == 2:
            # 当已经输入了两个字节时, 才下发AT指令
            if addr[0] == cls.EBYTE_ADDRH and addr[1] == cls.EBYTE_ADDRL:
                # 文本框内容和上一次Lora返回的地址相同时, 不发送AT指令
                return False
            else:
                cls.CHANGE_EBYTE_ADDR[3] = addr[0]
                cls.CHANGE_EBYTE_ADDR[4] = addr[1]
                return True
        else:
            return False

    @classmethod
    def update_ebyte_serial(cls, index: int, start_bit: int):
        '''
         亿佰特波特率 comboBox Index 变化时, 更新波特率 AT 指令
        :param index: comboBox 的 Index
        :param start_bit: 亿佰特串口参数字节位索引的起始值
        :return: None
        '''
        bit_index = start_bit
        for bit_value in SerialAsstConstant.EBYTE_SERIAL[start_bit][index]:
            # 遍历 EBYTE_SERIAL 这个字节的 对应位 替换为 EBYTE_SERIAL 字典里定义的值
            if bit_value == 1:
                cls.CHANGE_EBYTE_SERIAL[3] |= (1 << bit_index)
            else:
                cls.CHANGE_EBYTE_SERIAL[3] &= ~(1 << bit_index)
            bit_index += 1


if __name__ == '__main__':
    # while True:
    #     package = QueryCollectionStatus.package_send()
    #     package = ' '.join(f'{byte:02x}' for byte in package)
    #     print(package)
    pass