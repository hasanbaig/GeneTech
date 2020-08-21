import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class QDMGraphicsScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super().__init__(parent)
        
        self.scene = scene
        # settings
        self.gridSize = 20
        self.gridSquares = 5

        self._color_light = QColor("#2f2f2f")
        self._color_dark = QColor("#292929")

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

#       self.scene_width, self.scene_height = 4000, 4000
#       self.setSceneRect(-self.scene_width//2, -self.scene_height//2, self.scene_width, self.scene_height)
    
        self.setBackgroundBrush(QColor("#D3D3D3"))

    
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
        self.setSceneRect(-width // 2, -height // 2, width, height)

    # the drag events won't be allowed until dragMoveEvent is overriden
    def dragMoveEvent(self, event):
        pass


    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
    