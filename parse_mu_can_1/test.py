from mu_can_protocol import CAN_PROTOCOLS
import re

def LearniuH_print(parsed_data):
    # ANSI 颜色码,终端显示绿色
    highlight_start = '\033[32m'
    highlight_end = '\033[0m'
    '''
    '\033[31m'  红色
    '\033[32m'  绿色
    '\033[33m'  黄色
    '\033[34m'  蓝色
    '''

    # 正则表达式匹配中文字符
    chinese_characters = re.compile(r'[\u4e00-\u9fff]+')
    
    LearniuH_dict = {}
    
    for key, value in parsed_data.items():
        # 匹配汉字并高亮
        highlighted_key = re.sub(chinese_characters, lambda match: f'{highlight_start}{match.group()}{highlight_end}', key)
        LearniuH_dict[highlighted_key] = value
    
    for key, value in LearniuH_dict.items():
        print(f'{key}: {value}     ', end='')


def parse_can_message(frame_id, frame_data):
    # frame_id_hex = hex(frame_id)
    # frame_id 的 CAN 协议
    frame_protocol = CAN_PROTOCOLS.get(frame_id)

    if not frame_protocol:
        return f"未定义协议的CAN帧: {frame_id}, Data: {[hex(x) for x in frame_data]}"
    
    parsed_data = {}

    for byte_index in range(len(frame_data)):
        byte_num = byte_index + 1
        # 单字节按位处理
        if byte_num in frame_protocol:
            # 获取字节的定义
            byte_protocol = frame_protocol.get(byte_num)
            # 按 bit 处理
            for bit_position, function in byte_protocol.items():
                if (frame_data[byte_index] >> bit_position) & 1:
                    parsed_data[f'Byte{byte_num}_bit{bit_position}: {function}'] = 1
        # 字节整体处理
        else:
            # 对 frame 的 key 处理,存储 byte_num 和 byte_len
            num_len = {}
            byte_list = list(frame_protocol.keys())

            for i in range(len(byte_list)):
                num, byte_len = byte_list[i] % 8, byte_list[i] // 8
                if num == 0:
                    num, byte_len = 8, byte_len - 1
                num_len[num] = byte_len # {byte_num: byte_len, byte_num: byte_len}

            # 对多字节处理
            if byte_num in num_len:
                byte_value = 0
                # 根据数据长度,对字节左移
                for i in range(num_len[byte_num]):
                    byte_value = byte_value << 8 | frame_data[byte_index + i]
                    if byte_value != 0:
                        parsed_data[f'Byte{byte_num}: {frame_protocol[byte_num + num_len[byte_num] * 8]}'] = byte_value

    # 将解析后的内容存储到 parsed_data 中
    if parsed_data:
        LearniuH_print(parsed_data)
        # 换行
        print()

        # 一帧结束 初始化
        parsed_data = {}


# 测试用例
frame_id = 0x6
frame_data_9c4 = (0x09, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
frame_data_9c5 = (0xff, 0x00, 0x00, 0x00, 0xff, 0x00, 0x00, 0xff)
frame_data_6   = (0x00, 0x00, 0x00, 0x05, 0x22, 0x00, 0x00, 0x00)
frame = {0x9c4: (0x09, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00), # 引擎启动 空挡 / 驻刹 前灯
         0x9c5: (0xff, 0x00, 0x00, 0x00, 0xff, 0x00, 0x00, 0xff), # 油门  降臂  辅刹
         0x6:   (0x00, 0x00, 0x00, 0x05, 0x22, 0x00, 0x00, 0x00)  # 前车桥压力 1314
        }
for frame_id, frame_data in frame.items():
    parse_can_message(frame_id, frame_data)