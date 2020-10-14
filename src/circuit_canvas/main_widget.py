import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from circuit_parts import CircuitPart
from window_graphics_scene import MyGraphicsScene
from circuit_scene import CircuitScene
from part_widget import PartWidget
from part_graphics import GraphicsPart
from part_connector import *
from edges import *
from configuration import *

mime_type = "application/x-item"

class MainScreenWidget(QWidget):
    def __init__(self, parent=None):
        '''
        This class concerns the canvas that we see on the left side of the Window
        This is basically the canvas where the parts/objects from the right dock are
        dragged and dropped.
        '''
        super().__init__(parent)
        # output of the current circuit being drawn
        self.circuit_output = None
        self.initUI()

    def initUI(self):
        '''
        Helpder function to set the scene and settings of the canvas
        '''
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        # crate graphics scene
        self.scene = CircuitScene()
        self.view = MyGraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)
        #Event listeners for drag and drop.
        self.scene.addDragEnterListener(self.onDragEnter)
        self.scene.addDropListener(self.onDrop)


    def onDragEnter(self, event):
        '''
        This is a builtin function in QWidget and as the name
        suggests this is called when the drag event is triggered.
        To read more about this: https://doc.qt.io/qtforpython/overviews/dnd.html
        '''
        if event.mimeData().hasFormat(mime_type):
            event.acceptProposedAction()
        else:
            event.setAccepted(False)

    def onDrop(self, event):
        '''
        This is a builtin function in QWidget and as the name suggests this is
        called when the part is dropped, that is, drop event is triggered.
        To read more about this: https://doc.qt.io/qtforpython/overviews/dnd.html
        '''
        if event.mimeData().hasFormat(mime_type):
            eventData = event.mimeData().data(mime_type)
            dataStream = QDataStream(eventData, QIODevice.ReadOnly)
            #Data of the dropped object
            pixmap = QPixmap() #to hold the icon data
            dataStream >> pixmap #this writes the icon to pixmap from the data stream
            part_type = dataStream.readInt() #part type
            text = dataStream.readQString() #the name of the part
            mouse_position = event.pos() #where the object was dropped
            #this maps the mouse position to the coordinates corresponding to the scene
            scene_position = self.scene.grScene.views()[0].mapToScene(mouse_position)

            #Two inputs if the part type is not Input/Ouput/NOT
            inputs = [1, 2] if part_type > 2 else [1]
            if part_type == 0: #if input part type
                inputs = []

            #1 output in all cases except when the part is the output part
            outputs = [] if part_type == 1 else [1]

            #create a CircuitPart object corresponding the dropped part
            part = CircuitPart(self.scene, text, inputs=inputs, outputs=outputs)
            part.setPos(scene_position.x(), scene_position.y())
            if part_type == 1: #if part is output, then set the output of the circuit
                 self.circuit_output = part
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            #drop ignored, not one of the draggable objects
            event.ignore()

    def addParts(self):
        '''
        Useless function for debugging at the start, not needed anymore
        '''
        part1 = CircuitPart(self.scene, "NOT Gate", inputs=[1], outputs=[1])
        part2 = CircuitPart(self.scene, "NOR Gate", inputs=[1,2], outputs=[1])
        part3 = CircuitPart(self.scene, "INPUT Gate", inputs=[], outputs=[1])

        part1.setPos(-350, -250)
        part2.setPos(-75, 0)
        part3.setPos(200, -150)
        print("part1 ", part1.outputs[0].getConnectorPosition())
        print("part2 ", part2.outputs[0].getConnectorPosition())
        edge1 = Edge(self.scene, part1.outputs[0], part2.inputs[0])


CURRENT_MODE_NOOP = 1
CURRENT_MODE_EDGE_DRAG = 2

class MyGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None):
        '''
        This class concerns the graphical view of the canvas that we see on the
        left side of the Window This is basically the canvas where the parts/objects
        from the right are dragged and dropped.
        grScene: The graphic scene of the window
        parent: [optional] A graphics item on top of which this view is pasted.
        '''
        super().__init__(parent)
        self.grScene = grScene
        self.initUI()
        self.setScene(self.grScene)
        self.CURRENT_MODE_ = CURRENT_MODE_NOOP
        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]
        self.drag_enter_listeners = []
        self.drop_listeners = []
        self.edgeDragThreshold = 10

    def initUI(self):
        '''
        Helpder function to set the scene and settings of the view
        '''
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        #self.setDragMode(QGraphicsView.ScrollHandDrag)
        #self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAcceptDrops(True)

    def getItemAtClick(self, event):
        '''
        Get the part/item on which there is a mouse event, either press or release
        '''
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def edgeDragStart(self, item):
        '''
        This sets the tone for the dragging of the edge
        '''
        #get the edge corresponding to the connector that's clicked
        self.previousEdge = item.connector.edge
        self.last_start_connector = item.connector
        #new edge
        self.dragEdge = Edge(self.grScene.scene, item.connector, None)

    def edgeDragEnd(self, item):
        '''
        Called after edgeDragStart this function completes the dragging
        of the edge.
        '''
        #set CURRENT_MODE_ to default
        self.CURRENT_MODE_ = CURRENT_MODE_NOOP

        if type(item) is MyGraphicsConnector:
            #remove the current edge of the connector
            if item.connector.hasEdge():
                item.connector.edge.remove()
            if self.previousEdge is not None:
                self.previousEdge.remove()
            #set the parameters of the new edge
            self.dragEdge.start_connector = self.last_start_connector
            self.dragEdge.end_connector = item.connector
            self.dragEdge.start_connector.setConnectedEdge(self.dragEdge)
            self.dragEdge.end_connector.setConnectedEdge(self.dragEdge)
            #update position of the dragged edge
            self.dragEdge.updatePositions()
            return True

        #if the item we clicked on, that is, where the mouse button is released
        #is not a connector then simply remove the edge
        self.dragEdge.remove()
        self.dragEdge = None
        #set the edge to previous edge
        if self.previousEdge is not None:
            self.previousEdge.start_connector.edge = self.previousEdge
        return False

    def distanceStartEnd(self, event):
        '''
        Checks if we have moved the edge sufficiently for it to be dragged
        '''
        new_mouse_pos = self.mapToScene(event.pos())
        dist_scene = new_mouse_pos - self.last_click_pos
        distanceThreshold = self.edgeDragThreshold**2
        return (dist_scene.x()*dist_scene.x() + dist_scene.y()*dist_scene.y()) > distanceThreshold

    # Function related to drag and drop events
    def dragEnterEvent(self, event):
        for callback in self.drag_enter_listeners: callback(event)

    def dropEvent(self, event):
        for callback in self.drop_listeners: callback(event)

    def addDragEnterListener(self, callback):
        self.drag_enter_listeners.append(callback)

    def addDropListener(self, callback):
        self.drop_listeners.append(callback)

    def keyPressEvent(self, event):
        '''
        Function is called when a key is pressed.
        '''
        #Delete key is pressed then call delete_items
        if event.key() == Qt.Key_Delete:
            self.delete_item()
        else:
            super().keyPressEvent(event)


    def delete_item(self):
        '''
        This function removes the selected items from the view.
        '''
        #Get the selected items and remove them
        for item in self.grScene.selectedItems():
            if isinstance(item, MyGraphicsEdge):
                item.edge.remove()
            elif isinstance(item, GraphicsPart):
                 item.part.remove()

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
        '''
        Function is called when a mouse button is pressed.
        '''
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
        self.setDragCURRENT_MODE_(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragCURRENT_MODE_(QGraphicsView.NoDrag)


    def leftMouseButtonPress(self, event):
        '''
        This function is triggered when the left mouse button is pressed.
        It gets the item that is clicked and sets the CURRENT_MODE_ of operation:
        whether its a part drag or edge drag.
        '''
        # get item which we clicked on
        item = self.getItemAtClick(event)
        # store the position of mouse click
        self.last_click_pos = self.mapToScene(event.pos())

        # If a connector is clicked then we start the edge drag CURRENT_MODE_
        if type(item) is MyGraphicsConnector:
            if self.CURRENT_MODE_ == CURRENT_MODE_NOOP:
                self.CURRENT_MODE_ = CURRENT_MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return

        #This is called when the edge is already being dragged
        if self.CURRENT_MODE_ == CURRENT_MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res:
                return
        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        '''
        This function is triggered when the left mouse button is released.
        It gets the item that is clicked; in case of edge we see if the
        start and end point are sufficiently distanced if yes we accept
        otherwise we ignore the event. In case of part drag, we simply
        accept the event.
        '''
        # get item which we release mouse button on
        item = self.getItemAtClick(event)

        # logic
        if self.CURRENT_MODE_ == CURRENT_MODE_EDGE_DRAG:
            if self.distanceStartEnd(event):
                result = self.edgeDragEnd(item)
                if result:
                    return
        super().mouseReleaseEvent(event)


    def rightMouseButtonPress(self, event):
        '''
        This function is triggered when the right mouse button is pressed
        '''
        super().mousePressEvent(event)
        item = self.getItemAtClick(event)

    def rightMouseButtonRelease(self, event):
        '''
        This function is triggered when the right mouse button is released
        '''
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        '''
        This function responds to the wheel movement on the mouse,
        that is, zooming in and out of the screen.
        '''
        # calculate zoom out factor
        zoomOutFactor = 1 / self.zoomInFactor

        if event.angleDelta().y() > 0:
            #zoom-in
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            #zoom-out
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]:
            self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]:
            self.zoom, clamped = self.zoomRange[1], True

        # set scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)
