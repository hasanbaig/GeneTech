import sys
from PyQt5.QtWidgets import *

from main_window import CircuitBuilder


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = CircuitBuilder()
    sys.exit(app.exec_())
