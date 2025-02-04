import serial

class SendCycle:
    CYCLE = 100                     # MU/TU/串口 发包周期

class ConstantText:
    ''' 自定义常量 '''
    BLANK_TEXT = ''                 # checkBox 空白文本
    LINEEDIT_TEXT = 'Key'           # lineEdit 'Key'
    SPACER_WIDTH = 20               # OU模拟器每列之间的弹簧宽度
    WIDGET_PER_COL = 13             # OU模拟器每列13个控件
    TIMER_PERIOD = 6                # OU模拟器模拟量定时器的周期
    ROWS_PER_PAGES = 15             # 自动化界面TableWidget每页最多15行
    COLUMNS_TO_INSERT = ["用例编号", "用例标题", "操作步骤", "预期结果"]        # 自动化界面通过Excel数据导入的列


    @staticmethod
    def value_range(byte_num: str) -> list:
        ''' 提取多字节模拟量的字节序号
        Args:
            byte_num: 字节序号, '15-16'

        Return:
            起始字节序号 终止字节序号 组成的列表
        '''
        return [int(byte) for byte in byte_num.split('-')]

class SerialAsstConstant:
    ''' 串口助手界面的配置项 '''
    SERIAL_ASST_PAGE    = 0         # 串口助手 stackedWidget 索引
    ASHING_CONFIG_PAGE  = 1         # 串口助手 泽耀Lora 配置界面索引
    EBYTE_CONFIG_PAGE   = 2         # 串口助手 亿佰特Lora 配置界面索引

    BAUD_RATE_9600_INDEX            = 6        # 波特率 9600 索引
    BYTE_SIZE_EIGHTBITS_INDEX       = 3        # 数据位 8 索引
    PARITY_NONE_INDEX               = 0        # 奇偶校验 无 索引
    STOPBITS_ONE_INDEX              = 0        # 停止位 1 索引
    STOPBITS_ONE_POINT_FIVE_INDEX   = 1        # 停止位 1.5 索引

    EBYTE_BAUD_RATE_1200_INDEX          = 0         # 亿佰特波特率 1200 索引
    EBYTE_BAUD_RATE_2400_INDEX          = 1         # 亿佰特波特率 2400 索引
    EBYTE_BAUD_RATE_4800_INDEX          = 2         # 亿佰特波特率 4800 索引
    EBYTE_BAUD_RATE_9600_INDEX          = 3         # 亿佰特波特率 9600 索引
    EBYTE_BAUD_RATE_19200_INDEX         = 4         # 亿佰特波特率 19200 索引
    EBYTE_BAUD_RATE_38400_INDEX         = 5         # 亿佰特波特率 28400 索引
    EBYTE_BAUD_RATE_57600_INDEX         = 6         # 亿佰特波特率 57600 索引
    EBYTE_BAUD_RATE_115200_INDEX        = 7         # 亿佰特波特率 115200 索引

    EBYTE_PARITY_8N1_INDEX              = 0         # 亿佰特奇偶检验 8N1 索引
    EBYTE_PARITY_8O1_INDEX              = 1         # 亿佰特奇偶检验 8O1 索引
    EBYTE_PARITY_8E1_INDEX              = 2         # 亿佰特奇偶检验 8E1 索引

    EBYTE_AIRSPEED_24_INDEX             = 0         # 亿佰特空中速率 2.4 索引
    EBYTE_AIRSPEED_48_INDEX             = 1         # 亿佰特空中速率 4.8 索引
    EBYTE_AIRSPEED_96_INDEX             = 2         # 亿佰特空中速率 9.6 索引
    EBYTE_AIRSPEED_192_INDEX            = 3         # 亿佰特空中速率 19.2 索引
    EBYTE_AIRSPEED_384_INDEX            = 4         # 亿佰特空中速率 38.4 索引
    EBYTE_AIRSPEED_625_INDEX            = 5         # 亿佰特空中速率 62.5 索引

    # 串口助手 波特率 comboBox 索引 对应以下元素
    BAUD_RATE = (110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000, 256000)

    # 串口助手 数据位 comboBox 索引 对应以下元素
    DATA_BIT = (serial.EIGHTBITS, serial.SIXBITS, serial.SEVENBITS, serial.EIGHTBITS)

    # 串口助手 奇偶校验 comboBox 索引 对应以下元素
    PARITY = (serial.PARITY_NONE, serial.PARITY_ODD, serial.PARITY_EVEN)

    # 串口助手 停止位 comboBox 索引 对应以下元素
    STOP_BIT = (serial.STOPBITS_ONE, serial.STOPBITS_ONE_POINT_FIVE, serial.STOPBITS_TWO)

    # 串口助手 亿佰特Lora 配置的参数
    BAUD_RATE_EBYTE_CONFIG      = 9600
    DATA_BIT_EBYTE_CONFIG       = serial.EIGHTBITS
    PARITY_EBYTE_CONFIG         = serial.PARITY_NONE
    STOP_BIT_EBYTE_CONFIG       = serial.STOPBITS_ONE

    # 亿佰特串口参数配置
    EBYTE_SERIAL = {
        5: ((0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1), (1, 0, 1), (0, 1, 1), (1, 1, 1)),    # 亿佰特 波特率 comboBox 索引 对应该字节 bit5-7 具体量
        3: ((0, 0), (1, 0), (0, 1)),                                                                    # 亿佰特 校验位 comboBox 索引 对应该字节 bit3-4 具体量
        0: ((0, 1, 0), (1, 1, 0), (0, 0, 1), (1, 0, 1), (0, 1, 1), (1, 1, 1)),                          # 亿佰特 空中速率 comboBox 索引 对应该字节 bit0-2 具体量
    }