from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QListWidget, QHBoxLayout, QVBoxLayout,QListWidgetItem
from PyQt5.QtGui import QIcon, QPixmap
import sys
 
 
class CircuitBuilder(QMainWindow):
    def __init__(self, parent = None):
        super().__init__()
        #Setting the logos for the window
        self.setWindowIcon(QIcon('SmallLogo.png'))
        
        self.wid = QWidget(self)
        self.setCentralWidget(self.wid)
        layout = QVBoxLayout()
        
        self.myListWidget1 = QListWidget()
        self.myListWidget2 = QListWidget()
        self.myListWidget1.setViewMode(QListWidget.IconMode)
        self.myListWidget2.setViewMode(QListWidget.IconMode)
        self.myListWidget1.setAcceptDrops(True)
        self.myListWidget1.setDragEnabled(True)
        self.myListWidget2.setAcceptDrops(True)
        self.myListWidget2.setDragEnabled(True)
        self.setGeometry(300, 350, 800 , 600)
        
 
        l1 = QListWidgetItem(QIcon('AND.png'), "AND", self.myListWidget1)
        l5 = QListWidgetItem(QIcon('NAND.png'), "NAND", self.myListWidget1)
        l2 = QListWidgetItem(QIcon('OR.png'), "OR", self.myListWidget1)
        l3 = QListWidgetItem(QIcon('NOR.png'), "NOR", self.myListWidget1)
        l4 = QListWidgetItem(QIcon('NOT.png'), "NOT", self.myListWidget1)

 
#        self.myListWidget1.insertItem(1, l1)
 #       self.myListWidget1.insertItem(2, l2)
  #      self.myListWidget1.insertItem(3, l3)
   #     self.myListWidget1.insertItem(4, l4)
    #    self.myListWidget1.insertItem(5, l5) 
        
        #QListWidgetItem(QIcon('AND.png'), "AND", self.myListWidget2)
        self.myLayout = QHBoxLayout()
        self.myLayout.addWidget(self.myListWidget2, 3)
        self.myLayout.addWidget(self.myListWidget1, 1)
        
 
        self.setWindowTitle('GeneTech - CircuitBuilder');
        self.wid.setLayout(self.myLayout)
        print("what")
        
if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = CircuitBuilder()
    sys.exit(App.exec())