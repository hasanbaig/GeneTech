import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from main_widget import MainScreenWidget


class MainCircuitWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
    
    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("GeneTech - Circuit Builder")
        
        self.setWindowIcon(QIcon('../SmallLogo.png'))
        
        self.main_widget = MainScreenWidget(self)
        self.setCentralWidget(self.main_widget)
        self.captureCircuit()
        self.show()
        
    
    def captureCircuit(self):
        self.main_widget.scene.grScene.save("circuit.jpg")

    
        

