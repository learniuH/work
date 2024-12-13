import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton


def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('My PyQt5 Window')
    window.setGeometry(100, 100, 300, 200)

    button = QPushButton('Click Me', window)
    button.move(100, 80)

    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()