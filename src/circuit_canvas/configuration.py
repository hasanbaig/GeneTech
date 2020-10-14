#This file defines some configurations with respect to the
#drag drop of different circuit parts as well as how to
#transform the circuit into an expression.

#this converts each part to a string
OR_FORMAT = lambda x, y: f"({x} or {y})"
NOT_FORMAT = lambda x: f"~{x}"
AND_FORMAT = lambda x, y: f"({x} and {y})"
NAND_FORMAT = lambda x, y: f"({x} nand {y})"
NOR_FORMAT = lambda x, y: f"({x} nor {y})"
INPUT_OUTPUT_FORMAT = lambda x: x

#maps the part name to its format
GATE_FORMAT = {
    "OR": OR_FORMAT,
    "AND": AND_FORMAT,
    "NAND": NAND_FORMAT,
    "NOR": NOR_FORMAT,
    "NOT": NOT_FORMAT,
    "INPUT": INPUT_OUTPUT_FORMAT,
    "OUTPUT": INPUT_OUTPUT_FORMAT
}

#for drag drop: to check which part is dropped on the canvas
INPUT_GATE = 0
OUTPUT_GATE = 1
NOT_GATE = 2
OR_GATE = 3
AND_GATE = 4
NAND_GATE = 5
NOR_GATE = 6

