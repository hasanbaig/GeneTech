from PyQt5.QtWidgets import *

from PyQt5.QtGui import *
from PyQt5.QtCore import *

class PartWidget(QWidget):
    def __init__(self, part_type = "AND", parent=None):
        super().__init__(parent)
        self.part_type = part_type
        self.input = "IPTG"
        self.is_input = part_type == "INPUT"
        self.is_gate = part_type in ["AND", "OR", "NOT", "NOR", "NAND"]
        self.is_output = part_type == "OUTPUT"
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        if self.is_input:
            self.comboBox = QComboBox(self)
            self.comboBox.addItem("IPTG")
            self.comboBox.addItem("aTc")
            self.comboBox.addItem("Arabinose")
            self.comboBox.activated[str].connect(self.selected_input)
            self.layout.addWidget(self.comboBox)

        elif self.is_output:
            self.layout.addWidget(QLabel("Output"))

        else:
            self.wdg_label = QLabel(self.part_type if self.is_gate else "INPUT")
            pixmap =QIcon("./icons/"+self.part_type+".svg" if self.is_gate else 'AND.svg').pixmap(QSize(120, 80))
            self.wdg_label.setPixmap(pixmap)
            self.layout.addWidget(self.wdg_label)

    def selected_input(self, input_txt):
        self.input = input_txt
