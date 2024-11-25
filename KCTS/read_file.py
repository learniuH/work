import pandas as pd


def clean_number(value, prefix):
    """
    从 value 中提取数字，支持以指定 prefix（如 'bit' 或 'byte'）开头的格式。

    Args:
        value (str, int, float): 输入的值，可能是带前缀的字符串或数字。
        prefix (str): 指定的前缀（例如 'bit' 或 'byte'），用于识别并提取数字部分。

    Returns:
        int, str, float: 返回提取后的数字或范围字符串。
    """
    if isinstance(value, (int, float)):
        # 如果是数字直接返回
        return value

    # 统一处理字符串的大小写，去除前缀
    value_lower = value.lower()
    if prefix.lower() in value_lower:
        value_lower = value_lower.replace(prefix.lower(), '')

        # 如果是单一的数字，则转换为整数
        if value_lower.isdigit():
            return int(value_lower)

        # 如果是范围格式，如 '2-3'，则去除空格后返回原始字符串
        if '-' in value_lower:
            return value_lower.replace(' ', '')

    # 如果无法处理，返回原始值
    return value

def read_protocol_excel(file_path, sheet_name):
    ou_to_mu_df = pd.read_excel(file_path, sheet_name=sheet_name)

    # 找到包含 '字节序号' 的行号
    header_index = ou_to_mu_df[ou_to_mu_df.eq('字节序号').any(axis=1)].index[0]
    # 将 '字节序号' 行作为列名
    ou_to_mu_df.columns = ou_to_mu_df.iloc[header_index]
    # 删除作为列名的行，并重置索引
    ou_to_mu_df = ou_to_mu_df[(header_index + 1):].reset_index(drop=True)


    # 将名称和字节序号两列填充
    ou_to_mu_df.loc[:, '名称'] = ou_to_mu_df['名称'].fillna(method='ffill')
    ou_to_mu_df.loc[:, '字节序号'] = ou_to_mu_df['字节序号'].fillna(method='ffill')

    # 修改名称这列为 index
    ou_to_mu_df.set_index('名称', inplace=True)

    # 初始化协议字典
    ou_protocol = {}

    # 取开关量和模拟量这部分的 df
    switch_df = ou_to_mu_df.loc['开关量', :]
    analog_df = ou_to_mu_df.loc['模拟量', :]

    # 开关量协议更新
    for _, switch_row in switch_df.iterrows():
        # 通过 '字节序号' 索引读取 byte_num
        byte_num = switch_row['字节序号']
        # 提取 byte_num 中的数字
        byte_num = clean_number(byte_num, 'byte')

        # 通过 '内容' 索引读取 bit_index
        bit_index = switch_row['内容']
        # 提取 bit_index 中的数字
        bit_index = clean_number(bit_index, 'bit')

        # 通过 '描述' 更新
        switch_desc = switch_row['描述']
        # 更新字节序号
        if byte_num not in ou_protocol and switch_desc != '预留' and not pd.isnull(switch_desc):
            ou_protocol[byte_num] = {}
        # 更新协议内容
        if switch_desc != '预留' and not pd.isnull(switch_desc):
            ou_protocol[byte_num][bit_index] = switch_desc

    # 模拟量协议更新
    for _, analog_row in analog_df.iterrows():
        # 通过 '字节序号' 索引读取 byte_num
        byte_num = analog_row['字节序号']
        # 提取 byte_num 中的数字
        byte_num = clean_number(byte_num, 'byte')

        # 通过 '描述' 更新
        analog_desc = analog_row['描述']
        # 更新协议
        if analog_desc != '预留' and not pd.isnull(analog_desc):
            ou_protocol[byte_num] = analog_desc

    return ou_protocol

def learniuh_print(ou_protocol):
    ''' 打印字典中的内容 '''
    for byte_num in ou_protocol:
        # 开关量打印
        if isinstance(ou_protocol.get(byte_num), dict):
            for bit_index, des in ou_protocol[byte_num].items():
                print(f'Byte{byte_num}: bit{bit_index}  {des}')
        # 模拟量打印
        else:
            print(f'Byte{byte_num}: {ou_protocol[byte_num]}')

if __name__ == '__main__':
    file_path = 'D:\LearniuH\Project\中测推土机\功能定义\推土机标准化内部通信协议-V1.0-202400918.xlsx'
    sheet_name = 'OU->MU'
    ou_protocol = read_protocol_excel(file_path, sheet_name)
    learniuh_print(ou_protocol)