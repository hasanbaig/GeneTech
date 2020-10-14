import re
import random

class MinTermsProcessor:
	def __init__(self, inp_exp = None, sel_rand_idx = 0, out_exp = None):
		self.__input_expression = inp_exp
		self.__current_expression = inp_exp
		self.__sel_rand_idx = sel_rand_idx
		self.__sop_indices = dict() #dictionary containing pair of (start:end) indices
		self.__multiplicand, self.__multiplier = "", ""
		self.output_expression = out_exp
		self.rule_matched = False

	def expand_min_terms(self, inp_exp = None):
		if not inp_exp and not self.__input_expression:
			#print("please enter an input expression")
			return -1
		self.__input_expression = inp_exp if inp_exp else self.__input_expression
		string  = self.__input_expression
		self.__get_sop_indices(string)
		random_sop_idx = random.choice(list(self.__sop_indices.keys())) if len(self.__sop_indices) > 1 else -1
		#print("random index", random_sop_idx)
		#for random_sop_idx in self.__sop_indices.keys():
		if random_sop_idx != -1:
			random_sop_idx = (random_sop_idx, self.__sop_indices[random_sop_idx])
			self.__expand_sop_tag(self.__current_expression, random_sop_idx)
			print(self.__multiplicand, self.__multiplier)
			min_terms_count = self.count_min_terms_expression(self.__multiplicand)
			current_min_terms = self.generate_min_terms_array(self.__multiplicand, min_terms_count)
			print(current_min_terms)
			self.output_expression = self.expand_min_terms_array(current_min_terms)
		else:
			self.output_expression = string
		return self.output_expression

	#gets SOP indices in form of dictionary containing pair of start and end of SOP
	def __get_sop_indices(self, inp_exp = None):
		string = inp_exp if inp_exp else self.__input_expression
		self.__current_expression = self.replace_braces_tags(string)
		string = self.__current_expression
		for i in range(0, len(string) - 4):
			if "SOP" == string[i:i+3]:
				##print(string[i:i+4])
				start_sop = i
				brace_number = int(string[i+3])
				#print(self.__current_expression, brace_number)
				end_sop = string.index("EOP"+str(brace_number), start_sop)
				#print((start_sop, end_sop))
				#print(self.__sop_indices)
				self.__sop_indices.update([(start_sop, end_sop)])

	#repalces braces with tags
	def replace_braces_tags(self, expression = None):
		if self.__input_expression is None:
			self.__input_expression = expression.replace(" ", "")
		string = self.__input_expression

		if expression:
			string = expression
		#print("replace", string)
		brace_count = 0
		if "(" not in string and ")" not in string:
			return string
		i = 0
		while i < len(string):
			var = string[i]
			if var == "(":
				brace_count += 1
				string = string.replace("(", "SOP" + str(brace_count), 1)
			elif var == ")":
				string = string.replace(")", "EOP" + str(brace_count), 1)
				brace_count -= 1
			i += 1
		self.__current_expression = string
		return string

	# This method replace the SOP/EOP tags present in the expression
	# with braces.
	# Input: takes the input expression with tags -
	# Output: throws the expression without tags -
	def replace_tags_braces(self, input_expression):
		##print("\nExpression with Tags: "+input_expression)
		expanded_expression = input_expression
		if expanded_expression:
			##print(input_expression)
			expanded_expression = re.sub("(SOP)([0-9]+)", "(", expanded_expression)
			##print(expanded_expression)
			expanded_expression = re.sub("(EOP)([0-9]+)", ")", expanded_expression)
			##print(expanded_expression)
		##print("\nExpression without Tags: "+expanded_expression)
		return expanded_expression

	def __expand_sop_tag(self, string, sop_idx):
		start, end = sop_idx #start and end index of SOP
		multiplier = string[:start]
		#print("Method expand_sop_tag\n string: " + string)
		#print("Initial Multplier : " + multiplier)
		multiplicand = string[start + 4 : end]
		#print("Initial Multplicand : " + multiplicand)
		multiplier = multiplier.split("+")[-1]
		#print("Final Multplier : " + multiplier)
		self.__multiplier = multiplier
		self.__multiplicand = multiplicand

	def count_min_terms_expression(self, expression):
		original_expression = expression
		EOP = "EOP"
		idx = 0
		count_min_terms = 0					#Counter for minterms
		#To check the pattern of SOP1,SOP2, SOP3, and so on.
		pattern = re.compile("(SOP)([0-9]+)")
		while idx != -1 :
			try:
				idx = expression.index("+")
			except:
				idx = -1
			#If there is no + sign left in the string.
			if idx != -1:
				#split multiplicand into two halves around "+"
				split_multiplicand = expression.split("+", 1)
				#Creating a matcher object and search the "pattern" in the left side of multiplicand
				matcher = re.search(pattern, split_multiplicand[0])
				#print("\nidx: "+ str(idx))
				#print("\nFirst Multiplicand: " + split_multiplicand[0] +
				#				   "\nSecond Multiplicand: " +split_multiplicand[1])
				#If SOP with any digit is found in the left side of multiplicand, then
				if matcher:
					#print("in find\n ")
					#Concatenate the digit of SOP with the string EOP
					EOP += matcher.group(2)
					#print(matcher.group(2))
					#print(EOP)
					#Find the index of EOP[digit] in right side of multiplicand
					try:
						idx = split_multiplicand[1].index(EOP)
					except:
						idx = -1
					#If the above EOP is present, then extract rest of the string after EOP[digits]
					if idx != -1:
						expression = split_multiplicand[1][idx + len(EOP):]
						#print(expression)
						if "+" in expression and expression[0] != "+":
							expression = expression[expression.index("+"):]

					#Increase Min Terms counter
					count_min_terms += 1

				else:
					#If SOP with any digit is not found in the left side of multiplicand, then
					#Check if there is any + sign left in the multiplicand string
					#a'bc+bSOP1a'c'+acEOP1
					try:
						idx = expression.index("+")
					except:
						idx = -1
					#print("\nidx in else: "+ str(idx))
					#if neither SOP is present in the left multiplicand nor it is empty, then increase
					#min terms counter
					if len(split_multiplicand[0]):
						count_min_terms += 1
					#Assign only right multiplicand to main multiplicand string
					expression = split_multiplicand[1]
				EOP = "EOP"
			else: # if there is no + signs in the multiplicand string

				if len(expression) and expression != "'":
					count_min_terms += 1
		#print("\nTotal Minterms: "+str(count_min_terms))
		return count_min_terms

	#---------- This method generates the array of minterms -----------#
	# It takes the expression (or multiplicand) and the total number of
	# multiplicands calculated from previous method, and arranges all of
	# them in an array. It also assign unique IDs to each minterm.
	# Input: multiplicand expression (with Tags) -
	# Input: total number of minterms present in multiplicand - int
	# Output: generate minterms array
	def generate_min_terms_array(self, input_exp, count_min_terms):
		EOP = "EOP"
		SOP = "SOP"
		bar = ""
		idx = 0 #Holds index to check if anything exist in multiplicand string
		#To check the pattern of SOP1,SOP2, SOP3, and so on.
		pattern = re.compile("(SOP)([0-9]+)")
		current_min_terms = [""] * count_min_terms
		#print("expression MT generate : ", input_exp)
		for i in range(count_min_terms):
			bar = ""
			#Split multiplicand into two halves around "+"
			split_multiplicand = input_exp.split("+", 1)
			#Creating a matcher object and search the "pattern" in the left side of multiplicand
			matcher = re.search(pattern, split_multiplicand[0])
			#matcher = pattern.match(split_multiplicand[0])
			if matcher:
				SOP = "SOP" + matcher.group(2)
				##print("\nSOP: "+SOP)
				split_multiplicand[0] = split_multiplicand[0].replace(SOP, "(", 1)
				#print("\n****split_multiplicand[0]: "+split_multiplicand[0])
				split_multiplicand[0] = re.sub("(SOP)([0-9]+)", "(", split_multiplicand[0])
				#print("\n****split_multiplicand[0]: "+split_multiplicand[0])
				split_multiplicand[0] = re.sub("(EOP)([0-9]+)", ")", split_multiplicand[0])
				##print("\n****split_multiplicand[0] replace EOP: "+split_multiplicand[0])
				split_multiplicand[0] = split_multiplicand[0].replace(" ", "")
				EOP = "EOP" + matcher.group(2)
				#print(SOP, EOP)
				#print("\n\n****split_multiplicand[1] : "+split_multiplicand[1])
				split_multiplicand[1] = split_multiplicand[1].replace(EOP, ")", 1)
				#print(split_multiplicand[1])
				#print("\n\n****split_multiplicand[1] : "+split_multiplicand[1])
				if i != count_min_terms - 1:
					bar = split_multiplicand[1][split_multiplicand[1].index(")") + 1 : split_multiplicand[1].index(")") + 2]
				else:

					bar = split_multiplicand[1][split_multiplicand[1].index(")") + 1 :]
				bar = bar.replace(" ", "")
				if bar == "'":
					split_multiplicand2 = split_multiplicand[1].split(")'", 1)
				else:
					split_multiplicand2 = split_multiplicand[1].split(")", 1)
				##print("\n\n****split_multiplicand2[0] : "+split_multiplicand2[0]+"    split_multiplicand2[1] : "+split_multiplicand2[1])
				split_multiplicand2[0] = re.sub("(SOP)([0-9]+)", "(", split_multiplicand2[0])
				##print("\n****split_multiplicand2[0] : "+split_multiplicand2[0])
				split_multiplicand2[0] = re.sub("(EOP)([0-9]+)", ")", split_multiplicand2[0])
				split_multiplicand2[0] = split_multiplicand2[0].replace(" ", "")
				##print("\n****split_multiplicand2[0] : "+split_multiplicand2[0])
				##print("\nsplit_multiplicand2[1]: "+split_multiplicand2[1])
				##print("\nsplit_multiplicand2[1].substring(0, 1).contentEquals("+"): "+split_multiplicand2[1].charAt(0))
				input_exp = split_multiplicand2[1]
				if split_multiplicand2[1]:
					input_exp = split_multiplicand2[1] if split_multiplicand2[1][0] != "+" else split_multiplicand2[1][1:]
				##print("\ninpuExp: "+inp_exp)
				if bar == "'":
					current_min_terms[i] = split_multiplicand[0] + "+" + split_multiplicand2[0] + ")'"
				else:
					current_min_terms[i] = split_multiplicand[0] + "+" + split_multiplicand2[0] + ")"
			else:
				##print("split_multiplicand.length: "+ len(split_multiplicand))
				if not split_multiplicand[0]:
					current_min_terms[i] = split_multiplicand[1]
				else:
					current_min_terms[i] = split_multiplicand[0]
				if len(split_multiplicand) > 1:
					input_exp = split_multiplicand[1]
		#print("min terms array:")
		#print(current_min_terms)
		return current_min_terms

	# This method multiplies the multiplier with all minterms of multiplicand
	# and expand it in the form of expression.
	# Input: array of minterms - string array
	# Output: global output outExp
	def expand_min_terms_array(self, current_min_terms):
		output_min_terms = [""]*len(current_min_terms)
		for i in range(len(current_min_terms)):
			if "1" in current_min_terms[i]:
				current_min_terms[i] = ""
			output_min_terms[i] = self.scan_rules(self.__multiplier + current_min_terms[i])


		##print(output_min_terms)
		expanded_min_terms = self.min_terms_expression(output_min_terms)

		search_expression = self.__multiplier + "SOP1" + self.__multiplicand + "EOP1"
		##print("\nSearch Expression: "+search_expression)

		expanded_expression = self.__current_expression
		expanded_expression = expanded_expression.replace(search_expression, expanded_min_terms) #replaceFirst(search_expression, expanded_min_terms)

		##print("\nexpanded_expression "+expanded_expression)
		expanded_expression = self.replace_tags_braces(expanded_expression)
		#print("\nexpanded_expression "+expanded_expression)
		return expanded_expression

	# This method takes the minterms array and transformed it into expression
	#  E.g. a(b+c) => ab + ac
	# Input: Array of minterms -  array
	# Output: expanded expression -
	def min_terms_expression(self, input_min_terms):
		expanded_min_terms = '+'.join(input_min_terms)
		##print("\nExpanded Minterms: "+expanded_min_terms)
		return expanded_min_terms

	# This method scans for rules
	# Input: takes the input multiplicand to scanl for laws -
	# Output: output the replaced expression -
	def scan_rules(self, inp_exp):
		local_inp_exp = inp_exp
		variable = local_inp_exp
		replaced_rule = local_inp_exp
		ones = False
		variable = re.sub("1|\\+|0", "", variable)

		if variable:
			variable = variable[0]

		if "1" in local_inp_exp:
			break_around_one = local_inp_exp.split("1", 1)
			##print("\nbreak_around_one: "+Arrays.to(break_around_one))
			break_around_one[0] = break_around_one[0].replace(" ", "")
			##print("\nbreak_around_one length: "+break_around_one[0].length())
			if len(break_around_one[0]):
				break_around_one[0] = break_around_one[0][len(break_around_one[0]) - 1]

			break_around_one[1] = break_around_one[1].replace(" ", "")

			if len(break_around_one[1]):
				break_around_one[1] = break_around_one[1][0]
			if (break_around_one[0] == "+" or break_around_one[1] == "+") or (break_around_one[0]=="" and break_around_one[1]==""):
				ones = True
		#Replacing rules (defined in x) with the variable present in the current expression
		rules_variables = self.generate_rules_variable(variable)
		if ones:
			replaced_rule = "1"
			self.rule_matched = True
		else:
			for _rule in rules_variables.keys():
				if _rule == local_inp_exp:
					replaced_rule = rules_variables[_rule]
					self.rule_matched = True
					break
		##print("\nReplaced Rule: "+replaced_rule)
		return replaced_rule

	# This method replaces the standard variable x with the variable being used in
	# the current expression, and returns the dictionary of rules in that variable.
	# Input: Takes the variable of expression to replaced the standard laws with
	# that variable -
	# Output: dictionary of rules in the form of input varibale.
	def generate_rules_variable(self, variable = None):
		standard_rules = {"x+x" : "x", "x'+x'" : "x'", "x+1" : "1",
						"1+x" : "1", "x'+1" : "1", "1+x'" : "1",
						"x1" : "x",	"1x" : "x",	"x0" : "0",
						"0x" : "0",	"x+0" : "x", "0+x" : "x",
						"x+x'" : "1", "x'+x" : "1", "xx'" : "0",
						"x'x" : "0", "xx" : "x"}
		variable_rules = standard_rules
		if variable:
			variable_rules = dict([(key.replace("x", variable),
								value.replace("x", variable))
								for (key, value)
								in standard_rules.items()])
		return variable_rules

	# This method arranges literals of minterms in an array
	# Input: Minterm string with SOP tags
	# Output: list of literals arranged in ArrayList.
	def arrange_lit_array (self, min_term):
		arrays_literals_minterms = []
		mt_with_tag = "" #to hold the SOP1-EOP1 expression
		temp_string = ""
		##print("Original Minterm: "+min_term)
		if "SOP1" in min_term:
			#print(min_term)
			mt_with_tag = min_term[min_term.index("SOP1") : min_term.index("EOP1") + 4] # expression along with SOP-EOP tags
			temp_string = min_term[min_term.index("SOP1") + 4 : min_term.index("EOP1")]   # expression within SOP-EOP tags
			temp_string = self.replace_tags_braces(temp_string)
			arrays_literals_minterms.append(temp_string)
		rest_of_mt = min_term.replace(mt_with_tag, "")
		##print("\nRest of Minterm: " + rest_of_mt)
		arrays_literals_minterms = self.extract_literals_min_terms(arrays_literals_minterms, rest_of_mt)
		return arrays_literals_minterms

	def extract_literals_min_terms(self, arrays_literals_minterms, rest_of_mt):
		for i in range(0, len(rest_of_mt) - 1):
			if rest_of_mt[i+1] == "'":
				arrays_literals_minterms.append(
					rest_of_mt[i : min(i + 2, len(rest_of_mt))]
				)
			else:
				if rest_of_mt[i] != "'":
					arrays_literals_minterms.append(rest_of_mt[i])
				if i == len(rest_of_mt) - 2 and rest_of_mt[i+1] != "'":
					arrays_literals_minterms.append(rest_of_mt[i+1])
		return arrays_literals_minterms

	def split_two(self, input, splitter):
		if splitter in input:
			input = input.split(splitter, 1)
		return input


check = MinTermsProcessor()
print(check.expand_min_terms("c(a+b)'+d(b+c+f)+e(a+d+x+y)"))
#str1 = "a'bc+bSOP1a'c'+acEOP1"
#print("total : ", check.count_min_terms_expression(str1))

