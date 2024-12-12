from typing import Union

from PyQt5.QtWidgets import QCheckBox

try:
    from .constant import ConstantText
except ImportError:
    from constant import ConstantText

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

        self.setText(ConstantText.BLANKTEXT)        # 空白文本

        self.custom_styles()

    def custom_styles(self):
        ''' 自定义QSS样式 '''
        self.setStyleSheet('''
            QCheckBox {
                spacing: 0;     /* 去除 indicator 和 文字间的间隔 */
                max-width: 15px;    /* 整个控件的大小就是 indicator 的大小 */
            }
            
            QCheckBox::indicator:unchecked {
                image: url(./widget/img/unlock_1.png);
            }

            QCheckBox::indicator:checked {
                image: url(./widget/img/locked_1.png);
            }
            
            QCheckBox::indicator {
                /* 设置图片的宽度 高度 */
                width: 15px;
                height: 20px;
            }
        ''')


