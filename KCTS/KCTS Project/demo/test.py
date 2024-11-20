import socket
import threading

# 本机设备的IP和接收端口
LOCAL_IP = "192.168.1.23"
RECEIVE_PORT = 8000
SEND_PORT = 9000

# 目标设备的IP和接收端口
TARGET_IP = "192.168.1.3"
TARGET_PORT = 8888

def receiver():
    """接收端"""
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_sock.bind((LOCAL_IP, RECEIVE_PORT))  # 绑定本地接收端口

    print(f"接收端已启动，在 {LOCAL_IP}:{RECEIVE_PORT} 等待数据...")
    while True:
        data, addr = recv_sock.recvfrom(1024)  # 接收数据
        print(f"接收到来自 {addr} 的数据: {data.decode('utf-8')}")

def sender():
    """发送端"""
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send_sock.bind((LOCAL_IP, SEND_PORT))  # 绑定本地发送端口

    print(f"发送端已启动，从 {LOCAL_IP}:{SEND_PORT} 发送到 {TARGET_IP}:{TARGET_PORT}...")
    while True:
        message = input("请输入要发送的消息: ")
        send_sock.sendto(message.encode('utf-8'), (TARGET_IP, TARGET_PORT))  # 发送数据

if __name__ == "__main__":
    # 创建接收线程
    recv_thread = threading.Thread(target=receiver)
    recv_thread.daemon = True
    recv_thread.start()

    # 创建发送线程
    send_thread = threading.Thread(target=sender)
    send_thread.daemon = True
    send_thread.start()

    recv_thread.join()
    send_thread.join()

