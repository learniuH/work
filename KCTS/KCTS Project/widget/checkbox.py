from PyQt5.QtWidgets import QCheckBox, QApplication, QWidget, QHBoxLayout

class LearniuHCheckBox(QCheckBox):
    ''' 自定义的 checkBox '''
    def __init__(self, objectName: str, parent=None):
        super().__init__(parent)
        self.setObjectName(f'{objectName}_checkBox')    # 对象的名字是 xx_checkBox
        self.setText('')                                # 去除文本

        self.custom_styles()

    def custom_styles(self):
        ''' 自定义QSS样式 '''
        self.setStyleSheet('''
            QCheckBox::indicator {
                width: 45px;
                height: 20px;
            }
            
            QCheckBox::indicator:unchecked {
                image: url(./img/unlock.png);
            }

            QCheckBox::indicator:checked {
                image: url(./img/locked.png);
            }
        ''')



class MainWindow(QWidget):
    ''' 窗口显示类 '''
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout(self)

        # 创建自定义 checkBox
        checkBox = LearniuHCheckBox('byte')

        self.layout.addWidget(checkBox)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()