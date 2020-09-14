from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *



DEBUG = True

class Connector():
    def __init__(self, part, index=0, total = 1, is_left = True, input_output = False):

        self.part = part
        self.total = total
        self.index = index
        self.is_left = is_left
        self.input_output = input_output
        self.grConnector = QDMGraphicsConnector(self)

        self.grConnector.setPos(*self.part.getConnectorPosition(index, total, left = self.is_left, input_output = self.input_output))

        self.edge = None

    def getConnectorPosition(self):
        return self.part.getConnectorPosition(self.index, self.total, self.is_left, self.input_output)

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
        self._color_background = QColor("#4C000000")
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
