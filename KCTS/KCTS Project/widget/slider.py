from PyQt5.QtWidgets import QSlider

from typing import Union

class LearniuHSlider(QSlider):
    def __init__(self, byte_num: Union[str, int], minimum: int=0, maximum: int=100):

