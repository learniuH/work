from typing import Union

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

        self.custom_style()

    def custom_style(self):
        ''' 自定义QSS样式 '''
        self.setStyleSheet('''
            QPushButton {
                font: 9pt '幼圆';
                border: 2px solid qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #f6f7fa, stop: 1 #dadbde);
                border-radius: 5px;
                background-color: black;
                
                
            }
            
            QPushButton:pressed {
                padding-top: 1px;
                padding-left: 1px;
            }
        ''')