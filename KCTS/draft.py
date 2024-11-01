import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from ui import Ui_Window

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()  #初始化父类
        self.ui = Ui_Window()   # 创建 UI 类的实例
        self.ui.setupUi(self)   # 将 UI 布局加载到 MainWindow 上

        #绑定按钮点击事件到自定义的 slot 函数
        self.ui.connect_pushButton.clicked.connect(self.print_text)
        self.ui.openFile_pushButton.clicked.connect(self.open_file_dialog)
    
    def print_text(self):
        ''' 获取文本框的内容 '''
        ip = self.ui.ip_editText.toPlainText()
        port = self.ui.port_editText.toPlainText()

        print((ip, port))
    
    def open_file_dialog(self):
        ''' 打开文件选择对话框, 只显示 Excel 文件 '''
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择文件', '', 'Excel Files (*.xlsx);;All Files (*)'
        )
        if file_path:
            self.read_excel_content(file_path)
    
    def read_excel_content(self):
        pass
    


if __name__ == '__main__':
    app = QApplication(sys.argv)    # 创建应用程序对象
    window  = MainWindow()  # 创建主窗口
    window.show()   # 显示主窗口
    sys.exit(app.exec_())
