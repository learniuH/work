from CANalyst_init import open_device, receive_can_data
from mu_can_parse import parse_can_message

if __name__ == "__main__":
    device_type = 4  # 设备类型为 USBCAN-2A 或 CANalyst-II
    device_index = 0  # 设备索引
    # 打开 Canalyst 并初始化 ch1 和 ch2
    for can_index in [0, 1]:
        open_device(device_type, device_index, can_index)

    # 存储上一次的报文（以CAN ID为键，报文数据为值）
    previous_messages = {}

    while True:
        # 轮询通道 0(ch1) 和 1(ch2)
        for can_index in [0]:
            # 接收到 result 个 receive_buffer
            receive_buffer, result = receive_can_data(device_type, device_index, can_index)
            for i in range(result):
                frame = receive_buffer[i]
                frame_id = frame.ID
                # 过滤 0x9c4 和 0x1 的心跳
                if frame_id == 0x9c4: # 过滤最后一个Byte
                    frame_data = frame.Data[:frame.DataLen - 1]
                elif frame_id == 0x1: # 过滤第一个Byte
                    frame_data = frame.Data[1:] 
                else: # 获取当前帧的数据
                    frame_data = frame.Data[:frame.DataLen]
                
                # 检查此CAN ID是否已经有记录
                if frame_id not in previous_messages or previous_messages[frame_id] != frame_data:
                    # 打印 CAN 数据
                    hex_data = ' '.join(f'{byte:02X}' for byte in frame_data)
                    print(f'\nCAN_ID: {hex(frame_id)}  Data: \033[33m{hex_data}\033[0m')

                    # 解析 CAN 报文
                    parse_can_message(frame_id, frame_data)

                    # 记录当前帧数据
                    previous_messages[frame_id] = frame_data