import sys
from threading import Timer

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QTextEdit
from PyQt5.QtCore import QTimer, Qt
from ui import Ui_Window

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()  #初始化父类
        self.ui = Ui_Window()   # 创建 UI 类的实例
        self.ui.setupUi(self)   # 将 UI 布局加载到 MainWindow 上

        # 创建检测按钮长按的定时器
        self.detctLongPress = QTimer()
        self.detctLongPress.setInterval(300)    # 按键300ms视为按键被长按
        self.detctLongPress.timeout.connect(self.on_long_press)

        # 创建按钮长按状态的定时器
        self.longPressTimer = QTimer()
        self.longPressTimer.setInterval(100)    # 触发周期是100ms
        self.longPressTimer.timeout.connect(self.start_long_press)

        # 绑定按钮点击事件到自定义的 slot 函数
        self.ui.connect_pushButton.clicked.connect(self.print_text)
        self.ui.openFile_pushButton.clicked.connect(self.open_file_dialog)
        # 绑定按钮按下的事件
        self.ui.e_stop_button.clicked.connect(self.button_click)   # 鼠标按下抬起为一次 clicked
        self.ui.e_stop_button.pressed.connect(self.start_detctLongPressTimer)  # 绑定长按检测
        self.ui.e_stop_button.released.connect(self.stop_detctLongPressTimer)   # 停止长按检测
        self.ui.e_stop_button.released.connect(self.stop_long_press)           # 停止长按

        # 绑定复选框状态变化到 slot 函数
        self.ui.e_stop_lock_checkbox.stateChanged.connect(self.on_checkbox_changed)
    
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

    # keyPressEvent 方法
    def keyPressEvent(self, event):
        # 获取文本框中的内容
        expected_text = self.ui.e_stop_lineEdit.text()

        # 判断是否按下的键与文本框内容匹配
        if event.text() == expected_text.lower() or event.text() == expected_text.upper():
            print(f'检测到{expected_text}按键按下')
        else:
            print(f'不是{expected_text}键位')

    def button_click(self):
        print('急停触发')


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

    def on_checkbox_changed(self, state):
        if state == 2:  # 表示勾选状态
            print('复选框被勾选')
            self.on_long_press()
            self.ui.e_stop_button.setDisabled(True)
        if state == 0:  # 表示空选状态
            print('复选框没有勾选')
            self.stop_long_press()
            self.ui.e_stop_button.setEnabled(True)

    def mousePressEvent(self, event):
        # 当点击其他地方时, 取消文本框的焦点
        if not self.ui.e_stop_lineEdit.geometry().contains(event.pos()):
            self.ui.e_stop_lineEdit.clearFocus()
        super().mousePressEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)    # 创建应用程序对象
    window  = MainWindow()  # 创建主窗口
    window.show()   # 显示主窗口
    sys.exit(app.exec_())
