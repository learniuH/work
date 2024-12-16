import pandas as pd
import re
from PyQt5.QtCore import pyqtSignal, QObject

from config.error_message import ErrorMessage
from log.error_handle import ExcelReaderExceptionHandle

from typing import Union, Tuple


class ExcelRead(QObject):

    program_exception_signal = pyqtSignal(str)

    def __init__(self, file_path: str):
        super().__init__()
        # 表单的名字
        self.file_path = file_path


    def read_sheet_name(self) -> list:
        ''' 读取表格里所有的表单, 返回各表单的名字 '''
        excel_file = pd.ExcelFile(self.file_path)
        sheet_name = excel_file.sheet_names
        return sheet_name


    @ExcelReaderExceptionHandle.safe_excel_reader
    def read_file(self, sheet_name: str) -> Tuple[dict, int]:
        '''解析Excel表单的内容, 生成协议的定义

        Args:
            sheet_name: 通过comboBox的item传入的表单名字

        Returns:
            返回生成的协议定义和协议的长度
        '''

        protocol = {}   # 初始化协议字典
        switch_list = []    # 用于存储开关量的byte_num

        df = pd.read_excel(self.file_path, sheet_name=sheet_name, header=None)

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

        # 通过 CRC的行号 和 字节序号的列号 获取协议长度
        protocol_length = df.loc[end_row_index, col_index]
        protocol_length = self.clean_number(protocol_length)


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
            byte_num = self.clean_number(byte_num_raw)

            if byte_num not in protocol:
                if byte_num is None:
                    # 字节序号里面解析出三个数字时, 这个开关不进行解析, 生成
                    continue
                protocol[byte_num] = {}

            # 更新开关量
            if byte_num_raw in switch_list:
                bit_index = self.clean_number(row_index['内容'])
                if bit_index is None:
                    # 位索引里面解析出三个数字时, 这个开关不进行解析, 生成
                    continue

                protocol[byte_num][bit_index] = row_index['开关描述']
            # 更新模拟量
            else:
                protocol[byte_num] = row_index['开关描述']

        '''
           protocol = {
                10: {
                    0: 'light',
                    '1-2': 'horn',
                },
                12: 'go head',
                '13-14': 'back'
           } 
        '''
        return protocol, protocol_length

    def clean_number(self, value: Union[str, int, float]) -> Union[int, str, None]:
        '''提取字节序号列下面各个单元格的数字

        Args:
            value: 要清理的值

        Returns:
            清理后的数字或范围字符串, 如果清理后有两个以上数字, 返回 None, 将该开关丢弃
        '''
        if isinstance(value, (int, float)):
            return int(value)

        result = []
        for num in re.findall(r'\d+', value):
            result.append(int(num))

        if len(result) == 1:
            # 字符串里只有一个数字, 直接返回整型
            return result[0]
        elif len(result) == 2:
            # 字符串里有两个数字, 返回 str, 后期需要优化, 改为返回 list, 便于代码
            return f'{result[0]}-{result[1]}'
        else:
            # 字符串里出现两个以上的数字, 返回 None, 将该开关删除
            self.program_exception_signal.emit(ErrorMessage.EXCEL_PARSE_ERROR)
            return None


        # value_lower = value.lower()
        # if prefix in value_lower:
        #     value_lower = value_lower.replace(prefix, '')
        #
        #     if value_lower.isdigit():
        #         return int(value_lower)
        #
        #     if '-' in value_lower:
        #         return value_lower.replace(' ', '')
        #
        # return value



if __name__ == '__main__':
    file_path = "D:\LearniuH\Project\中测推土机\功能定义\推土机标准化内部通信协议-V1.0-202400918.xlsx"
    # file_path = "C:\\Users\L\Desktop\自动化测试\推土机标准化内部通信协议-V1.0-202400918.xlsx"
    sheet_name = '（推土机-OU）->MU&OC'
    a = ExcelRead(file_path)
    a.read_sheet_name()
    a.read_file(sheet_name)
