from PyQt5.QtCore import pyqtSignal, QObject

from .protocol_definition import StatusFeedBack

# class PackageProcess():
#     ''' PackageFromTU 和 PackageFromOU 的父类 '''


class PackageFromTU(QObject):
    ''' 处理来自TU的有效数据包 '''

    # 当检测到 DO 置 1 或 PWM 非 0 时, 发出pyqtSignal信号到主窗口
    update_do_signal = pyqtSignal(str, bool)
    update_pwm_signal = pyqtSignal(str, int)

    mu_output_record_signal = pyqtSignal(dict)      # 记录MU所有线号输出的信号

    # _instance = None
    #
    # def __new__(cls, *args, **kwargs):
    #     ''' 单例模式, 确保所有的实例对象内存地址相同 '''
    #     if cls._instance is None:
    #         # 调用父类的__new__()方法创建对象
    #         cls._isinstance = super(PackageFromTU, cls).__new__(cls)
    #     return cls._instance

    def __init__(self):
        super().__init__()
        self.package: bytearray = None
        self.message_type: dict = None

        self.mu_output_record: dict = {}
        self.previous_mu_status_package = None


    def define_message_type(self, eighth_byte: int):
        ''' TU反馈的消息类型定义 '''
        if self.message_type is None:
            self.message_type = {
                0x02: self.handle_mu_status,
                0x04: self.handle_tu_status
            }
        # 只处理byte8有定义的包
        if eighth_byte in self.message_type:
            # 消息类型未定义的包不做处理
            self.message_type[eighth_byte]()
        else:
            print('收到未作定义的包！')


    def handle_mu_status(self):
        ''' 根据协议对校验通过的数据包进行解析 '''
        for byte_num in StatusFeedBack.data_field_protocol:
            # 处理 DO 数据
            if isinstance(StatusFeedBack.data_field_protocol.get(byte_num), dict):
                # 遍历协议中定义的位索引
                for bit_index, description in StatusFeedBack.data_field_protocol.get(byte_num).items():
                    # if self.package[byte_num - 1] >> bit_index & 1:
                    #     # 字节的位索引为 1, 就发出 pyqtSignal 到主界面更新控件
                    #     print(f'Byte{byte_num}  bit{bit_index}  {description}')
                    #     # 发送DO线号 和 boolean值
                    #     self.update_do_signal.emit(description, True)

                    # 当前包的对应位与上一包不同, 将发送该位当前值的信号
                    if self.previous_mu_status_package is None \
                            or self.package[byte_num - 1] >> bit_index != \
                                self.previous_mu_status_package[byte_num - 1] >> bit_index:
                        if self.package[byte_num - 1] >> bit_index & 1:
                            self.update_do_signal.emit(description, True)
                            self.mu_output_record[description] = True       # 将DO的输出记录下
                            print(f'{description} emit True!')
                        else:
                            self.update_do_signal.emit(description, False)
                            self.mu_output_record[description] = False      # 将DO的输出记录下
                            print(f'{description} emit False!')

            else:
                # 处理 PWM 数据
                high_byte, low_byte = byte_num.split('-')
                high_byte, low_byte = int(high_byte) - 1, int(low_byte) - 1
                current_pwm_value = (self.package[high_byte] << 8) + self.package[low_byte]
                # 计算上一帧的PWM值
                if self.previous_mu_status_package is not None:
                    previous_pwm_value = (self.previous_mu_status_package[high_byte] << 8) + \
                                         self.previous_mu_status_package[low_byte]

                # 当前包对应的PWM与上一包不同, 发送当前的PWM线号 和 值
                if self.previous_mu_status_package is None or current_pwm_value != previous_pwm_value:
                    # print(f'Byte{byte_num}  {current_pwm_value}')
                    # 发送PWM的线号str 和 值int
                    self.update_pwm_signal.emit(StatusFeedBack.data_field_protocol[byte_num], current_pwm_value)
                    self.mu_output_record[StatusFeedBack.data_field_protocol[byte_num]] = current_pwm_value     # 将当前的PWM输出记录
                    print(f'{StatusFeedBack.data_field_protocol[byte_num]} emit {current_pwm_value}')

        # 更新previous包
        self.previous_mu_status_package = self.package
        # 每次解析完成后, 将MU输出的记录发送到主窗口
        self.mu_output_record_signal.emit(self.mu_output_record)


    def handle_tu_status(self):
        print('成功调用了TU_STA1TUS')


    def crc_check(self) -> bool:
        '''
         接收的所有数据包首先进行CRC校验

        Args:
            package: 接收的数据包

        Returns：
            bool: CRC校验是否通过
        '''
        if sum(self.package[:-1]) & 0xFF == self.package[-1]:
            return True
        else:
            print('crc校验不通过')
            return False


    def package_length_check(self) -> bool:
        '''
         crc校验通过的数据包进行包长度校验

        Args:
            package: 接收的数据包

        Returns：
            bool: 包长度校验是否通过
        '''
        package_length_expect = (self.package[1] << 8) + self.package[2] + 4
        package_length_actual = len(self.package)
        # 第2/3字节给出的包长与实际包长相同, 则为True
        if package_length_expect == package_length_actual:
            return True
        else:
            print('包长度校验不通过')
            return False


    def parse_tu_package(self, package: bytes):
        ''' 对来自TU的数据包区分并解析 '''
        self.package = package
        if self.package[0] == 0x5A and self.crc_check():
            # crc校验通过后对包长度进行校验
            if self.package_length_check():
                # 通过消息类型字节对TU的数据包进行处理
                self.define_message_type(self.package[7])


