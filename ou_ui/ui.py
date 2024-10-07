import random
from tkinter import *
from tkinter.ttk import *
class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_tabs_switch = self.__tk_tabs_switch(self)
        self.tk_label_frame_raw_data = self.__tk_label_frame_raw_data( self.tk_tabs_switch_0)
        self.tk_text_raw_text = self.__tk_text_raw_text( self.tk_label_frame_raw_data) 
        self.tk_label_frame_analog = self.__tk_label_frame_analog( self.tk_tabs_switch_0)
        self.tk_table_bit = self.__tk_table_bit( self.tk_tabs_switch_0)
        self.tk_text_historical_data = self.__tk_text_historical_data( self.tk_tabs_switch_1)
        self.tk_label_IP = self.__tk_label_IP(self)
        self.tk_input_IP = self.__tk_input_IP(self)
        self.tk_label_Port = self.__tk_label_Port(self)
        self.tk_input_Port = self.__tk_input_Port(self)
        self.tk_button_connect = self.__tk_button_connect(self)
        self.tk_button_disconnect = self.__tk_button_disconnect(self)
    def __win(self):
        self.title("VisuaLizer")
        # 设置窗口大小、居中
        width = 1000
        height = 600
        self.geometry('%dx%d' %(width, height))
        
        self.resizable(width=False, height=False)
        
    def scrollbar_autohide(self,vbar, hbar, widget):
        """自动隐藏滚动条"""
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())
    
    def v_scrollbar(self,vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')
    def h_scrollbar(self,hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')
    def create_bar(self,master, widget,is_vbar,is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)
    def __tk_tabs_switch(self,parent):
        frame = Notebook(parent)
        self.tk_tabs_switch_0 = self.__tk_frame_switch_0(frame)
        frame.add(self.tk_tabs_switch_0, text="实时解析")
        self.tk_tabs_switch_1 = self.__tk_frame_switch_1(frame)
        frame.add(self.tk_tabs_switch_1, text="历史数据")
        frame.place(x=8, y=5, width=984, height=555)
        return frame
    def __tk_frame_switch_0(self,parent):
        frame = Frame(parent)
        frame.place(x=8, y=5, width=984, height=555)
        return frame
    def __tk_frame_switch_1(self,parent):
        frame = Frame(parent)
        frame.place(x=8, y=5, width=984, height=555)
        return frame
    def __tk_label_frame_raw_data(self,parent):
        frame = LabelFrame(parent,text="原始数据",)
        frame.place(x=5, y=5, width=969, height=70)
        return frame
    def __tk_text_raw_text(self,parent):
        text = Text(parent)
        text.place(x=5, y=0, width=954, height=45)
        return text
    def __tk_label_frame_analog(self,parent):
        frame = LabelFrame(parent,text="模拟量",)
        frame.place(x=5, y=327, width=970, height=195)
        return frame
    def __tk_table_bit(self,parent):
        # 表头字段 表头宽度
        columns = {"Byte":54,"bit7":114,"bit6":114,"bit5":114,"bit4":114,"bit3":114,"bit2":114,"bit1":114,"bit0":114}
        tk_table = Treeview(parent, show="headings", columns=list(columns),)
        for text, width in columns.items():  # 批量设置列属性
            tk_table.heading(text, text=text, anchor='center')
            tk_table.column(text, anchor='center', width=width, stretch=False)  # stretch 不自动拉伸
        
        tk_table.place(x=7, y=82, width=969, height=240)
        return tk_table
    def __tk_text_historical_data(self,parent):
        text = Text(parent)
        text.place(x=5, y=5, width=970, height=518)
        vbar = Scrollbar(text, command=text.yview)
        text.configure(yscrollcommand=vbar.set)
        vbar.pack(side=RIGHT, fill=Y)
        return text
    def __tk_label_IP(self,parent):
        label = Label(parent,text="IP: ",anchor="center", )
        label.place(x=31, y=565, width=30, height=30)
        return label
    def __tk_input_IP(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=59, y=568, width=150, height=26)
        return ipt
    def __tk_label_Port(self,parent):
        label = Label(parent,text="Port: ",anchor="center", )
        label.place(x=243, y=565, width=40, height=30)
        return label
    def __tk_input_Port(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=286, y=568, width=80, height=26)
        return ipt
    def __tk_button_connect(self,parent):
        btn = Button(parent, text="连接", takefocus=False,)
        btn.place(x=395, y=565, width=90, height=30)
        return btn
    def __tk_button_disconnect(self,parent):
        btn = Button(parent, text="断开", takefocus=False,)
        btn.place(x=525, y=565, width=90, height=30)
        return btn
class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)
    def __event_bind(self):
        self.tk_button_connect.bind('<Button-1>',self.ctl.start_receiving)
        self.tk_button_disconnect.bind('<Button-1>',self.ctl.stop_receiving)
        pass
    def __style_config(self):
        # Colors for table rows and columns
        self.row_colors = ['#FFC0CB', '#ADD8E6']
        self.column_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE', '#F1948A', '#AED6F1']

        # Configure table styles
        style = Style()
        style.configure("Treeview", font=('微软雅黑', 10))
        style.configure("Treeview.Heading", font=('monospace', 11, 'bold'))

        # Configure tags for alternating row colors
        self.tk_table_bit.tag_configure('even', background=self.row_colors[0])
        self.tk_table_bit.tag_configure('odd', background=self.row_colors[1])

        # Apply column colors
        for i, column in enumerate(self.tk_table_bit["columns"]):
            self.tk_table_bit.tag_configure(f'column_{i}', background=self.column_colors[i % len(self.column_colors)])

        # 按钮风格
        style.configure('TButton', font=('楷体', 15, 'bold'))
        self.tk_button_connect.configure(style='TButton')
        self.tk_button_disconnect.configure(style='TButton')

        # Other existing configurations
        self.tk_text_raw_text.config(font=('Consolas', 12))
        self.tk_text_historical_data.config(font=('Consolas', 10))
        self.tk_label_IP.config(font=('monospace', 10, 'bold'))
        self.tk_label_Port.config(font=('monospace', 10, 'bold'))

    def insert_sample_data(self):
        # Clear existing data
        for item in self.tk_table_bit.get_children():
            self.tk_table_bit.delete(item)

        # Insert new sample data
        for i in range(10):  # Insert 10 rows of sample data
            values = [f"Byte{i}"] + [random.choice(["0", "1"]) for _ in range(8)]
            item = self.tk_table_bit.insert("", "end", values=values, tags=(f'row_{i%2}',))
            for j, value in enumerate(values):
                self.tk_table_bit.item(item, tags=(f'row_{i%2}', f'column_{j}'))



if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()