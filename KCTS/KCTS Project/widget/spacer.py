from PyQt5.QtWidgets import QSpacerItem, QSizePolicy

try:
    from constant import ConstantText
except ImportError:
    from .constant import ConstantText

class LearniuHSpacer(QSpacerItem):
    ''' 自定义 width 的 spacer '''
    def __init__(self):
        super().__init__(ConstantText.SPACER_WIDTH, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)

