from window_graphics_scene import QDMGraphicsScene

class CircuitScene:
    def __init__(self):
        self.nodes = []
        self.edges = []

        self.scene_width, self.scene_height = 4000, 4000

        self.initUI()

    def initUI(self):
        self.grScene = QDMGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)


    def removeNode(self, node):
        self.nodes.remove(node)

    def removeEdge(self, edge):
        self.edges.remove(edge)
