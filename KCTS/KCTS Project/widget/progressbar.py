
from PyQt5.QtWidgets import QProgressBar

from typing import Union

class LearniuHProgressBar(QProgressBar):
    ''' 自定义 ProgressBar '''

    def __init__(self, byte_num: Union[int, str], bit_index: Union[int, str] = None):
        '''
            byte_num:   ProgressBar 的字节序号属性
            bit_index:  ProgressBar 的位索引属性, 默认是 None
        '''
        super().__init__()
        self.byte_num = byte_num
        self.bit_index = bit_index

        self.custom_style()

    def custom_style(self):
        ''' 自定义QSS样式 '''
        self.setStyleSheet('''
            QProgressBar {
                border: none;
            }
        ''')