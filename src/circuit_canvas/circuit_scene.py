from window_graphics_scene import MyGraphicsScene

class CircuitScene:
    def __init__(self):
        '''
        This class is responsible for all the graphics related
        aspects of the Circuit
        '''
        self.parts = []
        self.edges = []
        self.scene_width, self.scene_height = 4000, 4000
        self.initUI()

    def initUI(self):
        self.grScene = MyGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def addNode(self, part):
        '''
        Adds the circuit part to the scene
        part: A Circuit Part
        '''
        self.parts.append(part)

    def addEdge(self, edge):
        '''
        Adds the edge belonging to a circuit part to the scene
        edge: An edge connecting two circuit parts
        '''
        self.edges.append(edge)

    def clear(self):
        '''
        Clears the circuit scene.
        '''
        while len(self.parts) > 0:
            self.parts[0].remove()

    def removeNode(self, part):
        '''
        Removes the part from the circuit scene
        part: Circuit Part
        '''
        if part in self.parts: self.parts.remove(part)
        else: print("part not in the list")

    def removeEdge(self, edge):
        '''
        Removes the edge from the circuit scene
        edge: An edge connecting two circuit parts
        '''
        if edge in self.edges: self.edges.remove(edge)
        else: print("edge not in the list")

    def addDragEnterListener(self, callback):
        '''
        Event listener for dragging a part which triggers a callback
        '''
        self.grScene.views()[0].addDragEnterListener(callback)

    def addDropListener(self, callback):
        '''
        Event listener for dropping a part which triggers a callback
        '''
        self.grScene.views()[0].addDropListener(callback)
