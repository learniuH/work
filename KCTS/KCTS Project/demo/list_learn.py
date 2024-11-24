from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, Qt
import sys
from test import UDPReceiver  # 假设上面的代码在 udp_receiver.py 文件中


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化 UI
        self.setWindowTitle("UDP Signal Demo")
        self.resize(400, 200)

        self.label = QLabel("状态未触发")
        self.label.setStyleSheet("background-color: lightgray; border: 1px solid black;")
        self.label.setAlignment(Qt.AlignCenter)

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 初始化 UDP 接收器
        self.udp_receiver = UDPReceiver("192.168.124.15", 8888)

        # 使用线程启动 UDP 接收器
        self.thread = QThread()
        self.udp_receiver.moveToThread(self.thread)
        self.thread.started.connect(self.udp_receiver.start_receiving)

        # 绑定信号与槽函数
        self.udp_receiver.update_label_signal.connect(self.update_label)

        # 启动线程
        self.thread.start()

    def update_label(self, triggered: bool):
        """更新 QLabel 状态"""
        if triggered:
            self.label.setText("状态触发")
            self.label.setStyleSheet("background-color: yellow; border: 1px solid black;")
        else:
            self.label.setText("状态未触发")
            self.label.setStyleSheet("background-color: lightgray; border: 1px solid black;")

    def closeEvent(self, event):
        """窗口关闭时清理线程"""
        self.udp_receiver.stop_receiving()
        self.thread.quit()
        self.thread.wait()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