class PackageFromOU(QObject):
    ''' 通过 comboBox 选择的表单处理出来的协议, 解析来自OU的包 '''

    # 将每一帧报文解析的结果发送到主窗口
    update_switch_signal = pyqtSignal(dict)

    def __init__(self, protocol: dict):
        super().__init__()
        self.protocol = protocol        # Excel表格解析出来的协议


    def parse_ou_package(self, package: bytes):
        ''' 根据协议内容, 解析接收到的数据包 '''
        package_parsed = {}
        for byte_num in self.protocol:
            if isinstance(self.protocol.get(byte_num), dict):
                # 遍历协议中所有的位索引
                for bit_index, description in self.protocol.get(byte_num).items():
                    if isinstance(bit_index, int):
                        # 单个位作为一个开关
                        if package[byte_num - 1] >> bit_index & 1:
                            if byte_num not in package_parsed:
                                package_parsed[byte_num] = {}
                            package_parsed[byte_num][bit_index] = self.protocol[byte_num][bit_index]

                    else:
                        # 多个位作为一个开关
                        bit_index_start, bit_index_end = bit_index.split('-')
                        index_start, index_end = int(bit_index_start), int(bit_index_end)
                        # 遍历所有位, 全为1则存入字典
                        for index in range(index_start, index_end + 1):
                            if package[byte_num - 1] >> index & 1:
                                if index == index_end:
                                    '''开关量存入字典的形式:{
                                        13: {
                                            0: '前灯'
                                            1: '测试模式'
                                            2: '正常模式'
                                            '1-2': '校准模式'
                                        }
                                    }
                                    '''
                                    if byte_num not in package_parsed:
                                        package_parsed[byte_num] = {}
                                    package_parsed[byte_num][bit_index] = self.protocol[byte_num][bit_index]
                                    '''
                                        Excel 表示协议时, 需要将多位表示一个开关的情况按如下方式写 例如:
                                        bit0: 正常
                                        bit1: 异常
                                        bit0-1: 测试模式
                                    '''
                                    # 将已存入字典的键值对移除, Excel解析出来的协议一定要上面的格式
                                    for idx in range(index_start, index_end + 1):
                                        package_parsed[byte_num].pop(idx)
                            else:
                                # 如果其中一位为0, 就不存入字典
                                break
            else:
                # 处理模拟量
                if isinstance(byte_num, int):
                    # 单个字节模拟量
                    if package[byte_num - 1]:
                        package_parsed[byte_num] = [self.protocol[byte_num], package[byte_num - 1]]
                else:
                    # 多个字节模拟量
                    byte_num_start, byte_num_end = byte_num.split('-')
                    value = 0
                    for byte_num_index in range(int(byte_num_start), int(byte_num_end) + 1):
                        value = (value << 8) + package[byte_num_index - 1]
                    if value:
                        '''模拟量开关存入字典的形式: {
                            12: ['前进', 100]
                            '14-15': ['后退', 25600]
                        }
                        '''
                        package_parsed[byte_num] = [self.protocol[byte_num], value]

        # 每一帧报文解析的结果 以 pyqtSignal 信号发送到主窗口
        self.update_switch_signal.emit(package_parsed)


if __name__ == '__main__':

    # packagefromtu = PackageFromTU()
    # tu_package = bytearray([00, 00, 15, 00, 00,
    #                         00, 00, 2, 00, 00,
    #                         10, 1,  2,  00, 00,
    #                         10, 22, 10])
    # tu_package.append(sum(tu_package) & 0xFF)   # 加上crc校验位
    # packagefromtu.parse_tu_package(tu_package)

    protocol = {
        12: {
            0: '前灯',
            3: '后灯'
        },
        14: {
            0: '正常',
            1: '异常',
            '0-1': '测试模式',
            # '5-6': '校准模式'
        },
        24: '前进',
        '28-30': '后退'
    }
    ou_package = bytearray([0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x09, 0x00, 0x63, 0x00,     # 前灯后灯 测试模式 校准模式
                            0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x64, 0x00,     # 前进 100
                            0x00, 0x00, 0x00, 0x64, 0x00,     # 后退 25600
                            ])

    package_from_ou = PackageFromOU(protocol)
    package_from_ou.parse_ou_package(ou_package)
    # print(result)