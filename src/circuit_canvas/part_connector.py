from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4


class Connector():
    def __init__(self, part, index=0, position=LEFT_TOP, total = 1):

        self.part = part
        self.index = index
        self.position = position

        self.grSocket = QDMGraphicsConnector(self.part.grNode)

        self.grSocket.setPos(*self.part.getConnectorPosition(index, position, total))




class QDMGraphicsConnector(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)

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
