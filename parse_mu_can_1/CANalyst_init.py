import ctypes
from ctypes import *

# 加载 ControlCAN DLL
can_dll = ctypes.windll.LoadLibrary("./ControlCAN.dll")

# 定义结构体
class VCI_CAN_OBJ(Structure):
    _fields_ = [("ID", c_uint),
                ("TimeStamp", c_uint),
                ("TimeFlag", c_byte),
                ("SendType", c_byte),
                ("RemoteFlag", c_byte),
                ("ExternFlag", c_byte),
                ("DataLen", c_byte),
                ("Data", c_ubyte * 8),
                ("Reserved", c_byte * 3)]

class VCI_INIT_CONFIG(Structure):
    _fields_ = [("AccCode", c_uint),
                ("AccMask", c_uint),
                ("Reserved", c_uint),
                ("Filter", c_byte),
                ("Timing0", c_byte),
                ("Timing1", c_byte),
                ("Mode", c_byte)]
    
# 接收 CAN 数据
def receive_can_data(device_type, device_index, can_index, max_frames=1000):
    can_obj = VCI_CAN_OBJ * max_frames  # 创建存储接收到数据的数组
    receive_buffer = can_obj()
    result = can_dll.VCI_Receive(device_type, device_index, can_index, byref(receive_buffer), max_frames, 100)
    return receive_buffer, result

# 启动 CAN 通道
def start_can(device_type, device_index, can_index):
    result = can_dll.VCI_StartCAN(device_type, device_index, can_index)
    if result == 1:
        print(f"CAN 通道 {can_index + 1} 启动成功!")
    else:
        print(f"CAN 通道 {can_index + 1} 启动失败!")
    return result

# 初始化 CAN 通道
def init_can(device_type, device_index, can_index, baud_rate=250):
    init_config = VCI_INIT_CONFIG()
    init_config.AccCode = 0x80000000
    init_config.AccMask = 0xFFFFFFFF
    init_config.Filter = 0  # 接收所有类型的报文
    # 根据波特率设置 Timing0 和 Timing1
    if baud_rate == 250:  # 250kbps
        init_config.Timing0 = 0x01
        init_config.Timing1 = 0x1C
    elif baud_rate == 500:  # 500kbps
        init_config.Timing0 = 0x00
        init_config.Timing1 = 0x1C
    else:
        print("未支持的波特率")
        return 0
    init_config.Mode = 0  # 正常模式

    result = can_dll.VCI_InitCAN(device_type, device_index, can_index, byref(init_config))
    if result == 1:
        # 启动 CAN 通道
        start_can(device_type, device_index, can_index)
    else:
        print(f"CAN 通道 {can_index} 初始化失败")
    return result

# 打开设备
def open_device(device_type, device_index, can_index):
    result = can_dll.VCI_OpenDevice(device_type, device_index, 0)
    if result == 1:
        # 初始化 CAN 通道
        init_can(device_type, device_index, can_index, baud_rate=250)
    else:
        print(f"设备 {device_index} 打开失败")
    return result
