from enum import Enum

class ConnectionStatus(Enum):
    ''' 连接状态枚举 '''
    DISCONNECTED = 0
    CONNECTED = 1

class NavigationBarItems:
    LIST = ['设备状态', 'MU功能测试', '输出查询']

