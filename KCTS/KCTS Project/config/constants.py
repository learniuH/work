

class NavigationBarItems:
    LIST = ['设备状态', 'MU功能测试', '输出查询']

class ConnectionStatus():
    ''' 连接状态枚举 '''
    DISCONNECTED = 0
    CONNECTED = 1

class SendCycle():
    CYCLE = 100

class QLabelStyleSheet():
    LABEL_QSS_HIGHLIGHT = ('QLabel {'
                           'border: 3px solid grey;'
                           'border-radius: 10px;'
                           'text-align: center;'
                           'font: 9pt "微软雅黑";'
                           'background-color: #fcd97f;'
                           '}')

    LABEL_QSS_NORMAL = ('QLabel {'
                        'border: 3px solid grey;'
                        'border-radius: 10px;'
                        'text-align: center;'
                        'font: 9pt "微软雅黑";'
                        'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f6f7fa, stop: 1 #dadbde);'
                        '}')