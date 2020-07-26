import re
from min_terms_processor import MinTermsProcessor

class NotNorConverter: 
	def __init__(self):
		self.__nor_not_processor = MinTermsProcessor("", 0.0, "")
	
	# most high level method for converting expression into NOR/NOT form
	def convert_into_not_nor(self, input_expression):
		output = input_expression
		print("not - nor - start: ", output)
		# if expression contains braces
		if self.search_brace_term(input_expression):
			#break minterm around + sign
			#First convert braces into SOP tags. 
			#Count and catch SOP1 (high level braces) terms are in the expression
			brace_indices = self.count_brace_indices(input_expression)
			#print("brace: ", brace_indices)
			for i in range(len(brace_indices)):
				interim_string = input_expression[brace_indices[i] + 1:]
				inside_braces = interim_string[:interim_string.index(")")]
				min_terms_inside_braces = self.split_plus_func(inside_braces)
				
				#search and process ANDed minterm inside braces
				min_terms_inside_braces = self.search_proccess_and_terms(min_terms_inside_braces)	
				#Convert OR terms to NAND
				if len(min_terms_inside_braces) > 1:
					exp_inside_braces = self.process_or_term(min_terms_inside_braces)
					output = output.replace(inside_braces, exp_inside_braces)
				else:
					exp_inside_braces = self.__nor_not_processor.min_terms_expression(min_terms_inside_braces)
					output = output.replace(inside_braces, exp_inside_braces)
				
				#print("inside for ", inside_braces, exp_inside_braces, output, min_terms_inside_braces)
				# Check if the terms inside braces contains NANDed terms (without having + sign in it)
				if "+" not in exp_inside_braces:
					if exp_inside_braces[exp_inside_braces.index("]") + 1] == "'":
						nand_to_or = self.process_nand_term(exp_inside_braces)
						print("output : " + nand_to_or);

					output = output.replace(exp_inside_braces, nand_to_or)
					
					
				else: # if it contains multiple terms
					interim_string = exp_inside_braces
					exp_inside_braces = exp_inside_braces[exp_inside_braces.index("[")+1: exp_inside_braces.index("]")]
					min_terms_inside_braces = self.split_plus_func(exp_inside_braces)
					min_terms_inside_braces = self.search_proccess_and_terms(min_terms_inside_braces)
					newExpInsideBraces = self.__nor_not_processor.min_terms_expression(min_terms_inside_braces)
					output = output.replace("(["+exp_inside_braces+"]')", "("+newExpInsideBraces+")'")
				
			
		else:
			#if there are no braces, then proceed further here.
			if "+" in input_expression:
				minterms = self.split_plus_func(input_expression)
				minterms = self.search_proccess_and_terms(minterms)
				output = self.__nor_not_processor.min_terms_expression(minterms)
			else:
				output = self.process_and_term(output)
			
		
		#processing terms outside braces
		output = output.replace("[", "(")
		output = output.replace("]", ")")
		result = self.__nor_not_processor.replace_braces_tags(output) 
		#print("result not nor ", result)
		current_min_terms = self.__nor_not_processor.generate_min_terms_array(
											result,
											self.__nor_not_processor.count_min_terms_expression(result)
											)
		
		for i in range(len(current_min_terms)):
			current_min_terms[i] = self.__nor_not_processor.replace_tags_braces(current_min_terms[i])
			#print("current min NOT", current_min_terms[i])
			brace_indices = self.count_brace_indices (current_min_terms[i])
			#print("brace", brace_indices)
			interim_string= current_min_terms[i]
			if len(brace_indices) == 1:		# if brace term is present
				interim_string = self.__nor_not_processor.replace_braces_tags(interim_string)
				multiplier = interim_string.replace(interim_string[interim_string.index("SOP1"): interim_string.index("EOP1")+4], "")
				multiplicand = interim_string[interim_string.index("SOP1"):]
				if len(multiplier) and multiplier!="'":
					interim_string= multiplier.replace("'", "")
					if len(interim_string) == 1:
						if "'" in multiplier:
							multiplier = multiplier.replace("'", "")
						else:
							multiplier = multiplier + "'"
					else:
						print("\nThe multiplier contains more than 1 literals")
					#print("multiiiiiiiiii ", multiplicand)
					interim_string = multiplicand[multiplicand.index("EOP1")+4:]
					
					if interim_string == "'":
						multiplicand = multiplicand[0: multiplicand.index("EOP1")+4]
					else:
						multiplicand = multiplicand + "'"	
					multiplicand = self.__nor_not_processor.replace_tags_braces(multiplicand)
					current_min_terms [i] = "("+ multiplier + "+" + multiplicand + ")'"
				
			else:			# if minterim_string do not contain braces
				current_min_terms[i] = self.process_and_term(current_min_terms[i])
			'''
				if(current_min_terms[i].length()>2)
					current_min_terms[i] = process_and_term(current_min_terms[i])
				else
					current_min_terms[i] = process_and_term(current_min_terms[i])
			'''
		
		if len(current_min_terms) > 1:
			output = self.__nor_not_processor.min_terms_expression(current_min_terms)
		else:
			output = ''.join(current_min_terms).replace("[", "").replace("]", "")
		
		output = output.replace("[", "(")
		output = output.replace("]", ")")
		#print(output)
		return output
	


	def search_proccess_and_terms(self, min_terms_inside_braces):
		n = len(min_terms_inside_braces)
		for j in range(n):
			if len(min_terms_inside_braces[j]) > 1: #may be ANDed terms
				if min_terms_inside_braces[j][1:] == "'": #Not term e.g a'
					if len(min_terms_inside_braces[j])>2: # e.g. a'b
						min_terms_inside_braces[j] = self.process_and_term(min_terms_inside_braces[j]) #pass the minterim_string to process AND term
					else:
						continue 
				else:
					min_terms_inside_braces[j] = self.process_and_term(min_terms_inside_braces[j]) #pass the minterim_string to process AND term
					'''
					if len(min_terms_inside_braces[j]) > 2:
						min_terms_inside_braces[j] = self.process_and_term(min_terms_inside_braces[j]) #pass the minterim_string to process AND term
					else:	
						min_terms_inside_braces[j] = self.process_and_term(min_terms_inside_braces[j]) #pass the minterim_string to process AND term
					'''
		return min_terms_inside_braces
	
	
	
	#rest of the methods.
	def process_nand_term(self, exp_inside_braces):
		exp_inside_braces = exp_inside_braces.replace("[", "", 1)
		exp_inside_braces = exp_inside_braces.replace("]'", "", 1)
		array_literals_minterms = self.__nor_not_processor.extract_literals_min_terms([], exp_inside_braces)
		#print("NAND : ", array_literals_minterms, exp_inside_braces)
		for i in range(len(array_literals_minterms)):
			if "'" in array_literals_minterms[i]:
				new_element = array_literals_minterms[i].replace("'", "")
			else:
				new_element = array_literals_minterms[i] + "'"
			if i == 0:
				interim_string = new_element
			else:
				interim_string = interim_string + "+" + new_element
		return interim_string

	#Count number of SOP tags
	def count_brace_indices(self, exp_with_braces): 
		brace_indices = []
		exp_with_braces = self.__nor_not_processor.replace_braces_tags(exp_with_braces)
		start = 0
		while start < len(exp_with_braces):
			try:
				idx_brace = exp_with_braces.index("SOP1", start)
				start = idx_brace + 4
				brace_indices.append(idx_brace)
			except:
				break
		return brace_indices
	
	def search_brace_term (self, input_expression):
		contain_brace_term = "(" in input_expression
		return contain_brace_term
	
	#Arrange minterm inside braces in a separate array
	def split_plus_func(self, input_expression):
		split_plus = input_expression.split("+")
		return split_plus
	
	def process_and_term(self, current_min_terms):
		array_literals_minterms = self.__nor_not_processor.extract_literals_min_terms([], current_min_terms)
		for i in range(len(array_literals_minterms)):
			if "'" in array_literals_minterms[i]:
				new_element = array_literals_minterms[i].replace("'", "")
			else:
				new_element = array_literals_minterms[i] + "'"
			if i == 0:
				interim_string = new_element
			else:
				interim_string = interim_string+ "+" + new_element
		interim_string = "[" + interim_string+ "]'" 	
		return interim_string
	
	def process_or_term(self, min_terms_inside_braces):
		n = len(min_terms_inside_braces)
		new_element  = ""
		interim_string = ""
		if n > 1:
			for i in range(n):
				if "'" in min_terms_inside_braces[i][len(min_terms_inside_braces[i]) - 1:]: #extracting last character.
					new_element = min_terms_inside_braces[i][:len(min_terms_inside_braces[i]) - 1]
				else:
					new_element = min_terms_inside_braces[i] + "'"
				if i == 0:
					interim_string = new_element
				else:
					interim_string = interim_string + new_element
			interim_string = interim_string.replace("[", "(")
			interim_string = interim_string.replace("]", ")")
			#print("interim string " + interim_string)
			# search for ( and bring the multiplier before (, instead of after ).
			#Extracting multiplier first. searching and replacing brace terms () with "".
			#Can process upto 1 braced term only.
			self.__nor_not_processor.result = interim_string
			multiplier = interim_string.replace(interim_string[interim_string.index("("):interim_string.index(")")+1], "")
			multiplicand = interim_string[interim_string.index("(")+1: interim_string.index(")")]
			#print("mult : ", multiplicand, multiplier)
			
			count_min_terms = self.__nor_not_processor.count_min_terms_expression(multiplicand)
			current_min_terms = self.__nor_not_processor.generate_min_terms_array (multiplicand, count_min_terms)
			##print("current count : ", current_min_terms, count_min_terms)
			
			interim_string = self.expand_min_terms(current_min_terms, multiplier, multiplicand)
			#print("INTERIMFINAL ", interim_string)
			interim_string = "[" + interim_string + "]'"
		return interim_string
		
	#This method is used by a class NotNorConverter
	def expand_min_terms(self, current_min_terms, multiplier, multiplicand):
		output_min_terms = ["" for i in range(len(current_min_terms))]
		
		for i in range(len(current_min_terms)):
			if "1" in current_min_terms[i]:
				current_min_terms[i] = ""
			elif "(" in multiplier:
				interim_string = multiplier
				exp_inside_multiplier = interim_string[interim_string.index("(") + 1:interim_string.index(")")]
				count_min_terms = self.__nor_not_processor.count_min_terms_expression(exp_inside_multiplier)
				min_terms_multiplier = self.__nor_not_processor.generate_min_terms_array(exp_inside_multiplier, count_min_terms)
				output_min_terms[i] = self.expand_min_terms(min_terms_multiplier, current_min_terms[i], exp_inside_multiplier)
			else:
				output_min_terms[i] = self.__nor_not_processor.scan_rules(multiplier + current_min_terms[i])				
				#print("TERM : ", multiplier + " " + current_min_terms[i], output_min_terms[i])
		
		expanded_min_terms = self.__nor_not_processor.min_terms_expression(output_min_terms)
		
		if "0" in expanded_min_terms:
			expanded_min_terms = re.sub("(.?){0,1}(0)(.?){0,1}", "", expanded_min_terms)
		#print("TERM expand : ", expanded_min_terms)
		return expanded_min_terms 
	

"""
a = "b(ac+a')"
n = NotNorConverter()
print(n.convert_into_not_nor(a)) # (b'+(a'+c)')'

a = "ab+abc+bc'a"
n = NotNorConverter()
print(n.convert_into_not_nor(a)) # (a'+b')'+(a'+b'+c')'+(b'+c+a')'
"""