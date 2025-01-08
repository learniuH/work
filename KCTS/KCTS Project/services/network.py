import socket
import serial
import threading
import time

from typing import Optional, Tuple, Literal

from PyQt5.QtCore import QObject, pyqtSignal

from .package_send import QueryCollectionStatus, PackageToMu
from .package_parse import PackageFromTU, PackageFromOU
from config.error_message import ErrorMessage

class NetworkManager(QObject):
    ''' 网络管理类, 处理UDP通信 '''

    program_exception_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.send_tu_socket: Optional[socket.socket] = None
        self.send_mu_socket: Optional[socket.socket] = None
        self.recv_tu_socket: Optional[socket.socket] = None
        self.recv_ou_socket: Optional[socket.socket] = None
        self.send_tu_thread: Optional[threading.Thread] = None
        self.send_mu_thread: Optional[threading.Thread] = None
        self.recv_ou_thread: Optional[threading.Thread] = None
        self.recv_tu_thread: Optional[threading.Thread] = None
        self.is_sending_tu: bool = False
        self.is_sending_mu: bool = False
        self.is_receiving_ou: bool = False
        self.is_receiving_tu: bool = False
        self.tu_package_recv: Optional[bytearray] = None                # TU发给TS的所有类型包
        self.ou_package_recv: Optional[bytearray] = None                # OU发给TS的包
        self.ou_package_parsed: bool = False                            # OU的包是否被解析的标志位
        self.send_tu_addr: Optional[Tuple[str, int]] = None
        self.send_mu_addr: Optional[Tuple[str, int]] = None

        self.tu_package_receiver: Optional[PackageFromTU] = PackageFromTU()
        self.ou_package_receiver: Optional[PackageFromOU] = None        # 主窗口发出Excel解析的信号才实例化


    def ou_package_receiver_inst(self, protocol: dict):
        ''' 接收到comboBox的index切换的信号就实例化 ou_package_receiver '''
        self.ou_package_receiver = PackageFromOU(protocol)

    def start_receiving_ou(self, local_ip: str,
                           recv_ou_port: str,
                           mu_ip: str,
                           mu_recv_port: str) -> bool:
        '''开始监听数据

        Args:
            local_ip: 本地IP地址
            recv_ou_port: 接收OU数据的端口
            mu_ip: MU IP 地址
            mu_recv_port: MU 接收端口

        Returns:
            bool: 端口绑定是否成功
        '''
        try:
            self.recv_ou_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.recv_ou_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # 接收端口复用
            self.recv_ou_socket.bind((local_ip, int(recv_ou_port)))   # 接收OU数据的端口

            self.send_mu_addr = (mu_ip, int(mu_recv_port))
            self.is_receiving_ou = True
            self.recv_ou_thread = threading.Thread(target=self.recving_ou_loop, daemon=True)
            self.recv_ou_thread.start()

            return True

        except ValueError as e:
            if 'invalid literal for int() with base 10' in str(e):
                self.program_exception_signal.emit(ErrorMessage.ENTER_RECV_PORT)

        except OSError as e:
            # 端口被占用
            self.program_exception_signal.emit(f'{recv_ou_port} {ErrorMessage.PORT_OCCUPIED}')
            return False


    def recving_ou_loop(self):
        ''' 接收 OU 的数据并转发到 MU '''
        while self.is_receiving_ou and self.recv_ou_socket:   # and self.package_recv:
            try:
                self.ou_package_recv, ou_addr = self.recv_ou_socket.recvfrom(1024)
                print(f'正在从{ou_addr}接收OU数据')

                if '' not in self.send_mu_addr:
                    # 将OU的数据转发到MU
                    self.recv_ou_socket.sendto(self.ou_package_recv, self.send_mu_addr)

                # 对接收到的数据进行解析
                if self.ou_package_receiver is not None:
                    # 每接收到一帧数据, 解析所有的字节
                    self.ou_package_receiver.parse_ou_package(self.ou_package_recv)

            except Exception as e:
                break

    def stop_receiving_ou(self):
        ''' 停止OU数据接收 '''
        self.is_receiving_ou = False
        if self.recv_ou_socket:
            self.recv_ou_socket.close()
            self.recv_ou_socket = None

    def start_receiving_tu(self, local_ip: str, recv_tu_port: str) -> bool:
        '''开始监听数据

        Args:
            local_ip: 本地IP地址
            recv_tu_port: 接收TU数据的端口

        Returns:
            bool: 端口绑定是否成功
        '''
        try:
            self.recv_tu_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.recv_tu_socket.bind((local_ip, int(recv_tu_port)))    # 接收TU数据的端口

            self.is_receiving_tu = True
            self.recv_tu_thread = threading.Thread(target=self.recving_tu_loop, daemon=True)
            self.recv_tu_thread.start()

            return True

        except ValueError as e:
            if 'invalid literal for int() with base 10' in str(e):
                self.program_exception_signal.emit(ErrorMessage.ENTER_RECV_TU_PORT)

        except OSError as e:
            # 端口占用
            self.program_exception_signal.emit(f'{recv_tu_port} {ErrorMessage.PORT_OCCUPIED}')
            return False


    def recving_tu_loop(self):
        ''' 接收循环 '''
        while self.is_receiving_tu and self.recv_tu_socket:   # and self.package_recv:
            try:
                self.tu_package_recv, tu_addr = self.recv_tu_socket.recvfrom(1024)
                print(f'Rx: {tu_addr}: ' + ' '.join(f'{byte:02X}' for byte in self.tu_package_recv))
                # 处理来自TU的数据包
                self.tu_package_receiver.parse_tu_package(self.tu_package_recv)

            except Exception as e:
                break

    def stop_receiving_tu(self):
        ''' 停止OU数据接收 '''
        self.is_receiving_tu = False
        if self.recv_tu_socket:     # and self.recv_ou_socket:
            self.recv_tu_socket.close()
            self.recv_tu_socket = None


    def start_sending_tu(self, local_ip: str, send_tu_port: str,
                      tu_ip: str, tu_recv_port: int, cycle_ms: int) -> bool:
        ''' 开始发送数据

        Args:
            local_ip: 本地IP地址
            send_tu_port: 给TU发送数据的端口
            tu_ip: TU IP地址
            tu_recv_port: 目标端口
            cycle_ms: 发送周期-ms

        Returns:
            bool: 连接是否成功
        '''
        try:
            self.send_tu_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.send_tu_socket.bind((local_ip, int(send_tu_port)))

            self.send_tu_addr = (tu_ip, int(tu_recv_port))
            self.is_sending_tu = True

            self.send_tu_thread = threading.Thread(
                target=self.sending_tu_loop,
                args=(cycle_ms,),
                daemon=True
            )
            self.send_tu_thread.start()
            return True

        except ValueError as e:
            if 'invalid literal for int() with base 10' in str(e):
                self.program_exception_signal.emit(ErrorMessage.ENTER_SEND_TU_PORT)
                return False

        except OSError as e:
            # 端口占用
            self.program_exception_signal.emit(f'{send_tu_port} {ErrorMessage.PORT_OCCUPIED}')
            return False

    def sending_tu_loop(self, cycle_ms: int):
        '''发送循环

        Args:
            cycle_ms: 发送周期(毫秒)
        '''
        while self.is_sending_tu and self.send_tu_socket:
            try:
                self.send_tu_socket.sendto(QueryCollectionStatus.package_send(), self.send_tu_addr)

                time.sleep(cycle_ms / 1000)
            except Exception as e:
                break

    def stop_sending_tu(self):
        ''' 停止连接 '''
        self.is_sending_tu = False
        if self.send_tu_socket:
            self.send_tu_socket.close()
            self.send_tu_socket = None


    def start_sending_mu(self, local_ip: str, send_mu_port: str,
                      mu_ip: str, mu_recv_port: int, cycle_ms: int) -> bool:
        ''' 开始发送数据

        Args:
            local_ip: 本地IP地址
            send_mu_port: 给MU发送数据的端口
            mu_ip: MU IP地址
            mu_recv_port: MU接收端口
            cycle_ms: 发送周期(毫秒)

        Returns:
            bool: 连接是否成功
        '''
        try:
            self.send_mu_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.send_mu_socket.bind((local_ip, int(send_mu_port)))

            # self.mu_package_send = package_to_mu
            self.send_mu_addr = (mu_ip, int(mu_recv_port))
            self.is_sending_mu = True

            self.send_mu_thread = threading.Thread(
                target=self.sending_mu_loop,
                args=(cycle_ms,),
                daemon=True
            )
            self.send_mu_thread.start()
            return True

        except ValueError as e:
            if 'invalid literal for int() with base 10' in str(e):
                self.program_exception_signal.emit(ErrorMessage.ENTER_SEND_MU_PORT)

        except OSError as e:
            self.program_exception_signal.emit(f'{send_mu_port} {ErrorMessage.PORT_OCCUPIED}')
            return False

    def sending_mu_loop(self, cycle_ms: int):
        '''发送循环

        Args:
            cycle_ms: 发送周期(毫秒)
        '''
        while self.is_sending_mu and self.send_mu_socket: # and self.mu_package_send:
            try:
                self.send_mu_socket.sendto(PackageToMu.package, self.send_mu_addr)

                time.sleep(cycle_ms / 1000)
            except Exception as e:
                break

    def stop_sending_mu(self):
        ''' 停止给MU发包 '''
        self.is_sending_mu = False
        if self.send_mu_socket:
            self.send_mu_socket.close()
            self.send_mu_socket = None


