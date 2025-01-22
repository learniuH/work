from PyQt5.QtGui import QRegExpValidator, QValidator
from PyQt5.QtCore import QRegExp
from typing import Optional


class Validators:
    """UI输入验证器类"""

    @staticmethod
    def get_ipv4_validator() -> QRegExpValidator:
        """获取IPv4地址验证器

        Returns:
            IPv4地址验证器
        """
        ipv4_regex = QRegExp(
            '^((25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})\.){3}'
            '(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})$'
        )
        return QRegExpValidator(ipv4_regex)

    @staticmethod
    def get_port_validator() -> QRegExpValidator:
        """获取端口号验证器

        Returns:
            端口号验证器
        """
        port_regex = QRegExp(
            '^([0-5]?\d{1,4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$'
        )
        return QRegExpValidator(port_regex)

    @staticmethod
    def get_hex_validator() -> QRegExpValidator:
        """获取十六进制验证器, 允许输入一位或两位十六进制数字和空格的组合

        Returns:
            十六进制验证器
        """
        # hex_regex = QRegExp('^(([A-Fa-f0-9]{2} ){0,9}[A-Fa-f0-9]{2})?$')
        hex_regex = QRegExp('^([0-9A-Fa-f]{1,2}(\s+[0-9A-Fa-f]{1,2})*\s*)?$')
        return QRegExpValidator(hex_regex)

    @staticmethod
    def get_key_validator() -> QRegExpValidator:
        """获取按键验证器(仅允许单个英文字母)

        Returns:
            按键验证器
        """
        key_regex = QRegExp('^[A-Za-z]?$')
        return QRegExpValidator(key_regex)

    @staticmethod
    def ebyte_channel_validator() ->QRegExpValidator:
        ''' 获取亿佰特信道验证器, 0-83

        Returns:
            lineEdit验证器
        '''
        channel_regex = QRegExp('^([0-9]|[0-7][0-9]|8[0-3])$')
        return QRegExpValidator(channel_regex)

    @staticmethod
    def ebyte_addr_vallidator() ->QRegExpValidator:
        ''' 获取亿佰特模块地址验证器

        :return: lineEdit 验证器
        '''
        # addr_regex = QRegExp(r'^[0-9A-Fa-f]{2} (?:[1-9A-Fa-f]{2}|0[0-9A-Fa-f]{2,3})$')
        addr_regex = QRegExp(r'^[0-9A-Fa-f]{2} (?:[1-9A-Fa-f]{2}|0[0-9A-Fa-f]{2,3})$')
        return QRegExpValidator(addr_regex)