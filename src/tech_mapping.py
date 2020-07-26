from min_terms_processor import MinTermsProcessor
import re

class TechMapper:
	sequence_gates_list =  []
	sequence_all_gates_list = [] 
	interim_nor_gates_list_exp = []
	size_list_inv = 0
	size_list_outer_input = 0		#(c+(b'+a)')' => c
	size_list_left_input	= 0	#(c+(b'+a)')' => b
	size_list_right_input = 0	#(c+(b'+a)')' => a
	size_list_inv_and_gates = 0
	circuit_count = 1
	
	def __init__(self, inp_expression):
		self.file = open("circuits.txt", "w")
		self.tech_map_process = MinTermsProcessor(None, 0, None)
		self.inp_expression_braces = self.tech_map_process.replace_braces_tags(inp_expression)
		self.external_inverters_list = []
		self.internal_inverters_list = []
		self.external_nor_gates_list = []
		self.semi_external_nor_gates_list = [] 
		self.internal_nor_gates_list = []
		#print("Minterms: "+ self.tech_map_process.countMinTermsInExpression(inp_expression_braces)) 
	
	'''
	 * @return Full file without being parsed to different categories of genetic gates
	 * @throws IOException
	 *
	'''
	def read_gates_lib(self):
		gates_lib_file = open("GatesLib1.txt", "r")
		self.file_content = ''.join([i for i in gates_lib_file.read().splitlines()])
		return self.file_content
	
	def finalize(self):
		self.file.close()
	
	'''
	 * @param input_gates_lib 
	 * 
	 * Take the input gates library file in the form of String. 
	 * It calls out intermediate method (to TechMapper class)
	 * and generate separate lists of genetic logic gates. 
	'''
	def parse_gates_lib(self, input_gates_lib):
	
		ext_inv = input_gates_lib[input_gates_lib.index("<Ext-Inverters>") + 15 : input_gates_lib.index("</Ext-Inverters>")]
		ext_inv = ext_inv[ext_inv.index("Out") + 3:]
		int_inv = input_gates_lib[input_gates_lib.index("<Int-Inverters>") + 15 : input_gates_lib.index("</Int-Inverters>")]
		ext_nor_gates = input_gates_lib[input_gates_lib.index("<Ext-NorGates>") + 14 : input_gates_lib.index("</Ext-NorGates>")]
		ext_nor_gates = ext_nor_gates[ext_nor_gates.index("Out") + 3:]
		semi_ext_nor_gates = input_gates_lib[input_gates_lib.index("<Semi-Ext-NorGates>") + 19 : input_gates_lib.index("</Semi-Ext-NorGates>")]
		int_nor_gates = input_gates_lib[input_gates_lib.index("<Int-NorGates>") + 14 : input_gates_lib.index("</Int-NorGates>")]
		
		self.external_inverters_list = self.generate_list_gates(ext_inv)
		self.internal_inverters_list = self.generate_list_gates(int_inv)
		self.external_nor_gates_list = self.generate_list_gates(ext_nor_gates)
		self.semi_external_nor_gates_list = self.generate_list_gates(semi_ext_nor_gates)
		self.internal_nor_gates_list = self.generate_list_gates(int_nor_gates)
		#print(self.external_nor_gates_list)
		
	
	'''
	 * @param parsedInputTake the parsed list of gates not arranged in the array lists. 
	 * @return ArrayLists containing the genetic gates
	'''
	 
	def generate_list_gates(self, parsed_input_string):
		input_list = []
		array = parsed_input_string.split(" END ")
		for i in range(len(array)):
			interim_list = [i for i in array[i].split("\t") if i]
			if interim_list:
				input_list.insert(i, interim_list)
		return input_list
	
	def generate_tree_expression(self):
		input_expression = self.inp_expression_braces
		interim_expression = input_expression
		SOP = "SOP1"
		EOP = "EOP1"
		min_terms = []
		interim_array = []
		count = self.count_sop_terms(input_expression, SOP) #search SOP1 terms first
		for i in range(1, count + 1):
			self.extract_nested_SOP_elements(interim_expression, SOP, EOP)
			SOP = "SOP1"
			EOP = "EOP1"
			interim_expression = input_expression[input_expression.index(EOP)+len(EOP) :]
	
	def extract_nested_SOP_elements(self, interim_expression, SOP, EOP):
		interim_array = []
		min_terms = [] 
		rx_list = []
		input_rx_list_wo_SOP = []
		interim_expression = interim_expression[interim_expression.index(SOP)+4: interim_expression.index(EOP)]
		pattern = re.compile("(?m)(.*?)\\+(SOP.*?$)")
		sop_min_terms = re.search(pattern, interim_expression)
		
		
		if sop_min_terms:
			min_terms.insert(0, sop_min_terms.group(1))
			min_terms.insert(1, sop_min_terms.group(2))
			SOP = "SOP"
			EOP = "EOP"
			for i in range(len(min_terms)):
				if SOP in min_terms[i]:
					self.extract_nested_SOP_elements(min_terms[i], SOP, EOP)
				else:
					rx_list = self.go_to_list(min_terms[i])
					self.size_list_outer_input = len(self.sequence_all_gates_list)
		
		else: #When none of the minterms contain SOP
			interim_array = interim_expression.split("+", 1)
			for j in range(len(interim_array)):
				min_terms.insert(j, interim_array[j])
			
			#print("in else", min_terms)
			self.interim_nor_gates_list_exp = self.gate_assignment(min_terms)
		#print("here", rx_list)
		
		if len(rx_list) > 0:
			#self.final_output_level(rx_list)		#for extracting single possible circuit
			#print("check1 : ", self.sequence_all_gates_list)
			self.final_output_multiple(rx_list)	#for extracting all possible circuits
			#print("check2 : ", self.sequence_all_gates_list)
			
			#remove inverter elements from self.sequence_gates_list
			check_inv_list = [] 
			inv_list =  []
			check_inv_list.extend(self.sequence_all_gates_list[0:self.size_list_inv])
			op_outer_gate_input = ""
			op_inner_left_input = ""
			op_inner_right_input = ""
			input1_inner_nor_gate = ""
			input2_inner_nor_gate = ""
			output_inner_nor_gate = ""
			input1_outer_nor_gate = ""
			input2_outer_nor_gate = ""
			count = 1
			double_check = []

			
			#Check the outer input i.e. i.e. from  (c+(b'+a)')'=> it checks the gates list of "c"
			for h in range(self.size_list_outer_input):
			
				op_outer_gate_input = self.sequence_all_gates_list[h][2]
				
				#Check the list of left inner inputs
				for i in range(self.size_list_left_input-self.size_list_outer_input):
				
					op_inner_left_input = self.sequence_all_gates_list[i+self.size_list_outer_input][2]

					#Check the list of right inner inputs
					for j in range(self.size_list_right_input - self.size_list_left_input):
					
						op_inner_right_input = self.sequence_all_gates_list[j+self.size_list_left_input][2]
						
						if op_inner_left_input != op_inner_right_input:
								#Check the list of intermediatte NOR gates i.e. from  (c+(b'+a)')'=> it checks for b'+a
								for k in range(self.size_list_inv_and_gates - self.size_list_right_input):								
									input1_inner_nor_gate = self.sequence_all_gates_list[k+self.size_list_right_input][0]
									input2_inner_nor_gate = self.sequence_all_gates_list[k+self.size_list_right_input][1]
									
									if ((op_inner_left_input == input1_inner_nor_gate or op_inner_left_input == input2_inner_nor_gate) and 
											(op_inner_right_input == input1_inner_nor_gate or op_inner_right_input == input2_inner_nor_gate)):
									
										output_inner_nor_gate = self.sequence_all_gates_list[k+self.size_list_right_input][2]
						
										for l in range(len(self.sequence_all_gates_list) - self.size_list_inv_and_gates):
											
												input1_outer_nor_gate = self.sequence_all_gates_list[l+self.size_list_inv_and_gates][0]
												input2_outer_nor_gate = self.sequence_all_gates_list[l+self.size_list_inv_and_gates][1]
												
												if ((output_inner_nor_gate == input1_outer_nor_gate or output_inner_nor_gate == input2_outer_nor_gate) and 
														(op_outer_gate_input == input1_outer_nor_gate or  op_outer_gate_input == input2_outer_nor_gate)):
												
													sequence_gates = []
													diagram2 = [] 
													
													#Adding circuit component of inner left input if it is not external input
													if self.sequence_all_gates_list[i+self.size_list_outer_input][0] != " ":
														sequence_gates.append(self.sequence_all_gates_list[i+self.size_list_outer_input])
													
													#Adding circuit component of inner Right input if it is not external input
													if self.sequence_all_gates_list[j+self.size_list_left_input][0] != " ":
														sequence_gates.append(self.sequence_all_gates_list[j+self.size_list_left_input])
													#Adding circuit component of intermediate NOR Gate
													sequence_gates.append(self.sequence_all_gates_list[k+self.size_list_right_input])
													
													#print("check 16: ", sequence_gates, k+self.size_list_right_input)
													#Adding the circuit component of outer NOR Gate
													sequence_gates.append(self.sequence_all_gates_list[self.size_list_inv_and_gates + l])
													
													#if(!double_check.contains(self.sequence_all_gates_list[self.size_list_inv_and_gates + l]))
													 #for 0x0B circuit
														#Checking if the input 1 of outer NOR gate is not external input. If not, then add it to include it 
														#in diagram2 of method construct_multiple_diagrams
													if self.sequence_all_gates_list[h][0] != " ":
														diagram2 = self.sequence_all_gates_list[h]
														self.construct_multiple_diagram(sequence_gates, count, diagram2)
														
													else:
														diagram2.insert(0, "null")
														self.construct_multiple_diagram(sequence_gates, count, diagram2)
														
													count += 1
													double_check.append(self.sequence_all_gates_list[self.size_list_inv_and_gates + l])		
												
												else:
													continue
									else:
										continue
	#this method is used to construct all possible circuits from the available components of library.
	def construct_multiple_diagram(self, sequence_gates, count, input1_outer_nor_gate):
		diagram = ""
		diagram2 = ""
		idx_d2 = 0
		length_d2 = 0
		protein = ""
		in1 = ""
		in2 = ""
		#print("check 15 : ", sequence_gates, count, input1_outer_nor_gate)
		#print("\n************************************** Genetic Circuit "+ count +" **************************************")
		#print("seq ", sequence_gates)
		for i in range(len(sequence_gates)):
			if "'" in sequence_gates[i][0]:
				in1 = sequence_gates[i][1]
				protein = sequence_gates[i][2]
				protein = protein.replace("P", "", 1)
				diagram = diagram + in1 + "-> (" + protein + ") ----|"

			else:			
				if sequence_gates[i][0] == "PTac" or sequence_gates[i][0] == "PTet" or sequence_gates[i][0] == "PBad":
					in1 = sequence_gates[i][1]
					in2 = sequence_gates[i][0]
					protein = sequence_gates[i][2]
					protein = protein.replace("P", "", 1)
					diagram = diagram + in1 + "-> " + in2 + "-> ("+ protein + ") ----|"	
				
				else:
					if sequence_gates[i-1][2] == sequence_gates[i][0]:
						in1 = sequence_gates[i][0]
						in2 = sequence_gates[i][1]
					
					elif sequence_gates[i-1][2] == sequence_gates[i][1]:
						in1 = sequence_gates[i][1]
						in2 = sequence_gates[i][0]
					
					protein = sequence_gates[i][2]
					protein = protein.replace("P", "", 1)
					diagram = diagram + in1 + "-> " + in2 + "-> ("+ protein + ") ----|"	
		
		diagram = diagram + "P" + protein + "-> " + "(YFP)"
		#print("\n" + diagram)
		
		if input1_outer_nor_gate[0] != "null":
			in1 = input1_outer_nor_gate[1]
			protein = input1_outer_nor_gate[2]
			protein = protein.replace("P", "", 1)
			diagram2 = diagram2 + in1 + "-> (" + protein + ")"
			
		self.check_circuit_diagram(count, diagram, diagram2, input1_outer_nor_gate)
		
		#print("\n***********************************************************************************************")
	
	def check_circuit_diagram(self, count, diagram, diagram2, input1_outer_nor_gate):
		first_prot = diagram[diagram.index("(") + 1: diagram.index(")")]
		first_prom = diagram[diagram.index("|") + 2: diagram.index("->", diagram.index("|"))] #+2 is added to exclude "P" in the name of promoters. 
		#print("check 12 : ", diagram)
		#print("check 13 : ", diagram2)
		#print("check 14 : ", first_prot)
		desired_prom = "P" + first_prot 	#Creating the name of desired promoter corresponding to "first Protein i.e. first_prot"
		
		
		diagram3 = ""
		if first_prot != first_prom: 
			diagram3 = diagram[0:diagram.index(")") + 1]
			diagram = diagram[diagram.index("|") + 1:]	#New main diagram
			idx = diagram.index(desired_prom)
			length = idx - len(diagram3)
			for i in range(length):
				diagram3 = diagram3 + "-"
			
			diagram3 = diagram3 + "--^"
		
		if diagram2:
			idx_d2 = diagram.index(input1_outer_nor_gate[2])
			length_d2 = idx_d2 - len(diagram2)
			for i in range(length_d2):
				diagram2 = diagram2 + "-"

			diagram2 = diagram2 + "--^"
		
		bad_solution = self.filter_bad_solutions (diagram, diagram2, diagram3)
		
		if not bad_solution:
			print("\n************************************** Genetic Circuit "+ str(self.circuit_count) +" **************************************")
			print("\n" + diagram)
			self.file.write("******************* Genetic Circuit "+ str(self.circuit_count) +" *****************\n")
			self.file.write("\n" + diagram)
	        
			if diagram2: 
				print(" 2 " ,diagram2)
				self.file.write("\n" + diagram2)
			if diagram3:
				print(" 3 " ,diagram3)
				self.file.write("\n" + diagram3)
			self.file.write("\n\n")
	        
			print("\n***********************************************************************************************")
			self.circuit_count += 1
		
	def filter_bad_solutions(self, diagram, diagram2, diagram3):
		prot_count = diagram.count("(")
		interim_diagram = diagram
		prot_main_diag = []
		# prot_diag2 = 
		prot_diag2 = ""
		prot_diag3 = ""
		# prot_diag3 = 
		
		bad_solution = False
		for i in range(prot_count - 1):		
			interm = interim_diagram[interim_diagram.index("("): interim_diagram.index(")") + 1]
			prot_main_diag.insert(i, interm)
			interim_diagram = interim_diagram[interim_diagram.index(")") + 1:]
		
		if diagram2:
				#prot_diag2.insert(diagram2[(diagram2.index("("), diagram2.index(")") + 1))
				prot_diag2 = diagram2[diagram2.index("("):diagram2.index(")") + 1]
			
		if diagram3:
			#prot_diag3.insert(diagram3[(diagram3.index("("), diagram3.index(")") + 1))
			prot_diag3 = diagram3[diagram3.index("("): diagram3.index(")") + 1]
		
		prot_main_diag_size = len(prot_main_diag)
		prot_diag_sub_size = prot_main_diag_size
		
		if prot_diag2 in prot_main_diag:
			bad_solution = True
		elif prot_diag3 in prot_main_diag:
			bad_solution = True
		else:
			for i in range(prot_main_diag_size):
				for j in range(1, prot_diag_sub_size):
					bad_solution = prot_main_diag[i] == prot_main_diag[i+j]
					if bad_solution:
						break
					elif j == prot_diag_sub_size - 1:
						prot_diag_sub_size = prot_diag_sub_size - 1 
						bad_solution = False
		return bad_solution
	
	

	def final_output_multiple(self, outer_not_gate_inputa): #for all possible combinations
		interim_list = []
		added_gate = []
		if len(outer_not_gate_inputa) == 1:#old: nor_gate_input_a[1].size() == 1
			if "PTac" in outer_not_gate_inputa[0][2] or "PTet" in outer_not_gate_inputa[0][2] or "PBad" in outer_not_gate_inputa[0][2]:
				#Call semi external gates lib
				if "PTac" in outer_not_gate_inputa[0][2]:
					interim_list.extend(self.semi_external_nor_gates_list[0:5])
				
				elif "PTet" in outer_not_gate_inputa[0][2]:
					interim_list.extend(self.semi_external_nor_gates_list[5:12])
				
				elif "PBad" in outer_not_gate_inputa[0][2]:
					interim_list.extend(self.semi_external_nor_gates_list[12:16])
				
				#Adding gates list in the sequence of all possible circuits
				self.sequence_all_gates_list.extend(self.interim_nor_gates_list_exp) 
				self.size_list_inv_and_gates = len(self.sequence_all_gates_list)
				
				#outerloop: 
				for i in range(len(self.interim_nor_gates_list_exp)):
					#innerloop:
					for j in range(len(interim_list)):
						if self.interim_nor_gates_list_exp[i][2] == interim_list[j][1]:		
							#matched
							#self.sequence_all_gates_list.append(gatesList[i])
							if interim_list[j][2] != self.interim_nor_gates_list_exp[i][1]:
								self.sequence_all_gates_list.append(interim_list[j])
							#break outerloop


		elif len(outer_not_gate_inputa) > 1:
		
			op_outer_input = ""
			op_interim_nor_gate_inp_exp = ""
			
			#Adding gates list in the sequence of all possible circuits
			self.sequence_all_gates_list.extend(self.interim_nor_gates_list_exp) 
			self.size_list_inv_and_gates = len(self.sequence_all_gates_list)

			
			for i in range(len(self.interim_nor_gates_list_exp)):
				for j in range(len(outer_not_gate_inputa)):
					op_outer_input = outer_not_gate_inputa[j][2]
					op_interim_nor_gate_inp_exp = self.interim_nor_gates_list_exp[i][2]
					
					if op_outer_input != op_interim_nor_gate_inp_exp:
						for k in range(len(self.internal_nor_gates_list)):
							if ((op_outer_input == self.internal_nor_gates_list[k][0] 
								or op_outer_input == self.internal_nor_gates_list[k][1]) and
								(op_interim_nor_gate_inp_exp == self.internal_nor_gates_list[k][0]
									or op_interim_nor_gate_inp_exp == self.internal_nor_gates_list[k][1])):
							
								if (self.internal_nor_gates_list[k][2] != self.interim_nor_gates_list_exp[i][0] and
										self.internal_nor_gates_list[k][2] != self.interim_nor_gates_list_exp[i][1]):
								
									if op_outer_input != self.interim_nor_gates_list_exp[i][0] and op_outer_input != self.interim_nor_gates_list_exp[i][1]:
									
										if self.internal_nor_gates_list[k] not in added_gate:									
											self.sequence_all_gates_list.append(self.internal_nor_gates_list[k])
											added_gate.append(self.internal_nor_gates_list[k])
					
					else:
						for m in range(len(self.internal_inverters_list)):
							if op_outer_input == self.internal_inverters_list[0]:
								self.sequence_all_gates_list.append(self.internal_inverters_list[m])
		#print("check 8 : ", self.sequence_all_gates_list)
		
	def go_to_list(self, min_term):
		output_list = [] 
		type = []
		element = []

		if "'" in min_term: # if this is inverted term
		
			if min_term == "a'": 
				
				output_list[0:0] = self.external_inverters_list[0: 4]
				self.sequence_all_gates_list.extend(output_list)
				#self.size_list_inv = len(self.sequence_all_gates_list)
			
			elif min_term == "b'":
				#output_list[0].set(0, "b'")
				output_list[0:0] = self.external_inverters_list[4: 6]
				self.sequence_all_gates_list.extend(output_list)
				#self.size_list_inv = len(self.sequence_all_gates_list)
			
			elif min_term == "c'": 
				output_list[0:0] = self.external_inverters_list[6: 9]
				self.sequence_all_gates_list.extend(output_list)
				#self.size_list_inv = len(self.sequence_all_gates_list)
			##print("check 3 : ", output_list, self.sequence_all_gates_list)
			
		else:	# if this is not inverted term
			##print("check 4 : ", output_list)
			output_list.insert(0, type)
			output_list[0].insert(0, "null")
			output_list[0].insert(1, "null")
			output_list[0].insert(2, "null")
			#output_list.insert(1, element)
			#output_list[1].insert(0, "null")
			##print("check 5 : ", output_list)
			if "a" in min_term:
				output_list[0][0] =  " "
				output_list[0][1] =  "a"
				#output_list[1].set(0, "PTac")
				output_list[0][2] = "PTac"
				self.sequence_all_gates_list.extend(output_list)
			
			elif "b" in min_term:
				output_list[0][0] =  " "
				output_list[0][1] =  "b"
				#output_list[1].set(0, "PTet")
				output_list[0][2] = "PTet"
				self.sequence_all_gates_list.extend(output_list)			
			
			elif "c" in min_term:
				output_list[0][0] =  " "
				output_list[0][1] = "c"
				#output_list[1].set(0, "PBad")
				output_list[0][2] = "PBad"
				self.sequence_all_gates_list.extend(output_list)
			##print("check 6 : ", output_list, self.sequence_all_gates_list)
		
		return output_list
	

	def gate_assignment(self, min_terms):
		interim_min_term_array = ["",""]
		min_term_l = min_terms[0]
		min_term_r = min_terms[1]
		min_term_array = min_terms[:]
		rx_list_l = []
		rx_list_r = []
		list_nor_gates = []
		interim_list = []
		
		nor_gate_type = ["", ""]
		
		if "'" in min_term_l:
			rx_list_l = self.go_to_list (min_term_l)
			self.size_list_left_input = len(self.sequence_all_gates_list)
			nor_gate_type[0] = "Int"
		
		else:
			rx_list_l = self.go_to_list(min_term_l)
			self.size_list_left_input = len(self.sequence_all_gates_list)
			nor_gate_type[0] = "Ext"
		
		if "'" in min_term_r:
			rx_list_r = self.go_to_list (min_term_r)
			self.size_list_right_input = len(self.sequence_all_gates_list)
			nor_gate_type[1] = "Int"
			
		else:
			rx_list_r = self.go_to_list (min_term_r)
			self.size_list_right_input = len(self.sequence_all_gates_list)
			nor_gate_type[1] = "Ext"
		
		#Assigning NOR Gates
		if nor_gate_type[0] == "Int" and nor_gate_type[1] == "Int":
			# call internal nor gates list
			gate_input1 = ""
			gate_input2 = ""
			left_t = ""
			right_t = ""
			interim_list.extend(self.internal_nor_gates_list)
			
			for left_term in range(len(rx_list_l)):
				for right_term in range(len(rx_list_r)):
					left_t = rx_list_l[left_term][2]
					right_t = rx_list_r[right_term][2]
					if left_t != right_t:
						#searchNorGates:
						for search_idx in range(len(interim_list)):
							gate_input1 = interim_list[search_idx][0]
							gate_input2 = interim_list[search_idx][1]							
							if ((left_t == gate_input1 or left_t == gate_input2)
								and (right_t == gate_input1 or right_t == gate_input2)):
									list_nor_gates.append(interim_list[search_idx])
									interim_list.remove(search_idx)
									#break searchNorGates
			
		elif nor_gate_type[0] == "Ext" and nor_gate_type[1] == "Ext":
			# call external nor gates list	
			if min_term_l == "a":
				if min_term_r == "b":
					interim_list.extend(self.external_nor_gates_list[0:5])
				
				elif min_term_r == "c":
					print("\nError: There are no gates available that can be integrated to implement the desired function.")
					#interim_list.extend(null)
					
			if min_term_l == "b":
				if min_term_r == "a":
					interim_list.extend(self.external_nor_gates_list[0: 5])
				
				elif min_term_r == "c":
					interim_list.extend(self.external_nor_gates_list[5: 8])			
				
			if min_term_l == "c":
				if min_term_r == "a":				
					print("\nError: There are no gates available that can be integrated to implement the desired function.")
					#interim_list.extend(null)
		
				elif min_term_r == "b":
					interim_list.extend(self.external_nor_gates_list[5: 8])	
			
			if "null" in interim_list:
				list_nor_gates.extend(interim_list)
			
		else: 
			# call semi external nor gates list
			#(Ptac)
			if "'" in min_term_l:
			
				if "PTac" in rx_list_r[0][2]:
					interim_list.extend(self.semi_external_nor_gates_list[0:5])

				elif "PTet" in rx_list_r[0][2]:
					interim_list.extend(self.semi_external_nor_gates_list[5:12])
				
				elif "PBad" in rx_list_r[0][2]:
					interim_list.extend(self.semi_external_nor_gates_list[12:16])					
					
				for inv in range(len(rx_list_l)):
					for gates in range(len(interim_list)):
						a = rx_list_l[inv][2]
						b = interim_list[gates][1]
						if a == b:
							list_nor_gates.append(interim_list[gates])
			
			elif  "'" in min_term_r:
			
				if "PTac" in rx_list_l[0][2]:
					interim_list.extend(self.semi_external_nor_gates_list[0:5])

				elif "PTet" in rx_list_l[0][2]:
					interim_list.extend(self.semi_external_nor_gates_list[5:12])
				
				elif "PBad" in rx_list_l[0][2]:
					interim_list.extend(self.semi_external_nor_gates_list[12:16])					
					
				for inv in range(len(rx_list_r)):
					for gates in range(len(interim_list)):
						a = rx_list_r[inv][2]
						b =interim_list[gates][1]
						if a == b:						
							list_nor_gates.append(interim_list[gates])
		##print("check 10: ", list_nor_gates)					
		return list_nor_gates

	def count_sop_terms(self, input_expression, searchSOP):
		count = 1
		#Count number of SOP1 terms
		array = input_expression.split("+", 1)
		while searchSOP in array[1]:
			input_expression = array[1][array[1].index(searchSOP)+4:]
			array = input_expression.split("+", 1)
			count += 1
		return count

	#this method is used to construct a single circuit similar to SBOL notation.
	def construct_diagram(self): 
		diagram = ""
		protein = ""
		in1, in2 = "", ""
		print("\n************************************** Genetic Circuit **************************************")
		for i in range(len(self.sequence_gates_list)):
			if "'" in self.sequence_gates_list[i][0]:
				in1 = self.sequence_gates_list[i][1]
				protein = self.sequence_gates_list[i][2]
				protein = protein.replace("P", "")
				diagram = diagram + in1 + "-> ("+ protein + ") ----|"
			
			else:
				if self.sequence_gates_list[i][0] == "PTac" or self.sequence_gates_list[i][0] == "PTet" or self.sequence_gates_list[i][0] == "PBad":
					in1 = self.sequence_gates_list[i][1]
					in2 = self.sequence_gates_list[i][0]
					protein = self.sequence_gates_list[i][2]
					protein = protein.replace("P", "")
					diagram = diagram + in1 + "-> " + in2 + "-> (" + protein + ") ----|"	
		
		diagram = diagram + "P" +  protein + "-> " + "(YFP)"
		print("\n" + diagram)
		
		print("\n*********************************************************************************************")
	
	def final_output_level(self, nor_gate_input_a):
		interim_list = []
		if len(nor_gate_input_a[1]) == 1:
			if "PTac" in nor_gate_input_a[1][0]  or "PTet" in nor_gate_input_a[1][0] or "PBad" in nor_gate_input_a[1][0]:
				#Call semi external gates lib
				if "PTac" in nor_gate_input_a[1][0]:
					interim_list.extend(self.semi_external_nor_gates_list[0: 5])
				
				elif "PTet" in nor_gate_input_a[1][0]:
					interim_list.extend(self.semi_external_nor_gates_list[5: 12])
				
				elif "PBad" in nor_gate_input_a[1][0]:
					interim_list.extend(self.semi_external_nor_gates_list[12: 16])				
				
				outer_loop = True
				for i in range(len(self.interim_nor_gates_list_exp)):
					if not outer_loop:
						break
					for j in range(len(interim_list)):
						if self.interim_nor_gates_list_exp[i][2] == interim_list[j][1]:
							#matched
							self.sequence_gates_list.append(self.interim_nor_gates_list_exp[i])
							self.sequence_gates_list.append(interim_list[j])
							outer_loop = False
							break
	
'''
expression1 = "(b'+(c+a')')'"
mapper = TechMapper(expression1)
libFile = mapper.read_gates_lib()
mapper.parse_gates_lib(libFile)
mapper.generate_tree_expression()
mapper.finalize()
'''								 
