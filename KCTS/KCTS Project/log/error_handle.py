import pandas as pd
import functools
import logging
from typing import Tuple, Dict, Any

from config.error_message import ErrorMessage


class ExcelReaderExceptionHandle():
    '''
    处理Excel读取过程中异常的装饰器和异常处理类
    '''


    @staticmethod
    def log_exception(e: Exception, method_name: str):
        '''
        记录异常日志
        :param e: 捕获的异常对象
        :param method_name: 发生异常的方法名
        '''
        logging.error(f'{method_name} 方法发生异常: {str(e)}')
        logging.error(f'异常的详细信息: {e.__traceback__}')

    @classmethod
    def safe_excel_reader(cls, func):
        '''
        Excel 读取方法的装饰器, 提供全面的异常处理

        :param func: 被装饰的原始方法
        :return: 装时候的方法
        '''

        @functools.wraps(func)
        def wrapper(self, sheet_name: str) -> Tuple[Dict, int]:
            try:
                return func(self, sheet_name)
            except PermissionError:
                cls.log_exception(Exception(f'没有权限访问文件 {self.file_path}'), func.__name__)
                return {}, 0
            except pd.errors.EmptyDataError:
                self.program_exception_signal.emit(ErrorMessage.EMPTY_SHEET_ERROR)
                return {}, 0
            except IndexError as e:
                # 找不到 '字节序号' 和 'CRC' 单元格, 界面提示 '请选择正确的表单！！！'
                if 'index 0 is out of bounds for axis 0 with size 0' in str(e):
                    self.program_exception_signal.emit(ErrorMessage.SHEET_NAME_ERROR)
                    return {}, 0
            except KeyError as e:
                cls.log_exception(Exception(f'未找到指定的表单或列: {str(e)}'), func.__name__)
                return {}, 0
            except ValueError as e:
                cls.log_exception(Exception(f'数据处理出错: {str(e)}'), func.__name__)
                return {}, 0
            except Exception as e:
                cls.log_exception(Exception(e, func.__name__))
                return {}, 0

        return wrapper
