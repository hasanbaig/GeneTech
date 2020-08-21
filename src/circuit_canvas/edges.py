from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from part_connector import *

DEBUG = False        

class QDMGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)
        self.edge = edge
        self._color = QColor("#001000")
        self._color_selected = QColor("#00ff00")
        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)
        self._pen.setWidthF(2.0)
        self._pen_selected.setWidthF(2.0)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)
        self.posSource = [0, 0]
        self.posDestination = [200, 100]

    def setSource(self, x, y):
        self.posSource = [x, y]

    def setDestination(self, x, y):
        self.posDestination = [x, y]

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.updatePath()
        painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def updatePath(self):
        """ Will handle drawing QPainterPath from Point A to B """
        raise NotImplemented("This method has to be overriden in a child class")


class QDMGraphicsEdgeBezier(QDMGraphicsEdge):
    def updatePath(self):
        s = self.posSource
        d = self.posDestination
        dist = (d[0] - s[0]) * 0.5
        cpx_s, cpx_d = dist, -dist
        cpy_s, cpy_d = 0, 0 
        ss_pos = self.edge.start_connector.position
        
        if (s[0] > d[0] and ss_pos in (RIGHT_TOP, RIGHT_BOTTOM)) \
            or (s[0] > d[0] and ss_pos in (LEFT_BOTTOM, LEFT_TOP)):
            cpx_d *= -1
            cpx_s *= -1
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.cubicTo( s[0] + cpx_s, s[1] + cpy_s, d[0] + cpx_d, d[1] + cpy_d, self.posDestination[0], self.posDestination[1])
        self.setPath(path)

class Edge:
    def __init__(self, scene, start_connector, end_connector):

        self.scene = scene

        self.start_connector = start_connector
        self.end_connector = end_connector
        
        self.start_connector.edge = self
        if self.end_connector is not None:
            self.end_connector.edge = self

        
        self.grEdge = QDMGraphicsEdgeBezier(self)

        self.updatePositions()
        if DEBUG: print("Edge: ", self.grEdge.posSource, "to", self.grEdge.posDestination)
        self.scene.grScene.addItem(self.grEdge)
        self.scene.addEdge(self)
        
        
    def updatePositions(self):
        source_pos = self.start_connector.getConnectorPosition()
        
        source_pos[0] += self.start_connector.part.grNode.pos().x()
        source_pos[1] += self.start_connector.part.grNode.pos().y()
        self.grEdge.setSource(*source_pos)
        if self.end_connector is not None:
            end_pos = self.end_connector.getConnectorPosition()
            end_pos[0] += self.end_connector.part.grNode.pos().x()
            end_pos[1] += self.end_connector.part.grNode.pos().y() 
            self.grEdge.setDestination(*end_pos)
        else:
            self.grEdge.setDestination(*source_pos)
        if DEBUG: print(" SS:", self.start_connector)
        if DEBUG: print(" ES:", self.end_connector)
        self.grEdge.update()


    def remove_from_sockets(self):
        if self.start_connector is not None:
            self.start_connector.edge = None
        if self.end_connector is not None:
            self.end_connector.edge = None
        self.end_connector = None
        self.start_connector = None


    def remove(self):
        self.remove_from_sockets()
        self.scene.grScene.removeItem(self.grEdge)
        self.grEdge = None
        self.scene.removeEdge(self)
