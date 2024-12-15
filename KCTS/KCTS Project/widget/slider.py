from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWidgets import QSlider
from PyQt5.Qt import Qt

from typing import Union


try:
    from constant import ConstantText
except ImportError:
    from .constant import ConstantText

class LearniuHSlider(QSlider):
    ''' 自定义 Slider '''

    def __init__(self, byte_num: Union[int, str], bit_index: Union[int, str] = None):
        '''
            byte_num:   pushButton 的字节序号属性
            bit_index:  pushbutton 的位索引属性, 默认是 None
        '''
        super().__init__(Qt.Horizontal)
        self.byte_num = byte_num
        self.bit_index = bit_index

        if isinstance(byte_num, int):
            # 单字节的模拟量取值范围
            self.setMinimum(0)      # 设置 slider 最小值
            self.setMaximum(100)       # 设置 slider 最大值
        else:
            # 多字节模拟量取值范围
            maximum = 0xFF
            value_range = ConstantText.value_range(byte_num)
            for i in range(value_range[1] - value_range[0]):
                maximum = maximum << 8 | 0xFF

            self.setMinimum(0)
            self.setMaximum(maximum)

        self.costom_style()

    def costom_style(self):
        self.setStyleSheet('''
            QSlider {
                max-height: 28px;
                max-width: 150px;
                min-width: 100px;
            }
        
            QSlider::groove:horizontal {
                background: transparent;
            }
            
            QSlider::handle:horizontal {
                border-radius: 5px;
                width: 6px;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                            stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
                border: 2px solid qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #f6f7fa, stop: 1 #dadbde);
                
                margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */
            
            }
            
            QSlider::add-page:horizontal {
                border: 2px solid qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #e7e8eb, stop: 1 #e1e3e6);
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
                background: white;
            }
            
            QSlider::sub-page:horizontal {
                border: 2px solid qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #e7e8eb, stop: 1 #e1e3e6);
                border-radius: 5px;
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                            stop: 0 #05b8cc, stop: 1 #06dcf4);
            }
        ''')

    def paintEvent(self, event):
        super().paintEvent(event)

        # 创建绘制器
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 设置字体
        font = QFont("微软雅黑", 10)
        painter.setFont(font)

        # 获取滑块的当前值
        value = self.value()

        # 获取滑块的几何位置和大小
        rect = self.geometry()
        slider_width = self.width()
        slider_height = self.height()

        # 计算文字位置（居中显示）
        text = f'0x{value:X}'
        text_width = painter.fontMetrics().width(text)
        text_height = painter.fontMetrics().height()
        x = (slider_width - text_width) / 2
        y = (slider_height + text_height) / 2 - 4

        # 绘制文字
        painter.drawText(int(x), int(y), text)
        painter.end()