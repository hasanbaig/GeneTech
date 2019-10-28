import dnaplotlib as dpl
from pylab import *
import matplotlib.pyplot as plt
from functions import *

class SBOLv:
	def __init__(self, total_gates, total_time):
		circuits = ReadFile()
		self.plot(circuits, total_gates, total_time)

	def plot(self, circuits, total_gates, total_time):
		# Colour map
		col_map = {}
		col_map[0] = '#e31414'	#red
		col_map[1] = '#34e681'	#green
		col_map[2] = '#34a4e6'	#blue
		col_map[3] = '#ff7b00'	#orange
		col_map[4] = '#44855a'	#dark green
		col_map[5] = '#1831c4'	#dark blue
		col_map[6] = '#9918c4'	#indigo
		col_map[7] = '#e6178f'	#violet
		col_map[8] = '#995f81'	#purple

		for i in range(len(circuits)):
			if Total_Gates(i) <= total_gates and Total_time(i) <= total_time:		#If Total Delay and number of gates are less than the input
				fig = plt.figure()
				design = []			#A list to be gathered to draw
				reg = []			#To store the Repression Lines
				color = 0			#A number to assign colors in order to coordinate with Logical Representation
				use = []			#To temporarily store the second input of NOR Gate
				coding_seq = []		#A List to temporarily hold coding sequences from each gate
				seperate = []
				for j in range(len(circuits[i])):
					if j==0:
						All_gates=circuits[i][0].split(' ----|')
						FP = All_gates[-1].split('-> ')[-1]  #YFP for our case right now
						for k in range(len(All_gates)):
							gate = All_gates[k].split('-> ')
							if FP not in gate[-1]:
								if len(gate) == 2: #NOT Gate
									if k==0:		#Append all the parts in a list
										promotor = {'type':'Promoter', 'name':gate[0], 'opts':{'color':(0,0,0), 'label':gate[0], 'label_x_offset':-5, 'label_y_offset':-4, 'label_size':5}}
										design.append(promotor)
										u = {'type': 'RBS', 'name': 'u'+str(color),  'opts':{'color': (0,0,0), 'start_pad': -6, 'x_extent': 6}}
										design.append(u)
										cds = {'type':'CDS', 'name':gate[1], 'opts':{'color':col_map[color], 'edge_color':col_map[color], 'x_extent':24, 'label':gate[1], 'label_color':(1,1,1), 'label_style':'italic', 'label_x_offset':-1, 'label_size':6}}
										design.append(cds)
										coding_seq.append(cds)
										terminator = {'type':'Terminator', 'name':'t'+str(color), 'opts':{'color':(0,0,0), 'start_pad':-1}}
										design.append(terminator)

									else:			#If it's not the first gate than it will contain the repression interaction form the previous gate
										promotor = {'type':'Promoter', 'name':gate[0], 'opts':{'color':col_map[color], 'label':gate[0], 'label_x_offset':-5, 'label_y_offset':-4, 'label_size':5}}
										rep = {'type':'Repression', 'from_part':coding_seq[0], 'to_part':promotor, 'opts':{'color':col_map[color], 'arc_height':20}}
										design.append(promotor)
										reg.append(rep)
										coding_seq.pop(0)
										color += 1		#Change color once the repression intercation is created
										u = {'type': 'RBS', 'name': 'u'+str(color),  'opts':{'color': (0,0,0), 'start_pad': -6, 'x_extent': 6}}
										design.append(u)
										cds = {'type':'CDS', 'name':gate[1], 'opts':{'color':col_map[color], 'edge_color':col_map[color], 'x_extent':24, 'label':gate[1], 'label_color':(1,1,1), 'label_style':'italic', 'label_x_offset':-1, 'label_size':6}}
										design.append(cds)
										coding_seq.append(cds)
										terminator = {'type':'Terminator', 'name':'t'+str(color), 'opts':{'color':(0,0,0), 'start_pad':-1}}
										design.append(terminator)


								elif len(gate) == 3: #NOR Gate
									if k==0:
										promotor1 = {'type':'Promoter', 'name':gate[0], 'opts':{'color':(0,0,0), 'label':gate[0], 'label_x_offset':-6, 'label_y_offset':-4, 'label_size':5}}
										design.append(promotor1)
										if gate[1] in baseList():		#If the input is one of PTet, PTac or PBad in our case, the color should be black
											promotor2 = {'type':'Promoter', 'name':gate[1], 'opts':{'color':(0,0,0), 'label':gate[1], 'label_x_offset':-1, 'label_y_offset':-4, 'label_size':5}}
										else:							#Other wise tthe color is stored so it can be assigned to its repression
											promotor2 = {'type':'Promoter', 'name':gate[1], 'opts':{'color':col_map[color], 'label':gate[1], 'label_x_offset':-1, 'label_y_offset':-4, 'label_size':5}}
											use.append((promotor2, color))
											color += 1
										design.append(promotor2)
										u = {'type': 'RBS', 'name': 'u'+str(color),  'opts':{'color': (0,0,0), 'start_pad': -6, 'x_extent': 6}}
										design.append(u)
										cds = {'type':'CDS', 'name':gate[2], 'opts':{'color':col_map[color], 'edge_color':col_map[color], 'x_extent':24, 'label':gate[2], 'label_color':(1,1,1), 'label_style':'italic', 'label_x_offset':-1, 'label_size':6}}
										design.append(cds)
										coding_seq.append(cds)
										terminator = {'type':'Terminator', 'name':'t'+str(color), 'opts':{'color':(0,0,0), 'start_pad':-1}}
										design.append(terminator)

									else:
										promotor1 = {'type':'Promoter', 'name':gate[0], 'opts':{'color':col_map[color], 'label':gate[0], 'label_x_offset':-6, 'label_y_offset':-4, 'label_size':5}}
										rep = {'type':'Repression', 'from_part':coding_seq[0], 'to_part':promotor1, 'opts':{'color':col_map[color], 'arc_height':20}}
										design.append(promotor1)
										reg.append(rep)
										coding_seq.pop(0)
										color += 1
										if gate[1] in baseList():
											promotor2 = {'type':'Promoter', 'name':gate[1], 'opts':{'color':(0,0,0), 'label':gate[1], 'label_x_offset':-1, 'label_y_offset':-4, 'label_size':5}}
										else:
											promotor2 = {'type':'Promoter', 'name':gate[1], 'opts':{'color':col_map[color], 'label':gate[1], 'label_x_offset':-1, 'label_y_offset':-4, 'label_size':5}}
											use.append((promotor2, color))
											color += 1
										design.append(promotor2)
										u = {'type': 'RBS', 'name': 'u'+str(color),  'opts':{'color': (0,0,0), 'start_pad': -6, 'x_extent': 6}}
										design.append(u)
										cds = {'type':'CDS', 'name':gate[2], 'opts':{'color':col_map[color], 'edge_color':col_map[color], 'x_extent':24, 'label':gate[2], 'label_color':(1,1,1), 'label_style':'italic', 'label_x_offset':-1, 'label_size':6}}
										design.append(cds)
										coding_seq.append(cds)
										terminator = {'type':'Terminator', 'name':'t'+str(color), 'opts':{'color':(0,0,0), 'start_pad':-1}}
										design.append(terminator)

							else:
								if len(gate) == 2: #YFP CDS
									promotor = {'type':'Promoter', 'name':gate[0], 'opts':{'color':col_map[color], 'label':gate[0], 'label_x_offset':-5, 'label_y_offset':-4, 'label_size':5}}
									rep = {'type':'Repression', 'from_part':coding_seq[0], 'to_part':promotor, 'opts':{'color':col_map[color], 'arc_height':20}}
									design.append(promotor)
									reg.append(rep)
									coding_seq.pop(0)
									color += 1
									u = {'type': 'RBS', 'name': 'u'+str(color),  'opts':{'color': (0,0,0), 'start_pad': -6, 'x_extent': 6}}
									design.append(u)
									cds = {'type':'CDS', 'name':gate[1], 'opts':{'color':(1,1,1), 'edge_color':(0,0,0), 'x_extent':24, 'label':gate[1], 'label_color':(0,0,0), 'label_style':'italic', 'label_x_offset':-1, 'label_size':6}}
									design.append(cds)
									coding_seq.append(cds)
									terminator = {'type':'Terminator', 'name':'t'+str(color), 'opts':{'color':(0,0,0), 'start_pad':-1}}
									design.append(terminator)

								elif len(gate) == 3: #OR Gate for YFP
									promotor1 = {'type':'Promoter1', 'name':gate[0], 'opts':{'color':col_map[color], 'label':gate[0], 'label_x_offset':-6, 'label_y_offset':-4, 'label_size':5}}
									rep = {'type':'Repression', 'from_part':coding_seq[0], 'to_part':promotor1, 'opts':{'color':col_map[color], 'arc_height':20}}
									design.append(promotor1)
									reg.append(rep)
									coding_seq.pop(0)
									color += 1
									if gate[1] in baseList():
										promotor2 = {'type':'Promoter2', 'name':gate[1], 'opts':{'color':(0,0,0), 'label':gate[1], 'label_x_offset':-1, 'label_y_offset':-4, 'label_size':5}}
									else:
										promotor2 = {'type':'Promoter2', 'name':gate[1], 'opts':{'color':col_map[color], 'label':gate[1], 'label_x_offset':-1, 'label_y_offset':-4, 'label_size':5}}
										use.append((promotor2, color))
										color += 1
									design.append(promotor2)
									u = {'type': 'RBS', 'name': 'u'+str(color),  'opts':{'color': (0,0,0), 'start_pad': -6, 'x_extent': 6}}
									design.append(u)
									cds = {'type':'CDS', 'name':gate[2], 'opts':{'color':(1,1,1), 'edge_color':(0,0,0), 'x_extent':24, 'label':gate[2], 'label_color':(0,0,0), 'label_style':'italic', 'label_x_offset':-1, 'label_size':6}}
									design.append(cds)
									coding_seq.append(cds)
									terminator = {'type':'Terminator', 'name':'t'+str(color), 'opts':{'color':(0,0,0), 'start_pad':-1}}
									design.append(terminator)

					else:		#For the rest of the lines
						endbracket=len(circuits[i][j])-circuits[i][j][-1::-1].index(")")
						All_gates=circuits[i][j][:endbracket].split(' ----|')
						for k in range(len(All_gates)):
							gate = All_gates[k].split('-> ')
							if len(gate)==2:
								terminator = {'type':'Terminator', 'name':'t'+str(color+2), 'opts':{'color':(0,0,0), 'start_pad':-1}}
								cds_color = use[-1][1]
								cds = {'type':'CDS', 'name':gate[1], 'opts':{'color':col_map[cds_color], 'edge_color':col_map[cds_color], 'x_extent':24, 'label':gate[1], 'label_color':(1,1,1), 'label_style':'italic', 'label_x_offset':-1, 'label_size':6}}
								u = {'type': 'RBS', 'name': 'u'+str(color+2),  'opts':{'color': (0,0,0), 'start_pad': -6, 'x_extent': 6}}
								promotor = {'type':'Promoter', 'name':gate[0], 'opts':{'color':(0,0,0), 'label':gate[0], 'label_x_offset':-5, 'label_y_offset':-4, 'label_size':5}}
								arc = {'type':'Repression', 'from_part':cds, 'to_part':use[-1][0], 'opts':{'color':col_map[cds_color], 'arc_height':35-(j*5)}}

								if j==len(circuits[i])-1:		#To avoid intersection of the Repression lines
									design.insert(0, terminator)
									design.insert(0, cds)
									design.insert(0, u)
									design.insert(0, promotor)

								else:							#Store it temporarily until because it needs to be appended at the end
									seperate.insert(0, terminator)
									seperate.insert(0, cds)
									seperate.insert(0, u)
									seperate.insert(0, promotor)

								reg.append(arc)
								use.pop()

				design = seperate + design

				# Set up the axes for the genetic constructs
				ax_dna = plt.axes()

				# Create the DNAplotlib renderer
				dr = dpl.DNARenderer()

				# Render the DNA to axis
				start, end = dr.renderDNA(ax_dna, design, dr.SBOL_part_renderers(), regs=reg, reg_renderers=dr.std_reg_renderers())

				ax_dna.set_xlim([start, end])
				ax_dna.set_ylim([-40,40])
				ax_dna.set_aspect('equal')
				ax_dna.set_xticks([])
				ax_dna.set_yticks([])
				ax_dna.axis('off')

				fig.savefig('SBOL visual '+str(i+1)+'.png', dpi=300)
				plt.close('all')

if __name__ == '__main__':
    visual = SBOLv(1000, 1000)


