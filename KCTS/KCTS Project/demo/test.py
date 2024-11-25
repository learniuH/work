from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import sys

class PacketParserWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Packet Parser")
        self.resize(800, 600)

        # 创建表格
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(9)  # 8列（Bit7-Bit0） + 1列（Byte Index）
        self.table_widget.setHorizontalHeaderLabels(
            ["Byte Index", "Bit7", "Bit6", "Bit5", "Bit4", "Bit3", "Bit2", "Bit1", "Bit0"]
        )

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

        # 模拟解析结果
        self.parsed_bytes = []  # 存储已解析的字节数据
        self.parse_packet([0b10101010, 0b11001100, 0b11110000])

    def parse_packet(self, byte_array):
        """
        解析报文，并更新表格内容
        :param byte_array: list of bytes
        """
        for byte_index, byte in enumerate(byte_array, start=len(self.parsed_bytes)):
            # 添加一行数据
            self.table_widget.insertRow(byte_index)
            self.parsed_bytes.append(byte)

            # 显示字节序号
            self.table_widget.setItem(byte_index, 0, QTableWidgetItem(str(byte_index)))

            # 按位解析并显示
            for bit_index in range(8):
                bit_value = (byte >> (7 - bit_index)) & 1  # 提取对应位
                self.table_widget.setItem(byte_index, bit_index + 1, QTableWidgetItem(str(bit_value)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = PacketParserWidget()
    widget.show()
    sys.exit(app.exec_())
