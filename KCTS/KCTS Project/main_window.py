from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QListWidgetItem


from UI.main_window_ui import Ui_KCTS

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_window_ui = Ui_KCTS()     # 主界面的 UI 实例
        self.main_window_ui.setupUi(self)   # 将 UI 加载到 MainWindow 上
        self.navigation_bar = ['设备状态', 'MU功能测试', 'MU输出查询', '配置管理']
        self.main_window_init()

    def main_window_init(self):
        ''' list 和 stacked 配置 '''
        # 导航栏初始化
        for index, page in enumerate(self.navigation_bar):
            item = QListWidgetItem(page)
            item.setSizeHint(QSize(180, 40))    # 设置项目高度
            item.setTextAlignment(Qt.AlignCenter)   # 文字居中
            self.main_window_ui.navigation_list.addItem(item)

        # 通过 QlistWidget 当前的 item 变化来切换 QStackedWidget 中的序号
        self.main_window_ui.navigation_list.currentRowChanged.connect(self.switch_page)

        # 解析界面的 pushButton 按下后切换 QStackedWidget 的界面
        self.main_window_ui.real_time_analysis_pushButton.clicked.connect(lambda:self.on_analysis_page_button_clicked(index=0))
        self.main_window_ui.history_pushButton.clicked.connect(lambda:self.on_analysis_page_button_clicked(index=1))

    def switch_page(self, index):
        ''' listWidget 的 item 切换 stackedWidget 的子界面 '''
        self.main_window_ui.sub_interface_stacked.setCurrentIndex(index)

    def on_analysis_page_button_clicked(self, index):
        ''' 点击 pushButton 切换 stackedWidget 的子界面 '''
        self.main_window_ui.analysis_stackedWidget.setCurrentIndex(index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())