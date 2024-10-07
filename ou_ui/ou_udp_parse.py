from ou_udp_protocol import OU_PROTOCOLS
'''
parsed_data_bit = {
    Byte_num: {
        bit_index: Function
    },

    Byte_num: {Function, Byte_value}
}
'''

def parse_ou_message(byte_num, data):
    # 存储解析后的数据
    parsed_data_bit = {}
    parsed_data_byte = {}
    
    # 获取指定字节
    byte_value = data[byte_num - 1]

    # 按位处理
    if isinstance(OU_PROTOCOLS.get(byte_num), dict):
        for bit_position, function in OU_PROTOCOLS.get(byte_num).items():
            # 单位数据
            if bit_position < 8 and byte_value >> bit_position & 1:
                if byte_num not in parsed_data_bit:
                    parsed_data_bit[byte_num] = {bit_position: function}
                else:
                    parsed_data_bit[byte_num].update({bit_position: function})
            # 多位数据
            elif bit_position > 8:
                start_bit, bit_len = bit_position % 8, bit_position // 8
                # 遍历多个bit
                for i in range(bit_len):
                    if byte_value >> (start_bit + i) & 1 == 0:
                        break
                    # 最后一个 for 循环,所有 bit 都为 1
                    if i == bit_len - 1:
                        for bit_index in [start_bit, start_bit + i]:
                            parsed_data_bit[byte_num].pop(bit_index)
                        parsed_data_bit[byte_num].update({bit_index: function})
    else: #按字节处理
        if byte_value:
            parsed_data_byte[byte_num] = {OU_PROTOCOLS.get(byte_num): byte_value}
    return parsed_data_bit, parsed_data_byte
    
# data = [0x00, 0x00, 0x00, 0x00, 0x00, # 1
#         0x00, 0x00, 0x00, 0x00, 0x00, # 2
#         0x00, 0x00, 0x00, 0x00, 0x00, # 3
#         0x00, 0x00, 0x00, 0x00, 0x00, # 4
#         0x00, 0x00, 0x00, 0x03, 0x00, # 5
#         0x09, 0x05, 0x00, 0x00, 0x00, # 6
#         0x00, 0x00, 0x00, 0x00, 0x00, # 7 
#         0x64, 0x00, 0x00, 0x00, 0x00, # 8
#         0x00, 0x00, 0x00, 0x03, 0x03, # 9
#         0x00, 0x00, 0x00, 0x00, 0x00, # 10
#         0x00, 0x00, 0x00, 0x00, 0x00, # 11
#         0x00
#         ] # (1)号车  挡位 3  平台使能  前灯  装料  引擎保持 测试模式  校准失败
# #test case
# for byte_num in OU_PROTOCOLS:
#     parsed_data_bit, parsed_data_byte = parse_ou_message(byte_num,data)
#     if parsed_data_bit:
#         print(parsed_data_bit)
#     if parsed_data_byte:
#         for function, byte_value in parsed_data_byte[byte_num].items():
#             print(function, byte_value)
#         print(parsed_data_byte)