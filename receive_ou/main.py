import socket
from ou_udp_protocol import OU_PROTOCOLS
from ou_udp_parse import parse_ou_message

# 创建基于 UDP 协议的 IPV4 socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('192.168.2.233', 8004))  # 监听电脑的IP和端口

if __name__ == "__main__":
    # 保存上一包数据
    previous_data_field = None

    while True:
        # 接收 UDP socket 的数据, 最多接收 1024Byte
        data, addr = sock.recvfrom(1024)

        if(len(data)) == 56:
            # 提取数据域: Byte24-Byte51
            current_data_field = data[23: 51]
            # 数据域改变时,对其进行处理
            if current_data_field != previous_data_field:
                # 打印 UDP 报文
                hex_data = ' '.join(f'{byte:02X}' for byte in data)
                print(f'\nData: \033[33m{hex_data}\033[0m')

                #解析报文
                for byte_num in OU_PROTOCOLS:
                    parse_ou_message(byte_num, data)
            
            # 更新保存的数据域
            previous_data_field = current_data_field