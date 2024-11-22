
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


if __name__ == '__main__':
    while True:
        package = QueryCollectionStatus.package_send()
        package = ' '.join(f'{byte:02x}' for byte in package)
        print(package)
