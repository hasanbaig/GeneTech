from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Connector():
    def __init__(self, part, index=0, total = 1, is_left = True, input_output = False):
        '''
        This class is responsible for the connectors, that is, the circular socket like
        structure that appears on either one or both sides of the circuit part. The connector,
        as the name suggests connects two circuit parts via an edge.
        part: The Circuit part to which the connector belongs
        index: index of the connector on the circuit part (increases from top to bottom with top being 0)
        total: total connectors in the part
        is_left: whether or not the connector is on the left
        input_output: is the part input/output or gate
        '''
        self.part = part
        self.total = total
        self.index = index
        self.is_left = is_left
        self.input_output = input_output
        #graphics of the connector
        self.grConnector = MyGraphicsConnector(self)
        #sets the position of the connector using current position of the part
        self.grConnector.setPos(*self.part.getConnectorPosition(index, total, left = self.is_left, input_output = self.input_output))
        #no edge at the start
        self.edge = None

    def getConnectorPosition(self):
        '''
        Update position based on the current position of the part as the part keeps moving
        '''
        return self.part.getConnectorPosition(self.index, self.total, self.is_left, self.input_output)

    def setConnectedEdge(self, edge=None):
        '''
        Set edge that the connector belongs to.
        '''
        self.edge = edge

    def hasEdge(self):
        '''
        Checks if the connector is already bound to an edge.
        '''
        return self.edge is not None



class MyGraphicsConnector(QGraphicsItem):
    def __init__(self, connector):
        '''
        This class is responsible for all the graphics related
        aspects of the connector. It is an extension of the QGraphicsItem
        read more here: https://doc.qt.io/qt-5/qgraphicsitem.html
        connector: the object of the connector
        '''
        self.connector = connector
        super().__init__(connector.part.grNode)

        # all of these can be changed
        self.radius = 6.0
        self.outline_width = 1.0
        self._color_background = QColor("#4C000000")
        self._color_outline = QColor("#FF000000")
        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._brush = QBrush(self._color_background)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        '''
        Overrides the paint method of QGraphicsItem, this paints
        a ellipse to draw the connector on the widget.
        read more on the paint method here: https://doc.qt.io/qt-5/qgraphicsitem.html
        '''
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

    def boundingRect(self):
        '''
        Overrides the boundingRect method of QGraphicsItem, this
        builds a bounding rect which is then used to get the position of
        where the connector is on the screen.
        read more on the method here: https://doc.qt.io/qt-5/qgraphicsitem.html
        '''
        return QRectF(
            - self.radius - self.outline_width,
            - self.radius - self.outline_width,
            2 * (self.radius + self.outline_width),
            2 * (self.radius + self.outline_width),
        )
