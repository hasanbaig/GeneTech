from not_nor_converter import NotNorConverter
from lv_interface import LVInterface
from scan_literals import ScanCommonLiterals
from calculate_cost import CostCalculator
from reduce_expression import ReduceExpression
from file_writer import FileWriter
from tech_mapping import TechMapper
from simulated_annealing import SimulatedAnnealing
from min_terms_processor import MinTermsProcessor

def process(inputBoolExp = None):
	inputInterface = LVInterface()
	#inputBoolExp = " IPTG'.aTc.Arabinose'+IPTG'.aTc.Arabinose+IPTG.aTc.Arabinose"
	if not inputBoolExp:
		inputBoolExp = "IPTG'.aTc'.Arabinose'+IPTG.aTc'.Arabinose'+IPTG.aTc.Arabinose'"
	inputProt = ["IPTG", "aTc", "Arabinose"]
	inputInterface.set_original_input_names(inputProt)	
	inputInterface.take_inputs(inputBoolExp)
	#print("Original Inputs: " + inputProt)
	#print("Original Equation: " + inputBoolExp)	
	newInputEq = inputInterface.replace_input_eq_with_new_names(inputInterface.replace_input_names())
	newInputEq1 = inputInterface.replace_input_eq_with_original_names(newInputEq)
	
	#print("New Expressions: " + newInputEq)

	print("***************************************************************************\n")
	print("Input Expression is: " + inputBoolExp)
	print("\n***************************************************************************")
	print("LV Expression is: " + newInputEq)
	print("\n***************************************************************************")
	
	# Calling method to run simulated annealing algorithm
	initTemp = inputInterface.initial_temp 		#10.0
	tempCoeff = inputInterface.temp_coeff 	#0.90
	timeToRun = inputInterface.time_to_run	#0.030	#0.5
	writeFile = open("Data.txt", "w")
	SimAnneal = SimulatedAnnealing(tempCoeff, initTemp, timeToRun, newInputEq)
	SimAnneal.minimise_expression()
	bestSolution = SimAnneal.best_solution()
	print("Optimized Expression: " + bestSolution)
	print("New Cost: " + str(SimAnneal.best_solution_cost))
	writeFile.write(SimAnneal.best_solution())
	writeFile.write("\n" + str(SimAnneal.best_solution_cost))	

	outExp = ""
	
	# *********************** Test block for NorNot converter ***********************
	inputExp = bestSolution #"c'(ab+b')"
	processExpression = MinTermsProcessor ("", 0, "")
	convertExp = NotNorConverter()
	outputString = convertExp.convert_into_not_nor(inputExp)
	print("best Solution", inputExp)
	print("Synthesized Expression into NOT-NOR Form: "+outputString)
	print(outputString == "(a+b'+c)'+(a+b'+c')'+(a'+b'+c')'")
	writeFile.write("\n" + outputString)
	
	# *********************************************************************
	
	newOrigEq = inputInterface.replace_input_eq_with_original_names(outputString)
	print("New Expression with input proteins: "+newOrigEq)
	writeFile.write("\n"+ newOrigEq)
	# Technology Mapping
	
	mapGatesOnExpression = TechMapper(outputString)
	libFile = mapGatesOnExpression.read_gates_lib()
	mapGatesOnExpression.parse_gates_lib(libFile)

	
	mapGatesOnExpression.generate_tree_expression()
	mapGatesOnExpression.finalize()
	
def output_checker(fname1 = "circuits.txt", fname2 = None):
	if not fname2:
		fname2 = "C:/Users/SANYA/genetech/Src/circuits_java.txt"
	f1 = open(fname1, "r")
	f2 = open(fname2, "r")
	lines1 = f1.readlines()
	lines2 = f2.readlines()
	try:
		assert len(lines1) == len(lines2)
	except:
		print(len(lines1), len(lines2))
	assert lines1 == lines2
	print("passed")
'''
main()
output_checker()
'''