from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox

from services.serial_port_assistant import SerialPortAsst

class LearniuHComboBox(QComboBox):
    ''' 自定义 comboBox 重写 showPopup 方法 '''
    def __init__(self):
        super().__init__()

        self.setFocusPolicy(Qt.NoFocus)

        self.custom_style()

    def custom_style(self):
        ''' 自定义 QSS '''
        self.setStyleSheet('''
            QComboBox {
                border: 1px solid qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #f6f7fa, stop: 1 #dadbde);
                background-color: qlineargradient(spread: pad, x1: 1, y1: 0, x2: 0, y2: 1,
		                                          stop: 0 #0d1117,  /* 起始颜色 */
		                                          stop: 1 #414a5a   /* 结束颜色 */ ); /* 背景颜色 */
                color: white;		/* 字体颜色 */
                font: 9pt "微软雅黑";
                height: 22px;
                max-width: 100px;
            }
            
            QComboBox:disabled {
                border: 1px solid #808080; /* 禁用状态下的边框颜色 */
                background-color: #333333; /* 禁用状态下的背景颜色 */
                color: #808080; /* 禁用状态下的字体颜色 */
            }
            
            QComboBox::drop-down {
                width: 18px; /* 保持 drop-down 的宽度一致 */
            }
            
            QComboBox::drop-down:disabled {
                width: 16px; /* 禁用状态下确保宽度一致，避免位移 */
                border: 1px solid #808080; /* 去掉边框 */
                background-color: #333333; /* 禁用状态下的背景颜色 */
            }
            
            QComboBox QAbstractItemView {
                outline: 0px solid gray;
                border: 2px solid qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #f6f7fa, stop: 1 #dadbde);
                color: white;
                background-color: qlineargradient(x1: 1, y1: 0, x2: 0, y2: 0,
                                                  stop: 0 #404959, stop: 1 #989da5);
                selection-background-color: #435068;
            }
            
            QComboBox QAbstractItemView::item {
                height: 22px;
            }
        ''')

    def showPopup(self):
        ''' 重写 showPopup 在comboBox 下拉框出现时, 更新可用串口号 '''
        SerialPortAsst.update_com_ports(self)
        # 调用父类的 showPopup 方法以显示下拉框
        super().showPopup()