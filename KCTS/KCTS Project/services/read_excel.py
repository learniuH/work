import pandas as pd
from typing import Union

class ExcelRead():
    def __init__(self, file_path: str):
        # 表单的名字
        self.file_path = file_path


    def read_sheet_name(self) -> list:
        ''' 读取表格里所有的表单, 返回各表单的名字 '''
        excel_file = pd.ExcelFile(self.file_path)
        sheet_name = excel_file.sheet_names
        return sheet_name


    def read_file(self, sheet_name: str):

        protocol = {}   # 初始化协议字典
        switch_list = []    # 用于存储开关量的byte_num

        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)



        # 获取 字节序号 所在的列索引
        # col_index = df.columns.get_loc(df.eq('字节序号').stack().idxmax()[1])
        ''' 
        df.eq('字节序号') - 返回 boolean型的DataFrame, 标记每个单元格是否是 '字节序号’
        .stack()     - 将DataFrame转为一维索引的 Series
        .idxmax()    - 找到第一个为 True 的位置, 返回行索引+列所用
        '''

        # 获取 字节序号 和 CRC 所在单元格的 行列索引
        row_index, col_index = df.stack()[df.stack() == '字节序号'].index[0]
        end_row_index, _ = df.stack()[df.stack() == 'CRC'].index[0]

        # 通过 CRC的行号 和 字节序号列 获取协议长度
        protocol_length = df.loc[end_row_index, col_index]
        protocol_length = ExcelRead.clean_number(protocol_length, 'byte')


        # 选取列范围, 从 字节序号 所在的列开始 往右取两列
        target_cells = df.iloc[row_index + 1:, col_index: col_index + 3]

        # 设置目标三列的 columns
        target_cells.columns = ['字节序号', '内容', '开关描述']
        # 填充 字节序号 列, 如果字节序号出现一次以上, 认为是开关量, 否则是模拟量
        target_cells.loc[:, '字节序号'] = target_cells['字节序号'].fillna(method='ffill')

        # 筛选出重复的字节序号, 作为开关量
        duplicates = target_cells['字节序号'].value_counts()
        repeat_values = duplicates[duplicates > 1]
        # 记录所有重复的字节序号, 作为开关量
        for digital_switch in repeat_values.index:
            switch_list.append(digital_switch)


        # 删除 开关描述 中为 nan 或 有 预留 的单元格所在行
        target_cells = target_cells.iloc[:][~(target_cells.iloc[:]['开关描述'].isna() |
                                               target_cells.iloc[:]['开关描述'].astype(str).str.contains('预留'))]

        # 行遍历获取的单元格 更新 协议内容
        for _, row_index in target_cells.iterrows():
            byte_num_raw = row_index['字节序号']
            byte_num = ExcelRead.clean_number(byte_num_raw, 'byte')

            if byte_num not in protocol:
                protocol[byte_num] = {}

            # 更新开关量
            if byte_num_raw in switch_list:
                bit_index = ExcelRead.clean_number(row_index['内容'], 'bit')
                protocol[byte_num][bit_index] = row_index['开关描述']
            # 更新模拟量
            else:
                protocol[byte_num] = row_index['开关描述']

        return protocol, protocol_length

    @staticmethod
    def clean_number(value: Union[str, int, float], prefix: str) -> Union[int, str]:
        '''清理 字节序号 位索引

        Args:
            value: 要清理的值
            prefix: 前缀(bit或byte)

        Returns:
            清理后的数字或范围字符串
        '''
        if isinstance(value, (int, float)):
            return int(value)

        value_lower = value.lower()
        if prefix in value_lower:
            value_lower = value_lower.replace(prefix, '')

            if value_lower.isdigit():
                return int(value_lower)

            if '-' in value_lower:
                return value_lower.replace(' ', '')

        return value



if __name__ == '__main__':
    file_path = "D:\LearniuH\Project\中测推土机\功能定义\推土机标准化内部通信协议-V1.0-202400918.xlsx"
    # file_path = "C:\\Users\L\Desktop\自动化测试\推土机标准化内部通信协议-V1.0-202400918.xlsx"
    sheet_name = '（推土机-OU）->MU&OC'
    a = ExcelRead(file_path)
    a.read_sheet_name()
    # a.read_file(sheet_name)
