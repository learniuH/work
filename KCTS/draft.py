import sys
import socket
import threading
import time

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLineEdit
from PyQt5.QtCore import QTimer

from ui import Ui_Window
from updateWidget import Switch, Analog

class MainWindow(QWidget):
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

        # Target Port 和 Local Port 和 周期 只能输入数字 且范围最多5位数
        self.ui.target_port_lineEdit.setValidator(QIntValidator(1, 65535))
        self.ui.local_port_lineEdit.setValidator(QIntValidator(1, 65535))
        self.ui.sending_cycle_lineEdit.setValidator(QIntValidator(1, 65535))



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




    def connect_button_clicked(self):
        ''' 启动发送数据的线程 '''
        if not self.send_message:
            self.send_message = True
            self.ui.connect_pushButton.setText('点击断开')

            # 启动数据发送线程, 主程序退出自动关闭
            self.send_thread = threading.Thread(target=self.sending_message, daemon=True)
            self.send_thread.start()


        else:
            self.send_message = False
            self.ui.connect_pushButton.setText('点击连接')


    def sending_message(self):
        ip = self.ui.target_ip_lineEdit.text()
        port = self.ui.target_port_lineEdit.text()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            try:
                local_port = self.ui.local_port_lineEdit.text()
                local_address = (self.local_ip, local_port)

                sock.bind((local_address[0], int(local_address[1])))
            except ValueError as e:
                # 错误信息打印
                self.ui.local_port_lineEdit.setPlaceholderText('错误： 请绑定本地端口！')
            except OSError as e:
                self.ui.tips_lineEdit.setText('错误： 端口已被占用！')
            message = self.package
            while self.send_message:
                sock.sendto(message, (ip, int(port)))
                time.sleep(int(self.ui.sending_cycle_lineEdit.text()) / 1000)   # 周期 ms



    def open_file_dialog(self):
        ''' 打开文件选择对话框, 只显示 Excel 文件 '''
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择文件', '', 'Excel Files (*.xlsx);;All Files (*)'
        )
        if file_path:
            pass



    def clear_prompt_info(self):
        self.ui.tips_lineEdit.clear()


    def updateSwitchs(self):
        try:
            count = int(self.ui.num_lineEdit.text())
        except ValueError:
            return  # 如果不是正数, 则不做任何操作

        # 如果之前有按键容器, 删除它
        if self.switch_container:
            self.ui.switch_container_layout.removeWidget(self.switch_container)
            self.switch_container.deleteLater()
            self.switch_container = None

        # 创建新的按键并添加到界面
        self.switch_container = Switch(self.ou_protocol, self.package)
        self.ui.switch_container_layout.addWidget(self.switch_container)

    def updateAnalog(self):
        try:
            count = int(self.ui.num_lineEdit.text())
        except ValueError:
            return  # 如果不是正数, 则不做任何操作

        # 如果之前有按键容器, 删除它
        if self.analog_container:
            self.ui.analog_container_layout.removeWidget(self.switch_container)
            self.analog_container.deleteLater()
            self.analog_container = None

        # 创建新的按键并添加到界面
        self.analog_container = Analog(self.ou_protocol, self.package)
        self.ui.analog_container_layout.addWidget(self.analog_container)




    # 重写键盘按下事件
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
                        # 开关量, 按键所在的位赋 1
                        self.switch_container.package[byte_num - 1] |= (1 << bit_index)
                        # 对应的 button disabled
                        button.setDisabled(True)

                        # 调试打印信息
                        message = ' '.join(f'{byte:02X}' for byte in self.switch_container.package)
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

    # 重写键盘松开事件
    def keyReleaseEvent(self, event):
        '''
        当焦点在 lineedit 上时，松开 key 会自动触发 keyrelease 事件, 影响其他逻辑
        '''
        # 获取松开的键盘按键
        key_char = event.text().upper()
        # 文本框初始化
        lineEdit = None

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
                        # 开关量, 按键所在的位赋 0
                        self.switch_container.package[byte_num - 1] &= ~(1 << bit_index)
                        # 对应的 button disabled
                        button.setEnabled(True)

                        # 调试打印信息
                        message = ' '.join(f'{byte:02X}' for byte in self.switch_container.package)
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

    def mousePressEvent(self, event):
        # 清除所有控件的焦点
        self.setFocus()
        super().mousePressEvent(event)  # 调用父类的鼠标点击事件处理


if __name__ == '__main__':
    app = QApplication(sys.argv)    # 创建应用程序对象
    window  = MainWindow()  # 创建主窗口
    window.show()   # 显示主窗口
    sys.exit(app.exec_())
