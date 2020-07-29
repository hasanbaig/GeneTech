import sys
from PyQt5.QtWidgets import *

from window import Window


if __name__ == '__main__':
    app = QApplication(sys.argv)

    
    wnd = Window()

    sys.exit(app.exec_())
