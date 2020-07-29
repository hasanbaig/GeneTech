import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from circuit_parts import CircuitPart

from window_graphics_scene import QDMGraphicsScene
from circuit_scene import CircuitScene
from part_widget import PartWidget

class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()


    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.setWindowIcon(QIcon('../SmallLogo.png'))
        
        # crate graphics scene
        #self.grScene = QDMGraphicsScene()
        self.scene = CircuitScene()
        #self.grScene = self.scene.grScene
        part1 = CircuitPart(self.scene, "NOT Gate", inputs=[1], outputs=[1])
        part2 = CircuitPart(self.scene, "NOR Gate", inputs=[1,2], outputs=[1])
        part3 = CircuitPart(self.scene, "OR Gate", inputs=[1,2], outputs=[1])   
        
        part1.setPos(-350, -250)
        part2.setPos(-75, 0)
        part3.setPos(200, -150)

        
        self.myListWidget1 = QListWidget()
        self.myListWidget1.setViewMode(QListWidget.IconMode)
        self.myListWidget1.setAcceptDrops(True)
        self.myListWidget1.setDragEnabled(True)
        #self.myListWidget2.setAcceptDrops(True)
        #self.myListWidget2.setDragEnabled(True)
        #self.setGeometry(300, 350, 800 , 600)
        
    
        l1 = QListWidgetItem(QIcon('AND.png'), "AND", self.myListWidget1)
        l5 = QListWidgetItem(QIcon('NAND.png'), "NAND", self.myListWidget1)
        l2 = QListWidgetItem(QIcon('OR.png'), "OR", self.myListWidget1)
        l3 = QListWidgetItem(QIcon('NOR.png'), "NOR", self.myListWidget1)
        l4 = QListWidgetItem(QIcon('NOT.png'), "NOT", self.myListWidget1)

        # create graphics view
        self.view = QDMGraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)
        self.layout.addWidget(self.myListWidget1)

        self.setWindowTitle("GeneTech - Circuit Builder")
        self.save("circuit.jpg")
        self.show()
    
    def save(self, filename):
        self._master_rect = self.scene.grScene.itemsBoundingRect()
        print(self._master_rect)
        self._master_rect.adjust(-20, -20, 20, 20)
        print(self._master_rect)
        width = int(self._master_rect.width())
        height = int(self._master_rect.height())
        
        image = QImage(width, height, QImage.Format_ARGB32_Premultiplied)
        painter = QPainter(image)

        # Render the region of interest to the QImage.
        self.scene.grScene.render(painter, QRectF(image.rect()), self._master_rect)
        painter.end()

        # Save the image to a file.
        image.save(filename)
        

class QDMGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene
        self.setAcceptDrops(True)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.initUI()

        self.setScene(self.grScene)
    """
    def dragMoveEvent(self, event):
        pass
        
    def dragEnterEvent(self, event):   
        if event.mimeData():
            event.setAccepted(True)
            self.dragOver = True
            self.update()
            
    def dropEvent(self, event):
        pos = event.pos()
        event.acceptProposedAction()
    """
    
    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

#        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
 #       self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
