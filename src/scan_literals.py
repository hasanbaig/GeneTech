import re
from min_terms_processor import MinTermsProcessor

class ScanCommonLiterals:
	def __init__(self, rand_el1, rand_el2):
		self.reduced_rand_el1 = rand_el1
		self.reduced_rand_el2 = rand_el2
		self.matched_var = None
		self.arrays_literals_minterms = [[], []] #separate arrays of literals
												 #in midterm 0 and midterm 1
	
	def execute_scan_literals(self, rand_el1, rand_el2):
		self.process_expression = MinTermsProcessor("", 0, "")
		#print("check 9 ", rand_el1, rand_el2)
		self.arrays_literals_minterms[0] = self.split_min_terms_literals(rand_el1)
		#print("\n Separate Arrays of Literals in Minterm 0 ", self.arrays_literals_minterms[0])
		self.arrays_literals_minterms[1] = self.split_min_terms_literals(rand_el2)
		#print("check 7 : {0} {1} {2} {3}".format(rand_el1, rand_el2, self.arrays_literals_minterms[0], self.arrays_literals_minterms[1]))
		#print("\n Separate Arrays of Literals in Minterm 1 ", self.arrays_literals_minterms[1])
		#received output in the form of matched_variable, 
		#reduced random element of MT0 and MT1
		matched_variable, reduced_rand_el_mt0, reduced_rand_el_mt1  = self.search_common_literals(
																			self.arrays_literals_minterms[0],
																			self.arrays_literals_minterms[1],
																			rand_el1,
																			rand_el2
																			)
		#print("\nMatched Variable: "+ matched_variable)
		#print("\nReduced Element0: "+ reduced_rand_el_mt0) 
		#print("\nReduced Element1: "+ reduced_rand_el_mt1)
		reduced_rand_el_mt0 = self.process_expression.replace_braces_tags(reduced_rand_el_mt0)
		reduced_rand_el_mt1 = self.process_expression.replace_braces_tags(reduced_rand_el_mt1)
		reduced_rand_el_mt0 = self.process_reduced_rand_mt_el(reduced_rand_el_mt0)
		reduced_rand_el_mt1 = self.process_reduced_rand_mt_el(reduced_rand_el_mt1)
		reduced_rand_el_mt0 = self.process_empty_braces(reduced_rand_el_mt0)
		reduced_rand_el_mt1 = self.process_empty_braces(reduced_rand_el_mt1)
		#print("\nReduced Element0 after processing braces: "+ reduced_rand_el_mt0) 
		#print("\nReduced Element1 after processing braces: "+ reduced_rand_el_mt1)
		self.reduced_rand_el1 = reduced_rand_el_mt0
		self.reduced_rand_el2 = reduced_rand_el_mt1
		self.matched_var = matched_variable	
	
	# The following method splits the minterms into an array of literals
	def split_min_terms_literals(self, rand_el_mt):
		process_min_term = MinTermsProcessor(rand_el_mt, 0, "")
		#Separate array of literals in minterm 0
		string = process_min_term.replace_braces_tags(rand_el_mt)
		#print("check6 ", rand_el_mt, string)
		separate_array_lit_mt = process_min_term.arrange_lit_array(string) 
		return separate_array_lit_mt
	
	# The following method scan for the common literals in the minterms
	def search_common_literals(self, 
							arrays_literals_minterms0, 
							arrays_literals_minterms1,
							rand_el_mt0, 
							rand_el_mt1):
		matched_variable = ""
		for i in arrays_literals_minterms0:
			for j in arrays_literals_minterms1:
				if i == j:
					interim_string = i
					if "+" in i:
						interim_string = "(" + i + ")"
					rand_el_mt0 = rand_el_mt0.replace(interim_string, "", 1)
					rand_el_mt1 = rand_el_mt1.replace(interim_string, "", 1)
					matched_variable += interim_string
		return (matched_variable, rand_el_mt0, rand_el_mt1)
	
	# process reduced minterm elements which were chosen randomly
	def process_reduced_rand_mt_el(self, reduced_rand_mt_el):
		start_indices = [i.start() for i in re.finditer(reduced_rand_mt_el, "SOP1")]
		#print('here', reduced_rand_mt_el)
		splitted = self.split_string_two(reduced_rand_mt_el, "SOP1")
		#print("splitted", splitted)
		intermediate = reduced_rand_mt_el
		if splitted[0] == "":
			if splitted[1] != "":
				intermediate = splitted[1][:splitted[1].index("EOP1")]
		reduced_rand_mt_el = self.process_expression.replace_tags_braces(intermediate)
		if not reduced_rand_mt_el: #if empty
			reduced_rand_mt_el = "1"
		return reduced_rand_mt_el
	
	def split_string_two(self, string, splitter):
		if splitter in string:
			return string.split(splitter, 1)
		return [string, ""]
	# The following method is used to search and remove the empty pair of braces
	def process_empty_braces(self, reduced_rand_mt_el):
		start_indices = [i.start() for i in re.finditer(reduced_rand_mt_el, "(")]
		#print(start_indices)
		replacing_indices = []
		for idx in start_indices:
			if str[idx + 1] == ")":
				replacing_indices.append(idx)
		str = ''.join([reduced_rand_mt_el[i] for i in range(len(reduced_rand_mt_el)) if i not in replacing_indices])
		return str