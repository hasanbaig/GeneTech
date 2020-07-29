import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from main_widget import MainScreenWidget


class MainCircuitWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_name_image = None
        self.initUI()
		
    
    def initUI(self):
	
		self.menu = self.menuBar()
		self.file_menu = self.menu.addMenu("File")
		capture_action = QAction("Save Image", self)
		capture_action.setShortcut("Ctrl+S")
		capture_action.setToolTip("Capture image of the circuit you have drawn")
		capture_action.triggered.connect(self.captureCircuit)
		self.statusBar().showMessage("")
		self.file_menu.addAction(capture_action)
		
		
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("GeneTech - Circuit Builder")
		
        
        self.setWindowIcon(QIcon('../SmallLogo.png'))
        
        self.main_widget = MainScreenWidget(self)
        self.setCentralWidget(self.main_widget)
        self.captureCircuit()
        self.show()
        
    
    def captureCircuit(self):
		if not self.file_name_image:
			filename, filter = QFileDialog.getSaveFileName(self, "Save Circuit To Image")
			self.file_name_image = filename
			self.main_widget.scene.grScene.save(filename)
			self.statusBar().showMessage("Saved Successfuly")
		else:
			self.main_widget.scene.grScene.save(self.file_name_image)
			self.statusBar().showMessage("Saved Successfuly")
		
    
        

