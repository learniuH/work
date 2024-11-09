from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget, QPushButton, QCheckBox, QGridLayout, QLineEdit, QSlider, QProgressBar, QLabel, \
    QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, QRegExp


class Switch(QWidget):
    def __init__(self, ou_protocol, package):
        super().__init__()
        self.switches = []
        self.switchesLayout = QGridLayout()


        # 存放 ou 的包 校验和
        self.package = package
        self.cumulative_sum = 0


        i = 0
        # 循环创建组合控件
        for byte_num in ou_protocol:
            if isinstance(ou_protocol.get(byte_num), dict):
                # 开关量区域控件创建
                for bit_index in ou_protocol.get(byte_num):
                    ''' pushButton '''
                    self.pushButton = QPushButton(ou_protocol[byte_num][bit_index])
                    # 赋予 pushButton 两个自定义属性
                    self.set_costom_property(self.pushButton, byte_num, bit_index)
                    # pushButton 按下和松开 绑定到 slot
                    self.pushButton.pressed.connect(self.on_button_pressed)
                    self.pushButton.released.connect(self.on_button_released)

                    ''' checkBox '''
                    self.checkBox = QCheckBox('自锁')
                    self.set_costom_property(self.checkBox, byte_num, bit_index)
                    # 复选框状态变化绑定到 slot
                    self.checkBox.stateChanged.connect(self.on_checkbox_changed)

                    ''' lineEdit: 当 button 按下时, 对应绑定的 key 按下, lineEdit 会获得焦点, 程序异常'''
                    self.lineEdit = QLineEdit()
                    self.lineEdit.setFocusPolicy(Qt.ClickFocus)     # 只能通过单击获得焦点
                    self.lineEdit.setPlaceholderText('Key')
                    self.set_costom_property(self.lineEdit, byte_num, bit_index)
                    self.lineEdit.setValidator(QRegExpValidator(QRegExp('^[A-Za-z]?$')))    # 正则表达式匹配26个英文字母


                    self.switches.append([self.pushButton, self.checkBox, self.lineEdit])
                    # 第 i 行第 1 列放 checkBox
                    self.switchesLayout.addWidget(self.checkBox, i, 0)
                    # 第 i 行第 2 列放 PushButton
                    self.switchesLayout.addWidget(self.pushButton, i, 1)
                    # 第 i 行第 3 列放 lineEdit
                    self.switchesLayout.addWidget(self.lineEdit, i, 2)
                    i += 1


                self.setLayout(self.switchesLayout)

    def set_costom_property(self, widget, byte_num, bit_index):
        ''' 给控件设置自定义属性 '''
        widget.setProperty('byte_num', byte_num)
        widget.setProperty('bit_index', bit_index)

    def on_button_pressed(self):
        # 获取发送信号的 pushButton
        sender = self.sender()
        byte_num = sender.property('byte_num')
        bit_index = sender.property('bit_index')

        # 校验和减去历史的字节量
        self.cumulative_sum -= self.package[byte_num - 1]
        # 开关量, 按键所在的位赋 1
        if isinstance(bit_index, int):
            # 1个 bit 代表一个开关
            self.package[byte_num - 1] |= (1 << bit_index)
        else:
            # 多个 bit 代表一个开关, 所有 bit 置 1
            start_index, end_index = bit_index.split('-')
            start_index, end_index = int(start_index), int(end_index)
            for i in range(start_index, end_index + 1):
                self.package[byte_num - 1] |= (1 << i)
        # 校验和更新新的字节量
        self.cumulative_sum += self.package[byte_num - 1]

        # 调试打印信息
        message = ' '.join(f'{byte:02X}' for byte in self.package)
        print(f'{message}\n校验和(HEX): {self.cumulative_sum:02X}    CRC: {self.cumulative_sum & 0xFF:02X}')

    def on_button_released(self):
        # 获取发送信号的 pushButton
        sender = self.sender()
        byte_num = sender.property('byte_num')
        bit_index = sender.property('bit_index')

        # 开关量, 按键所在的位赋 0 校验和减去历史的字节量
        self.cumulative_sum -= self.package[byte_num - 1]
        if isinstance(bit_index, int):
            # 1个 bit 代表一个开关
            self.package[byte_num - 1] &= ~(1 << bit_index)
        else:
            # 多个 bit 代表一个开关, 所有 bit 置 0
            start_index, end_index = bit_index.split('-')
            start_index, end_index = int(start_index), int(end_index)
            for i in range(start_index, end_index + 1):
                self.package[byte_num - 1] &= ~(1 << i)
        # 校验和更新新的字节量
        self.cumulative_sum += self.package[byte_num - 1]

        # 调试打印信息
        message = ' '.join(f'{byte:02X}' for byte in self.package)
        print(f'{message}\n校验和(HEX): {self.cumulative_sum:02X}    CRC: {self.cumulative_sum & 0xFF:02X}')


    def get_button_by_property(self, property1, property2):
        # 遍历窗口中的所有 pushButton  找到匹配的按钮
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
        checkBox_ischecked = sender.isChecked()

        # 开关量, 所在位赋 1, 并且按键 disabled
        if checkBox_ischecked:  # 如果被勾选
            # 复选框所在的位赋 1 校验和减去历史的字节量
            self.cumulative_sum -= self.package[byte_num - 1]
            if isinstance(bit_index, int):
                # 1个 bit 代表一个开关
                self.package[byte_num - 1] |= (1 << bit_index)
            else:
                # 多个 bit 代表一个开关, 所有 bit 置 1
                start_index, end_index = bit_index.split('-')
                start_index, end_index = int(start_index), int(end_index)
                for i in range(start_index, end_index + 1):
                    self.package[byte_num - 1] |= (1 << i)
            # 校验和更新新的字节量
            self.cumulative_sum += self.package[byte_num - 1]

            # 对应 button disabled
            button = self.get_button_by_property(['byte_num', byte_num],
                                                 ['bit_index', bit_index])
            button.setDisabled(True)

        else:
            # 校验和减去历史的字节量
            self.cumulative_sum -= self.package[byte_num - 1]
            # 复选框所在的位赋 0
            if isinstance(bit_index, int):
                # 1个 bit 代表一个开关
                self.package[byte_num - 1] &= ~(1 << bit_index)
            else:
                # 多个 bit 代表一个开关, 所有 bit 置 0
                start_index, end_index = bit_index.split('-')
                start_index, end_index = int(start_index), int(end_index)
                for i in range(start_index, end_index + 1):
                    self.package[byte_num - 1] &= ~(1 << i)
            # 校验和更新新的字节量
            self.cumulative_sum += self.package[byte_num - 1]

            # 对应 button enabled
            button = self.get_button_by_property(['byte_num', byte_num],
                                                 ['bit_index', bit_index])
            button.setEnabled(True)

        # 调试打印信息
        message = ' '.join(f'{byte:02X}' for byte in self.package)
        print(f'{message}\n校验和(HEX): {self.cumulative_sum:02X}    CRC: {self.cumulative_sum & 0xFF:02X}')

    def get_checkBox_by_property(self, property1, property2):
        # 遍历窗口中的所有 checkBox  找到匹配的按钮
        for checkBox in self.findChildren(QCheckBox):
            if checkBox.property(property1[0]) == property1[1] and checkBox.property(property2[0]) == property2[1]:
                return checkBox
        return None


