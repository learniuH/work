import socket
import threading
import time
from itertools import cycle
from typing import Optional, Tuple

class NetworkManager:
    ''' 网络管理, 处理UDP通信 '''

    # 信号定义


    def __init__(self):
        self.send_socket: Optional[socket.socket] = None
        self.recv_socket: Optional[socket.socket] = None
        self.send_thread: Optional[threading.Thread] = None
        self.recv_thread: Optional[threading.Thread] = None
        self.is_sending: bool = False
        self.is_receiving: bool = False
        self.package_send: Optional[bytearray] = None
        self.package_recv: Optional[bytearray] = None
        self.target_address: Optional[Tuple[str, int]] = None
        self.local_address: Optional[Tuple[str, int]] = None

    def start_receiving(self, local_ip: str, recv_port: str) -> bool:
        '''开始监听数据

        Args:
            local_ip: 本地IP地址
            recv_port: 监听端口

        Returns:
            bool: 端口绑定是否成功
        '''
        try:
            self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.recv_socket.bind((local_ip, int(recv_port)))    # 绑定接收端口

            self.is_receiving = True
            self.send_thread = threading.Thread(target=self.recving_loop, daemon=True)
            self.send_thread.start()

            return True

        except OSError as e:
            return False


    def recving_loop(self):
        ''' 接收循环 '''
        while self.is_receiving and self.recv_socket:   # and self.package_recv:
            try:
                self.package_recv, addr = self.recv_socket.recvfrom(1024)
                print(f'正在从{addr}接收数据')
            except Exception as e:
                break

    def stop_receiving(self):
        ''' 停止接收 '''
        self.is_receiving = False
        if self.recv_socket:
            self.recv_socket.close()
            self.recv_socket = None
            print('数据接收停止')

    def start_sending(self, local_ip: str, send_port: str,
                      target_ip: str, target_port: int,
                      package: bytearray, cycle_ms: int) -> bool:
        ''' 开始发送数据

        Args:
            local_ip: 本地IP地址
            send_port: 本地端口
            target_ip: 目标IP地址
            target_port: 目标端口
            package: 要发送的数据包
            cycle_ms: 发送周期(毫秒)

        Returns:
            bool: 连接是否成功
        '''
        try:
            self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.send_socket.bind((local_ip, int(send_port)))

            self.package_send = package
            self.target_address = (target_ip, int(target_port))
            self.is_sending = True

            self.send_thread = threading.Thread(
                target=self.sending_loop,
                args=(cycle_ms,),
                daemon=True
            )
            self.send_thread.start()
            print('已经走到start sending 并且线程启动了')
            return True

        except OSError as e:
            return False

    def sending_loop(self, cycle_ms: int):
        '''发送循环

        Args:
            cycle_ms: 发送周期(毫秒)
        '''
        print('已经走到sending loop了')
        while self.is_sending and self.send_socket and self.package_send:
            try:
                self.send_socket.sendto(self.package_send, self.target_address)

                time.sleep(cycle_ms / 1000)
            except Exception as e:
                break

    def stop_sending(self):
        ''' 停止连接 '''
        self.is_sending = False
        if self.send_socket:
            self.send_socket.close()
            self.send_socket = None
            print('发送数据停止')


