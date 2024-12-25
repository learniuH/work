class ConstantText:
    ''' 自定义控件的文本 '''
    BLANK_TEXT = ''                 # checkBox 空白文本
    LINEEDIT_TEXT = 'Key'           # lineEdit 'Key'
    SPACER_WIDTH = 20               # OU模拟器每列之间的弹簧宽度
    WIDGET_PER_COL = 13             # OU模拟器每列13个控件
    TIMER_PERIOD = 6                # OU模拟器模拟量定时器的周期
    SERIAL_ASST_PAGE = 0            # 串口助手 stackedWidget 索引
    ASHING_CONFIG_PAGE = 1               # 串口助手 泽耀Lora 配置界面索引
    EBYTE_CONFIG_PAGE = 2                # 串口助手 亿佰特Lora 配置界面索引

    @staticmethod
    def value_range(byte_num: str) -> list:
        ''' 提取多字节模拟量的字节序号
        Args:
            byte_num: 字节序号, '15-16'

        Return:
            起始字节序号 终止字节序号 组成的列表
        '''
        return [int(byte) for byte in byte_num.split('-')]

# if __name__ == '__main__':
#     print(ConstantText.value_range('15-16'))
