from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4

DEBUG = True 

class Connector():
    def __init__(self, part, index=0, position=LEFT_TOP, total = 1):

        self.part = part
        self.index = index
        self.position = position

        self.grConnector = QDMGraphicsConnector(self)

        self.grConnector.setPos(*self.part.getConnectorPosition(index, position, total))
        
        self.edge = None

    def getConnectorPosition(self):
        if DEBUG: print("  GSP: ", self.index, self.position, "part:", self.part)
        res = self.part.getConnectorPosition(self.index, self.position)
        if DEBUG: print("  res", res)
        return res


    def setConnectedEdge(self, edge=None):
        self.edge = edge

    def hasEdge(self):
        return self.edge is not None



class QDMGraphicsConnector(QGraphicsItem):
    def __init__(self, connector):
        self.connector = connector
        super().__init__(connector.part.grNode)

        self.radius = 6.0
        self.outline_width = 1.0
        self._color_background = QColor("#FFFF7700")
        self._color_outline = QColor("#FF000000")

        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._brush = QBrush(self._color_background)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # painting circle
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

    def boundingRect(self):
        return QRectF(
            - self.radius - self.outline_width,
            - self.radius - self.outline_width,
            2 * (self.radius + self.outline_width),
            2 * (self.radius + self.outline_width),
        )