class Analog(QWidget):
    def __init__(self, ou_protocol, package):
        super().__init__()
        self.analog = []
        self.analogLayout = QGridLayout()

        # ou 的包 校验和
        self.package = package
        self.cumulative_sum = 0

        i = 0
        # 循环创建组合控件
        for byte_num in ou_protocol:
            # 模拟量区域控件创建
            if isinstance(ou_protocol.get(byte_num), str):
                ''' pushButton '''
                self.pushButton = QPushButton(ou_protocol.get(byte_num))
                self.set_costom_property(self.pushButton, byte_num)
                # pushButton 按下和松开 绑定到 slot
                self.pushButton.pressed.connect(self.startIncreasing)
                self.pushButton.released.connect(self.startDecreasing)

                ''' Timer '''
                # 计时器用于增加和减少进度条的值
                self.increase_timer = QTimer(self)
                self.increase_timer.setProperty('increase', byte_num)
                self.increase_timer.timeout.connect(self.increaseProgress)

                self.decrease_timer = QTimer(self)
                self.decrease_timer.setProperty('decrease', byte_num)
                self.decrease_timer.timeout.connect(self.decreaseProgress)

                ''' lineEdit: 当 button 按下时, 对应绑定的 key 按下, lineEdit 会获得焦点, 程序异常'''
                self.lineEdit = QLineEdit()
                self.lineEdit.setFocusPolicy(Qt.ClickFocus)  # 只能通过单击获得焦点
                self.lineEdit.setPlaceholderText("Key")
                self.set_costom_property(self.lineEdit, byte_num)
                self.lineEdit.setValidator(QRegExpValidator(QRegExp('^[A-Za-z]?$')))  # 正则表达式匹配26个英文字母 且只能是1个

                ''' hLayout '''
                self.hLayout = QHBoxLayout()

                ''' Slider '''
                self.slider = QSlider(Qt.Horizontal)
                self.set_costom_property(self.slider, byte_num)
                # 模拟信号可配置的范围 (0, 100)
                self.slider.setRange(1, 100)
                # 模拟信号的初始值都是 100
                self.slider.setValue(100)
                self.slider.valueChanged.connect(self.update_max_value)

                ''' Label '''
                self.label = QLabel(f'{self.slider.value()}')
                self.set_costom_property(self.label, byte_num)

                # 把 slider 和 label 添加到 hLayout 里
                self.hLayout.addWidget(self.slider)
                self.hLayout.addWidget(self.label)

                ''' progressBar '''
                self.progressBar = QProgressBar()
                self.set_costom_property(self.progressBar, byte_num)
                self.progressBar.limit = 100
                self.progressBar.valueChanged.connect(self.on_value_changed)



                self.analog.append([self.pushButton, self.lineEdit, self.hLayout, self.progressBar])
                # 第 2 行第 1 列放 PushButton
                self.analogLayout.addWidget(self.pushButton, i, 0)
                # 第 1 行第 2 列放 lineEdit
                self.analogLayout.addWidget(self.lineEdit, i + 1, 0)
                # 第 1 行第 1 列放 hLayout
                self.analogLayout.addLayout(self.hLayout, i + 1, 1)
                # 第 2 行第 2 列放 progressBar
                self.analogLayout.addWidget(self.progressBar, i, 1)
                i += 2


                self.setLayout(self.analogLayout)


    def set_costom_property(self, widget, byte_num):
        ''' 给控件设置自定义属性 '''
        widget.setProperty('byte_num', byte_num)

    def get_label_by_property(self, property):
        # 遍历窗口中的所有 label  找到匹配的 label
        for label in self.findChildren(QLabel):
            if label.property(property[0]) == property[1]:
                return label
        return None

    def update_max_value(self):
        '''
        当 slider 值变化时, 更新 label, 限制对应 byte 输出的最大值
        '''
        sender = self.sender()
        byte_num = sender.property('byte_num')
        # 更新对应 label 的值
        label = self.get_label_by_property(['byte_num', byte_num])
        label.setText(str(sender.value()))

        # 限制 progressBar 的最大值
        progressBar = self.get_progressBar_by_property(['byte_num', byte_num])
        progressBar.limit = sender.value()

    def get_timer_by_property(self, property):
        ''' QTimer 需要有父对象才能被 findChildren 找到'''
        # 遍历窗口中的所有 timer  找到匹配的定时器
        for timer in self.findChildren(QTimer):
            if timer.property(property[0]) == property[1]:
                return timer
        return None

    def startIncreasing(self):
        ''' 当按钮按下时增加进度条的值，'''
        sender = self.sender()
        byte_num = sender.property('byte_num')

        # 通过 byte_num 找到 increase / decrease 定时器
        increaseTimer = self.get_timer_by_property(['increase', byte_num])
        decreaseTimer = self.get_timer_by_property(['decrease', byte_num])

        decreaseTimer.stop()  # 停止进度减少的定时器
        increaseTimer.start(6)   # 每6ms增加一次

    def startDecreasing(self):
        ''' 当按钮释放时减少进度条的值，'''
        sender = self.sender()
        byte_num = sender.property('byte_num')

        # 通过 byte_num 找到 increase / decrease 定时器
        increaseTimer = self.get_timer_by_property(['increase', byte_num])
        decreaseTimer = self.get_timer_by_property(['decrease', byte_num])

        increaseTimer.stop()  # 停止增加的计时器
        decreaseTimer.start(6)   # 每6ms减少一次

    def get_progressBar_by_property(self, property):
        # 遍历窗口中的所有 progressBar
        for progressBar in self.findChildren(QProgressBar):
            if progressBar.property(property[0]) == property[1]:
                return progressBar
        return None

    def increaseProgress(self):
        ''' 增加进度条的值 '''
        sender = self.sender()
        byte_num = sender.property('increase')
        progressBar = self.get_progressBar_by_property(['byte_num', byte_num])

        if progressBar.value() < progressBar.limit:
            progressBar.setValue(progressBar.value() + 1)
        else:
            sender.stop()  # 达到最大值时停止增加

    def decreaseProgress(self):
        ''' 减少进度条的值 '''
        sender = self.sender()
        byte_num = sender.property('decrease')
        progressBar = self.get_progressBar_by_property(['byte_num', byte_num])

        if progressBar.value() > progressBar.minimum():
            progressBar.setValue(progressBar.value() - 1)
        else:
            sender.stop()


    def on_value_changed(self):
        ''' progressBar 值变化的时候, 更新报文 '''
        sender = self.sender()
        byte_num = sender.property('byte_num')
        # 校验和减去历史的字节量
        self.cumulative_sum -= self.package[byte_num - 1]
        self.package[byte_num - 1] = sender.value()
        # 校验和更新新的字节量
        self.cumulative_sum += self.package[byte_num - 1]

        # 调试打印信息
        message = ' '.join(f'{byte:02X}' for byte in self.package)
        print(f'{message}\n校验和(HEX): {self.cumulative_sum:02X}    CRC: {self.cumulative_sum & 0xFF:02X}')


    def get_button_by_property(self, property):
        # 遍历窗口中的所有 pushButton  找到匹配的按钮
        for button in self.findChildren(QPushButton):
            if button.property(property[0]) == property[1]:
                return button
        return None


