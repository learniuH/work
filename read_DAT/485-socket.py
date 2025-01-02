import socket
import threading
import time

local_port = 8888                                               # 本地 端口

target_ip = '192.168.48.5'                                      # MU IP
target_port = 6666                                              # 端口

cycle = 100                                                     # 发送周期 100 ms


class SocketSender:
    def __init__(self):
        self.local_ip = socket.gethostbyname(socket.gethostname())                      # 电脑本地 IP
        self.local_port = local_port                                                    # 电脑发送端口
        self.target_ip = target_ip                                                      # MU IP
        self.target_port = target_port                                                  # MU 端口
        self.cycle = cycle                                                              # 发送周期

        self.packages = None                                                            # 数据包
        self.read_dat()                                                                 # 读取DAT文本, 更新 packages

        self.socket:socket.socket = None                                                # 发送数据的 socket
        self.is_sending = False                                                         # 发送标志位

        # 初始化时打印电脑本地 IP
        print(f'local_ip: {self.local_ip}')

    def start_sending_dat(self):
        ''' 创建 socket 对象, 创建线程 '''

        self.is_sending = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.local_ip, self.local_port))

        send_thread = threading.Thread(target=self.sending_loop, daemon=True)
        send_thread.start()

    def sending_loop(self):
        ''' 发送数据的线程 '''
        i = 0
        while self.is_sending and self.socket and i < len(self.packages):
            self.socket.sendto(bytes(self.packages[i]), (self.target_ip, self.target_port))
            i += 1

            if i == len(self.packages):
                i = 0

            # 发送周期
            time.sleep(cycle / 1000)

    def stop_sending(self):
        ''' 停止给 MU 发送数据 '''
        self.is_sending = False
        if self.socket:
            self.socket.close()
            self.socket = None

    def read_dat(self):
        ''' 打开 DAT 文件, 读取 '''
        with open('./顺时针1圈.DAT', 'rb') as file:
            data = file.read()
            self.parse_packages(data)

    def parse_packages(self, data):
        """
        解析二进制数据并提取以 A3 52 33 01 开头的数据包

        Args:
            data (bytes): 要解析的二进制数据

        Returns:
            list: 提取出的数据包列表
        """
        # 转换头部为字节进行比较
        header = bytes([0x18])
        self.packages = []                                   # 返回的数据包

        # 查找所有头部出现的位置
        current_pos = 0
        while True:
            # 查找下一个头部
            pos = data.find(header, current_pos)

            # 打印调试信息
            print(f"当前位置: {current_pos}, 找到头部位置: {pos}")

            if pos == -1:  # 没有找到更多头部
                # 如果还有剩余数据，将其作为最后一个包
                if current_pos < len(data):
                    last_package = data[current_pos - 1:]
                    if last_package.startswith(header):  # 确保最后一个包也是以正确的头部开始
                        self.packages.append(last_package)
                        print(f"添加最后一个包，长度: {len(last_package)} 字节")
                break

            # 如果这不是第一个包，添加前一个包
            if current_pos > 0 and pos > current_pos:
                package = data[current_pos - 1:pos]
                if package.startswith(header):  # 只添加以正确头部开始的包
                    self.packages.append(package)
                    print(f"添加包，长度: {len(package)} 字节")

            # 关键修复：确保 current_pos 始终向前移动
            current_pos = pos + 1  # 移动到头部后的下一个位置
            if current_pos >= len(data):
                break


if __name__ == '__main__':
    sender = SocketSender()
    sender.start_sending_dat()
    while True:
        pass