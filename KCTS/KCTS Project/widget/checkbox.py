from typing import Union

from PyQt5.QtWidgets import QCheckBox


class LearniuHCheckBox(QCheckBox):
    ''' 自定义的 checkBox '''
    def __init__(self, byte_num: Union[int, str], bit_index: Union[int, str]=None):
        '''
            byte_num:   checkBox 的字节序号属性
            bit_index:  checkBox 的位索引属性, 默认是 None
        '''
        super().__init__()
        self.byte_num = byte_num
        self.bit_index = bit_index

        self.setText('')        # 不显示文本

        self.custom_styles()

    def custom_styles(self):
        ''' 自定义QSS样式 '''
        self.setStyleSheet('''
            QCheckBox::indicator {
                /* 设置图片的宽度 高度 */
                width: 15px;
                height: 20px;
            }
            
            QCheckBox::indicator:unchecked {
                image: url(./img/unlock_1.png);
            }

            QCheckBox::indicator:checked {
                image: url(./img/locked_1.png);
            }
        ''')


