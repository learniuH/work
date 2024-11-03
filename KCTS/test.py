import pandas as pd
import re


def clean_byte_number(byte_str):
    """从byte字符串中提取数字"""
    if isinstance(byte_str, (int, float)):
        return int(byte_str)
    if 'byte' in byte_str.lower():
        # 处理 byte1, byte2 等格式
        num = byte_str.lower().replace('byte', '')
        if num.isdigit():
            return int(num)
        # 对于形如 byte10-20 的情况返回原始字符串
        if '-' in num:
            return f'byte{num}'
    return byte_str


def clean_bit_number(bit_str):
    """从bit字符串中提取数字"""
    if isinstance(bit_str, (int, float)):
        return int(bit_str)
    if 'bit' in bit_str.lower():
        # 处理 bit0, bit1 等格式
        num = bit_str.lower().replace('bit', '')
        if num.isdigit():
            return int(num)
        # 处理 bit0-6 这样的范围格式
        if '-' in num:
            return f'bit{num}'
    return bit_str


def excel_to_protocol_dict(file_path):
    # 读取Excel文件
    df = pd.read_excel(file_path)

    # 初始化结果字典
    result = {
        '开关量': {},
        '模拟量': {}
    }

    # 处理开关量数据
    current_byte = None
    for index, row in df.iterrows():
        # 检查是否是新的byte
        if pd.notna(row['字节序号']):
            byte_value = row['字节序号']
            current_byte = clean_byte_number(byte_value)
            # 如果是整数byte，创建新的字典
            if isinstance(current_byte, int):
                result['开关量'][current_byte] = {}
            # 如果是范围byte，也创建字典
            elif isinstance(current_byte, str) and 'byte' in current_byte.lower():
                if '-' in current_byte:
                    result['开关量'][current_byte] = {}

        # 处理bit数据
        if pd.notna(row['内容']) and 'bit' in str(row['内容']).lower():
            bit = clean_bit_number(row['内容'])
            value = row.iloc[4] if len(row) > 4 and pd.notna(row.iloc[4]) else None
            if current_byte is not None and value is not None:
                # 检查current_byte是否在字典中
                if current_byte not in result['开关量']:
                    result['开关量'][current_byte] = {}
                result['开关量'][current_byte][bit] = value

        # 处理模拟量数据
        if pd.notna(row['字节序号']):
            byte_value = row['字节序号']
            if isinstance(byte_value, (int, float)):
                if len(row) > 4 and pd.notna(row.iloc[4]):
                    result['模拟量'][int(byte_value)] = row.iloc[4]
            elif isinstance(byte_value, str) and 'byte' in byte_value.lower():
                if '-' in byte_value:  # 处理 byte23-24 这样的格式
                    byte_key = byte_value.lower()
                    if len(row) > 4 and pd.notna(row.iloc[4]):
                        result['模拟量'][byte_key] = row.iloc[4]

    # 清理空字典
    result['开关量'] = {k: v for k, v in result['开关量'].items() if v}
    result['模拟量'] = {k: v for k, v in result['模拟量'].items() if v}

    return result

# 使用示例：
file_path = './test.xlsx'
ou_protocol = excel_to_protocol_dict(file_path)
print(ou_protocol)
