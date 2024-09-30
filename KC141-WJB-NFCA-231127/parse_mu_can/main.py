from mu_can_protocol import CAN_PROTOCOLS
from CANalyst_init import open_device, receive_can_data

# 解析 CAN 报文
def parse_can_message(frame_id, frame_data):
    frame_id_hex = hex(frame_id)
    protocol = CAN_PROTOCOLS.get(frame_id_hex)
    # print(protocol)

    if not protocol:
        return f"未定义协议的帧ID: {frame_id_hex}, 数据: {[hex(x) for x in frame_data]}"
    
    parsed_data = {}
    for byte_index, byte_value in enumerate(frame_data):
        byte_key = f"byte{byte_index + 1}"
        if byte_key in protocol:
            if isinstance(protocol[byte_key], dict):
                byte_protocol = protocol[byte_key]
                for bit_position in range(8):
                    bit_value = (byte_value >> bit_position) & 1
                    bit_key = f"Bit{bit_position}"
                    if bit_key in byte_protocol:
                        parsed_data[f"{byte_key} - {byte_protocol[bit_key]}"] = bit_value
            else:
                #parsed_data[byte_key] = byte_value
                parsed_data[f"{byte_key} - {protocol[byte_key]}"] = byte_value
    return parsed_data

# 打印解析结果
def print_can_message(parsed_data):
    if isinstance(parsed_data, str):
        print(parsed_data)  # 对于未定义协议的帧，直接输出
    else:
        for key, value in parsed_data.items():
            if value:
                print(f"{key}: {value}")

# 主函数
if __name__ == "__main__":
    device_type = 4  # 设备类型为 USBCAN-2A 或 CANalyst-II
    device_index = 0  # 设备索引

    # 创建一个字典，存储上一次的报文（以CAN ID为键，报文数据为值）
    previous_messages = {}

    # 打开 Canalyst 并初始化 ch1 和 ch2
    for can_index in [0, 1]:
        open_device(device_type, device_index, can_index)

    # 接收 两条通道上的 CAN 报文
    while True:
        for can_index in [0]:  # 轮询通道 0 和 1
            receive_buffer, result = receive_can_data(device_type, device_index, can_index)
            if result > 0:
                for i in range(result):
                    frame = receive_buffer[i]
                    frame_id = frame.ID
                    if frame_id == 0x9c4:
                        frame_data = frame.Data[:frame.DataLen - 1] # 心跳信号不做处理
                    else:
                        frame_data = frame.Data[:frame.DataLen]  # 获取当前帧的数据

                    # 将数据转换为元组便于比较
                    frame_data_tuple = tuple(frame_data)

                    # 检查此CAN ID是否已经有记录
                    if frame_id not in previous_messages or frame_id != 0x9c4 and previous_messages[frame_id] != frame_data_tuple or frame_id == 0x9c4 and previous_messages[frame_id][:7] != frame_data_tuple:
                        # 打印 CAN 数据
                        print(f"\nCAN_ID: {hex(frame_id)}, 数据: {[hex(x) for x in frame_data]}")
                        # 解析 CAN 报文
                        parsed_data = parse_can_message(frame_id, frame_data)
                        # 打印解析后的数据
                        print_can_message(parsed_data)
                        
                        # 记录当前帧数据
                        previous_messages[frame_id] = frame_data_tuple
