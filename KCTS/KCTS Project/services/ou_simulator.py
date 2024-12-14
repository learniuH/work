from PyQt5.QtWidgets import QCheckBox, QPushButton, QSlider, QLineEdit


class OUSimulator:
    ''' OU 模拟器相关控件的函数 '''

    key_button = None     # 将 lineEdit 里面的字母与 pushButton 绑定

    @staticmethod
    def checkBox_status_changed(checkBox: QCheckBox, pushButton: QPushButton, lineEdit: QLineEdit):
        ''' checkBox 选中时, 驱动对应按键 pressed, unchecked 同理'''
        if checkBox.isChecked():
            # cheBox checked 时, 禁用 pushButton, 触发 pressed 函数
            pushButton.setDisabled(True)
            OUSimulator.switch_pushButton_pressed(pushButton)
            print(f'byte_num:{checkBox.byte_num} bit_index:{checkBox.bit_index} is checked')

        else:
            pushButton.setEnabled(True)
            OUSimulator.switch_pushButton_released(pushButton)
            print(f'byte_num:{checkBox.byte_num} bit_index:{checkBox.bit_index} is unchecking')

    @staticmethod
    def switch_pushButton_pressed(pushButton: QPushButton):
        ''' 开关量区的按键按下时, 改变报文对应位的值 '''
        print(f'byte_num:{pushButton.byte_num} bit_index:{pushButton.bit_index} pressed')

    @staticmethod
    def switch_pushButton_released(pushButton: QPushButton):
        ''' 开关量区的按键释放时, 改变报文对应位的值 '''
        print(f'byte_num:{pushButton.byte_num} bit_index:{pushButton.bit_index} released')

    @staticmethod
    def analog_pushButton_pressed(pushButton: QPushButton):
        ''' 模拟量区的按键按下, 驱动对应 slider value 增加'''
        print(f'byte_num:{pushButton.byte_num} bit_index:{pushButton.bit_index} pressed')

    @staticmethod
    def analog_pushButton_released(pushButton: QPushButton):
        ''' 模拟量区的按键释放, 驱动对应 slider value 减小 '''
        print(f'byte_num:{pushButton.byte_num} bit_index:{pushButton.bit_index} released')

    @staticmethod
    def slider_value_changed(slider: QSlider):
        ''' slider 的值变化时, 改变对应报文的值 '''
        print(f'byte_num: {slider.byte_num} bit_index: {slider.bit_index} value changed')

    @staticmethod
    def lineEdit_text_changed(lineEdit: QLineEdit, pushButton: QPushButton, checkBox: QCheckBox=None):
        ''' lineEdit text 改变时, 将 lineEdit: {key: pushButton} 存入字典 '''
        print(f'byte_num: {lineEdit.byte_num} bit_index: {lineEdit.bit_index} text: {lineEdit.text()}')
        if lineEdit not in OUSimulator.key_button:
            # 将 字母 与 pushButton 绑定
            if lineEdit.bit_index is not None:
                # 如果是开关量 需要将 checkBox 一并存入
                OUSimulator.key_button[lineEdit] = {lineEdit.text().upper(): [pushButton, checkBox]}
            else:
                OUSimulator.key_button[lineEdit] = {lineEdit.text().upper(): pushButton}

        else:
            # 删除 字母 与 pushButton 的绑定
            OUSimulator.key_button[lineEdit] = {}
            if lineEdit.text() != '':
                # 更新 字母 与 pushButton 的绑定
                if lineEdit.bit_index is not None:
                    # 如果是开关量 需要将 checkBox 一并存入
                    OUSimulator.key_button[lineEdit] = {lineEdit.text().upper(): [pushButton, checkBox]}
                else:
                    OUSimulator.key_button[lineEdit] = {lineEdit.text().upper(): pushButton}
            else:
                # 将 lineEdit 从字典里移除
                OUSimulator.key_button.pop(lineEdit)




