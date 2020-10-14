from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class GraphicsPart(QGraphicsItem):
    def __init__(self, part, parent=None):
        '''
        This class concerns the graphical aspect of the circuit parts
        that we see on the canvas, including gates, input and output.
        part: CircuitPart object signifying the part that needs to be rendered
        parent: [optional] signifies the Graphic on top of which the part will appear
                e.g. the circuit canvas
        '''
        super().__init__(parent)
        self.part = part
        self.part_gate = self.part.part_gate
        '''
        #concerning the title of the circuit part; denoting what Gate or input/output it is
        self.title = self.part.title
        self.title_color = Qt.white
        self.title_font = QFont("Times",  11)
        '''
        self.title_height = 10.0
        #height and width of the circuit part that appears on screen
        self.width = 120
        #if its an input, the height must be less
        self.height = 80 if self.part_gate.is_gate else 40
        self.edge_size = 4.0

        #pen to draw the outline; selected to denote a selected part on screen
        self.pen_default = QPen(QColor("#7F000000"))
        self.pen_selected = QPen(QColor("#FFFFA637"))
        self.init()

    def mouseMoveEvent(self, event):
        '''
        This is called when the part is dragged on screen
        as a result of which all edges connected to the part are
        updated.
        '''
        super().mouseMoveEvent(event)
        self.part.updateConnectedEdges()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    def boundingRect(self):
        '''
        Returns the bounding rect coordinates of the part.
        '''
        return QRectF(0, 0, self.width, self.height).normalized()

    def init(self):
        '''
        Helper function to initialize some flags
        and settings for the graphcis part UI.
        '''
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)
        self.initContent()

    def initContent(self):
        self.grContent = QGraphicsProxyWidget(self)
        self.part_gate.setGeometry(0, 0, self.width, self.height)
        self.grContent.setWidget(self.part_gate)



    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        #title of the circuit part; denoting what Gate or input/output it is
        '''
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0,0, self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())
        '''
        # the inside of the part, here the icon concering the gate
        # or the input/output parts are displayed
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_content.simplified())

        # outline: this draws the outline of the Graphics part
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        painter.setPen(self.pen_default if not self.isSelected() else self.pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())
