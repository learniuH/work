from itertools import cycle

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QListWidgetItem


from UI.main_window_ui import Ui_KCTS


from config.validators import Validators
from config.constants import NavigationBarItems
from services.network import NetworkManager

import sys
import socket

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_window_ui = Ui_KCTS()     # 主界面的 UI 实例
        self.main_window_ui.setupUi(self)   # 将 UI 加载到 MainWindow 上

        self.network_manager = NetworkManager()     # 初始化网络管理器

        self.main_window_init()     # 窗口界面初始化

        self.setup_validators()     # 正则表达式匹配 IP 端口 信息
        self.setup_connections()    # 信号连接绑定


    def main_window_init(self):
        ''' listWdiget items 创建, 获取电脑IP   '''
        # 导航栏初始化
        navigation_bar = NavigationBarItems.LIST    # listWidget items
        for index, page in enumerate(navigation_bar):
            item = QListWidgetItem(page)
            item.setSizeHint(QSize(180, 40))    # 设置项目高度
            item.setTextAlignment(Qt.AlignCenter)   # 文字居中
            self.main_window_ui.navigation_list.addItem(item)

        # 通过 QlistWidget 当前的 item 变化来切换 QStackedWidget 中的序号
        self.main_window_ui.navigation_list.currentRowChanged.connect(self.switch_sub_interface_stacked_page)

        # 主程序启动时, 更新此时电脑的 IP 地址
        self.update_current_ip()

    def update_current_ip(self):
        local_ip = socket.gethostbyname(socket.gethostname())
        self.main_window_ui.kc_ts_ip_lineEdit.setText(local_ip)
        return local_ip

    def switch_sub_interface_stacked_page(self, index: int):
        ''' listWidget 的 item 切换 stackedWidget 的子界面 '''
        self.main_window_ui.sub_interface_stacked.setCurrentIndex(index)
        # 切换到 MU输出查询界面时, 启动监听线程
        if index == 2:
            local_ip = self.update_current_ip()
            recv_port = self.main_window_ui.kc_ts_recv_port_lineEdit.text()
            self.network_manager.start_receiving(local_ip, recv_port)
            # 与此同时在实时解析界面中的OU模拟器界面, 启动发送线程
            if self.main_window_ui.tabWidget.currentIndex() == 0 \
                    and self.main_window_ui.ou_analysis_send_stacked.currentIndex() == 1:
                local_ip = self.update_current_ip()
                send_port = self.main_window_ui.kc_ts_send_port_lineEdit.text()
                target_ip = self.main_window_ui.mu_ip_lineEdit.text()
                target_port = self.main_window_ui.mu_recv_port_lineEdit.text()
                package = bytearray(56)
                cycle_ms = 100
                self.network_manager.start_sending(local_ip, send_port, target_ip, target_port, package, cycle_ms)
                print('此时启动发送线程')
        # 切换到其他界面关闭监听和发送线程
        else:
            self.network_manager.stop_receiving()   # 关闭接收数据的线程



    def setup_validators(self):
        ''' 设置输入验证器 '''
        self.main_window_ui.kc_ts_ip_lineEdit.setValidator(Validators.get_ipv4_validator())         # KCTS IP 验证器
        self.main_window_ui.kc_ts_recv_port_lineEdit.setValidator(Validators.get_port_validator())  # KCTS 接收端口验证器
        self.main_window_ui.kc_ts_send_port_lineEdit.setValidator(Validators.get_port_validator())  # KCTS 发送端口验证器
        self.main_window_ui.mu_ip_lineEdit.setValidator(Validators.get_ipv4_validator())            # MU IP 验证器
        self.main_window_ui.mu_recv_port_lineEdit.setValidator(Validators.get_port_validator())     # MU 接收端口验证器
        self.main_window_ui.kc_tu_ip_lineEdit.setValidator(Validators.get_ipv4_validator())         # KCTU IP 验证器
        self.main_window_ui.kc_tu_recv_port_lineEdit.setValidator(Validators.get_port_validator())  # KCTU 接收端口验证器

    def setup_connections(self):
        ''' 设置信号连接 '''
        self.main_window_ui.IOQuery_pushButton.clicked.connect(lambda: self.switch_ou_analysis_send_stacked_page(index=0))
        self.main_window_ui.send_package_pushButton.clicked.connect(lambda: self.switch_ou_analysis_send_stacked_page(index=1))

    def switch_ou_analysis_send_stacked_page(self, index):
        ''' 点击 pushButton 切换 ou 解析界面和发包界面 '''
        self.main_window_ui.ou_analysis_send_stacked.setCurrentIndex(index)
        # OU 解析界面, IO查询禁用, 模拟发包使能, 关闭发送数据线程
        if index == 0:
            self.main_window_ui.IOQuery_pushButton.setDisabled(True)
            self.main_window_ui.send_package_pushButton.setEnabled(True)
            print('发送数据线程关闭')
        # 模拟发包界面, IO查询使能, 模拟发包禁用, 启动发送数据线程
        else:
            self.main_window_ui.IOQuery_pushButton.setEnabled(True)
            self.main_window_ui.send_package_pushButton.setDisabled(True)
            print('发送数据线程打开')

    def mousePressEvent(self, event):
        ''' 鼠标点击空白区域清除所有控件的焦点 '''
        self.setFocus()
        super().mousePressEvent(event)  # 调用父类的鼠标点击事件处理

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())