
# CAN 协议定义
CAN_PROTOCOLS = {
    '0x9c4': {
        'byte1': {
            'Bit0': '引擎启动',
            'Bit1': '引擎保持',
            'Bit2': '前进档',
            'Bit3': '空档',
            'Bit4': '后退档',
            'Bit5': '加档',
            'Bit6': '减档',
            'Bit7': '拖车',
        },
        'byte2': {
            'Bit0': '驻车刹车',
            'Bit1': '急停开关',
            'Bit2': '前灯',
            'Bit3': '后灯',
            'Bit4': '喇叭',
        },
        'byte8': {
            'heartbeat': '心跳信号'
        }
    },
    '0x9c5': {
        'byte1': '油门',
        'byte2': '左转',
        'byte3': '右转',
        'byte4': '升臂',
        'byte5': '降臂',
        'byte6': '装料',
        'byte7': '卸料',
        'byte8': '辅助刹车'
    },
    '0x6': {
        'byte4': '前车桥压力',
        'byte5': '前车桥压力'
    }
}
'''

# CAN 协议定义，包含 0x5DC 的转向角度解析
CAN_PROTOCOLS = {
    '0x9c4': {
        'byte1': {
            'Bit0': {'name': '引擎启动', 'length': 1},  
            'Bit1': {'name': '引擎熄火', 'length': 1},  
            'Bit2': {'name': '前进档', 'length': 1},
            'Bit3': {'name': '空档', 'length': 1},
            'Bit4': {'name': '后退档', 'length': 1},
            'Bit5': {'name': '加档', 'length': 1},
            'Bit6': {'name': '减档', 'length': 1},
            'Bit7': {'name': '拖车', 'length': 1}
        },
        'byte2': {
            'Bit0': {'name': '驻车刹车', 'length': 1},
            'Bit1': {'name': '急停开关', 'length': 1},
            'Bit2': {'name': '前灯', 'length': 1},
            'Bit3': {'name': '后灯', 'length': 1},
            'Bit4': {'name': '喇叭', 'length': 1},
        },
        'byte8': {
            'heartbeat': {'name': '心跳信号', 'length': 1}
        }
    },
    '0x9c5': {
        'byte1': {'name': '油门', 'length': 1},
        'byte2': {'name': '左转', 'length': 1},
        'byte3': {'name': '右转', 'length': 1},
        'byte4': {'name': '升臂', 'length': 2},  # 2字节数据示例
        'byte6': {'name': '装料', 'length': 1},
        'byte7': {'name': '卸料', 'length': 1},
        'byte8': {'name': '辅助刹车', 'length': 1}
    },
    '0x5dc': {
        'byte5_byte4': {'name': '转向角度', 'length': 2}  # 2字节的数据组合
    }
}
'''