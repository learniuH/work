import socket
import time

class UDPer():

    def generate_udp_message(self, length = 27):
        '''生成特定的 UDP 报文'''
        data = bytearray(length)
        data[0] = 255

        #print(f'{bytes(data)}')
        return bytes(data)

    def send_udp_message(self):
        '''创建一个 UDP Socket '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        ######################## 目标的 IP 和 Port ########################
        target_ip = '192.168.3.7'
        target_port = 9000

        try:
            while True:
                # 生成一个消息并发送
                data = self.generate_udp_message()
                sock.sendto(data, (target_ip, target_port))
                print(f'send data:{data}')

                # 间隔 100 毫秒发送一次
                time.sleep(0.1)
        except KeyboardInterrupt:
            print('停止发送')
        finally:
            sock.close()

    def receive_udp_message(self):
        ''' 创建一个 UDP Socket'''
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        ######################## 本地的 IP 和 Port ########################
        local_ip = '192.168.3.7'
        local_port = 8000

        sock.bind((local_ip, local_port))   # 绑定本地的IP和端口

        try:
            while True:
                ''' 接收 UDP 数据'''
                raw_data, addr = sock.recvfrom(1024)
                data = ' '.join(f'{byte:02X}' for byte in raw_data)
                print(f'数据来自: {addr}', end='')
                print(f'{data}')
        except KeyboardInterrupt:
            print('停止接收')
        finally:
            sock.close()
    
if __name__ == '__main__':
    udp = UDPer()   # 创建 UDPer 实例
    #udp.send_udp_message()
    udp.receive_udp_message()
    #udp.generate_udp_message()
    pass

