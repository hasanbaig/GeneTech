from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class PartWidget(QWidget):

    def __init__(self, part_type = "AND", parent=None):
        '''
        Extends the QWidget class. Each circuit part that appears on the
        canvas is a QWidget, whether its input, output or a gate.
        part_type: name of the Circuit part
        parent: parent widget on top of which this would appear
        '''
        super().__init__(parent)
        self.part_type = part_type
        self.input = "IPTG" #default input
        self.is_input = part_type == "INPUT" #if input
        self.is_gate = part_type in ["AND", "OR", "NOT", "NOR", "NAND"] #if gate
        self.is_output = part_type == "OUTPUT" #if output
        self.initWidget()

    def initWidget(self):
        '''
        This function initializes the widget: Creates a vertical layout, with 0 margins
        on all sides. Then a widget is added to the layout depending on what type of
        part we are dealing with.
        '''
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        if self.is_input:
            #adds a combobox inside the Graphics Part object in case of input
            self.comboBox = QComboBox(self)
            self.comboBox.addItem("IPTG")
            self.comboBox.addItem("aTc")
            self.comboBox.addItem("Arabinose")
            self.comboBox.activated[str].connect(self.selected_input) #input text is changed based on what the user selects
            self.layout.addWidget(self.comboBox)

        elif self.is_output:
            #adds a simple label inside the Graphics Part object to signify output
            self.layout.addWidget(QLabel("Output"))

        else:
            #adds widget for the different gates and their corresponding icons
            self.wdg_label = QLabel(self.part_type if self.is_gate else "INPUT")
            pixmap = QIcon("./icons/"+self.part_type+".svg" if self.is_gate else 'AND.svg').pixmap(QSize(120, 80))
            self.wdg_label.setPixmap(pixmap)
            self.layout.addWidget(self.wdg_label)

    def selected_input(self, input_txt):
        '''
        Sets the input to what the user selected from the dropdown.
        '''
        self.input = input_txt
