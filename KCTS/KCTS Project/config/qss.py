

class SendCycle():
    CYCLE = 100

class QLabelStyleSheet():
    ''' QLabel 解析界面的两个状态'''
    LABEL_QSS_HIGHLIGHT = ('QLabel {'
                           '    border: 3px solid grey;'
                           '    border-radius: 10px;'
                           '    text-align: center;'
                           '    font: 9pt "微软雅黑";'
                           '    background-color: #fcd97f;'
                           '}')

    LABEL_QSS_NORMAL = ('QLabel {'
                        '   border: 3px solid grey;'
                        '   border-radius: 10px;'
                        '   text-align: center;'
                        '   font: 9pt "微软雅黑";'
                        '   background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,'
                        '                                     stop: 0 #f6f7fa, stop: 1 #dadbde);'
                        '}')

class AnalogStyleSheet():
    ''' OU解析界面 ProgressBar Label 的 QSS '''
    Label_QSS = ('QLabel {'
                 '    font: 9pt "微软雅黑";'
                 '    color: white;'
                 '}')

    ProgressBar_QSS = ('QProgressBar {'
                       '    border: 3px solid qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,'
                       '                                      stop: 0 #f6f7fa, stop: 1 #dadbde);'
                       '    border-radius: 10px;'
                       '    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,'
                       '                                      stop: 0 #f6f7fa, stop: 1 #dadbde);'
                       '}'
                       'QProgressBar::chunk {'
                       '    border-radius: 5px;'
                       '    background-color: #e77060;' 
                       '}')

