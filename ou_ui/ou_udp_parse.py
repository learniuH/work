from ou_udp_protocol import OU_PROTOCOLS
import re

def LearniuH_ou_print(byte_num, parsed_data):
    # ANSI 颜色码,终端显示绿色
    red_highlight_start = '\033[31m'
    red_highlight_end = '\033[0m'

    green_highlight_start = '\033[32m'
    green_highlight_end = '\033[0m'

    yellow_highlight_start = '\033[33m'
    yellow_highlight_end = '\033[0m'

    blue_highlight_start = '\033[34m'
    blue_highlight_end = '\033[0m'
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
        highlighted_key = re.sub(chinese_characters, lambda match: f'{green_highlight_start}{match.group()}{green_highlight_end}', key)
        LearniuH_dict[highlighted_key] = value
    
    # 打印
    print(f'{blue_highlight_start}Byte{byte_num}{blue_highlight_end}: ', end='')

    for key, value in LearniuH_dict.items():
        print(f'{key}: {value}\t', end='')

def parse_ou_message(byte_num, data):
    # 存储解析后的数据
    parsed_data = {}
    
    # 获取指定字节
    byte_value = data[byte_num - 1]

    # 按位处理
    if isinstance(OU_PROTOCOLS.get(byte_num), dict):
        for bit_position, function in OU_PROTOCOLS.get(byte_num).items():
            # 单位数据
            if bit_position < 8 and byte_value >> bit_position & 1:
                parsed_data[f'bit{bit_position}: {function}'] = 1
            # 多位数据
            elif bit_position > 8:
                start_bit, bit_len = bit_position % 8, bit_position // 8
                # 遍历多个bit
                for i in range(bit_len):
                    if byte_value >> (start_bit + i) & 1 == 0:
                        break
                    # 最后一个 for 循环,所有 bit 都为 1
                    if i == bit_len - 1:
                        parsed_data[f'bit{start_bit}-{start_bit + i}: {function}'] = 1
                        for bit_index in [start_bit, start_bit + i]:
                            parsed_data.pop(f'bit{bit_index}: {OU_PROTOCOLS.get(byte_num)[bit_index]}')
    #按字节处理
    else:
        if byte_value:
            parsed_data[f'{OU_PROTOCOLS[byte_num]}'] = byte_value
    
    if parsed_data:
        #LearniuH_ou_print(byte_num, parsed_data)
        #print() # 1个 Byte 结束换行
        return parsed_data