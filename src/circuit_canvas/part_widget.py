from PyQt5.QtWidgets import *

from PyQt5.QtGui import *

class PartWidget(QWidget):  
    def __init__(self, part_type = "AND", parent=None):
        super().__init__(parent)
        self.part_type = part_type
        self.input = ""
        self.is_input = part_type == "INPUT"
        self.is_gate = part_type in ["AND", "OR", "NOT", "NOR", "NAND"]
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
            print("here 1")
            self.comboBox.activated[str].connect(self.selected_input)
            print("here 2")
            self.layout.addWidget(self.comboBox)

        else:
            self.wdg_label = QLabel(self.part_type if self.is_gate else "INPUT")
            pixmap = QPixmap("../"+self.part_type+".png" if self.is_gate else '../AND.png')
            self.wdg_label.setPixmap(pixmap)
            self.layout.addWidget(self.wdg_label)
        
    def selected_input(self, input_txt):
        self.input = input_txt
        #self.myListWidget1 = QListWidget()
        #self.myListWidget1.setViewMode(QListWidget.IconMode)
        #self.myListWidget1.setAcceptDrops(False)
        #self.myListWidget1.setDragEnabled(False)
        #labelImage = QLabel(self)
        #vbox.addWidget(labelImage)
        #l1 = QListWidgetItem(QIcon('../AND.png'), "AND", self.myListWidget1)
        #self.layout.addWidget(self.myListWidget1)
