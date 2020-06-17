import random
import numpy 
import pandas as pd
from min_terms_processor import MinTermsProcessor
from calculate_cost import CostCalculator
from scan_literals import ScanCommonLiterals

class ReduceExpression:
	input_expression = ""
	loop_count = 0
	process_expression_reduce = None
	process_rand_elements = None
	new_expression = ""
	expression_to_process = ""
	output_expression = ""
	total_min_terms = 0
	current_cost = 0
	new_cost = 0
	#************************* Control Switches for testing ************************* 
	__expand = False
	__force_expand = False
	__expand_prob = 0.6 # reduce self value to increase the chances of expansion
	
	
	#manual combination selector
	manual_sel_comb = False
	manual_comb = "M2M3"
	create__file = True
	# *******************************************************************************   
	
	def __init__(self, file = None):
		self.variables_in_exp = []
		self.arrays_literals_minterms = [[], []]
		self.var_count = 0
		columns = ["Iteration Count", "Input Expression", "Current Cost", "Expand ?\t", 
				"Expression to Process", "selected_rand_comb", "Rand El 1", "Rand El 2", "Matched Variable", 
				"Loop Reduced Expression", "law_replace", "New Expression", "New Cost\r"]
		self.file_data = pd.DataFrame(columns=columns)	
		self.file = self.file_data.to_csv('..\Debug.csv')
		#print("I am in REDUCE Constructor Class")
	
	# Main method to run the REDUCE procedure.
	def perform_reduction(self,  input_expression,  loop_count):
		self.process_expression_reduce = MinTermsProcessor(input_expression, 0, "")
		current_cost_calc = CostCalculator(input_expression)
		self.current_cost = current_cost_calc.get_cost()
		expression_to_process = input_expression
		law_replace = ""
		#Decide whether to expand or reduce minterms 
		#and paste it in reduce exp
		if self.__force_expand:
			expression_to_process = self.process_expression_reduce.expand_min_terms(input_expression)
		else:
			if random.random() > self.__expand_prob:
				#print("expandeddddd");
				expression_to_process = self.process_expression_reduce.expand_min_terms(input_expression) #Replace it with the same object of class E_expand_min_terms here.
				self.__expand = True
			else:
				self.__expand = False
				
		result = self.process_expression_reduce.replace_braces_tags(expression_to_process)
		#print("RESULT reduce ", result)
		total_min_terms = self.process_expression_reduce.count_min_terms_expression(result)
		current_min_terms = self.process_expression_reduce.generate_min_terms_array(result, total_min_terms)
		#print("TOTAL; current: ", total_min_terms, current_min_terms)
		current_min_terms_ids = ["M"+str(i) for i in range(len(current_min_terms))] #Generating the list of minterms IDs
		##print("\nMinterim_strings IDs: "+ Arrays.to(self, current_min_terms_ids))
		possible_combinations = self.__generate_possible_combs(current_min_terms_ids)
		#print(possible_combinations)
		##print("Size of Possible combinations: "+possible_combinations.size())
		selected_rand_comb = ""
		rand_el_comb =  ["", "", ""]
		matched_variable = "" 
		loop_reduced_expression = ""
		if total_min_terms > 1:		
			#Selecting a random combination of minterms to check 
			rand_comb_idx = self.rand_mt_comb_id(possible_combinations)
			##print("\nRandom Combination Idx: "+rand_comb_idx)
			
			#Extracting random combination and its repective minterms
			#Manual selection of random minterms
			if self.manual_sel_comb:
				rand_comb_idx = possible_combinations.index(manual_comb)
				
			rand_el_comb = self.obtain_rand_mt(possible_combinations, rand_comb_idx, current_min_terms)
			selected_rand_comb = rand_el_comb[2]
			#print("\nRandom Combination: "+rand_el_comb[2])
			#print("\nRandom minterim_string 1: "+rand_el_comb[0])
			#print("\nRandom minterim_string 2: "+rand_el_comb[1])
			#sequence 7 of Reduce: Scan common literal
			self.process_rand_elements = ScanCommonLiterals(rand_el_comb[0], rand_el_comb[1])
			self.process_rand_elements.execute_scan_literals(rand_el_comb[0], rand_el_comb[1])
			matched_variable = self.process_rand_elements.matched_var
			reduced_rand_el_mt0 = self.process_rand_elements.reduced_rand_el1
			reduced_rand_el_mt1 = self.process_rand_elements.reduced_rand_el2
			self.arrays_literals_minterms[0] = self.process_rand_elements.arrays_literals_minterms[0]
			self.arrays_literals_minterms[1] = self.process_rand_elements.arrays_literals_minterms[1]
			
			# Sequence 8 of REDUCE: searching single literals in both minterms
			single_lit_mts = self.search_single_lit_mt(self.arrays_literals_minterms[0]) and self.search_single_lit_mt(self.arrays_literals_minterms[1])
			##print("\nsingle_lit_mt: "+ single_lit_mts)
			
			# Sequence 9 of REDUCE: if single minterim_string is present, then process
			man_reduced_rand_el_mt0, man_reduced_rand_el_mt1 = "", ""
			if single_lit_mts:
				#print("HERE in single MT")
				law_replace = self.process_expression_reduce.scan_rules(self.arrays_literals_minterms[0][0] + "+" + self.arrays_literals_minterms[1][0])
			else:
				#print(rand_el_comb)
				self.process_rand_elements.execute_scan_literals(rand_el_comb[0], rand_el_comb[1])
				matched_variable = self.process_rand_elements.matched_var
				man_reduced_rand_el_mt0 = self.process_rand_elements.reduced_rand_el1
				man_reduced_rand_el_mt1 = self.process_rand_elements.reduced_rand_el2
				self.arrays_literals_minterms[0] = self.process_rand_elements.arrays_literals_minterms[0]
				self.arrays_literals_minterms[1] = self.process_rand_elements.arrays_literals_minterms[1]
			
			#print("STEP 1 output checking : "+ " " + matched_variable+ " " + man_reduced_rand_el_mt0+ " " + man_reduced_rand_el_mt1+ " " + "".join(self.arrays_literals_minterms[0])+ " " + "".join(self.arrays_literals_minterms[1]))
			
			##print("\nLaw replace: "+law_replace)
			
			# Sequence 10 of REDUCE: find reduced expression before applying replacement rules
			loop_reduced_expression = self.find_reduced_expression(matched_variable, man_reduced_rand_el_mt0, man_reduced_rand_el_mt1)
			if loop_reduced_expression:
				law_replace = loop_reduced_expression
			##print("\nloop_reduced_expression: "+loop_reduced_expression)

			# Sequence 11 of REDUCE: replacement rules implementation 
			if loop_reduced_expression:
				law_replace = self.replaced_law(loop_reduced_expression, matched_variable)
			
			#print("STEP 2 output checking : " + " " + loop_reduced_expression + "law: " + law_replace)
			
			# Sequence 12 of REDUCE: Deleting elements from the array of minterms and inserting  reduced elements
			if len(law_replace) != 0:
				next_min_terms = self.delete_el_mt_array(current_min_terms, selected_rand_comb)
				next_min_terms.append(law_replace)
			else:
				next_min_terms = current_min_terms[:]
			
			# Sequence 13 of REDUCE: Constructing  expression
			new_expression = ""
			new_expression = self.__construct_new_expression(next_min_terms, new_expression)
			##print("\nNew _expression: "+_expression) 
			
			# Sequence 14 of REDUCE: Calculate the cost of  expression
			new_cost_calc =  CostCalculator(new_expression)
			self.new_cost = new_cost_calc.get_cost()
			##print("\nNew Cost: "+_cost)
		
		else:
			new_expression = input_expression
			new_cost_calc = CostCalculator(new_expression)
			self.new_cost = new_cost_calc.get_cost()
		
		output_expression = new_expression
		
		self.__write_date([loop_count, input_expression, self.current_cost, self.__expand, 
						expression_to_process, selected_rand_comb, rand_el_comb[0], rand_el_comb[1],
						matched_variable, loop_reduced_expression, law_replace, new_expression,
						self.new_cost])
		
		return output_expression
	
	# ******************* Methods ********************* #
	
	def __write_date(self, data):
		#print(len(self.file_data.columns), len(data))
		assert len(self.file_data.columns) == len(data)
		self.file_data.loc[len(self.file_data)] = list(data)
		self.file = self.file_data.to_csv("..\Debug.csv")
		
	def __construct_new_expression(self, next_min_terms,  new_expression):
		new_expression += '+'.join(next_min_terms)
		return new_expression
	
	# The following method generate the list of possible input combinations of minterms
	# in the expression. 
	def __generate_possible_combs(self, min_terms_ids):
		possible_combinations = []
		for i in range(len(min_terms_ids)):
			for j in range(0, len(min_terms_ids)-i-1):
				possible_combinations.append(str(min_terms_ids[i]) + str(min_terms_ids[i+1+j]))
		return possible_combinations
	
	# The following method extracts the list of variables used in the input expression
	def extract_variable(self, inp_exp):	
		current_exp_cost =  CostCalculator(inp_exp)
		literals_only = current_exp_cost.get_literals()
		self.variables_in_exp = list(set([i for i in literals_only]))
		self.var_count = len(self.variables_in_exp)
		return self.variables_in_exp
	
	# The following method randomly select the combination of minterms
	def rand_mt_comb_id(self,  possible_combinations):
		return random.choice(list(range(len(possible_combinations))))
	
	# The following method extracts the random combination IDs and then the respective
	# elements to be compared **** Switch to select specific combination is here ****
	def obtain_rand_mt (self,  possible_combinations,  rand_comb_idx, current_min_terms):
		rand_idx =  possible_combinations[rand_comb_idx][1:].split("M")
		#print(rand_comb_idx, rand_idx)
		rand_el_comb = [current_min_terms[int(i)].replace(" ", "") for i in rand_idx]
		rand_el_comb.append(possible_combinations[rand_comb_idx])
		return rand_el_comb
	
	#The following method test if minterms contain only one literal
	def search_single_lit_mt(self, array_lit_mt):
		single_lit_mt = False
		if not array_lit_mt[-1]:
			del array_lit_mt[-1]		
		if len(array_lit_mt) == 1:
			single_lit_mt = True
		return single_lit_mt
	
	# The following method find reduce expression before applying replacement rules
	def find_reduced_expression (self, matched_variable, reduced_rand_el_mt0, reduced_rand_el_mt1):
		initial_reduced_expression = ""
		if matched_variable:
			if matched_variable == reduced_rand_el_mt0 and reduced_rand_el_mt0 == reduced_rand_el_mt1:
				initial_reduced_expression = ""
			else:
				initial_reduced_expression = matched_variable + "(" +reduced_rand_el_mt0 + "+" +reduced_rand_el_mt1 + ")"
				initial_reduced_expression = initial_reduced_expression.replace(" ", "")
		return initial_reduced_expression
	
	# This method extracts subminterms from reduced expression and give the law after replacement
	def replaced_law(self,  loop_reduced_expression,  matched_variable):
		interim_string = loop_reduced_expression[len(matched_variable) : ]
		interim_string = self.process_expression_reduce.replace_braces_tags(interim_string)
		after_sop_tag = self.process_expression_reduce.split_two(interim_string, "SOP1")
		if "SOP1" in interim_string:
			interim_string = after_sop_tag[1]
		else:
			interim_string = after_sop_tag[0]
		before_eop_tag = self.process_expression_reduce.split_two(interim_string, "EOP1")
		interim_string = before_eop_tag[0]
		
		count_sub_min_terms = self.process_expression_reduce.count_min_terms_expression(interim_string)
		sub_min_terms_array = self.process_expression_reduce.generate_min_terms_array(interim_string, count_sub_min_terms)
		
		#generating minterm Ids
		sub_min_terms_ids = self.generate_min_terms_ids(len(sub_min_terms_array))
		sub_possible_comb = self.__generate_possible_combs(sub_min_terms_ids)
		
		for i in range(len(sub_min_terms_array)):
			interim_string = self.process_expression_reduce.scan_rules(sub_min_terms_array[i])
			
			if self.process_expression_reduce.rule_matched:
				loop_reduced_expression = loop_reduced_expression.replace(sub_min_terms_array[i], interim_string, 1)
			else:
				loop_reduced_expression = loop_reduced_expression
			sub_min_terms_array[i] = interim_string
		
		# finding if any minterm contain braces
		sub_el_brace = False
		idx_brace = []
		#Find if any minterim_string contains braces
		for i in range(len(sub_min_terms_array)):
			if "(" in sub_min_terms_array[i]:
				sub_el_brace = True
				idx_brace.append(i)
		if sub_el_brace:
			for i in range(len(idx_brace)):
				#implement Seq 11 of Reduce. 11TT2.T.0.0.
				sub_min_term_el = sub_min_terms_array[idx_brace[i]]
				interim_string = sub_min_term_el[sub_min_term_el.index("(") + 1 :]
				##print("\nIntinterim_stringediate: "+interim_string)
				to_replace = interim_string[0: interim_string.index(")")] # changed here
				#implement Seq 11 of Reduce. 11TT2.T.0.1
				replaced_rule = self.process_expression_reduce.scan_rules(to_replace)
				
				if self.process_expression_reduce.rule_matched == False:
					replaced_law = sub_min_term_el
				else:
					replaced_law = rules_replacer(sub_min_term_el, to_replace, replaced_rule)				
				sub_min_terms_array[idx_brace[i]] = replaced_law
			loop_reduced_expression = self.sub_expression_reducer(sub_min_terms_array, matched_variable, sub_possible_comb)
		else:
			loop_reduced_expression = self.sub_expression_reducer(sub_min_terms_array, matched_variable, sub_possible_comb)
			#last check
		#Seq Reduce 11.T.T.3
		if "(" in loop_reduced_expression:
			before_brace = self.process_expression_reduce.split_two(loop_reduced_expression, "(")
			
			if ")" in before_brace[1]:			
				after_brace = self.process_expression_reduce.split_two(loop_reduced_expression, "(")
				if after_brace[0] == "1" or after_brace[0] == "0" or after_brace[0] == "":
					law_replace = loop_reduced_expression.replace("("+after_brace[0]+")", "")
				else:
					law_replace = loop_reduced_expression
			law_replace = loop_reduced_expression
		law_replace = loop_reduced_expression
		return law_replace
	
	# The following method is used to generate minterm IDS
	def generate_min_terms_ids(self, number_mts):
		sub_min_terms_ids = ["M"+str(i) for i in range(number_mts)]
		return sub_min_terms_ids
	
	# The following method is used to reduce subexpression. REDUCE 11of15, Seq T2T1
	def sub_expression_reducer (self, sub_min_terms_array,  matched_variable,  sub_possible_comb):
		idx = 0
		while True:
			if sub_possible_comb and idx < len(sub_possible_comb):
				rand_el_comb = self.obtain_rand_mt(sub_possible_comb, idx, sub_min_terms_array)
			rand_comb = rand_el_comb[2]
			
			rand_el1 = self.process_expression_reduce.scan_rules(rand_el_comb[0])
			rand_el2 = self.process_expression_reduce.scan_rules(rand_el_comb[1])
			
			self.process_rand_elements.execute_scan_literals(rand_el_comb[0], rand_el_comb[1])
			
			reduced_rand_el1 = self.process_rand_elements.reduced_rand_el1
			reduced_rand_el2 = self.process_rand_elements.reduced_rand_el2
			matched_var = self.process_rand_elements.matched_var
		
			new_expression = ""
			if matched_var:
				new_expression = ""
				interim_string = reduced_rand_el1 + "+" + reduced_rand_el2
				interim_string = self.process_expression_reduce.scan_rules(interim_string)
				if len(interim_string) > 2:
					interim_string = "("+"interim_string"+")"
				else:
					if interim_string == "1":
						interim_string = ""
				if interim_string:
					interim_string = matched_var + interim_string
				else:
					interim_string = matched_var
				interim_string = self.process_expression_reduce.scan_rules(interim_string)
				next_min_terms_array = self.delete_el_mt_array(sub_min_terms_array, rand_comb)
				next_min_terms_array.append(interim_string)
				idx = 0
				# jugad
				new_expression = self.create_exp(new_expression, next_min_terms_array)
				
				sub_min_terms_array = next_min_terms_array[:]
				sub_possible_comb = self.__generate_possible_combs(self.generate_min_terms_ids(len(next_min_terms_array)))					
			
			else:
				
				interim_string = self.process_expression_reduce.scan_rules(rand_el1 + "+" +rand_el2)
				
				if (self.process_expression_reduce.rule_matched):
					next_min_terms_array = self.delete_el_mt_array(sub_min_terms_array, rand_comb)
					next_min_terms_array.append(interim_string)
					idx = 0
					new_expression = self.create_exp(new_expression, next_min_terms_array)
					
					##print(next_min_terms_array)
					sub_min_terms_array = next_min_terms_array[:] 
					sub_possible_comb = self.__generate_possible_combs(self.generate_min_terms_ids(len(next_min_terms_array)))
					#print("check3 ", new_expression)
				else:
					new_expression = ""
					next_min_terms_array = sub_min_terms_array[:]
					new_expression = self.create_exp(new_expression, next_min_terms_array)
					#print("check4 ", new_expression)
					idx = 0	#idx += 1
			if not ((len(sub_possible_comb) - 1 != idx) and sub_possible_comb): #(sub_possible_comb.size() -1 != idx)
				break
		#print("check5 ", new_expression, matched_variable)
		
		if new_expression != "1":
			new_expression = matched_variable + "(" + new_expression + ")"
		else:
			new_expression = matched_variable
		return new_expression 

	def delete_el_mt_array(self, sub_min_terms_array,  rand_comb):
		next_min_terms_array = sub_min_terms_array[:]
		##print("\nrand_comb: "+rand_comb)
		##print("\nNextMinTinterim_stringsArray: "+next_min_terms_array)
		#Remove x of combination MxMy 
		del next_min_terms_array[int(rand_comb[3])]
		#Remove y of combination MxMy 
		del next_min_terms_array[int(rand_comb[1 : len(rand_comb) - 2])]
		return next_min_terms_array 

	def create_exp(self,  new_expression,  next_min_terms_array):
		new_expression += "+".join(next_min_terms_array)
		return new_expression
	
	#Rule replacer 
	def rules_replacer(self, law_to_replace,  to_replace,  replaced_rule):
		interim_string = law_to_replace.replace(to_replace, replaced_rule, 1)
		idx = interim_string.index(replaced_rule)
		interim_string = interim_string.replace(interim_string[idx-1], ' ', 1)
		idx = interim_string.index(replaced_rule)
		interim_string = interim_string.replace(interim_string[idx + len(replaced_rule)], ' ')
		if replaced_rule == "0" or replaced_rule == "1":
			replaced_law = interim_string.replace(replaced_rule, " ")
		else:
			replaced_law = interim_string		
		return replaced_law