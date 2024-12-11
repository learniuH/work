
from PyQt5.QtWidgets import QProgressBar

from typing import Union

class LearniuHProgressBar(QProgressBar):
    ''' 自定义 ProgressBar '''

    def __init__(self, byte_num: Union[int, str], minimum: int=0, maximum: int=100):
        '''
            byte_num:   ProgressBar 的字节序号属性
            bit_index:  ProgressBar 的位索引属性, 默认是 None
        '''
        super().__init__()
        self.byte_num = byte_num

        self.setValue(80)
        self.setMinimum(minimum)    # 进度条最小值
        self.setMaximum(maximum)    # 进度条最大值
        self.setFormat('%v')        # 进度条文字样式

        self.custom_style()

    def custom_style(self):
        ''' 自定义QSS样式 '''
        self.setStyleSheet('''
            QProgressBar {
                border: 2px solid #204789;
                border-radius: 5px;
                text-align: center;
                font: 10pt '幼圆';
                height: 20px;
                max-width: 75px;
            }
            
            QProgressBar::chunk {
                border-radius: 4px;
                background-color: #05B8CC;
            }
        ''')