from PyQt5.QtCore import pyqtSignal, QObject

from .tu_protocol import StatusFeedBack


class PackageFromTU(QObject):
    ''' 处理来自TU的有效数据包 '''

    # 当检测到 DO 置 1 或 PWM 非 0 时, 发出pyqtSignal信号到主窗口
    update_do_signal = pyqtSignal(str, bool)
    update_pwm_signal = pyqtSignal(str, int)

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
        self.previous_mu_status_package = None

    #     self.setup()
    #
    # def setup(self):
    #     self.update_do_signal.connect(self.do)
    #     self.update_pwm_signal.connect(self.pwm)
    #
    # def do(self, do_num: str):
    #     print(f'{do_num}触发了')
    #
    # def pwm(self, pwm_num: str, value: float):
    #     print(f'{pwm_num}触发了, value is {value}')


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
                            print(f'{description} emit True!')
                        else:
                            self.update_do_signal.emit(description, False)
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
                    print(f'{StatusFeedBack.data_field_protocol[byte_num]} emit {current_pwm_value}')

        # 更新previous包
        self.previous_mu_status_package = self.package


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


    def parse_tu_package(self, package: bytearray):
        ''' 对来自TU的数据包区分并解析 '''
        self.package = package
        if self.package[0] == 0x5A and self.crc_check():
            # crc校验通过后对包长度进行校验
            if self.package_length_check():
                # 通过消息类型字节对TU的数据包进行处理
                self.define_message_type(self.package[7])



if __name__ == '__main__':
    packagefromtu = PackageFromTU()
    tu_package = bytearray([00, 00, 15, 00, 00,
                            00, 00, 2, 00, 00,
                            10, 1,  2,  00, 00,
                            10, 22, 10])
    tu_package.append(sum(tu_package) & 0xFF)   # 加上crc校验位
    packagefromtu.parse_tu_package(tu_package)
