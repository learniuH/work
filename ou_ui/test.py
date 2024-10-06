import socket
import time
import random

def generate_mock_data():
    # 生成一个56字节的模拟数据包
    data = bytearray(56)
    
    # 设置一些随机值，模拟实际数据
    data[23] = random.randint(0, 5)  # 挡位
    data[24] = random.randint(0, 63)  # 随机设置一些标志位
    data[25] = random.randint(0, 255)  # 随机设置一些标志位
    data[26] = random.randint(0, 255)  # 随机设置一些标志位
    
    
    # 设置一些模拟的模拟量输入
    data[33] = random.randint(0, 100)  # 左转
    data[34] = random.randint(0, 100)  # 右转
    data[35] = random.randint(0, 100)  # 装料
    data[36] = random.randint(0, 100)  # 卸料
    data[37] = random.randint(0, 100)  # 降臂
    data[38] = random.randint(0, 100)  # 升臂
    data[39] = random.randint(0, 100)  # 油门
    data[40] = random.randint(0, 100)  # 辅刹

    data[43] = 3 # 测试模式
    
    return bytes(data)

def send_mock_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('192.168.2.5', 8004)  # 确保这与main.py中的地址和端口匹配
    
    try:
        while True:
            mock_data = generate_mock_data()
            sock.sendto(mock_data, server_address)
            print(f"Sent mock UDP packet: {mock_data.hex()}")
            time.sleep(1)  # 每秒发送一次数据
    except KeyboardInterrupt:
        print("Stopping UDP simulation...")
    finally:
        sock.close()

if __name__ == "__main__":
    print("Starting UDP packet simulation. Press Ctrl+C to stop.")
    send_mock_udp()
