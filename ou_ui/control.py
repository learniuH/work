import socket
import threading
from tkinter import *
from tkinter.ttk import *
from ui import Win
from ou_udp_protocol import OU_PROTOCOLS
from ou_udp_parse import parse_ou_message

class Controller:
    ui: Win
    def __init__(self):
        self.sock = None
        self.receiving = False
        self.receive_thread = None

    def init(self, ui):
        self.ui = ui
        self.ui.tk_button_disconnect.configure(state='disabled')

    def start_receiving(self, evt):
        ip = '192.168.2.5'
        port = 8004
        # ip = self.ui.tk_input_IP.get()
        # port = int(self.ui.tk_input_Port.get())

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((ip, port))
        except Exception as e:
            print("Error", f"无法绑定到 {ip}:{port}: {str(e)}")
            return

        self.receiving = True
        self.receive_thread = threading.Thread(target=self.receive_data)
        self.receive_thread.start()

        self.ui.tk_button_connect.configure(state='disabled')
        self.ui.tk_button_disconnect.configure(state='normal')

    def stop_receiving(self, evt):
        self.receiving = False
        if self.sock:
            self.sock.close()
        if self.receive_thread:
            self.receive_thread.join()

        self.ui.tk_button_connect.configure(state='normal')
        self.ui.tk_button_disconnect.configure(state='disabled')

    def receive_data(self):
        previous_data_field = None
        while self.receiving:
            try:
                data, addr = self.sock.recvfrom(1024)
                current_data_field = data[23: 51]
                if current_data_field != previous_data_field:
                    self.process_data(data)
                    previous_data_field = current_data_field
            except socket.error:
                break

    def process_data(self, data):
        # 显示原始数据
        raw_text = self.ui.tk_text_raw_text
        raw_text.delete('1.0', END)
        hex_data = ' '.join(f'{byte:02X}' for byte in data)
        raw_text.insert(END, hex_data)
        
        # 清空表格
        for item in self.ui.tk_table_bit.get_children():
            self.ui.tk_table_bit.delete(item)

        # 解析数据并填充表格
        analog_data = {}
        for byte_num in OU_PROTOCOLS:
            row_data = [''] * 9

            parsed_data_bit, parsed_data_byte = parse_ou_message(byte_num, data)
            if parsed_data_bit:
                for bit_position, function in parsed_data_bit[byte_num].items():
                    row_data[0] = f'Byte{byte_num}'
                    row_data[8 - bit_position] = function
                self.ui.tk_table_bit.insert('', 'end', values=row_data)
            if parsed_data_byte:
                if analog_data == {}:
                    analog_data = parsed_data_byte[byte_num]
                else:
                    analog_data.update(parsed_data_byte[byte_num])

        # 更新模拟量区域
        analog_frame = self.ui.tk_label_frame_analog
        for widget in analog_frame.winfo_children():
            widget.destroy()

        for i, (name, value) in enumerate(analog_data.items()):
            label = Label(analog_frame, text=f"{name}: {value}")
            label.grid(row=1, column=i, sticky='w', padx=5, pady=2)

            progressbar = Progressbar(analog_frame, length=140, orient=VERTICAL)
            progressbar['value'] = value
            progressbar.grid(row=0, column=i, padx=5, pady=2)

        # 更新历史数据
        history_text = self.ui.tk_text_historical_data
        history_text.insert('end', f"Raw Data: {hex_data}\n")
        for byte_num in OU_PROTOCOLS:
            parsed_data_bit, parsed_data_byte = parse_ou_message(byte_num, data)
            if parsed_data_bit:
                history_text.insert('end', f"Byte{byte_num}: ")
                for bit_index in parsed_data_bit[byte_num]:
                    history_text.insert('end', f"bit{bit_index}: {parsed_data_bit[byte_num][bit_index]}\t")
                history_text.insert('end', "\n")
            if parsed_data_byte:
                for function, byte_value in parsed_data_byte[byte_num].items():
                    history_text.insert('end', f"Byte{byte_num}: {function}:{byte_value}\n")
        history_text.insert('end', "\n")
        history_text.see('end')
