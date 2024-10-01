from mu_can_protocol import CAN_PROTOCOLS
from CANalyst_init import open_device, receive_can_data

def parse_can_message(frame_id, frame_data):
    frame_id_hex = hex(frame_id)
    # frame_id 的 CAN 协议
    frame_protocol = CAN_PROTOCOLS.get(frame_id_hex)

    # 这句话用于调试, 功能完善后删除
    if not frame_protocol:
        return f"未定义协议的帧ID: {frame_id_hex}, 数据: {[hex(x) for x in frame_data]}"
    
    parsed_data = {}

    for byte_index, byte_value in enumerate(frame_data):
        byte_num = byte_index + 1
        if byte_num in frame_protocol:
            # 获取字节的定义
            byte_protocol = frame_protocol.get(byte_num)
            for key in byte_protocol.keys():
                # 按 bit 处理
                if key < 8:
                    for bit_position, function in byte_protocol.items():
                        if (byte_value >> bit_position) & 1:
                            parsed_data[f'bit{bit_position}: {function}'] = 1
                    print(f'Byte{byte_num} {parsed_data}')
                #按 byte 处理
                else:
                    pass

            

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
                            print(f"\nCAN_ID: {hex(frame_id)}  Data: {[hex(x) for x in frame_data]}")
                            # 解析 CAN 报文
                            parse_can_message(frame_id, frame_data)

                            # 记录当前帧数据
                            previous_messages[frame_id] = frame_data_tuple

                        