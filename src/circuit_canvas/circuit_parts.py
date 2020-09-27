from part_graphics import GraphicsPart
from part_widget import PartWidget
from part_connector import *

OR_FORMAT = lambda x, y: f"({x} or {y})"
NOT_FORMAT = lambda x: f"~{x}"
AND_FORMAT = lambda x, y: f"({x} and {y})"
NAND_FORMAT = lambda x, y: f"({x} nand {y})"
NOR_FORMAT = lambda x, y: f"({x} nor {y})"
INPUT_OUTPUT_FORMAT = lambda x: x

GATE_FORMAT = {
    "OR": OR_FORMAT,
    "AND": AND_FORMAT,
    "NAND": NAND_FORMAT,
    "NOR": NOR_FORMAT,
    "NOT": NOT_FORMAT,
    "INPUT": INPUT_OUTPUT_FORMAT,
    "OUTPUT": INPUT_OUTPUT_FORMAT
}
class CircuitPart():
    def __init__(self, scene, part_type = "OR Gate",  inputs=[], outputs=[]):
        self.scene = scene

        self.title = part_type
        self.part_name = part_type.split()[0]
        self.part_gate = PartWidget(self.part_name )
        self.evaluated = False
        self.grNode = GraphicsPart(self)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)


        self.connector_spacing = 22

        # create socket for inputs and outputs
        self.inputs = []
        self.outputs = []

        #to check if it's input or output node
        inp_out = (len(outputs) + len(inputs)) == 1

        counter = 0
        for item in inputs:
            connector = Connector(part=self, index=counter, total = len(inputs), input_output = inp_out)
            counter += 1
            self.inputs.append(connector)

        counter = 0
        for item in outputs:
            connector = Connector(part=self, index=counter, total = len(outputs), is_left = False, input_output = inp_out)
            counter += 1
            self.outputs.append(connector)

    def evaluate_output(self):
        self.evaluated = False
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
                part2 = self.inputs[1].edge.start_connector.part.evaluate_output()
                self.gate_output = GATE_FORMAT[self.part_name](part1, part2)
                self.evaluated = True
                return self.gate_output
        return self.gate_output

    @property
    def pos(self):
        return self.grNode.pos()

    def setPos(self, x, y):
        self.grNode.setPos(x, y)

    def getConnectorPosition(self, index, total = 1, left = True, input_output = False):
        x = 0 if left else self.grNode.width

        if input_output:
            return [0, self.grNode.height] if left else  [self.grNode.width, self.grNode.height]
        if total > 1:
            y = ((index+1) * self.grNode.height )/2 - 13.5*(index+1)
        else:
            y = self.grNode.height//2
        return [x, y]

    def updateConnectedEdges(self):
        for connector in self.inputs + self.outputs:
            if connector.hasEdge():
                connector.edge.updatePositions()


    def remove(self):
        for connector in (self.inputs + self.outputs):
            if connector.hasEdge():
                connector.edge.remove()
        self.scene.grScene.removeItem(self.grNode)
        self.grNode = None
        self.scene.removeNode(self)


"""
c+a'b' = a'bc + a'b'c + ab'c + a'b'c
 720
"""
