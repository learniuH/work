from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt

from typing import Union

try:
    from .constant import ConstantText
except ImportError:
    from constant import ConstantText

class LearniuHLineEdit(QLineEdit):
    ''' 自定义 LineEdit '''

    def __init__(self, byte_num: Union[int, str], bit_index: Union[int, str] = None):
        '''
            byte_num:   pushButton 的字节序号属性
            bit_index:  pushbutton 的位索引属性, 默认是 None
        '''
        super().__init__()
        self.byte_num = byte_num
        self.bit_index = bit_index

        self.setPlaceholderText(ConstantText.LINEEDITTEXT)      # 提示的文本 key
        self.setAlignment(Qt.AlignCenter)                       # 文本 placeholderText 居中显示

        self.custom_style()

    def custom_style(self):
        ''' 自定义QSS样式 '''
        self.setStyleSheet('''
            QLineEdit {
                border: 2px solid qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #f6f7fa, stop: 1 #dadbde);
                border-radius: 5px;
                font: 9pt '微软雅黑';
                color: #ff55ff;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #f6f7fa, stop: 1 #dadbde);
                height: 22px;
                max-width: 35px;
            }
        ''')