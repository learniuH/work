from PyQt5.QtWidgets import QWidget, QPushButton, QCheckBox, QGridLayout, QLineEdit
from PyQt5.QtCore import QTimer


class Switch(QWidget):
    def __init__(self, ou_protocol):
        super().__init__()
        self.switches = []
        self.layout = QGridLayout()

        self.package = bytearray(24)

        # 创建检测按钮长按的定时器
        self.detctLongPress = QTimer()
        self.detctLongPress.setInterval(300)  # 按键300ms视为按键被长按
        self.detctLongPress.timeout.connect(self.on_long_press)

        # 创建按钮长按状态的定时器
        self.longPressTimer = QTimer()
        self.longPressTimer.setInterval(100)  # 触发周期是100ms
        self.longPressTimer.timeout.connect(self.start_long_press)

        i = 0
        # 循环创建组合控件
        for byte_num in ou_protocol:
            if isinstance(ou_protocol.get(byte_num), dict):
                for bit_index in ou_protocol.get(byte_num):
                    self.pushButton = QPushButton(ou_protocol[byte_num][bit_index])
                    # 赋予 pushButton 两个自定义属性
                    self.set_costom_property(self.pushButton, byte_num, bit_index)
                    # pushButton 按下和松开 绑定到 slot
                    self.pushButton.pressed.connect(self.on_button_pressed)
                    self.pushButton.released.connect(self.on_button_released)

                    self.checkBox = QCheckBox('自锁')
                    self.set_costom_property(self.checkBox, byte_num, bit_index)
                    # 复选框状态变化绑定到 slot
                    self.checkBox.stateChanged.connect(self.on_checkbox_changed)

                    self.lineEdit = QLineEdit()
                    self.set_costom_property(self.lineEdit, byte_num, bit_index)


                    self.switches.append([self.pushButton, self.checkBox, self.lineEdit])
                    # 第 i 行第 1 列放 checkBox
                    self.layout.addWidget(self.checkBox, i, 0)
                    # 第 i 行第 2 列放 PushButton
                    self.layout.addWidget(self.pushButton, i, 1)
                    # 第 i 行第 3 列放 lineEdit
                    self.layout.addWidget(self.lineEdit, i, 2)
                    i += 1


                self.setLayout(self.layout)

    def set_costom_property(self, widget, byte_num, bit_index):
        ''' 给控件设置自定义属性 '''
        widget.setProperty('byte_num', byte_num)
        widget.setProperty('bit_index', bit_index)

    def on_button_pressed(self):
        # 获取发送信号的 pushButton
        sender = self.sender()
        byte_num = sender.property('byte_num')
        bit_index = sender.property('bit_index')

        try:
            # 如果是开关量, 按键所在的位赋 1
            self.package[byte_num - 1] |= (1 << bit_index)
        except TypeError:
            # 如果是模拟量
            pass

        # 调试打印信息
        message = ' '.join(f'{byte:02X}' for byte in self.package)
        print(message)

    def on_button_released(self):
        # 获取发送信号的 pushButton
        sender = self.sender()
        byte_num = sender.property('byte_num')
        bit_index = sender.property('bit_index')

        try:
            # 如果是开关量, 按键所在的位赋 0
            self.package[byte_num - 1] &= ~(1 << bit_index)
        except TypeError:
            # 如果是模拟量
            pass

        # 调试打印信息
        message = ' '.join(f'{byte:02X}' for byte in self.package)
        print(message)

    def get_button_by_property(self, property1, property2):
        # 遍历窗口中的所有子控件, 找到匹配的按钮
        for button in self.findChildren(QPushButton):
            if button.property(property1[0]) == property1[1] and button.property(property2[0]) == property2[1]:
                return button
        return None

    def on_checkbox_changed(self):
        # 获取发送信号的 checkBox
        sender = self.sender()
        byte_num = sender.property('byte_num')
        bit_index = sender.property('bit_index')

        # checkBox 现在的状态
        checkBox_state = sender.isChecked()

        try:
            # 如果是开关量, 所在位赋 1, 并且按键 disabled
            if checkBox_state:  # 如果被勾选
                # 复选框所在的位赋 1
                self.package[byte_num - 1] |= (1 << bit_index)
                # 对应 button disabled
                button = self.get_button_by_property(['byte_num', byte_num], ['bit_index', bit_index])
                button.setDisabled(True)

            else:
                # 复选框所在的位赋 0
                self.package[byte_num - 1] &= ~(1 << bit_index)
                # 对应 button enabled
                button = self.get_button_by_property(['byte_num', byte_num], ['bit_index', bit_index])
                button.setEnabled(True)

        except TypeError:
            # 如果是模拟量
            pass

        # 调试打印信息
        message = ' '.join(f'{byte:02X}' for byte in self.package)
        print(message)


    def start_detctLongPressTimer(self):
        # 按下按钮时启动定时器
        self.detctLongPress.start()

    def stop_detctLongPressTimer(self):
        # 松开按键关闭定时器
        self.detctLongPress.stop()

    def on_long_press(self):
        self.detctLongPress.stop()  # 停止检测长按的定时器
        self.longPressTimer.start() # 开始按键长按的定时器
        print('按键处于长按状态')

    def start_long_press(self):
        print('急停, 100ms发一包')

    def stop_long_press(self):
        # 当按钮释放时关闭定时器
        self.longPressTimer.stop()



    # # 重写 keyPressEvent 方法
    # def keyPressEvent(self, event):
    #     # 获取按下的字符
    #     key_char = event.text().upper()
    #
    #     # 检查按下的键是字母或数字
    #     if key_char.isalnum():
    #         # 遍历窗口中所有的子控件, 检查是否有绑定的键
    #         for lineEdit in self.findChildren(QLineEdit):
    #             if lineEdit.text().upper() == key_char:
    #                 byte_num = lineEdit.property('byte_num')
    #                 bit_index = lineEdit.property('bit_index')
    #
    #                 # 如果是开关量, 按键所在的位赋 1
    #                 self.package[byte_num - 1] |= (1 << bit_index)
    #                 # 对应的 button disabled
    #                 button = self.get_button_by_property(['byte_num', byte_num], ['bit_index', bit_index])
    #                 button.setDisabled(True)
    #
    #     # 调试打印信息
    #     message = ' '.join(f'{byte:02X}' for byte in self.package)
    #     print(message)






    # # 重写 mousePressEvent 方法
    # def mousePressEvent(self, event):
    #     # 当点击其他地方时, 取消文本框的焦点
    #     if not self.lineEdit.geometry().contains(event.pos()):
    #         self.lineEdit.clearFocus()
    #     super().mousePressEvent(event)
