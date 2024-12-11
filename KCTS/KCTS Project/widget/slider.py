from PyQt5.QtWidgets import QApplication, QSlider, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QStyleOptionSlider


class DoubleSlider(QSlider):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.low_value = 20
        self.high_value = 80
        self.slider_pressed = None
        self.setRange(0, 100)

    def paintEvent(self, event):
        """重绘双滑块"""
        painter = QPainter(self)
        rect = self.rect()

        # 绘制滑槽
        self.style().drawComplexControl(
            self.style().CC_Slider,
            self.init_style_option(self.minimum(), self.maximum()),
            painter,
            self,
        )

        # 绘制范围背景
        x1 = self.value_to_position(self.low_value)
        x2 = self.value_to_position(self.high_value)
        painter.setBrush(Qt.green)
        painter.drawRect(QRect(QPoint(x1, rect.top() + 10), QPoint(x2, rect.bottom() - 10)))

        # 绘制低滑块
        self.style().drawComplexControl(
            self.style().CC_Slider,
            self.init_style_option(self.low_value, self.maximum()),
            painter,
            self,
        )

        # 绘制高滑块
        self.style().drawComplexControl(
            self.style().CC_Slider,
            self.init_style_option(self.high_value, self.maximum()),
            painter,
            self,
        )

    def init_style_option(self, value, max_value):
        """初始化滑块样式选项"""
        opt = QStyleOptionSlider()
        opt.initFrom(self)
        opt.minimum = self.minimum()
        opt.maximum = max_value
        opt.sliderValue = value
        opt.sliderPosition = value
        opt.tickPosition = self.tickPosition()
        opt.tickInterval = self.tickInterval()
        opt.orientation = self.orientation()
        return opt

    def value_to_position(self, value):
        """将值映射到像素位置"""
        span = self.maximum() - self.minimum()
        slider_width = self.width()
        return int((value - self.minimum()) / span * slider_width)

    def mousePressEvent(self, event):
        """检测按下的滑块"""
        self.slider_pressed = self.get_pressed_slider(event.pos())
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """根据鼠标移动更新滑块值"""
        if self.slider_pressed == "low":
            self.low_value = self.position_to_value(event.pos().x())
        elif self.slider_pressed == "high":
            self.high_value = self.position_to_value(event.pos().x())
        self.update()

    def position_to_value(self, position):
        """将像素位置映射到值"""
        span = self.maximum() - self.minimum()
        slider_width = self.width()
        return int(position / slider_width * span + self.minimum())

    def get_pressed_slider(self, position):
        """判断按下的是哪个滑块"""
        x1 = self.value_to_position(self.low_value)
        x2 = self.value_to_position(self.high_value)
        if abs(position.x() - x1) < abs(position.x() - x2):
            return "low"
        return "high"


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.slider = DoubleSlider(Qt.Horizontal, self)
        layout.addWidget(self.slider)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
