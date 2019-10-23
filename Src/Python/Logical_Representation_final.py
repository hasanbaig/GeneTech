import matplotlib
matplotlib.use('Qt5Agg')
import re
import SchemDraw as schem
import SchemDraw.logic as l
import SchemDraw.elements as e
import matplotlib.pyplot as plt
from functions import *

class Logical_Representation:
    def __init__(self):
        DeleteExistingImages()
        circuits = ReadFile()
        self.plot(circuits)

    def plot(self, circuits):
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
            fig = plt.figure()
            d = schem.Drawing(unit=.25, fontsize=7)
            G1 = 0
            G4 = G1
            use = []
            color = 0
            nor_color = 0
            for j in range(len(circuits[i])):
                if j==0:
                    All_gates=circuits[i][0].split(' ----|')
                    FP = All_gates[-1].split('-> ')[-1]  #YFP for our case right now
                    for k in range(len(All_gates)):
                        gate = All_gates[k].split('-> ')
                        if FP not in gate[-1]:
                            if len(gate) == 2: #NOT Gate
                                if k==0: #for first gate (to make text at the start of line)
                                    G1 = d.add(e.LINE, d='right', toplabel=gate[0])
                                    xx = d.add(e.LINE, d='right',l=0.5)
                                    NOT = d.add(l.NOT, zoom=1, endpts=[xx.end,[xx.end[0]+3,xx.end[1]]], botlabel=gate[1], fill=col_map[color])
                                    color += 1
                                else:
                                    xx = d.add(e.LINE, d='right',l=0.5, toplabel=gate[0])
                                    NOT = d.add(l.NOT, zoom=1, endpts=[xx.end,[xx.end[0]+3,xx.end[1]]], botlabel=gate[1], fill=col_map[color])
                                    color += 1
                                G2 = d.add(e.LINE, d='right', xy=NOT.out)
                                
                            elif len(gate) == 3: #NOR Gate
                                if k==0:
                                    G1 = d.add(e.LINE, d='right', toplabel=gate[0])
                                    d.add(e.LINE, d='right',l=1.5)
                                else:
                                    d.add(e.LINE, d='right',l=1.5,  toplabel=gate[0])
                                if gate[1] in ['PBad', 'PTac', 'PTet']:
                                    NOR = d.add(l.NOR2, anchor='in1', zoom=1, botlabel=gate[2], fill = col_map[color])
                                    G3 = d.add(e.LINE, xy=NOR.in2, d='left', toplabel=gate[1])
                                    down_line_key = d.add(e.LINE, xy=G3.end, d='down')
                                    use.append((gate[1], down_line_key, col_map[color]))
                                    color += 1
                                else:
                                    NOR = d.add(l.NOR2, anchor='in1', zoom=1, botlabel=gate[2], fill = col_map[color+1])
                                    G3 = d.add(e.LINE, xy=NOR.in2, d='left', toplabel=gate[1])
                                    down_line_key = d.add(e.LINE, xy=G3.end, d='down')
                                    use.append((gate[1], down_line_key, col_map[color]))
                                    color += 2
                                d.add(e.LINE, xy=NOR.out, d='right')
                               
                                
                        else:
                            if len(gate) == 2: #FP directly produces
                                d.add(e.LINE, d='right', l=1.5, toplabel=gate[0])

                            elif len(gate) == 3: #OR Gate for FP
                                d.add(e.LINE, d='right',l=1.5,  botlabel=gate[0])
                                OR = d.add(l.OR2, anchor='in1', zoom=1)
                                G3 = d.add(e.LINE, xy=OR.in2, d='left', toplabel=gate[1])
                                down_line_key = d.add(e.LINE, xy=G3.end, d='down')
                                use.append((gate[1], down_line_key, col_map[color]))
                                color += 1
                                d.add(e.LINE, xy=OR.out, d='right')

                else:
                    endbracket=len(circuits[i][j])-circuits[i][j][-1::-1].index(")")
                    All_gates=circuits[i][j][:endbracket].split(' ----|')
                    for k in range(len(All_gates)):
                        gate = All_gates[k].split('-> ')
                        if len(gate)==2:
                            if k==0:
                                if j==len(circuits[i])-1:
                                    G4 = d.add(e.LINE, d='right', toplabel=gate[0], xy=[G1.start[0],G1.end[1]-1.5])
                                else:
                                    G4 = d.add(e.LINE, d='right', toplabel=gate[0], xy=[G1.start[0],G1.end[1]-3])
                                    nor_color = -1
                                xx = d.add(e.LINE, d='right',l=0.5, xy=G4.end)
                                if k == len(All_gates)-1:
                                    if use[nor_color][0] in baseList():
                                        nor_color += 1
                                    NOT = d.add(l.NOT, zoom=1, endpts=[xx.end,[xx.end[0]+3,xx.end[1]]], botlabel=gate[1], fill=use[nor_color][2])
                                    nor_color -= 1
                                else:
                                    NOT = d.add(l.NOT, zoom=1, botlabel=gate[1], endpts=[xx.end,[xx.end[0]+3,xx.end[1]]], fill = col_map[color])
                                    color += 1
                            else:
                                xx = d.add(e.LINE, d='right',l=0.5, toplabel=gate[0], xy=G5.end)
                                if k == len(All_gates)-1:
                                    nor_color = 0
                                    NOT = d.add(l.NOT, zoom=1, endpts=[xx.end,[xx.end[0]+3,xx.end[1]]], botlabel=gate[1], fill=use[nor_color][2])
                                    nor_color -= 1
                                else:
                                    NOT = d.add(l.NOT, zoom=1, endpts=[xx.end,[xx.end[0]+3,xx.end[1]]], botlabel=gate[1], fill=col_map[color])
                                    color += 1
                            G5 = d.add(e.LINE, d='right', xy=NOT.out)

                        elif len(gate)==3:
                            if k==0:
                                G4 = d.add(e.LINE, d='right', toplabel=gate[0],xy=[G1.start[0],G1.end[1]-j-0.5])
                                G4 = d.add(e.LINE, d='right',l=2.5, xy = G4.end)
                            else:
                                G4 = d.add(e.LINE, d='right', toplabel=gate[0], xy=G5.end, l=1.5)

                            if len(circuits[i]) == 3:
                                if k == len(All_gates)-1:
                                    nor_color = 0
                                    NORx = d.add(l.NOR2, anchor='in2', zoom=1 , botlabel=gate[2], xy=G4.end , fill = use[nor_color][2])
                                    nor_color -= 1
                                else:
                                    NORx = d.add(l.NOR2, anchor='in2', zoom=1 , botlabel=gate[2], xy=G4.end , fill = col_map[color+1])
                                G5 = d.add(e.LINE, xy=NORx.out, d='right')
                                G7 = d.add(e.LINE, xy=NORx.in1, d='left', label=gate[1], l=1.3)
                                up_key = d.add(e.LINE, xy=G7.end, d='up')
                                use.append((gate[1], up_key, col_map[color]))
                                color += 1

                            else:
                                NORx = d.add(l.NOR2, anchor='in1', zoom=1 , botlabel=gate[2], xy=G4.end, fill = col_map[color+1])
                                G5 = d.add(e.LINE, xy=NORx.out, d='right')
                                G7 = d.add(e.LINE, xy=NORx.in2, d='left', label=gate[1], l=1.3)
                                down_key = d.add(e.LINE, xy=G7.end, d='down')
                                use.append((gate[1], down_key,  col_map[color]))
                                color += 1


                    last_gate = All_gates[-1].split('-> ')
                    if len(circuits[i])==3 and j == 2 and last_gate[1][1:-1] in circuits[i][1]:
                        d.add(e.LINE, endpts=[G5.end,[use[-1][1].end[0],G5.end[1]]])
                        d.add(e.LINE, d='down', endpts=[[use[-1][1].end[0], G5.end[1]], use[-1][1].end])
                        use.pop()

                    for z in range(len(use)):
                        if last_gate[-1][1:-1] == use[z][0][1:]:
                            d.add(e.LINE, endpts=[G5.end,[use[z][1].end[0],G5.end[1]]])
                            d.add(e.LINE, d='up', endpts=[[use[z][1].end[0], G5.end[1]], use[z][1].end])
                            cc = use[z][2]
                            use.pop(z)
                            use.insert(z,('0','0',cc))

            if G4 == 0:
                G4 = G1
            lst = baseList()
            for z in range(len(use)):
                if use[z][0] in lst:
                    G4 = d.add(e.LINE, d='right', toplabel=use[z][0], xy=[G1.start[0],G4.start[1]-1.5])
                    d.add(e.LINE, d='right', endpts=[G4.end,[use[z][1].end[0],G4.start[1]]])
                    d.add(e.LINE, xy=G4.end, d='up', endpts=[[use[z][1].end[0],G4.start[1]],use[z][1].end])

            d.draw(showplot=False)
            d.save('Circuit'+str(i+1)+'.png', dpi=300)
            plt.close('all')



if __name__ == '__main__':
    logic = Logical_Representation()
