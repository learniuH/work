import socket

# 创建基于 UDP 协议的 IPV4 socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('192.168.2.233', 8004))  # 监听电脑的IP和端口

print("Listening for UDP packets on 192.168.2.233:8004...")

# 保存上一条接收到的报文的数据域
previous_data_field = None

# 定义每个字节的bit描述
bit_definitions = {
    25: {
        0: "智能导向",
        1: "点刹车",
        2: "安全开关左",
        3: "加档",
        4: "减档",
        5: "安全开关右",
        6: "预留",
        7: "预留"
    },
    26: {
        0: "平台使能",
        1: "前进档",
        2: "后退档",
        3: "车辆切换+",
        4: "车辆切换-",
        5: "一键逃逸",
        6: "自动灭火",
        7: "报警屏蔽"
    },
    27: {
        0: "前灯",
        1: "后灯",
        2: "引擎保持",
        3: "引擎启动",
        4: "拖车",
        5: "驻刹",
        6: "急停",
        7: "喇叭"
    },
    29: {
        0: "智能导向",
        1: "点刹车",
        2: "安全开关左",
        3: "加档",
        4: "减档",
        5: "安全开关右",
        6: "预留",
        7: "预留"
    },
    30: {
        0: "平台使能",
        1: "前进档",
        2: "后退档",
        3: "车辆切换+",
        4: "车辆切换-",
        5: "一键逃逸",
        6: "自动灭火",
        7: "报警屏蔽"
    },
    31: {
        0: "前灯",
        1: "后灯",
        2: "引擎保持",
        3: "引擎启动",
        4: "拖车",
        5: "驻刹",
        6: "急停",
        7: "喇叭"
    }
}

# 对第15到42字节，若字节值不为0则视为触发
bytes_definition = {
    24: "挡位",
    28: "挡位",
    34: "左转",
    35: "右转",
    36: "装料",
    37: "卸料",
    38: "降臂",
    39: "升臂",
    40: "油门",
    41: "辅刹"
}

# 对字节的每一位进行解析
def parse_bits(byte, bit_definitions):
    bit_status = {}
    for bit_position, label in bit_definitions.items():
        if (byte >> bit_position) & 1:  # 只在bit位为1时触发
            bit_status[label] = "Triggered"
    return bit_status

# 打印单字节数据状态
def process_byte(byte_number, data):
    if byte_number in bit_definitions:
        byte = data[byte_number - 1]  # 获取指定字节
        status = parse_bits(byte, bit_definitions[byte_number])
        if status:
            print(f"\nByte{byte_number}:{status}")
    elif byte_number in bytes_definition:
        byte = data[byte_number - 1]
        if byte != 0:  # 只要字节不为0就认为触发
            print(f"\nByte{byte_number} ({bytes_definition[byte_number]}): {byte}")

while True:
    try:
        # 接收 UDP socket 的数据, 最多接收 1024Byte
        data, addr = sock.recvfrom(1024)
        
        # 确保报文长度为56字节
        if len(data) == 56:
            # 提取当前数据域（第24个字节到第41个字节）
            current_data_field = data[23:41]

            # 如果当前数据域和 previous_data_field 不一样，打印出来
            if current_data_field != previous_data_field:
                print(f"\nReceived packet from {addr}:")
                # 将数据以十六进制(两位)格式打印,并用 ' ' 连接起来
                hex_data = ' '.join(f'{byte:02X}' for byte in data)
                print(f"Data (hex): {hex_data}")

                # 处理数据域
                for byte_number in range(24, 42):
                    process_byte(byte_number, data)

                # 更新保存的中间部分报文
                previous_data_field = current_data_field
        else:
            print("Received packet too short to process.")

    except KeyboardInterrupt:
        print("\nStopped by user")
        break
    except Exception as e:
        print(f"Error receiving packet: {e}")

# 关闭Socket
sock.close()
