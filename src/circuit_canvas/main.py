import sys
from PyQt5.QtWidgets import *

from main_window import MainCircuitWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    wnd = MainCircuitWindow()

    sys.exit(app.exec_())
