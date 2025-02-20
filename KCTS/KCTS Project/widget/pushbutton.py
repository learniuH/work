from typing import Union

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QPushButton

class LearniuHPushButton(QPushButton):
    ''' 自定义 pushButton '''
    def __init__(self, text: str, byte_num: Union[int, str], bit_index: Union[int, str]=None):
        '''
            text:       pushButton 的文字显示
            byte_num:   pushButton 的字节序号属性
            bit_index:  pushbutton 的位索引属性, 默认是 None
        '''
        super().__init__()
        self.byte_num = byte_num
        self.bit_index = bit_index

        self.setText(text)

        # 模拟量的 pushButton: 与定时器进行绑定
        if bit_index is None:
            self.timer_increase = QTimer(self)
            self.timer_decrease = QTimer(self)

        self.custom_style()

    def custom_style(self):
        ''' 自定义QSS样式 '''
        self.setStyleSheet('''
            QPushButton {
                border: 2px solid qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #e7e8eb, stop: 1 #e1e3e6);
                border-radius: 5px;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #f6f7fa, stop: 1 #dadbde);
                font: 9pt '微软雅黑';
                
                max-height: 28px;
                max-width: 200px;
            }
        
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #fafafa, stop: 0.4 #f4f4f4,
                                                  stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
            }
            
            QPushButton:pressed {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #dadbde, stop: 1 #f6f7fa);
                padding-top: 1px;
                padding-left: 1px;
            }
                      
            QPushButton:disabled {
                color: black;
                background-color: #fcd97f;
            }
        ''')