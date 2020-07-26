import re

class CostCalculator:
	def __init__(self, input_eq):
		self.__input_eq = input_eq
		input_eq = re.sub(" ", "", input_eq)
		input_eq = re.sub("'", "", input_eq)
		input_eq = re.sub("\\.", "", input_eq)	
		input_eq = re.sub("\\+", "", input_eq)
		input_eq = re.sub(re.escape("("), "", input_eq)
		input_eq = re.sub(re.escape(")"), "", input_eq)
		self.__cost = len(input_eq)
		self.__literals = input_eq		
	
	def get_cost(self):
		return self.__cost
	
	def get_literals(self):
		return self.__literals
		
'''
for i in range(3):
	eq = input("Enter Eq: ")
	calc = CostCalculator(eq)
	print(calc.get_cost())
	print(calc.get_literals())
'''