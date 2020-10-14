from part_graphics import GraphicsPart
from part_widget import PartWidget
from part_connector import *
from configuration import *

class CircuitPart():
    def __init__(self, scene, part_type = "OR Gate",  inputs=[], outputs=[]):
        '''
        This is the class responsible for creating the parts of the circuit
        including Gates and Input/Output. This is more of an abstraction
        for different parts that comprise a circuit.
        scene: Graphics scene on which everything is drawn.
        part_type: title of the part. One of [OR Gate, AND Gate, NOR Gate, NOT Gate, NAND Gate, NOT Gate, INPUT, OUTPUT].
        inputs: list of input connectors on the left
        outputs: list of output connectors on the right
        '''
        self.scene = scene
        self.title = part_type
        self.part_name = part_type.split()[0]
        self.part_gate = PartWidget(self.part_name)

        #Each circuit part is either a gate or a node this attribute
        #keeps check of whether the expression of the node or gate is evaluated
        self.evaluated = False

        #grNode is basically the graphical part of the Circuit Part
        self.grNode = GraphicsPart(self)
        #add Circuit Part to the scene
        self.scene.addNode(self)
        #add graphical node corresponding to the part to the Graphical Scene
        self.scene.grScene.addItem(self.grNode)
        self.connector_spacing = 22

        # create connector for inputs and outputs
        self.inputs = []
        self.outputs = []

        #to check if it's input or output node
        inp_out = (len(outputs) + len(inputs)) == 1

        #To keep check of number of connectors for positioning a connector
        counter = 0
        for item in inputs:
            connector = Connector(part=self, index=counter, total = len(inputs), input_output = inp_out)
            counter += 1
            self.inputs.append(connector)

        #To keep check of number of connectors for positioning a connector
        counter = 0
        for item in outputs:
            connector = Connector(part=self, index=counter, total = len(outputs), is_left = False, input_output = inp_out)
            counter += 1
            self.outputs.append(connector)

    def evaluate_output(self):
        '''
        This function evaluates the output of the gate or node
        '''
        self.evaluated = False
        #Each circuit part is either a gate or a node
        #only evaluate if not previously evaluated
        if not self.evaluated:

            if self.part_name == "INPUT":
                self.gate_output = GATE_FORMAT[self.part_name](self.part_gate.input)
                self.evaluated = True
                return self.gate_output

            part1 = self.inputs[0].edge.start_connector.part.evaluate_output()
            if self.part_name == "OUTPUT" or self.part_name == "NOT":
                self.gate_output = GATE_FORMAT[self.part_name](part1)
                self.evaluated = True
                return self.gate_output
            else:
                #if not input/output/NOT gate then there is a second part
                part2 = self.inputs[1].edge.start_connector.part.evaluate_output()
                self.gate_output = GATE_FORMAT[self.part_name](part1, part2)
                self.evaluated = True
                return self.gate_output
        return self.gate_output

    def pos(self):
        '''
        position of the node
        '''
        return self.grNode.pos()

    def setPos(self, x, y):
        '''
        set position of the node
        x, y: desired position of the node
        '''
        self.grNode.setPos(x, y)

    def getConnectorPosition(self, index, total = 1, left = True, input_output = False):
        '''
        This function gets the position of the connector on the circuit part.
        index: connector number from top to bottom
        total: total number of connectors
        left: whether connector is on the left or right
        intput_output: True if Circuit part is not a gate
        '''
        x = 0 if left else self.grNode.width
        if input_output:
            return [0, self.grNode.height] if left else  [self.grNode.width, self.grNode.height]
        if total > 1:
            y = ((index+1) * self.grNode.height )/2 - 13.5*(index+1)
        else:
            y = self.grNode.height//2
        return [x, y]

    def updateConnectedEdges(self):
        '''
        If Circuit part is moved on the screen, this updates position of all the edges
        '''
        for connector in self.inputs + self.outputs:
            if connector.hasEdge():
                connector.edge.updatePositions()


    def remove(self):
        '''
        This function removes the node, graphical part of it,
        as well as edges corresponding to it.
        '''
        for connector in (self.inputs + self.outputs):
            if connector.hasEdge():
                connector.edge.remove()
        self.scene.grScene.removeItem(self.grNode)
        self.grNode = None
        self.scene.removeNode(self)
