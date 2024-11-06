import sys
from threading import Timer

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLineEdit
from PyQt5.QtCore import QTimer

from ui import Ui_Window
from switchWidget import Switch

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()  #初始化父类
        self.ui = Ui_Window()   # 创建 UI 类的实例
        self.ui.setupUi(self)   # 将 UI 布局加载到 MainWindow 上


        # # 创建检测按钮长按的定时器
        # self.detctLongPress = QTimer()
        # self.detctLongPress.setInterval(300)    # 按键300ms视为按键被长按
        # self.detctLongPress.timeout.connect(self.on_long_press)
        #
        # # 创建按钮长按状态的定时器
        # self.longPressTimer = QTimer()
        # self.longPressTimer.setInterval(100)    # 触发周期是100ms
        # self.longPressTimer.timeout.connect(self.start_long_press)

        # 绑定按钮点击事件到自定义的 slot 函数
        self.ui.connect_pushButton.clicked.connect(self.print_text)
        self.ui.openFile_pushButton.clicked.connect(self.open_file_dialog)

        # # 绑定按钮按下的事件
        # self.ui.e_stop_button.clicked.connect(self.button_click)   # 鼠标按下抬起为一次 clicked
        # self.ui.e_stop_button.pressed.connect(self.start_detctLongPressTimer)  # 绑定长按检测
        # self.ui.e_stop_button.released.connect(self.stop_detctLongPressTimer)   # 停止长按检测
        # self.ui.e_stop_button.released.connect(self.stop_long_press)           # 停止长按

        # # 绑定复选框状态变化到 slot 函数
        # self.ui.e_stop_lock_checkbox.stateChanged.connect(self.on_checkbox_changed)

        # num_lineEdit 文本框内容变化绑定到生成按键函数
        self.ui.num_lineEdit.textChanged.connect(self.updateSwitchs)
        # 按键容器存放处
        self.switch_container = None

        # 用于追踪按键是否被按下
        self.is_key_down = False
    
    def print_text(self):
        ''' 获取文本框的内容 '''

        ip = self.ui.ip_editText.toPlainText()
        port = self.ui.port_editText.toPlainText()


        print(f'现在的IP和Port：({ip}, {port})')
    
    def open_file_dialog(self):
        ''' 打开文件选择对话框, 只显示 Excel 文件 '''
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择文件', '', 'Excel Files (*.xlsx);;All Files (*)'
        )
        if file_path:
            pass

    # # keyPressEvent 方法
    # def keyPressEvent(self, event):
    #     # 获取文本框中的内容
    #     expected_text = self.ui.e_stop_lineEdit.text()
    #
    #     # 判断是否按下的键与文本框内容匹配
    #     if event.text() == expected_text.lower() or event.text() == expected_text.upper():
    #         print(f'检测到{expected_text}按键按下')
    #     else:
    #         print(f'不是{expected_text}键位')
    #
    # def button_click(self):
    #     print('急停触发')


    # def start_detctLongPressTimer(self):
    #     # 按下按钮时启动定时器
    #     self.detctLongPress.start()
    #
    # def stop_detctLongPressTimer(self):
    #     # 松开按键关闭定时器
    #     self.detctLongPress.stop()
    #
    # def on_long_press(self):
    #     self.detctLongPress.stop()  # 停止检测长按的定时器
    #     self.longPressTimer.start() # 开始按键长按的定时器
    #     print('按键处于长按状态')
    #
    # def start_long_press(self):
    #     print('急停, 100ms发一包')
    #
    # def stop_long_press(self):
    #     # 当按钮释放时关闭定时器
    #     self.longPressTimer.stop()

    # def on_checkbox_changed(self, state):
    #     if state == 2:  # 表示勾选状态
    #         print('复选框被勾选')
    #         self.on_long_press()
    #         self.ui.e_stop_button.setDisabled(True)
    #     if state == 0:  # 表示空选状态
    #         print('复选框没有勾选')
    #         self.stop_long_press()
    #         self.ui.e_stop_button.setEnabled(True)

    # def mousePressEvent(self, event):
    #     # 当点击其他地方时, 取消文本框的焦点
    #     if not self.ui.e_stop_lineEdit.geometry().contains(event.pos()):
    #         self.ui.e_stop_lineEdit.clearFocus()
    #     super().mousePressEvent(event)

    def updateSwitchs(self):
        try:
            count = int(self.ui.num_lineEdit.text())
        except ValueError:
            return  # 如果不是正数, 则不做任何操作

        # 如果之前有按键容器, 删除它
        if self.switch_container:
            self.ui.verticalLayout_3.removeWidget(self.switch_container)
            self.switch_container.deleteLater()
            self.switch_container = None

        dict = {
            11: {
                0: '前进',
                7: '后退'
            },
            12: {
                6: '灯'
            },
            24: '升臂'
        }

        # 创建新的按键并添加到界面
        self.switch_container = Switch(dict)
        self.ui.verticalLayout_3.addWidget(self.switch_container)

    # 重写键盘按下事件
    def keyPressEvent(self, event):
        '''
        在大多数操作系统中，键盘按键长按会触发「重复按键」的功能。这种机制会在一定的时间间隔内重复触发 keyPressEvent，
        所以即使长按一个键，程序仍会检测到多次按下和松开事件（keyPressEvent 和 keyReleaseEvent 交替触发）
        '''
        # 获取按下的字符
        key_char = event.text().upper()

        # 检查按下的键是字母, 并且没有被按下
        if key_char.isalpha():
            # 遍历窗口中所有的子控件, 检查是否有绑定的键
            for lineEdit in self.switch_container.findChildren(QLineEdit):
                if lineEdit.text().upper() == key_char and not self.is_key_down:
                    byte_num = lineEdit.property('byte_num')
                    bit_index = lineEdit.property('bit_index')

                    # 如果是开关量, 按键所在的位赋 1
                    self.switch_container.package[byte_num - 1] |= (1 << bit_index)
                    # 对应的 button disabled
                    button = self.switch_container.get_button_by_property(['byte_num', byte_num],
                                                                          ['bit_index', bit_index])
                    button.setDisabled(True)
                    self.is_key_down = True

                    # 调试打印信息
                    message = ' '.join(f'{byte:02X}' for byte in self.switch_container.package)
                    print(f'{key_char}: {message}')

    # 重写键盘按下事件
    def keyReleaseEvent(self, event):
        # 获取松开的字符
        key_char = event.text().upper()

        # 检查按下的键是字母
        if key_char.isalpha():
            # 遍历窗口中所有的子控件, 检查是否有绑定的键
            for lineEdit in self.switch_container.findChildren(QLineEdit):
                if lineEdit.text().upper() == key_char and self.is_key_down:
                    byte_num = lineEdit.property('byte_num')
                    bit_index = lineEdit.property('bit_index')

                    # 如果是开关量, 按键所在的位赋 0
                    self.switch_container.package[byte_num - 1] &= ~(1 << bit_index)
                    # 对应的 button disabled
                    button = self.switch_container.get_button_by_property(['byte_num', byte_num],
                                                                          ['bit_index', bit_index])
                    button.setEnabled(True)
                    self.is_key_down = False

                    # 调试打印信息
                    message = ' '.join(f'{byte:02X}' for byte in self.switch_container.package)
                    print(f'{key_char}: {message}')

    def mousePressEvent(self, event):
        # 清除所有控件的焦点
        self.setFocus()
        super().mousePressEvent(event)  # 调用父类的鼠标点击事件处理



if __name__ == '__main__':
    app = QApplication(sys.argv)    # 创建应用程序对象
    window  = MainWindow()  # 创建主窗口
    window.show()   # 显示主窗口
    sys.exit(app.exec_())
