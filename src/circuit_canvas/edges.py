from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from part_connector import *

class MyGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        '''
        This class is responsible for all the graphics related
        aspects of the Edge. It is an extension of the QGraphicsPathItem
        read more here: https://doc.qt.io/archives/qt-4.8/qgraphicspathitem.html
        edge: an edge connecting two circuit parts
        parent: parent graphic scene to
        '''
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
        '''
        set position of the source circuit part of edge
        '''
        self.posSource = [x, y]

    def setDestination(self, x, y):
        '''
        set position of the destination circuit part of edge
        '''
        self.posDestination = [x, y]

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        '''
        This paints the path between source and destination.
        '''
        self.updatePath()
        painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def updatePath(self):
        '''
        Updates the path between source and destination circuit part.
        It draws a bezier curve.
        More here: https://doc.qt.io/qtforpython/PySide2/QtGui/QPainterPath.html
        '''
        s = self.posSource
        d = self.posDestination
        dist = (d[0] - s[0]) * 0.5
        cpx_s, cpx_d = dist, -dist
        cpy_s, cpy_d = 0, 0
        is_left = self.edge.start_connector.is_left

        if (s[0] > d[0] and not is_left) \
            or (s[0] > d[0] and is_left):
            cpx_d *= -1
            cpx_s *= -1
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.cubicTo( s[0] + cpx_s, s[1] + cpy_s, d[0] + cpx_d, d[1] + cpy_d, self.posDestination[0], self.posDestination[1])
        self.setPath(path)


# class MyGraphicsEdgeBezier(MyGraphicsEdge):
#     def updatePath(self):
#         s = self.posSource
#         d = self.posDestination
#         dist = (d[0] - s[0]) * 0.5
#         cpx_s, cpx_d = dist, -dist
#         cpy_s, cpy_d = 0, 0
#         is_left = self.edge.start_connector.is_left

#         if (s[0] > d[0] and not is_left) \
#             or (s[0] > d[0] and is_left):
#             cpx_d *= -1
#             cpx_s *= -1
#         path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
#         path.cubicTo( s[0] + cpx_s, s[1] + cpy_s, d[0] + cpx_d, d[1] + cpy_d, self.posDestination[0], self.posDestination[1])
#         self.setPath(path)


class Edge:
    def __init__(self, scene, start_connector, end_connector):
        '''
        Class responsible for the edge connecting two connectors
        scene: Graphic Scene in which the edge is added
        start_connector: start connector corresponding to the source
        end_connector: end connector corresponding to the destination
        '''
        self.scene = scene
        self.start_connector = start_connector
        self.end_connector = end_connector

        self.start_connector.edge = self
        if self.end_connector is not None:
            self.end_connector.edge = self

        self.grEdge = MyGraphicsEdge(self)

        self.updatePositions()
        self.scene.grScene.addItem(self.grEdge)
        self.scene.addEdge(self)


    def updatePositions(self):
        '''
        Update position of source and destination connectors
        adjusts and sets the source and destination of the edge
        '''
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
        self.grEdge.update()


    def remove_from_connectors(self):
        '''
        Removes edge from the source and destination connector
        '''
        if self.start_connector is not None:
            self.start_connector.edge = None
        if self.end_connector is not None:
            self.end_connector.edge = None
        self.end_connector = None
        self.start_connector = None


    def remove(self):
        '''
        Removes the Edge
        '''
        self.remove_from_connectors()
        self.scene.grScene.removeItem(self.grEdge)
        self.grEdge = None
        try:
            self.scene.removeEdge(self)
        except ValueError:
            pass

