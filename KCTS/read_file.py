import pandas as pd

def clean_bit_number(bit_index):
    ''' 从 bit_index 中提取数字 '''
    if isinstance(bit_index, (int, float)):
        # 如果是数字直接 return
        return bit_index
    if 'bit' in bit_index.lower():
        # 处理 bit0 等格式
        bit_index = bit_index.lower().replace('bit', '')
        if bit_index.isdigit():
            # 返回 int
            return int(bit_index)
        # 处理 byte2-3 等范围格式
        if '-' in bit_index:
            # 返回 str
            return bit_index
    return bit_index

def clean_byte_number(byte_num):
    ''' 从 byte_num 中提取数字 '''
    if isinstance(byte_num, (int, float)):
        # 如果是数字直接 return
        return byte_num
    if 'byte' in byte_num.lower():
        # 处理 byte1 等格式
        byte_num = byte_num.lower().replace('byte', '')
        if byte_num.isdigit():
            # 返回 int
            return int(byte_num)
        # 处理 byte2-3 等范围格式
        if '-' in byte_num:
            # 返回 str
            return byte_num
    return byte_num

def read_protocol_excel(file_path, sheet_name):
    ou_to_mu_df = pd.read_excel(file_path, sheet_name=sheet_name, header=1)


    # # 筛选 '字节序号' 所在行的索引
    # header = ou_to_mu_df[ou_to_mu_df.eq('字节序号').any(axis=1)].index[0]
    # ou_to_mu_df.columns[header]


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
        byte_num = clean_byte_number(byte_num)
        # 更新协议
        if byte_num not in ou_protocol:
            ou_protocol[byte_num] = {}

        # 通过 '内容' 索引读取 bit_index
        bit_index = switch_row['内容']
        # 提取 bit_index 中的数字
        bit_index = clean_bit_number(bit_index)

        # 通过 '描述' 更新
        switch_desc = switch_row['描述']
        # 更新协议
        if switch_desc != '预留' and not pd.isnull(switch_desc):
            ou_protocol[byte_num][bit_index] = switch_desc
        else:   # 删除预留和空白的字节序号
            ou_protocol.pop(byte_num)

    # 模拟量协议更新
    for _, analog_row in analog_df.iterrows():
        # 通过 '字节序号' 索引读取 byte_num
        byte_num = analog_row['字节序号']
        # 提取 byte_num 中的数字
        byte_num = clean_byte_number(byte_num)

        # 通过 '描述' 更新
        analog_desc = analog_row['描述']
        # 更新协议
        if analog_desc != '预留' and not pd.isnull(analog_desc):
            ou_protocol[byte_num] = analog_desc

    return ou_protocol


if __name__ == '__main__':
    file_path = './金冠铜业-双闪配料行车KC144-CRB-JG-220725-通信协议设计-洪常乐-双车20240603.xls'
    sheet_name = 'OU->MU'
    ou_protocol = read_protocol_excel(file_path, sheet_name)
    print(ou_protocol)