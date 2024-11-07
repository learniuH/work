import sys
from distutils.command.check import check
from threading import Timer

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLineEdit, QCheckBox
from PyQt5.QtCore import QTimer

from ui import Ui_Window
from updateWidget import Switch, Analog

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
        self.ui.num_lineEdit.textChanged.connect(self.updateAnalog)

        # 按键容器存放处
        self.switch_container = None
        # 模拟量按键存放处
        self.analog_container = None



        # OU的包
        self.package = bytearray(24)

        self.ou_protocol = {
            11: {
                0: '前进',
                7: '后退'
            },
            12: {
                6: '灯'
            },
            24: '升臂',
            5: '取料',
            1: '装料'
        }

    
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

        # 创建新的按键并添加到界面
        self.switch_container = Switch(self.ou_protocol, self.package)
        self.ui.verticalLayout_3.addWidget(self.switch_container)

    def updateAnalog(self):
        try:
            count = int(self.ui.num_lineEdit.text())
        except ValueError:
            return  # 如果不是正数, 则不做任何操作

        # 如果之前有按键容器, 删除它
        if self.analog_container:
            self.ui.verticalLayout_6.removeWidget(self.switch_container)
            self.analog_container.deleteLater()
            self.analog_container = None

        # 创建新的按键并添加到界面
        self.analog_container = Analog(self.ou_protocol, self.package)
        self.ui.verticalLayout_6.addWidget(self.analog_container)




    # 重写键盘按下事件
    def keyPressEvent(self, event):
        '''
        在大多数操作系统中，键盘按键长按会触发「重复按键」的功能。这种机制会在一定的时间间隔内重复触发 keyPressEvent，
        所以即使长按一个键，程序仍会检测到多次按下和松开事件（keyPressEvent 和 keyReleaseEvent 交替触发）
        '''
        # 获取按下的键盘按键
        key_char = event.text().upper()

        # 返回 True 表示是由按键长按自动触发的, 返回 False 表示是真正的按键松开事件
        if not event.isAutoRepeat() and key_char.isalpha():
            # 遍历 switch_container 中所有的 LineEdit  检查按键与 lineEdit 内容相同
            for lineEdit in self.switch_container.findChildren(QLineEdit):
                if lineEdit.text().upper() == key_char:
                    byte_num = lineEdit.property('byte_num')
                    bit_index = lineEdit.property('bit_index')
                    # 检查 lineEdit 对应的 checkBox 是否被选中
                    checkBox = self.switch_container.get_checkBox_by_property(['byte_num', byte_num],
                                                                              ['bit_index', bit_index])
                    if not checkBox.isChecked():
                        # 开关量, 按键所在的位赋 1
                        self.switch_container.package[byte_num - 1] |= (1 << bit_index)
                        # 对应的 button disabled
                        button = self.switch_container.get_button_by_property(['byte_num', byte_num],
                                                                              ['bit_index', bit_index])
                        button.setDisabled(True)

                        # 调试打印信息
                        message = ' '.join(f'{byte:02X}' for byte in self.switch_container.package)
                        print(f'{key_char}: {message}')
                        break

            # 遍历 analog_container 中所有的 LineEdit  检查按键与 lineEdit 内容相同
            for lineEdit in self.analog_container.findChildren(QLineEdit):
                if lineEdit.text().upper() == key_char:
                    byte_num = lineEdit.property('byte_num')

                    # 获取 lineEdit 对应的属性对应的 timer
                    increaseTimer = self.analog_container.get_timer_by_property(['increase', byte_num])
                    decreaseTimer = self.analog_container.get_timer_by_property(['decrease', byte_num])
                    # 按键按下, 开启使 progressBar 增加的定时器
                    increaseTimer.start(6)
                    decreaseTimer.stop()

                    # 对应的 button disabled
                    button = self.analog_container.get_button_by_property(['byte_num', byte_num])
                    button.setDisabled(True)

                    # # 调试打印信息
                    # message = ' '.join(f'{byte:02X}' for byte in self.switch_container.package)
                    # print(f'{key_char}: {message}')
                    # break

    # 重写键盘按下事件
    def keyReleaseEvent(self, event):
        '''
        当焦点在 lineedit 上时，松开 key 会自动触发 keyrelease 事件, 影响其他逻辑
        '''
        # 获取松开的键盘按键
        key_char = event.text().upper()

        # 手动松开 且 按键是字母
        if not event.isAutoRepeat() and key_char.isalpha():
            # 遍历 switch_container 中所有的 LineEdit  检查按键与 lineEdit 内容相同
            for lineEdit in self.switch_container.findChildren(QLineEdit):
                # 如果焦点在 lineEdit 上不做处理   按键与 lineEdit 内容相同
                if not lineEdit.hasFocus() and lineEdit.text().upper() == key_char:
                    byte_num = lineEdit.property('byte_num')
                    bit_index = lineEdit.property('bit_index')
                    # 检查 lineEdit 对应的 checkBox 是否被选中
                    checkBox = self.switch_container.get_checkBox_by_property(['byte_num', byte_num],
                                                                              ['bit_index', bit_index])
                    if not checkBox.isChecked():
                        # 开关量, 按键所在的位赋 0
                        self.switch_container.package[byte_num - 1] &= ~(1 << bit_index)
                        # 对应的 button disabled
                        button = self.switch_container.get_button_by_property(['byte_num', byte_num],
                                                                              ['bit_index', bit_index])
                        button.setEnabled(True)

                        # 调试打印信息
                        message = ' '.join(f'{byte:02X}' for byte in self.switch_container.package)
                        print(f'{key_char}: {message}')
                        break

            #  遍历 analog_container 中所有的 LineEdit  检查按键与 lineEdit 内容相同
            for lineEdit in self.analog_container.findChildren(QLineEdit):
                # 如果焦点在 lineEdit 上不做处理   按键与 lineEdit 内容相同
                if not lineEdit.hasFocus() and lineEdit.text().upper() == key_char:
                    byte_num = lineEdit.property('byte_num')

                    # 获取 lineEdit 对应的属性对应的 timer
                    increaseTimer = self.analog_container.get_timer_by_property(['increase', byte_num])
                    decreaseTimer = self.analog_container.get_timer_by_property(['decrease', byte_num])
                    # 按键松开, 开启使 progressBar 减少的定时器
                    increaseTimer.stop()
                    decreaseTimer.start(6)

                    # 对应的 button disabled
                    button = self.analog_container.get_button_by_property(['byte_num', byte_num])
                    button.setEnabled(True)

                    # # 调试打印信息
                    # message = ' '.join(f'{byte:02X}' for byte in self.switch_container.package)
                    # print(f'{key_char}: {message}')
                    # break

    def mousePressEvent(self, event):
        # 清除所有控件的焦点
        self.setFocus()
        super().mousePressEvent(event)  # 调用父类的鼠标点击事件处理


if __name__ == '__main__':
    app = QApplication(sys.argv)    # 创建应用程序对象
    window  = MainWindow()  # 创建主窗口
    window.show()   # 显示主窗口
    sys.exit(app.exec_())
