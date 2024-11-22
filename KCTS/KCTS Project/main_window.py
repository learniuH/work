from itertools import cycle

from PyQt5.QtCore import QSize, Qt, QSettings
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QListWidgetItem

from UI.main_window_ui import Ui_KCTS


from config.validators import Validators
from config.constants import NavigationBarItems, SendCycle
from services.network import NetworkManager

import sys
import socket

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_window_ui = Ui_KCTS()     # 主界面的 UI 实例
        self.main_window_ui.setupUi(self)   # 将 UI 加载到 MainWindow 上

        self.load_last_content()  # 加载上一次运行时的配置

        self.network_manager = NetworkManager()     # 初始化网络管理器

        self.main_window_init()     # 窗口界面初始化



        self.setup_validators()     # 正则表达式匹配 IP 端口 信息
        self.setup_connections()    # 信号连接绑定

    def load_last_content(self):
        ''' 加载上一次程序运行时的相关配置 '''
        settings = QSettings('KCTS', 'CONFIGURE')
        self.main_window_ui.kc_ts_recv_tu_port_lineEdit.setText(settings.value('KCTS_recv_tu_port_content', ''))
        self.main_window_ui.kc_ts_send_tu_port_lineEdit.setText(settings.value('KCTS_send_tu_port_content', ''))
        self.main_window_ui.kc_ts_recv_ou_port_lineEdit.setText(settings.value('KCTS_recv_ou_port_content', ''))
        self.main_window_ui.kc_ts_send_mu_port_lineEdit.setText(settings.value('KCTS_send_mu_port_content', ''))
        self.main_window_ui.mu_ip_lineEdit.setText(settings.value('MU_IP_content', ''))
        self.main_window_ui.mu_recv_port_lineEdit.setText(settings.value('MU_recv_port_content', ''))
        self.main_window_ui.kc_tu_ip_lineEdit.setText(settings.value('KCTU_IP_content', ''))
        self.main_window_ui.kc_tu_recv_port_lineEdit.setText(settings.value('KCTU_recv_port_content', ''))

    def setup_validators(self):
        ''' 设置输入验证器 '''
        self.main_window_ui.kc_ts_ip_lineEdit.setValidator(Validators.get_ipv4_validator())             # KCTS IP 验证器
        self.main_window_ui.kc_ts_recv_tu_port_lineEdit.setValidator(Validators.get_port_validator())   # KCTS 接收端口验证器
        self.main_window_ui.kc_ts_send_tu_port_lineEdit.setValidator(Validators.get_port_validator())   # KCTS 发送端口验证器
        self.main_window_ui.kc_ts_recv_ou_port_lineEdit.setValidator(Validators.get_port_validator())   # KCTS 接收端口验证器
        self.main_window_ui.kc_ts_send_mu_port_lineEdit.setValidator(Validators.get_port_validator())   # KCTS 发送端口验证器
        self.main_window_ui.mu_ip_lineEdit.setValidator(Validators.get_ipv4_validator())            # MU IP 验证器
        self.main_window_ui.mu_recv_port_lineEdit.setValidator(Validators.get_port_validator())     # MU 接收端口验证器
        self.main_window_ui.kc_tu_ip_lineEdit.setValidator(Validators.get_ipv4_validator())         # KCTU IP 验证器
        self.main_window_ui.kc_tu_recv_port_lineEdit.setValidator(Validators.get_port_validator())  # KCTU 接收端口验证器

    def setup_connections(self):
        ''' 设置信号连接 '''
        self.main_window_ui.apply_pushButton.clicked.connect(self.apply_current_configuration)
        self.main_window_ui.IOQuery_pushButton.clicked.connect(lambda: self.switch_ou_analysis_send_stacked_page(index=0))
        self.main_window_ui.send_package_pushButton.clicked.connect(lambda: self.switch_ou_analysis_send_stacked_page(index=1))

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

        # 主程序启动时, 启动监听OU数据的线程
        self.listening_ou_thread_init()
        self.listening_tu_thread_init()

    def listening_ou_thread_init(self):
        # 启动监听OU数据的线程
        current_configuration = self.update_current_configuration()
        self.network_manager.start_receiving_ou(current_configuration['local_ip'],
                                                current_configuration['recv_ou_port'],
                                                current_configuration['mu_ip'],
                                                current_configuration['mu_recv_port']
                                                )

    def listening_tu_thread_init(self):
        current_configuration = self.update_current_configuration()
        # 启动监听TU数据的线程
        self.network_manager.start_receiving_tu(current_configuration['local_ip'],
                                                current_configuration['recv_tu_port']
                                                )

    def update_current_configuration(self):
        ''' 获取当前设备状态页文本框的内容 '''
        # 更新当前电脑的 IP
        local_ip = socket.gethostbyname(socket.gethostname())
        self.main_window_ui.kc_ts_ip_lineEdit.setText(local_ip)

        # 获取当前文本框中的配置
        recv_tu_port = self.main_window_ui.kc_ts_recv_tu_port_lineEdit.text()
        send_tu_port = self.main_window_ui.kc_ts_send_tu_port_lineEdit.text()
        recv_ou_port = self.main_window_ui.kc_ts_recv_ou_port_lineEdit.text()
        send_mu_port = self.main_window_ui.kc_ts_send_mu_port_lineEdit.text()

        mu_ip = self.main_window_ui.mu_ip_lineEdit.text()
        mu_recv_port = self.main_window_ui.mu_recv_port_lineEdit.text()

        kctu_ip = self.main_window_ui.kc_tu_ip_lineEdit.text()
        kctu_recv_port = self.main_window_ui.kc_tu_recv_port_lineEdit.text()

        current_configuration = {
            'local_ip': local_ip,
            'recv_tu_port': recv_tu_port,
            'send_tu_port': send_tu_port,
            'recv_ou_port': recv_ou_port,
            'send_mu_port': send_mu_port,
            'mu_ip': mu_ip,
            'mu_recv_port': mu_recv_port,
            'kctu_ip': kctu_ip,
            'kctu_recv_port': kctu_recv_port
        }
        return current_configuration




    def switch_sub_interface_stacked_page(self, index: int):
        ''' listWidget 的 item 切换 stackedWidget 的子界面 '''
        self.main_window_ui.sub_interface_stacked.setCurrentIndex(index)

        # 切换到输出查询界面, index == 2(输出查询页面)时, 往TU一直发包采集MU状态
        if index == 2:
            self.sending_tu_thread_init()   # 开始往TU发包

            # 同时在模拟发包界面, 开启往MU发包线程
            if self.main_window_ui.ou_analysis_send_stacked.currentIndex() == 1:
                self.sending_mu_thread_init()

        # 切换到非输出查询界面, 关闭给TU发送数据的线程
        else:
            self.network_manager.stop_sending_tu()
            # 如果同时在主动给MU发包, 就关闭给MU发数据的线程
            if self.network_manager.is_sending_mu:
                self.network_manager.stop_sending_mu()


    def apply_current_configuration(self):
        ''' 点击应用, 停止所有收发的线程, 更新配置后重新启用 '''
        self.network_manager.stop_receiving_ou()
        self.network_manager.stop_receiving_tu()

        # 启动两个监听的线程
        self.listening_ou_thread_init()
        self.listening_tu_thread_init()

    def sending_tu_thread_init(self):
        ''' 初始化给TU发送数据的线程 '''
        current_configuration = self.update_current_configuration()
        self.network_manager.start_sending_tu(current_configuration['local_ip'],
                                              current_configuration['send_tu_port'],
                                              current_configuration['kctu_ip'],
                                              current_configuration['kctu_recv_port'],
                                              SendCycle.CYCLE
                                              )

    def sending_mu_thread_init(self):
        ''' 初始化给MU发送数据的线程 '''
        current_configuration = self.update_current_configuration()
        self.network_manager.start_sending_mu(current_configuration['local_ip'],
                                              current_configuration['send_mu_port'],
                                              current_configuration['mu_ip'],
                                              current_configuration['mu_recv_port'],
                                              bytearray(56),
                                              SendCycle.CYCLE
                                              )

    def switch_ou_analysis_send_stacked_page(self, index):
        ''' 点击 pushButton 切换 ou 解析界面和发包界面 '''
        self.main_window_ui.ou_analysis_send_stacked.setCurrentIndex(index)

        # OU 解析界面, IO查询禁用, 模拟发包使能, 关闭往MU发包的线程, 启动接收OU数据线程
        if index == 0:
            self.network_manager.stop_sending_mu()
            self.listening_ou_thread_init()
            self.main_window_ui.IOQuery_pushButton.setDisabled(True)
            self.main_window_ui.send_package_pushButton.setEnabled(True)
        # 模拟发包界面, IO查询使能, 模拟发包禁用, 关闭接收OU数据的线程, 启动往MU发包线程
        elif index == 1 and not self.network_manager.is_sending_mu:
            self.network_manager.stop_receiving_ou()
            self.sending_mu_thread_init()
            self.main_window_ui.IOQuery_pushButton.setEnabled(True)
            self.main_window_ui.send_package_pushButton.setDisabled(True)


    def mousePressEvent(self, event):
        ''' 鼠标点击空白区域清除所有控件的焦点 '''
        self.setFocus()
        super().mousePressEvent(event)  # 调用父类的鼠标点击事件处理

    def closeEvent(self, event):
        ''' 主程序关闭时, 保存配置页面的所有配置 '''
        settings = QSettings('KCTS', 'CONFIGURE')
        settings.setValue('KCTS_recv_tu_port_content', self.main_window_ui.kc_ts_recv_tu_port_lineEdit.text())
        settings.setValue('KCTS_send_tu_port_content', self.main_window_ui.kc_ts_send_tu_port_lineEdit.text())
        settings.setValue('KCTS_recv_ou_port_content', self.main_window_ui.kc_ts_recv_ou_port_lineEdit.text())
        settings.setValue('KCTS_send_mu_port_content', self.main_window_ui.kc_ts_send_mu_port_lineEdit.text())
        settings.setValue('MU_IP_content', self.main_window_ui.mu_ip_lineEdit.text())
        settings.setValue('MU_recv_port_content', self.main_window_ui.mu_recv_port_lineEdit.text())
        settings.setValue('KCTU_IP_content', self.main_window_ui.kc_tu_ip_lineEdit.text())
        settings.setValue('KCTU_recv_port_content', self.main_window_ui.kc_tu_recv_port_lineEdit.text())
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())