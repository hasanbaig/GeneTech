import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from circuit_parts import CircuitPart

from window_graphics_scene import QDMGraphicsScene
from circuit_scene import CircuitScene
from part_widget import PartWidget
from part_connector import *
from edges import *

MODE_NOOP = 1
MODE_EDGE_DRAG = 2

EDGE_DRAG_START_THRESHOLD = 10
DEBUG = True

class MainScreenWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()


    def initUI(self):
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        
        # crate graphics scene
        #self.grScene = QDMGraphicsScene()
        self.scene = CircuitScene()
        #self.grScene = self.scene.grScene
        self.addNodes()
        self.view = QDMGraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)

        """        
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
        self.myListWidget1.setIconSize(QSize(200, 100))
        # create graphics view
        self.layout.addWidget(self.myListWidget1)
        """
        
    def addNodes(self):
        part1 = CircuitPart(self.scene, "NOT Gate", inputs=[1], outputs=[1])
        part2 = CircuitPart(self.scene, "NOR Gate", inputs=[1,2], outputs=[1])
        part3 = CircuitPart(self.scene, "OR Gate", inputs=[1,2], outputs=[1])   
        
        part1.setPos(-350, -250)
        part2.setPos(-75, 0)
        part3.setPos(200, -150)
        print("part1 ", part1.outputs[0].getConnectorPosition())
        print("part2 ", part2.outputs[0].getConnectorPosition())
        edge1 = Edge(self.scene, part1.outputs[0], part2.inputs[0])
        edge2 = Edge(self.scene, part2.outputs[0], part3.inputs[0])
     

class QDMGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene

        self.initUI()

        self.setScene(self.grScene)

        self.mode = MODE_NOOP

        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]
		self.setAcceptDrops(True)
		
    
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
        
    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        #self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
#        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
 #       self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    
    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)


    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)



    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)


    def leftMouseButtonPress(self, event):
        # get item which we clicked on
        item = self.getItemAtClick(event)

        # we store the position of last LMB click
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        # logic
        if type(item) is QDMGraphicsConnector:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return

        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res: return


        super().mousePressEvent(event)


    def leftMouseButtonRelease(self, event):
        # get item which we release mouse button on
        item = self.getItemAtClick(event)

        # logic
        if self.mode == MODE_EDGE_DRAG:
            if self.distanceBetweenClickAndReleaseIsOff(event):
                res = self.edgeDragEnd(item)
                if res: return


        super().mouseReleaseEvent(event)


    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)

        item = self.getItemAtClick(event)

        if DEBUG:
            if isinstance(item, QDMGraphicsEdge): print('RMB DEBUG:', item.edge, ' connecting connectors:',
                                            item.edge.start_connector, '<-->', item.edge.end_connector)
            if type(item) is QDMGraphicsConnector: print('RMB DEBUG:', item.connector, 'has edge:', item.connector.edge)

            if item is None:
                print('SCENE:')
                print('  Nodes:')
                for part in self.grScene.scene.parts: print('    ', part)
                print('  Edges:')
                for edge in self.grScene.scene.edges: print('    ', edge)


    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)


    def getItemAtClick(self, event):
        """ return the object on which we've clicked/release mouse button """
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj


    def edgeDragStart(self, item):
        if DEBUG: print('View::edgeDragStart ~ Start dragging edge')
        if DEBUG: print('View::edgeDragStart ~   assign Start Socket')
        self.previousEdge = item.connector.edge
        self.last_start_connector = item.connector
        self.dragEdge = Edge(self.grScene.scene, item.connector, None)
        if DEBUG: print('View::edgeDragStart ~ dragEdge: ', self.dragEdge)
        
    def edgeDragEnd(self, item):
        """ return True if skip the rest of the code """
        self.mode = MODE_NOOP

        if type(item) is QDMGraphicsConnector:
            if DEBUG: print('View::edgeDragEnd ~   prev edge')
            if item.connector.hasEdge():
                item.connector.edge.remove()
            if DEBUG: print('View::edgeDragEnd ~   assign End Socket')
            if self.previousEdge is not None: self.previousEdge.remove()
            if DEBUG: print('View::edgeDragEnd ~   prev edge removed')
            self.dragEdge.start_connector = self.last_start_connector
            self.dragEdge.end_connector = item.connector
            self.dragEdge.start_connector.setConnectedEdge(self.dragEdge)
            self.dragEdge.end_connector.setConnectedEdge(self.dragEdge)
            if DEBUG: print('View::edgeDragEnd ~   assigned start and end sochet to edge`')
            self.dragEdge.updatePositions()
            return True

        if DEBUG: print('View::edgeDragEnd ~ End dragging edge')
        self.dragEdge.remove()
        self.dragEdge = None
        if self.previousEdge is not None:
            self.previousEdge.start_connector.edge = self.previousEdge
        return False


    def distanceBetweenClickAndReleaseIsOff(self, event):
        """ measures if we are too far from the last LMB click scene position """
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_threshold_sq = EDGE_DRAG_START_THRESHOLD*EDGE_DRAG_START_THRESHOLD
        return (dist_scene.x()*dist_scene.x() + dist_scene.y()*dist_scene.y()) > edge_drag_threshold_sq



    def wheelEvent(self, event):
        # calculate our zoom Factor
        zoomOutFactor = 1 / self.zoomInFactor

        # calculate zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep


        clamped = False
        if self.zoom < self.zoomRange[0]: self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[1], True

        # set scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)
    
    def mouseMoveEvent(self, event):
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.dragEdge.grEdge.setDestination(pos.x(), pos.y())
            self.dragEdge.grEdge.update()
            