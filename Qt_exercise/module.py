from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QMessageBox
class Stats:
    def __init__(self):
        self.window = QMainWindow()
        self.window.resize(500,600)
        self.window.move(300,300)
        self.window.setWindowTitle('薪资统计')

        self.textEdit = QPlainTextEdit(self.window)
        self.textEdit.setPlaceholderText('请输入薪资表')
        self.textEdit.move(10, 25)
        self.textEdit.resize(300, 500)

        self.button = QPushButton('统计', self.window)
        self.button.move(380, 80)

        self.button.clicked.connect(self.handleCalc)

    def handleCalc(self):
        info = self.textEdit.toPlainText()

        salary_above_20k = ''
        salary_bellow_20k = ''

        for line in info.splitlines(): # 去除换行符
            if not line.strip(): # 去除首尾的空格
                continue
            parts = line.split(' ') # 以空格为分隔符分割str
            # 去掉列表中空的字符串的内容
            name, salary, age = parts
            if int(salary) > 2000:
                salary_above_20k += name + '\n'
            else:
                salary_bellow_20k += name + '\n'
        QMessageBox.about(self.window, '统计结果', 
                        f'''薪资20000 以上的有: \n{salary_above_20k}\n薪资20000 以下的有: \n{salary_bellow_20k}''')
        
if __name__ == '__main__':
    app = QApplication()
    stats = Stats()
    stats.window.show()
    app.exec_()