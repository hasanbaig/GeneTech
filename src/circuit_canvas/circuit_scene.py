from window_graphics_scene import QDMGraphicsScene

class CircuitScene:
    def __init__(self):
        self.parts = []
        self.edges = []

        self.scene_width, self.scene_height = 4000, 4000

        self.initUI()

    def initUI(self):
        self.grScene = QDMGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def addNode(self, part):
        self.parts.append(part)

    def addEdge(self, edge):
        self.edges.append(edge)
    
    def clear(self):
        while len(self.parts) > 0:
            self.parts[0].remove()

    def removeNode(self, part):
        if part in self.parts: self.parts.remove(part)
        else: print("!W:", "Scene::removeNode", "wanna remove part", part, "from self.parts but it's not in the list!")

    def removeEdge(self, edge):
        if edge in self.edges: self.edges.remove(edge)
        else: print("!W:", "Scene::removeEdge", "wanna remove edge", edge, "from self.edges but it's not in the list!")
