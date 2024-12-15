from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QCheckBox, QPushButton, QSlider, QLineEdit

from widget.constant import ConstantText

class OUSimulator:
    ''' OU 模拟器相关控件的函数 '''

    key_button = None     # 将 lineEdit 里面的字母与 pushButton 绑定

    @staticmethod
    def checkBox_status_changed(checkBox: QCheckBox, pushButton: QPushButton):
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
        ''' 模拟量区的按键按下, 启动使 slider value 增加的定时器(同时关闭减少的定时器) '''
        pushButton.timer_decrease.stop()
        pushButton.timer_increase.start(ConstantText.TIMER_PERIOD)

        print(f'byte_num:{pushButton.byte_num} bit_index:{pushButton.bit_index} pressed')

    @staticmethod
    def analog_pushButton_released(pushButton: QPushButton):
        ''' 模拟量区的按键释放, 启动使 slider value 减少的定时器(同时关闭增加的定时器) '''
        pushButton.timer_increase.stop()
        pushButton.timer_decrease.start(ConstantText.TIMER_PERIOD)

        print(f'byte_num:{pushButton.byte_num} bit_index:{pushButton.bit_index} released')

    @staticmethod
    def slider_value_increase(timer_increase: QTimer, slider: QSlider):
        ''' increase 定时器 timeout 时, 增加 slider value 值 '''
        # 鼠标拖动滑块的优先级最高, 鼠标点击时 将定时器关闭
        if not slider.isSliderDown() and slider.value() < slider.maximum():
            slider.setValue(slider.value() + 1)
            print(f'byte_num:{slider.byte_num} bit_index:{slider.bit_index} slider value increase')
        else:
            # slider 到达最大值后, 停止 increase 定时器, 停止继续增加
            timer_increase.stop()

    @staticmethod
    def slider_value_decrease(timer_decrease: QTimer, slider: QSlider):
        ''' decrease 定时器 timeout 时, 减少 slider value 值'''
        # 鼠标拖动滑块的优先级最高, 鼠标点击时 将定时器关闭
        if not slider.isSliderDown() and slider.value() > slider.minimum():
            slider.setValue(slider.value() - 1)
            print(f'byte_num:{slider.byte_num} bit_index:{slider.bit_index} slider value decrease')
        else:
            # slider 到达最小值后, 停止 decrease 定时器, 停止继续减少
            timer_decrease.stop()

    @staticmethod
    def slider_value_changed(slider: QSlider):
        ''' slider 的值变化时, 改变对应报文的值 '''

        print(f'byte_num: {slider.byte_num} bit_index: {slider.bit_index} value changed')

    @staticmethod
    def lineEdit_text_changed(lineEdit: QLineEdit, pushButton: QPushButton, checkBox: QCheckBox=None, slider: QSlider=None):
        ''' lineEdit text 改变时, 将 lineEdit: {key: pushButton} 存入字典 '''
        print(f'byte_num: {lineEdit.byte_num} bit_index: {lineEdit.bit_index} text: {lineEdit.text()}')
        if lineEdit not in OUSimulator.key_button:
            # 将 字母 与 pushButton 绑定
            if lineEdit.bit_index is not None:
                # 如果是开关量 需要将 checkBox 一并存入
                OUSimulator.key_button[lineEdit] = {lineEdit.text().upper(): [pushButton, checkBox]}
            else:
                # 模拟量 将 slider 一并存入
                OUSimulator.key_button[lineEdit] = {lineEdit.text().upper(): [pushButton, slider]}

        else:
            # 删除 字母 与 pushButton 的绑定
            OUSimulator.key_button[lineEdit] = {}
            if lineEdit.text() != '':
                # 更新 字母 与 pushButton 的绑定
                if lineEdit.bit_index is not None:
                    # 如果是开关量 需要将 checkBox 一并存入
                    OUSimulator.key_button[lineEdit] = {lineEdit.text().upper(): [pushButton, checkBox]}
                else:
                    # 模拟量 将 slider 一并存入
                    OUSimulator.key_button[lineEdit] = {lineEdit.text().upper(): [pushButton, slider]}
            else:
                # 将 lineEdit 从字典里移除
                OUSimulator.key_button.pop(lineEdit)




