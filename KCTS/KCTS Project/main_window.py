from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QListWidgetItem


from UI.main_window_ui import Ui_KCTS
from UI.page1 import Ui_Form as page1
from UI.page2 import Ui_Form as page2

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_window_ui = Ui_KCTS()     # 主界面的 UI 实例
        self.main_window_ui.setupUi(self)   # 将 UI 加载到 MainWindow 上
        self.navigation_bar = ['界面1', '界面2', '界面3', '界面4']
        self.main_window_init()

    def main_window_init(self):
        ''' list 和 stacked 配置 '''
        # 通过 QlistWidget 当前的 item 变化来切换 QStackedWidget 中的序号
        self.main_window_ui.navigation_list.currentRowChanged.connect(
            self.main_window_ui.sub_interface_stacked.setCurrentIndex)
        # 导航栏初始化
        for index, page in enumerate(self.navigation_bar):
            item = QListWidgetItem(page)
            item.setSizeHint(QSize(180, 40))    # 设置项目高度
            item.setTextAlignment(Qt.AlignCenter)   # 文字居中
            self.main_window_ui.navigation_list.addItem(item)

        for index, page in enumerate(self.navigation_bar):
            # 实例化各个子界面
            pageone = page1()
            pageone.setupUi(self.main_window_ui.sub_interface_stacked)   # 将界面1加载到stacked上
            self.main_window_ui.sub_interface_stacked.addWidget(pageone)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())