from PyQt5.QtWidgets import QSlider
from PyQt5.Qt import Qt

from typing import Union

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

        self.costom_style()

    def costom_style(self):
        self.setStyleSheet('''
            QSlider {
                max-width: 100px;
                min-width: 100px;
            }
        
            QSlider::groove:horizontal {
                background: transparent;
            }
            
            QSlider::handle:horizontal {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                            stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
                border: 2px solid qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #f6f7fa, stop: 1 #dadbde);
                border-radius: 5px;
                width: 4px;
                margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */
            
            }
            
            QSlider::add-page:horizontal {
                background: transparent;
            }
            
            QSlider::sub-page:horizontal {
                border: 1px solid #204789;
                border-radius: 5px;
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                            stop: 0 #05b8cc, stop: 1 #06dcf4);
            }
        ''')