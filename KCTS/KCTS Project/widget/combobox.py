from PyQt5.QtWidgets import QComboBox

class LearniuHComboBox(QComboBox):
    ''' 自定义 comboBox 重写 Popup 方法 '''
    def __init__(self):
        super().__init__()

        self.custom_style()

    def custom_style(self):
        ''' 自定义 QSS '''
        self.setStyleSheet('''
            QComboBox {
                background-color: ; /* 背景颜色 */
                color: white;		/* 字体颜色 */
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