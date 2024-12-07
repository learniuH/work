import pandas as pd
import functools
import logging
from typing import Tuple, Dict, Any


class ExcelReaderExceptionHandler:
    """
    专门处理Excel读取过程中异常的装饰器和异常处理类
    """

    @staticmethod
    def log_exception(e: Exception, method_name: str):
        """
        记录异常日志

        :param e: 捕获的异常对象
        :param method_name: 发生异常的方法名
        """
        logging.error(f"在 {method_name} 方法中发生异常: {str(e)}")
        logging.error(f"异常详细信息: {e.__traceback__}")

    @classmethod
    def safe_excel_reader(cls, func):
        """
        Excel读取方法的装饰器，提供全面的异常处理

        :param func: 被装饰的原始方法
        :return: 装饰后的方法
        """

        @functools.wraps(func)
        def wrapper(self, sheet_name: str) -> Tuple[Dict, int]:
            try:
                return func(self, sheet_name)
            except FileNotFoundError:
                cls.log_exception(Exception(f"Excel文件 {self.file_path} 未找到"), func.__name__)
                return {}, 0
            except PermissionError:
                cls.log_exception(Exception(f"没有权限访问文件 {self.file_path}"), func.__name__)
                return {}, 0
            except pd.errors.EmptyDataError:
                cls.log_exception(Exception(f"Excel表格 {sheet_name} 为空"), func.__name__)
                return {}, 0
            except KeyError as e:
                cls.log_exception(Exception(f"未找到指定的表单或列: {str(e)}"), func.__name__)
                return {}, 0
            except ValueError as e:
                cls.log_exception(Exception(f"数据处理出错: {str(e)}"), func.__name__)
                return {}, 0
            except Exception as e:
                cls.log_exception(e, func.__name__)
                return {}, 0

        return wrapper


class ExcelRead:
    @staticmethod
    def clean_number(value: Any, num_type: str = 'byte') -> int:
        """
        清理并转换数字

        :param value: 输入值
        :param num_type: 转换类型（'byte' 或 'bit'）
        :return: 清理后的整数
        """
        try:
            if pd.isna(value):
                return 0

            str_value = str(value).strip()

            if num_type == 'byte':
                return int(str_value.split('.')[0])
            elif num_type == 'bit':
                return int(str_value)
        except (ValueError, TypeError):
            logging.warning(f"无法转换数值: {value}")
            return 0

    @ExcelReaderExceptionHandler.safe_excel_reader
    def read_file(self, sheet_name: str) -> Tuple[Dict[int, Any], int]:
        """
        解析Excel表单的内容，生成协议的定义

        :param sheet_name: 通过comboBox的item传入的表单名字
        :return: 返回生成的协议定义和协议的长度
        """
        # 配置日志记录
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s: %(message)s',
            filename='excel_reader_log.txt',
            filemode='a'
        )

        protocol = {}  # 初始化协议字典
        switch_list = []  # 用于存储开关量的byte_num

        # 读取Excel文件
        df = pd.read_excel(self.file_path, sheet_name=sheet_name, header=None)

        # 查找 '字节序号' 和 'CRC' 单元格的位置
        try:
            row_index, col_index = df.stack()[df.stack() == '字节序号'].index[0]
            end_row_index, _ = df.stack()[df.stack() == 'CRC'].index[0]
        except IndexError:
            logging.error(f"在表单 {sheet_name} 中未找到关键单元格")
            return {}, 0

        # 获取协议长度
        protocol_length = self.clean_number(df.loc[end_row_index, col_index], 'byte')

        # 选取目标单元格范围
        target_cells = df.iloc[row_index + 1:, col_index: col_index + 3]
        target_cells.columns = ['字节序号', '内容', '开关描述']

        # 填充字节序号
        target_cells.loc[:, '字节序号'] = target_cells['字节序号'].fillna(method='ffill')

        # 识别开关量
        duplicates = target_cells['字节序号'].value_counts()
        repeat_values = duplicates[duplicates > 1]
        switch_list = list(repeat_values.index)

        # 过滤不需要的行
        target_cells = target_cells.iloc[:][~(
            target_cells.iloc[:]['开关描述'].isna() |
            target_cells.iloc[:]['开关描述'].astype(str).str.contains('预留')
        )]

        # 处理协议内容
        for _, row_index in target_cells.iterrows():
            byte_num_raw = row_index['字节序号']
            byte_num = self.clean_number(byte_num_raw, 'byte')

            if byte_num not in protocol:
                protocol[byte_num] = {}

            # 处理开关量
            if byte_num_raw in switch_list:
                bit_index = self.clean_number(row_index['内容'], 'bit')
                protocol[byte_num][bit_index] = row_index['开关描述']
            # 处理模拟量
            else:
                protocol[byte_num] = row_index['开关描述']

        return protocol, protocol_length


# 使用示例
if __name__ == "__main__":
    reader = ExcelRead()
    reader.file_path = "your_excel_file.xlsx"
    protocol, length = reader.read_file("Sheet1")
    print(f"协议长度: {length}")
    print(f"协议内容: {protocol}")