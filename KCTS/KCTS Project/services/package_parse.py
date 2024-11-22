class PackageFromTU:
    ''' TU数据包结构定义 '''
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
    def crc_check(cls, package: bytearray) -> bool:
        '''
         接收的所有数据包首先进行CRC校验

        Args:
            package: 接收的数据包

        Returns：
            bool: CRC校验是否通过
        '''
        if sum(package[:-1]) == package[-1]:
            return True
        else:
            return False



if __name__ == '__main__':
    package = bytearray(3)
    package[0] = 1
    package[1] = 4
    package[2] = 3
    print(PackageFromTU.crc_check(package))