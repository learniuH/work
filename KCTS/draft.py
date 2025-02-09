from PyQt5.QtGui import QRegExpValidator, QIntValidator, QColor, QPalette, QTextCursor, QTextCharFormat
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLineEdit
from PyQt5.QtCore import QRegExp, QTimer, QSettings, pyqtSignal

from ui import Ui_Window
from updateWidget import Switch, Analog

import sys
import pandas as pd
import socket
import threading
import time


class MainWindow(QWidget):
    # 定义信号, 将更新 textEdit 的请求发送到主线程
    update_textEdit_signal = pyqtSignal(bytearray)

    def __init__(self):
        super().__init__()  #初始化父类
        self.ui = Ui_Window()   # 创建 UI 类的实例
        self.ui.setupUi(self)   # 将 UI 布局加载到 MainWindow 上


        # 绑定按钮点击事件到自定义的 slot 函数
        self.ui.connect_pushButton.clicked.connect(self.connect_button_clicked)
        self.ui.openFile_pushButton.clicked.connect(self.open_file_dialog)
        self.ui.clear_info_pushButton.clicked.connect(self.clear_prompt_info)

        # 初始化线程变量
        self.send_thread = None
        self.send_message = False

        # 获取本地电脑 IP 和 端口
        self.local_ip = socket.gethostbyname(socket.gethostname())
        self.ui.local_ip_lineEdit.setText(f'{self.local_ip}')

        # target IP lineEdit正则表达式匹配 IPv4 地址格式
        ipv4_regex = QRegExp('^((25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})\.){3}(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})$')
        ipv4_validator = QRegExpValidator(ipv4_regex, self.ui.target_ip_lineEdit)
        self.ui.target_ip_lineEdit.setValidator(ipv4_validator)

        # Target Port 和 Local Port 匹配为 0-65535 之间的有效端口号
        self.ui.target_port_lineEdit.setValidator(QRegExpValidator(QRegExp('^([0-5]?\d{1,4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$')))
        self.ui.local_port_lineEdit.setValidator(QRegExpValidator(QRegExp('^([0-5]?\d{1,4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$')))
        self.ui.sending_cycle_lineEdit.setValidator(QRegExpValidator(QRegExp('^([0-5]?\d{1,4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$')))
        self.ui.sending_cycle_lineEdit.setText('100')     # 周期的默认值是 100 ms, 可以修改, 范围是 0-65535

        # 协议头内容 格式: hex hex hex 最多10个两位十六进制, 9个空格
        self.ui.protocol_header_lineEdit.setValidator(QRegExpValidator(QRegExp('^(([A-Fa-f0-9]{2} ){0,9}[A-Fa-f0-9]{2})?$')))

        # 配置协议头 lineEdit placeholdertext 颜色为红色
        palceholderText_color = QColor('red')
        palette = self.ui.protocol_header_lineEdit.palette()
        palette.setColor(QPalette.PlaceholderText, palceholderText_color)
        self.ui.protocol_header_lineEdit.setPalette(palette)

        # 将子线程中请求更新 textEdit 的信号绑定到对应的更新函数
        self.update_textEdit_signal.connect(self.update_raw_message_textEdit)


        # 按键容器存放处
        self.switch_container = None
        # 模拟量按键存放处
        self.analog_container = None


        # 初始化 OU 协议和要发送的 UDP 包
        self.ou_protocol = None
        self.protocol_length = None
        self.package = None


        # 初始化 CRC 校验和
        self.cumulative_sum = 0

        # 加载上一次程序退出时的部分配置
        self.load_last_content()


    def load_last_content(self):
        ''' 加载上一次的运行时部分 lineEdit 的内容 '''
        settings = QSettings('ou_simulator', 'configure')
        self.ui.protocol_header_lineEdit.setText(settings.value('protocol_header_content', ''))
        self.ui.target_ip_lineEdit.setText(settings.value('target_ip_content', ''))
        self.ui.target_port_lineEdit.setText(settings.value('target_port_content', ''))
        self.ui.local_port_lineEdit.setText(settings.value('local_port_content', ''))


    def open_file_dialog(self):
        ''' 打开文件选择对话框, 只显示 Excel 文件 '''
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择项目通信协议', '', 'Excel Files (*.xlsx);;All Files (*)'
        )
        if file_path:
            # 读取文件的 OU->MU 表单, 更新协议内容
            sheet_name = 'OU->MU'
            try:
                self.ou_protocol, self.protocol_length = self.read_protocol_excel(file_path, sheet_name)
                # 定义 package 长度
                self.package = bytearray(self.protocol_length)

                # 更新界面上的 switch 和 analog 控件
                self.updateSwitchs()
                self.updateAnalog()
            except TypeError:
                self.ui.tips_lineEdit.setText('协议读取失败！请按提示内容修改协议！')
                return


    def clean_number(self, value, prefix):
        """
        从 value 中提取数字，支持以指定 prefix（如 'bit' 或 'byte'）开头的格式。

        Args:
            value (str, int, float): 输入的值，可能是带前缀的字符串或数字。
            prefix (str): 指定的前缀（例如 'bit' 或 'byte'），用于识别并提取数字部分。

        Returns:
            int, str, float: 返回提取后的数字或范围字符串。
        """
        if isinstance(value, (int, float)):
            # 如果是数字直接返回
            return value

        # 统一处理字符串的大小写，去除前缀
        value_lower = value.lower()
        if prefix.lower() in value_lower:
            value_lower = value_lower.replace(prefix.lower(), '')

            # 如果是单一的数字，则转换为整数
            if value_lower.isdigit():
                return int(value_lower)

            # 如果是范围格式，如 '2-3'，则去除空格后返回原始字符串
            if '-' in value_lower:
                return value_lower.replace(' ', '')

        # 如果无法处理，返回原始值
        return value

    def read_protocol_excel(self, file_path, sheet_name):
        """
        读取通信协议表, 提取其中对 开关量和模拟量 的字节定义、位定义、描述

        Args:
            file_path (str): 通信协议的路径，只能是 Excel 文件
            sheet_name (str): Excel表单名字（例如 OU->MU）

        Returns:
            ou_protocol(dict): {
                byte_num: {
                    bit_index: describe     # 开关量部分
                }
                byte_num: describe          # 模拟量部分
            }   # byte_num 和 bit_index 如果是 str 代表是 describe 由多个字节或多个位组成
        """
        try:
            ou2mu_df = pd.read_excel(file_path, sheet_name=sheet_name)
        except ValueError as e:
            if "Worksheet named 'OU->MU' not found" in str(e):
                self.ui.tips_lineEdit.setText('请检查协议中是否有 "OU->MU" 表单！')
                return

        try:
            # 找到包含 '字节序号' 的行号
            header_index = ou2mu_df[ou2mu_df.eq('字节序号').any(axis=1)].index[0]
            # 将 '字节序号' 行作为 columns
            ou2mu_df.columns = ou2mu_df.iloc[header_index]
            # 删除作为列名的行，并重置索引
            ou2mu_df = ou2mu_df[(header_index + 1):].reset_index(drop=True)
        except IndexError as e:
            if 'index 0 is out of bounds for axis 0 with size 0' in str(e):
                self.ui.tips_lineEdit.setText('检查模块定义行中是否有"字节序号"单元格！')
                return

        try:
            # 将名称和字节序号两列填充
            ou2mu_df.loc[:, '名称'] = ou2mu_df['名称'].fillna(method='ffill')
            ou2mu_df.loc[:, '字节序号'] = ou2mu_df['字节序号'].fillna(method='ffill')
        except KeyError as e:
            if '名称' in str(e):
                self.ui.tips_lineEdit.setText('请检查模块定义行中是否有"名称"单元格！')
                return

        # 将 '名称' 列置为 index
        ou2mu_df.set_index('名称', inplace=True)

        # 初始化协议字典
        ou_protocol = {}

        # 取开关量和模拟量这部分的 df
        try:
            switch_df = ou2mu_df.loc['开关量', :]
            analog_df = ou2mu_df.loc['模拟量', :]
        except KeyError as e:
            if '开关量' in str(e):
                self.ui.tips_lineEdit.setText('请检查协议中名称列是否有"开关量"单元格！')
                return
            if '模拟量' in str(e):
                self.ui.tips_lineEdit.setText('请检查协议中名称列是否有"模拟量"单元格！')
                return

        try:
            # 读取 CRC 校验位所在的行
            crc_ser = ou2mu_df.loc['CRC']
        except KeyError as e:
            if 'CRC' in str(e):
                self.ui.tips_lineEdit.setText('请检查通信协议中名称列是否有"CRC"单元格，大小写注意！')
                return
        # OU->MU 协议的字节数量
        protocol_length = self.clean_number(crc_ser['字节序号'], 'byte')

        # 开关量协议更新
        for _, switch_row in switch_df.iterrows():
            # 通过 '字节序号' 索引读取 byte_num
            byte_num = switch_row['字节序号']
            # 提取 byte_num 中的数字
            byte_num = self.clean_number(byte_num, 'byte')

            try:
                # 通过 '内容' 索引读取 bit_index
                bit_index = switch_row['内容']
                # 提取 bit_index 中的数字
                bit_index = self.clean_number(bit_index, 'bit')

                # 通过 '描述' 更新协议内容
                switch_desc = switch_row['描述']
            except KeyError as e:
                if '内容' in str(e):
                    self.ui.tips_lineEdit.setText('请检查通信协议中模块定义行是否有"内容"单元格！')
                    return
                if '描述' in str(e):
                    self.ui.tips_lineEdit.setText('请将功能定义所在列的列名修改为"描述"！')
                    return


            # 更新字节序号
            if byte_num not in ou_protocol and switch_desc != '预留' and not pd.isnull(switch_desc):
                ou_protocol[byte_num] = {}
            # 更新协议内容
            if switch_desc != '预留' and not pd.isnull(switch_desc):
                ou_protocol[byte_num][bit_index] = switch_desc

        # 模拟量协议更新
        for _, analog_row in analog_df.iterrows():
            # 通过 '字节序号' 索引读取 byte_num
            byte_num = analog_row['字节序号']
            # 提取 byte_num 中的数字
            byte_num = self.clean_number(byte_num, 'byte')

            # 通过 '描述' 更新协议内容
            analog_desc = analog_row['描述']
            # 更新协议
            if analog_desc != '预留' and not pd.isnull(analog_desc):
                ou_protocol[byte_num] = analog_desc

        return ou_protocol, protocol_length



    def updateSwitchs(self):
        ''' 更新界面上的开关量 '''
        # 如果之前有按键容器, 删除它
        if self.switch_container:
            self.ui.switch_container_layout.removeWidget(self.switch_container)
            self.switch_container.deleteLater()
            self.switch_container = None

        # 创建新的按键并添加到界面
        self.switch_container = Switch(self.ou_protocol, self.package, self.cumulative_sum, self.ui.tips_lineEdit)
        self.ui.switch_container_layout.addWidget(self.switch_container)

    def updateAnalog(self):
        ''' 更新界面上的模拟量 '''
        # 如果之前有模拟开关容器, 删除它
        if self.analog_container:
            self.ui.analog_container_layout.removeWidget(self.switch_container)
            self.analog_container.deleteLater()
            self.analog_container = None

        # 创建新的按键并添加到界面
        self.analog_container = Analog(self.ou_protocol, self.package, self.cumulative_sum, self.ui.tips_lineEdit)
        self.ui.analog_container_layout.addWidget(self.analog_container)


    def connect_button_clicked(self):
        # 没有导入协议, 没有输入协议头, 点击按钮不做处理
        if self.ou_protocol is None or self.ui.protocol_header_lineEdit.text() == '':
            self.ui.tips_lineEdit.setText('请先导入项目通信协议！')
            return

        ''' 点击连接  判断所有 lineEdit 里是否有内容且合法 '''
        if not self.send_message:
            # 检查 target ip / target port / local port / 周期 是否都为有效值
            if self.ui.target_ip_lineEdit.text() == '':
                self.ui.target_ip_lineEdit.setPlaceholderText('请输入Target IP！')
                return
            elif self.ui.target_port_lineEdit.text() == '':
                self.ui.target_port_lineEdit.setPlaceholderText('请输入Target Port！')
                return
            elif self.ui.local_port_lineEdit.text() == '':
                self.ui.local_port_lineEdit.setPlaceholderText('请绑定本地Port！')
                return
            elif self.ui.sending_cycle_lineEdit.text() == '':
                self.ui.sending_cycle_lineEdit.setPlaceholderText('请输入发送周期！')
                return

            # 验证 target IP 是否合法
            if not self.ui.target_ip_lineEdit.hasAcceptableInput():
                self.ui.tips_lineEdit.setText('请输入合法的 Target IP！')
                return


            # 处理 protocol header lineEdit 中的内容, 更新 package 的前 10 个byte
            self.protocol_header = self.ui.protocol_header_lineEdit.text().split(' ')
            # lineEdit 里面有 10个十六进制数字, 不能是9个数字 加一个空格
            if len(self.protocol_header) == 10 and self.protocol_header[9] != '':
                for i in range(len(self.protocol_header)):
                    # 校验和减去上一次协议头的内容
                    self.cumulative_sum -= self.package[i]
                    # 更新协议值
                    self.package[i] = int(self.protocol_header[i], 16)
                    # 更新累加值
                    self.cumulative_sum += self.package[i]

            else:
                self.ui.tips_lineEdit.setText('请输入协议头 Byte1-10！')
                return


            # 更新电脑此时的IP, 避免更改 IP 后, sock 无法绑定的问题
            self.local_ip = socket.gethostbyname(socket.gethostname())
            self.ui.local_ip_lineEdit.setText(f'{self.local_ip}')

            ''' 启动数据发送线程, 主程序退出自动关闭 '''
            self.send_thread = threading.Thread(target=self.sending_message, daemon=True)
            self.send_thread.start()

        # 点击断开
        else:
            # 清除 textEdit 第二行的内容, 保留字节序号
            line = self.ui.raw_message_textEdit.toPlainText().splitlines()
            self.ui.raw_message_textEdit.setText(line[0])

            # lineEdit 恢复正常使用
            self.ui.target_ip_lineEdit.setReadOnly(False)
            self.ui.target_port_lineEdit.setReadOnly(False)
            self.ui.local_port_lineEdit.setReadOnly(False)
            self.ui.protocol_header_lineEdit.setReadOnly(False)
            self.ui.sending_cycle_lineEdit.setReadOnly(False)
            self.ui.openFile_pushButton.setEnabled(True)

            # 更新标志位状态
            self.send_message = False
            self.ui.connect_pushButton.setText('点击连接')


    def sending_message(self):
        ''' 用于发送报文的线程 '''
        ip = self.ui.target_ip_lineEdit.text()
        port = self.ui.target_port_lineEdit.text()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            try:
                local_port = self.ui.local_port_lineEdit.text()
                local_address = (self.local_ip, local_port)
                # 绑定电脑的 IP 和 端口
                sock.bind((local_address[0], int(local_address[1])))

                ''' 如果 bind 不成功, 下面的内容将不会被执行 '''
                # 只有包成功发送出去了, 才能改变标志位 改变文字
                self.send_message = True
                self.ui.connect_pushButton.setText('点击断开')


                # 发送 udp 报文时, 不允许修改 lineEdit 内容, 不允许打开协议
                self.ui.target_ip_lineEdit.setReadOnly(True)
                self.ui.target_port_lineEdit.setReadOnly(True)
                self.ui.local_port_lineEdit.setReadOnly(True)
                self.ui.protocol_header_lineEdit.setReadOnly(True)
                self.ui.sending_cycle_lineEdit.setReadOnly(True)
                self.ui.openFile_pushButton.setDisabled(True)

            except OSError as e:
                self.ui.tips_lineEdit.setText('错误：本地端口可能被占用，请使用其他端口！')

            # 发送 UDP 包
            while self.send_message:
                # 计算三部分的 校验和 取低8位
                crc = self.cumulative_sum + self.switch_container.cumulative_sum + self.analog_container.cumulative_sum
                self.package[-1] = crc & 0xFF
                sock.sendto(self.package, (ip, int(port)))

                # 发射信号到主线程, 将报文更新到 textEdit 上
                self.update_textEdit_signal.emit(self.package)

                time.sleep(int(self.ui.sending_cycle_lineEdit.text()) / 1000)   # 周期 ms


    def update_raw_message_textEdit(self, raw_message):
        ''' 同步更新 raw message textEdit '''
        lines = self.ui.raw_message_textEdit.toPlainText().splitlines()

        # 保留第一行的字节序号, 从第二行开始更新
        byte_num_series = lines[0]
        raw_message = ' '.join(f'{byte:02X} ' for byte in raw_message)

        # 清空 textEdit
        self.ui.raw_message_textEdit.clear()

        # 设置第一行的内容为蓝色
        cursor = self.ui.raw_message_textEdit.textCursor()
        cursor.movePosition(QTextCursor.Start)

        blue_format = QTextCharFormat()
        blue_format.setForeground(QColor("blue"))

        black_format = QTextCharFormat()
        black_format.setForeground(QColor('black'))

        cursor.insertText(f'{byte_num_series}', blue_format)  # 第一行蓝色
        cursor.insertText(f'\n{raw_message}', black_format)  # 其他行默认颜色



    def clear_prompt_info(self):
        ''' 清除提示信息 '''
        self.ui.tips_lineEdit.clear()


    # 处理 开关量 和 模拟量 区域英文键盘按下的事件
    def keyPressEvent(self, event):
        '''
        在大多数操作系统中，键盘按键长按会触发「重复按键」的功能。这种机制会在一定的时间间隔内重复触发 keyPressEvent，
        所以即使长按一个键，程序仍会检测到多次按下和松开事件（keyPressEvent 和 keyReleaseEvent 交替触发）
        '''
        # 获取按下的键盘按键
        key_char = event.text().upper()

        # 返回 True 表示是由按键长按自动触发的, 返回 False 表示是真正的按键松开事件
        if (self.switch_container is not None or self.analog_container is not None) and \
                not event.isAutoRepeat() and key_char.isalpha():
            # 遍历 switch_container 中所有的 LineEdit  检查按键与 lineEdit 内容相同
            for lineEdit in self.switch_container.findChildren(QLineEdit):
                if lineEdit.text().upper() == key_char:
                    byte_num = lineEdit.property('byte_num')
                    bit_index = lineEdit.property('bit_index')
                    # 检查 lineEdit 对应的 checkBox 是否被选中
                    checkBox = self.switch_container.get_checkBox_by_property(['byte_num', byte_num],
                                                                              ['bit_index', bit_index])
                    # 获取对应的 button
                    button = self.switch_container.get_button_by_property(['byte_num', byte_num],
                                                                          ['bit_index', bit_index])
                    # 如果按钮没有被按下 checkbox 没有被选择
                    if button.isEnabled() and not checkBox.isChecked():
                        try:
                            # 校验和减去历史的字节量
                            self.switch_container.cumulative_sum -= self.switch_container.package[byte_num - 1]
                            # 开关量, 按键所在的位赋 1
                            if isinstance(bit_index, int):
                                # 1个 bit 代表一个开关
                                self.switch_container.package[byte_num - 1] |= (1 << bit_index)
                            else:
                                # 多个 bit 代表一个开关, 所有 bit 置 1
                                start_index, end_index = bit_index.split('-')
                                start_index, end_index = int(start_index), int(end_index)
                                for i in range(start_index, end_index + 1):
                                    self.switch_container.package[byte_num - 1] |= (1 << i)
                            # 校验和更新新的字节量
                            self.switch_container.cumulative_sum += self.switch_container.package[byte_num - 1]

                            # 对应的 button disabled
                            button.setDisabled(True)
                            # 对应的 lineEdit 只读
                            lineEdit.setReadOnly(True)
                        except TypeError:
                            self.ui.tips_lineEdit.setText('请检查协议，现阶段不对多字节的开关量做处理！')

                        # 调试打印信息
                        message = ' '.join(f'{byte:02X}' for byte in self.package)
                        print(f'{key_char}: {message}')
                        # break 允许多个 lineEdit 绑定同一个按键

            # 遍历 analog_container 中所有的 LineEdit  检查按键与 lineEdit 内容相同
            for lineEdit in self.analog_container.findChildren(QLineEdit):
                if lineEdit.text().upper() == key_char:
                    byte_num = lineEdit.property('byte_num')
                    # 检查 button 没有被鼠标按下
                    button = self.analog_container.get_button_by_property(['byte_num', byte_num])
                    if not button.isDown():
                        # 获取 lineEdit 对应的属性对应的 timer
                        increaseTimer = self.analog_container.get_timer_by_property(['increase', byte_num])
                        decreaseTimer = self.analog_container.get_timer_by_property(['decrease', byte_num])
                        # 按键按下, 开启使 progressBar 增加的定时器
                        increaseTimer.start(6)
                        decreaseTimer.stop()

                        # 对应的 button disabled
                        button.setDisabled(True)
                        # 对用的 lineEdit 只读
                        lineEdit.setReadOnly(True)

    # 处理 开关量 和 模拟量 区域英文键盘松开的事件
    def keyReleaseEvent(self, event):
        '''
        当焦点在 lineedit 上时，松开 key 会自动触发 keyrelease 事件, 影响其他逻辑
        '''
        # 获取松开的键盘按键
        key_char = event.text().upper()
        # 文本框初始化
        # lineEdit = None

        # 手动松开 且 按键是字母
        if (self.switch_container is not None or self.analog_container is not None) and \
                not event.isAutoRepeat() and key_char.isalpha():
            # 遍历 switch_container 中所有的 LineEdit  检查按键与 lineEdit 内容相同
            for lineEdit in self.switch_container.findChildren(QLineEdit):
                # 如果焦点在任意一个 lineEdit 上不做处理
                if lineEdit.hasFocus():
                    return
            #  遍历 analog_container 中所有的 LineEdit  检查按键与 lineEdit 内容相同
            for lineEdit in self.analog_container.findChildren(QLineEdit):
                # 如果焦点在任意一个 lineEdit 上不做处理
                if lineEdit.hasFocus():
                    return

            # 确保所有的开关量 lineEdit 没有焦点
            for lineEdit in self.switch_container.findChildren(QLineEdit):
                # 按键与 lineEdit 内容相同
                if lineEdit.text().upper() == key_char:
                    byte_num = lineEdit.property('byte_num')
                    bit_index = lineEdit.property('bit_index')
                    # 检查 lineEdit 对应的 checkBox 是否被选中
                    checkBox = self.switch_container.get_checkBox_by_property(['byte_num', byte_num],
                                                                              ['bit_index', bit_index])
                    # 检查 button 是否被按下
                    button = self.switch_container.get_button_by_property(['byte_num', byte_num],
                                                                          ['bit_index', bit_index])
                    if not button.isEnabled() and not checkBox.isChecked():
                        # 校验和减去历史的字节量
                        self.switch_container.cumulative_sum -= self.switch_container.package[byte_num - 1]
                        # 开关量, 按键所在的位赋 0
                        if isinstance(bit_index, int):
                            # 1个 bit 代表一个开关
                            self.switch_container.package[byte_num - 1] &= ~(1 << bit_index)
                        else:
                            # 多个 bit 代表一个开关, 所有 bit 置 0
                            start_index, end_index = bit_index.split('-')
                            start_index, end_index = int(start_index), int(end_index)
                            for i in range(start_index, end_index + 1):
                                self.switch_container.package[byte_num - 1] &= ~(1 << i)
                        # 校验和更新新的字节量
                        self.switch_container.cumulative_sum += self.switch_container.package[byte_num - 1]

                        # 对应的 button enabled
                        button.setEnabled(True)
                        # 对应的 lineEdit 可写
                        lineEdit.setReadOnly(False)

                        # 调试打印信息
                        message = ' '.join(f'{byte:02X}' for byte in self.package)
                        print(f'{key_char}: {message}')
                        # break 允许多个 lineEdit 绑定同一个按键


            # 确保所有的模拟量 lineEdit 没有焦点
            for lineEdit in self.analog_container.findChildren(QLineEdit):
                # 按键与 lineEdit 内容相同
                if lineEdit.text().upper() == key_char:
                    byte_num = lineEdit.property('byte_num')
                    # 检查按钮是 Disable 且不是鼠标按下(鼠标优先级高)
                    button = self.analog_container.get_button_by_property(['byte_num', byte_num])
                    if not button.isDown() and not button.isEnabled():
                        # 获取 lineEdit 对应的属性对应的 timer
                        increaseTimer = self.analog_container.get_timer_by_property(['increase', byte_num])
                        decreaseTimer = self.analog_container.get_timer_by_property(['decrease', byte_num])
                        # 按键松开, 开启使 progressBar 减少的定时器
                        increaseTimer.stop()
                        decreaseTimer.start(6)

                        # 对应的 button disabled
                        button.setEnabled(True)
                        # 对应的 lineEdit 可写
                        lineEdit.setReadOnly(False)


    def update_byte_num_placeholderText(self):
        ''' 获取当前宽度并计算需要的字节数 '''
        width = self.ui.raw_message_textEdit.width()    # 当前控件的宽度
        font_metrics = self.ui.raw_message_textEdit.fontMetrics()   # 当前字体的宽度
        char_width = font_metrics.horizontalAdvance('0')    # 计算一个字符的宽度
        num_pairs = max(1, width // (char_width * 4))  # 计算当前宽度适合的 "01  " 数量

        # 更新到 textEdit 上
        byte_num = '  '.join(f'{i:02d}' for i in range(1, num_pairs + 1))
        self.ui.raw_message_textEdit.setText(byte_num)


    def resizeEvent(self, event):
        ''' 当窗口大小变化时, 更新 raw_message_textEdit 的 placeholderText '''
        self.update_byte_num_placeholderText()
        super().resizeEvent(event)


    def mousePressEvent(self, event):
        ''' 鼠标点击空白区域清除所有控件的焦点 '''
        self.setFocus()
        super().mousePressEvent(event)  # 调用父类的鼠标点击事件处理

    def closeEvent(self, event):
        ''' 主程序关闭时, 保存 协议头 target IP/port 、local port '''
        settings = QSettings('ou_simulator', 'configure')
        settings.setValue('protocol_header_content', self.ui.protocol_header_lineEdit.text())
        settings.setValue('target_ip_content', self.ui.target_ip_lineEdit.text())
        settings.setValue('target_port_content', self.ui.target_port_lineEdit.text())
        settings.setValue('local_port_content', self.ui.local_port_lineEdit.text())
        super().closeEvent(event)



if __name__ == '__main__':
    app = QApplication(sys.argv)    # 创建应用程序对象
    window  = MainWindow()  # 创建主窗口
    window.show()   # 显示主窗口
    sys.exit(app.exec_())
