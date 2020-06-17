"""
@author Mudasir Hanif Shaikh
LVInterface class is used to create LabVIEW-JAVA interface. It takes the unoptimized input equation from
LabVIEW logic analysis VI and the name of input genetic components. It then replace the names of input
genetic components with the simple alphabets in the equation. 

Inputs: 
Original Input Equation from Labview 
Names of input genetic components

Output: 
New Input Equation. 
"""

import re

class LVInterface:
	orginal_input_eq = ""			
	original_input_names = []		
	new_input_eq = ""
	new_input_names = []
	temp_coeff = 0.0
	initial_temp = 0.0
	time_to_run = 0.0
	
	def __init__(self, input = None):
		self.orginal_input_eq = input if input else ''
		pass
		
	def get_orginal_input_eq(self):
		return self.orginal_input_eq

	def set_orginal_input_eq(self, orginal_input_eq):
		self.orginal_input_eq = orginal_input_eq

	def get_original_input_names(self):
		return self.original_input_names
		
	def set_original_input_names(self, original_input_names):
		self.original_input_names = original_input_names

	def get_new_input_eq(self):
		return new_input_eq

	def set_new_input_eq(self, new_input_eq):
		self.new_input_eq = new_input_eq

	def replace_input_names(self):
		n = len(self.original_input_names)
		self.new_input_names = [chr(97+i) for i in range(n)]
		return self.new_input_names

	def replace_input_eq_with_new_names (self, new_input_names):
		new_input_eq = self.orginal_input_eq
		self.indices_orig = dict([(i, []) for i in self.original_input_names])
		for i in range(len(self.original_input_names)):
			current_input = self.original_input_names[i]
			new_input = new_input_names[i]
			new_input_eq = re.sub(current_input, new_input, new_input_eq)
		new_input_eq = re.sub(" ", "", new_input_eq) 
		new_input_eq = re.sub("\\.", "", new_input_eq) 
		return new_input_eq

	def get_new_input_names(self):
		return self.new_input_names
	
	def replace_input_eq_with_original_names(self, input_eq, new_input_names = None, original_input_names = None):
		new_original_eq = input_eq
		if not new_input_names:
			new_input_names = self.new_input_names
			
		if not original_input_names:
			print(self.original_input_names)
			original_input_names = self.original_input_names
		for i in range(len(original_input_names)):
			current_input = original_input_names[i]
			new_input = new_input_names[i]
			#new_original_eq = re.sub("\\b"+new_input, current_input, new_original_eq)
			#new_original_eq = re.sub(new_input+"\\b", current_input, new_original_eq)
			new_original_eq = re.sub("\\b"+new_input+"\\b", current_input, new_original_eq)
			
		new_original_eq = re.sub(" ", "", new_original_eq)
		new_original_eq = re.sub("\\.", "", new_original_eq)
		return new_original_eq
		
	def take_inputs(self, input_bool_expression):
	
		print("*********** Please enter the following values ***********")
		
		while(True):
			try:
				self.temp_coeff = 0.9 #int(input("Temperature Coefficient (e.g. 0.9). => "))
				break;
			except:
				print("You have entered a wrong value. Please try again. \n\n");
				continue;
		
		while(True):
			try:
				self.initial_temp = 10 #int(input("Initial Temperature (e.g. 10). => "))
				break;
			except:
				print("You have entered a wrong value. Please try again. \n\n");
				continue;
		
		while(True):
			try:
				self.time_to_run = 5 #int(input("Time to run in seconds (e.g. 0.5 secs). => "))
				break;
			except:
				print("You have entered a wrong value. Please try again. \n\n");
				continue;
		
		while(True):
			try:
				self.orginal_input_eq = input_bool_expression
				'''input("Enter boolean expression in terms of inputs IPTG, aTc and Arabinose. \n"
					+ "(Use \" ' \" for inverted terms; \" . \" for ANDed terms; and \" + \" for ORed terms, without any spaces.) \n"
					+ "(e.g. IPTG'.aTc.Arabinose'+IPTG'.aTc.Arabinose+IPTG.aTc.Arabinose) \n"
					+ "=> ")
				'''
				break;
			except:
				print("You have entered a wrong value. Please try again. \n\n");
				continue;
	
'''
input = "IPTG'.aTc.Arabinose'+IPTG'.aTc.Arabinose+IPTG.aTc.Arabinose"
interface = LVInterface(input)
input_prot = ["IPTG", "aTc", "Arabinose"]
interface.set_original_input_names(input_prot)
print(input)
new_eq = interface.replace_input_eq_with_new_names(interface.replace_input_names())
print(new_eq)
old_eq = interface.replace_input_eq_with_original_names(new_eq)
print(old_eq)
'''


#replace original not working; not even in java.. so gotta chagne that