class SerialAssistant(QObject):
    ''' 串口助手的线程管理器 '''
    ebyte_config_received_signal = pyqtSignal(list)                             # 亿佰特配置数据接收完成信号

    def __init__(self):
        super().__init__()
        self.serial: Optional[serial.Serial] = None                             # 接收串口数据的对象
        self.recv_serial_port_thread: Optional[threading.Thread] = None         # 接收串口数据的线程
        self.is_receiving_serial: bool = False

    def start_recv_serial(self, port: str, baudrate: int,
                          bytesize: Literal[serial.FIVEBITS, serial.SIXBITS, serial.SEVENBITS, serial.EIGHTBITS],
                          parity: Literal[serial.PARITY_NONE, serial.PARITY_ODD, serial.PARITY_EVEN],
                          stopbits: Literal[serial.STOPBITS_ONE, serial.STOPBITS_ONE_POINT_FIVE, serial.STOPBITS_TWO]
                          ):
        '''
        开启接收串口数据的线程
        :param port: 端口号
        :param baudrate: 波特率
        :param bytesize: 数据位
        :param parity: 奇偶校验
        :param stopbits: 停止位
        :return:
        '''
        try:
            self.serial = serial.Serial(port=port, baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits)

            self.is_receiving_serial = True

            self.recv_serial_port_thread = threading.Thread(target=self.receiving_serial_loop, daemon=True)
            self.recv_serial_port_thread.start()

        except serial.SerialException as e:
            print(f'串口打开失败: {e}')


    def receiving_serial_loop(self):
        ''' 接收串口数据的线程 '''
        count       = 0
        length      = 0                         # 数据包数据域长度
        ebyte_config_recv_flag = False          # 亿佰特配置数据接收
        ashing_config_recv_flag = False         # 泽耀配置数据接收
        recv_buffer = []                        # 数据接收缓存区
        while self.is_receiving_serial and self.serial.is_open:
            # 检查是否有数据等待接收
            if self.serial.in_waiting:
                serial_port_data = self.serial.read(self.serial.in_waiting)
                if count == 0:
                    # 接收第一个字节 包头
                    if serial_port_data[0] == 0xC1:
                        recv_buffer.append(serial_port_data[0])
                        ebyte_config_recv_flag = True
                        print(f'已接受亿佰特包头！')
                    else:
                        # 接收泽耀模块的包头
                        pass
                    # else:
                    #     continue
                elif ebyte_config_recv_flag:
                    # 接收亿佰特配置数据包
                    if count == 1:
                        # 寄存器起始地址
                        recv_buffer.append(serial_port_data[0])
                        print(f'第一个字节寄存器地址已接收')
                    elif count == 2:
                        # 长度
                        if serial_port_data[0] > 0:
                            recv_buffer.append(serial_port_data[0])
                            length = recv_buffer[count]
                            print(f'第二个字节长度已接收')
                        else:
                            # 如果第三个字节为0(长度为0) 丢弃这一包, 重新开始接收
                            count = 0
                            recv_buffer = []
                            ebyte_config_recv_flag = False
                            print(f'收到亿佰特配置包长度为0, 重新开始接收 !')
                    elif count == 3:
                        # 数据域接收
                        if length > 0:
                            recv_buffer.append(serial_port_data[0])
                            print(f'数据域接收')
                            length -= 1
                            if length == 0:
                                # 数据接收完成 !
                                print(f'亿佰特Lora配置参数接收完成 !{recv_buffer}')
                                self.ebyte_config_received_signal.emit(recv_buffer)
                                count = 0
                                recv_buffer = []
                                ebyte_config_recv_flag = False

                            # 数据域接收数据 跳过 count + 1
                            continue


                elif ashing_config_recv_flag:
                    # 接收泽耀配置数据包
                    pass

                count += 1


                print(f'串口Rx:' + ' '.join(f'{byte:02X}' for byte in serial_port_data))


    def stop_receiving_serial(self):
        ''' 停止接收串口数据的线程 '''
        self.is_receiving_serial = False
        if self.serial:
            self.serial.close()
            self.serial = None

