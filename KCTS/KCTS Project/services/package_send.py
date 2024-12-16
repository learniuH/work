import re
from typing import Union

from PyQt5.QtWidgets import QLineEdit


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

if __name__ == '__main__':
    # while True:
    #     package = QueryCollectionStatus.package_send()
    #     package = ' '.join(f'{byte:02x}' for byte in package)
    #     print(package)
    value = '15-23'
    print(PackageToMu.extract_num(value))