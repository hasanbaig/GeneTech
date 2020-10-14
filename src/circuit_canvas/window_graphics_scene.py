import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MyGraphicsScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        '''
        This class extends the QGraphicsScene class in PyQT5 and
        is responsible for all the graphics related
        aspects of the entire scene, that is the canvas.
        This here deals primarily with the background.
        more on the class here: https://doc.qt.io/qt-5/qgraphicsscene.html
        '''
        super().__init__(parent)
        self.scene = scene
        #the background grid color can be changed here
        self.setBackgroundBrush(QColor(200, 200, 200))


    def save(self, filename):
        '''
        To capture the entire circuit and save it at {filename}.
        It does so by creating a master rect which is a boundary
        containing all objects on the Graphic Scene.
        '''
        self._master_rect = self.itemsBoundingRect()
        self._master_rect.adjust(-20, -20, 20, 20)
        width = int(self._master_rect.width())
        height = int(self._master_rect.height())

        image = QImage(width, height, QImage.Format_ARGB32_Premultiplied)
        painter = QPainter(image)

        # Render the region of interest to the QImage.
        self.render(painter, QRectF(image.rect()), self._master_rect)
        painter.end()

        # Save the image to the speficied filename.
        image.save(filename)

    def setGrScene(self, width, height):
        '''
        Sets the scene width and height, this is basically the height
        and width of the canvas that we see on screen.
        '''
        self.setSceneRect(-width // 2, -height // 2, width, height)

    # the drag events won't be allowed until dragMoveEvent is overriden
    def dragMoveEvent(self, event):
        pass

    # draws the background of the graphics scene
    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
