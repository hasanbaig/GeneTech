from part_graphics import QDMGraphicsPart
from part_widget import PartWidget
from part_connector import *

class CircuitPart():
    def __init__(self, scene, type = "OR Gate",  inputs=[], outputs=[]):
        self.scene = scene

        self.title = type
        
        self.part_gate = PartWidget(type.split()[0]) 
        
        self.grNode = QDMGraphicsPart(self)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)


        self.connector_spacing = 22

        # create socket for inputs and outputs
        self.inputs = []
        self.outputs = []
        
        counter = 0
        for item in inputs:
            connector = Connector(part=self, index=counter, position=LEFT_BOTTOM, total = len(inputs))
            counter += 1
            self.inputs.append(connector)

        counter = 0
        for item in outputs:
            socket = Connector(part=self, index=counter, position=RIGHT_TOP, total = len(outputs))
            counter += 1
            self.outputs.append(connector)

    @property
    def pos(self):
        return self.grNode.pos()        # QPointF
    def setPos(self, x, y):
        self.grNode.setPos(x, y)

    def getConnectorPosition(self, index, position, total = 1):
        x = 0 if (position in (LEFT_TOP, LEFT_BOTTOM)) else self.grNode.width

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # start from bottom
            if total > 1:
                y = self.grNode.height - self.grNode.edge_size - self.grNode._padding - index * self.connector_spacing - 14
            else:
                y = self.grNode.height - self.grNode.edge_size - self.grNode._padding - index * self.connector_spacing - 23
        else:
            # start from top
            if total > 1:
                y = self.grNode.title_height + self.grNode._padding + self.grNode.edge_size + index * self.connector_spacing 
            else:
                y = self.grNode.title_height + self.grNode._padding + self.grNode.edge_size + index * self.connector_spacing + 24
        return [x, y]

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()

