from mu_can_protocol import CAN_PROTOCOLS
from CANalyst_init import open_device, receive_can_data
from mu_can_parse import parse_can_message

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
        for can_index in [0]:  # 轮询通道 0 和 1 (ch1/ch2)
            receive_buffer, result = receive_can_data(device_type, device_index, can_index)
            if result > 0:
                for i in range(result):
                    frame = receive_buffer[i]
                    frame_id = frame.ID
                    if frame_id == 0x9c4:
                        frame_data = frame.Data[:frame.DataLen - 1] # 不要最后一个字节心跳信号不做处理
                    elif frame_id == 0x1:
                        frame_data = frame.Data[1:] # 不要第一个字节
                    else:
                        frame_data = frame.Data[:frame.DataLen]  # 获取当前帧的数据
                    
                    # 将数据转换为元组便于比较
                    # frame_data_tuple = tuple(frame_data)

                    # 检查此CAN ID是否已经有记录
                    if frame_id not in previous_messages or previous_messages[frame_id] != frame_data:
                        # 打印 CAN 数据
                        print(f"\nCAN_ID: {hex(frame_id)}  Data: {[hex(x) for x in frame_data]}")
                        # 解析 CAN 报文
                        parse_can_message(frame_id, frame_data)

                        # 记录当前帧数据
                        previous_messages[frame_id] = frame_data

                        