import socket
import threading
import time

from typing import Optional, Tuple

from .package_send import QueryCollectionStatus as QueryStatus
from .package_parse import PackageFromTU

class NetworkManager:
    ''' 网络管理, 处理UDP通信 '''

    # 信号定义


    def __init__(self):
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
        self.mu_package_send: Optional[bytearray] = None
        self.tu_package_recv: Optional[bytearray] = None
        self.ou_package_recv: Optional[bytearray] = None
        self.send_tu_addr: Optional[Tuple[str, int]] = None
        self.send_mu_addr: Optional[Tuple[str, int]] = None

        self.tu_package_receiver: Optional[PackageFromTU] = PackageFromTU()

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
                print('请输入接收OU的端口!')

        except OSError as e:
            print('端口可能被占用了')
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
            except Exception as e:
                break

    def stop_receiving_ou(self):
        ''' 停止OU数据接收 '''
        self.is_receiving_ou = False
        if self.recv_ou_socket:     # and self.recv_ou_socket:
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
                print('请输入接收TU的端口!')

        except OSError as e:
            print('端口可能被占用了')
            return False


    def recving_tu_loop(self):
        ''' 接收循环 '''
        while self.is_receiving_tu and self.recv_tu_socket:   # and self.package_recv:
            try:
                self.tu_package_recv, tu_addr = self.recv_tu_socket.recvfrom(1024)

                # tu_package = ' '.join(f'{byte:02X}' for byte in self.tu_package_recv)
                # print(f'recv_from: {tu_addr[0]} {tu_addr[1]}\tRaw Data: {tu_package}')

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
                print('请输入接收给TU发送数据的端口!')
                return False

        except OSError as e:
            return False

    def sending_tu_loop(self, cycle_ms: int):
        '''发送循环

        Args:
            cycle_ms: 发送周期(毫秒)
        '''
        while self.is_sending_tu and self.send_tu_socket:
            try:
                self.send_tu_socket.sendto(QueryStatus.package_send(), self.send_tu_addr)

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
                      mu_ip: str, mu_recv_port: int,
                      package_to_mu: bytearray, cycle_ms: int) -> bool:
        ''' 开始发送数据

        Args:
            local_ip: 本地IP地址
            send_mu_port: 给MU发送数据的端口
            mu_ip: MU IP地址
            mu_recv_port: MU接收端口
            package_to_mu: 要发送给MU的数据包
            cycle_ms: 发送周期(毫秒)

        Returns:
            bool: 连接是否成功
        '''
        try:
            self.send_mu_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.send_mu_socket.bind((local_ip, int(send_mu_port)))

            self.mu_package_send = package_to_mu
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
                print('请输入给MU发送数据的端口!')

        except OSError as e:
            return False

    def sending_mu_loop(self, cycle_ms: int):
        '''发送循环

        Args:
            cycle_ms: 发送周期(毫秒)
        '''
        while self.is_sending_mu and self.send_mu_socket and self.mu_package_send:
            try:
                self.send_mu_socket.sendto(self.mu_package_send, self.send_mu_addr)

                time.sleep(cycle_ms / 1000)
            except Exception as e:
                break

    def stop_sending_mu(self):
        ''' 停止给MU发包 '''
        self.is_sending_mu = False
        if self.send_mu_socket:
            self.send_mu_socket.close()
            self.send_mu_socket = None
