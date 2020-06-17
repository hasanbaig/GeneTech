import math
import random
from calculate_cost import CostCalculator
from reduce_expression import ReduceExpression
import time 


class SimulatedAnnealing:
	def __init__(
		self,
		temp_coef,
		init_temp,
		time_to_run,
		input_expression
	):
		"""
		Implementation of the simulated annealing algorithm. We start with a given state, find
		all its neighbors. Pick a random neighbor, if that neighbor improves the solution, we move
		in that direction, if that neighbor does not improve the solution, we generate a random
		real number between 0 and 1, if the number is within a certain range (calculated using
		temperature) we move in that direction, else we pick another neighbor randomly and repeat the process.

		Args:
			input_expression: The input circuit to be optimised.
			init_temp: Initial temperature.
			time_to_run: Time in seconds to run the algorithm.
			temp_coef: the rate at which the temperate decreases in each iteration.
			
		Returns the minimised circuit.
		"""
		self.__temp_coef = temp_coef
		self.__init_temp = init_temp
		self.__time_to_run = time_to_run
		self.__input_expression = input_expression
		self.__best_solution = input_expression #The current best solution
		self.best_solution_cost = CostCalculator(input_expression).get_cost()
		
	def minimise_expression(self):
		current_time = 0 #current time in seconds
		start_time = time.time()
		expression_reducer = ReduceExpression()
		current_string = self.__input_expression
		count = 0
		current_temp = self.__init_temp
		
		while current_time < self.__time_to_run:
			current_temp = current_temp * self.__temp_coef
			new_string = expression_reducer.perform_reduction(current_string, count)
			current_cost = expression_reducer.current_cost
			new_cost = expression_reducer.new_cost
			#print(new_string)
			if new_cost < current_cost:
				current_string = new_string
				current_cost = new_cost
			else:
				acceptance_prob = math.exp(-(new_cost - current_cost)/current_temp)
				if acceptance_prob > random.random():
					current_string = new_string
					current_cost = new_cost
			current_time = self.__get_time(start_time)
			count += 1
		print("run count : ", count)
		self.__best_solution = current_string
		self.best_solution_cost = current_cost
	
	def __get_time(self, start_time):
		end_time = time.time()
		return end_time - start_time
	
	def best_solution(self):
		return self.__best_solution