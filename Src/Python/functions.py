import glob, os

def baseList():
    f = open("GatesLib.txt")
    lst = []
    for i in f:
        lst.append(i.replace('\n',''))

    lst = list(filter(bool,lst))
    lst = lst[lst.index('<Ext-Inverters>')+2:lst.index('</Ext-Inverters>')]

    base = []
    for i in lst:
        a = i.split('\t')[1]
        if a not in base:
            base.append(a)

    return base

def DeleteExistingImages():
    list = glob.glob('**/*.png', recursive=True)
    for i in range(len(list)):
        os.remove(list[i])

def DeleteExistingFiles():
    list = glob.glob('**/*.xml', recursive=True)
    for i in range(len(list)):
        os.remove(list[i])

def ReadFile():
    f = open("circuits.txt")
    circuits = []
    for i in f:
        if "*" in i:
            cnt = []
            circuits.append(cnt)
        else:
            cnt.append(i.replace('\n',''))

    for i in circuits:
        for j in i:
            if j == '':
                i.remove(j)

    return circuits

def Delay(promotor1, CDS, promotor2 = None):
    """
        Gates[0] = External NOT Gates which have basic gates as input
        Gates[1] = Internal NOT Gates which don't have basic gates
        Gates[2] = External NOR Gates with basic gates as input
        Gates[3] = Semi-External NOR Gates with basic and non-basic both
        Gates[4] = Internal NOR Gates where both inputs are not basic
    """

    Gates = GatherGates()
    Output_P = 'P' + CDS[1:-1]

    if promotor2 == None:                   #The condition for NOT gates
        if promotor1 in baseList():         #If the promotor is one of the basic promotors
            return Check_NOT(promotor1, Output_P, Gates[0])
        else:
            return Check_NOT(promotor1, Output_P, Gates[1])

    else:       #For NOR Gates
        if promotor1 in baseList() and promotor2 in baseList():
            return Check_NOR(promotor1, promotor2, Output_P, Gates[2])
        elif promotor1 in baseList() and promotor2 not in baseList():
            return Check_NOR(promotor1, promotor2, Output_P, Gates[3])
        elif promotor2 in baseList() and promotor1 not in baseList():
            return Check_NOR(promotor1, promotor2, Output_P, Gates[3])
        else:
            return Check_NOR(promotor1, promotor2, Output_P, Gates[4])

def Check_NOT(promotor, Output_P, Gates):
    for i in Gates:
        if i[0] == promotor and i[1] == Output_P:
            return i[2]

def Check_NOR(promotor1, promotor2, Output_P, Gates):
    for i in Gates:
        if i[0] == promotor1 and i[1] == promotor2 and i[2] == Output_P:
            return i[3]
        elif i[0] == promotor2 and i[1] == promotor1 and i[2] == Output_P:
            return i[3]

def GatherGates():
    f = open("GatesLib.txt")
    lst = []
    for i in f:
        lst.append(i.replace('\n',''))
    lst = list(filter(bool,lst))

    temp = lst[lst.index('<Ext-Inverters>')+2:lst.index('</Ext-Inverters>')]
    Ext_NOTs= []
    for i in temp:
        gate = i.split('\t')[1:]
        gate[1] = gate[1].split()[0]        #Get Rid of 'END' in the promotor name
        Ext_NOTs.append(gate)

    temp = lst[lst.index('<Int-Inverters>')+1:lst.index('</Int-Inverters>')]
    Int_NOTs= []
    for i in temp:
        gate = i.split('\t')
        gate[1] = gate[1].split()[0]
        Int_NOTs.append(gate)

    temp = lst[lst.index('<Ext-NorGates>')+1:lst.index('</Ext-NorGates>')]
    Ext_NORs= []
    for i in temp:
        gate = i.split('\t')
        gate[2] = gate[2].split()[0]
        Ext_NORs.append(gate)

    temp = lst[lst.index('<Semi-Ext-NorGates>')+1:lst.index('</Semi-Ext-NorGates>')]
    SemiExt_NORs= []
    for i in temp:
        gate = i.split('\t')
        gate[2] = gate[2].split()[0]
        SemiExt_NORs.append(gate)

    temp = lst[lst.index('<Int-NorGates>')+1:lst.index('</Int-NorGates>')]
    Int_NORs= []
    for i in temp:
        gate = i.split('\t')
        gate[2] = gate[2].split()[0]
        Int_NORs.append(gate)

    return [Ext_NOTs, Int_NOTs, Ext_NORs, SemiExt_NORs, Int_NORs]

def Total_time(i):
    time = 0
    circuits = ReadFile()
    line_time = []
    for j in range(len(circuits[i])-1, -1, -1):
        if j!= 0:
            t = 0
            endbracket=len(circuits[i][j])-circuits[i][j][-1::-1].index(")")
            All_gates=circuits[i][j][:endbracket].split(' ----|')
            for k in range(len(All_gates)):
                gate = All_gates[k].split('-> ')
                if len(gate)==2:
                    t += float(Delay(gate[0], gate[1]))
                elif len(gate)==3:
                    if gate[1] not in baseList():
                        if gate[1] == 'P'+line_time[0][1]:
                            if t < line_time[0][0]:
                                t = line_time[0][0]
                                line_time.pop(0)
                            else:
                                line_time.pop(0)
                    t += float(Delay(gate[0], gate[2], gate[1]))
                if k == len(All_gates)-1:
                    line_time.append((t, gate[-1][1:-1]))

        else:
            All_gates=circuits[i][0].split(' ----|')
            FP = All_gates[-1].split('-> ')[-1]  #YFP for our case right now
            for k in range(len(All_gates)):
                gate = All_gates[k].split('-> ')
                if FP not in gate[-1]:
                    if len(gate) == 2:
                        time += float(Delay(gate[0], gate[1]))
                    elif len(gate)==3:
                        if gate[1] not in baseList():
                            if gate[1] == 'P'+line_time[0][1]:
                                if time < line_time[0][0]:
                                    time = line_time[0][0]
                                    line_time.pop(0)
                                else:
                                    line_time.pop(0)
                        time += float(Delay(gate[0], gate[2], gate[1]))

                else:
                    if len(gate)==3:
                        if gate[1] not in baseList():
                            if gate[1] == 'P'+line_time[0][1]:
                                if time > line_time[0][0]:
                                    time = line_time[0][0]
                                    line_time.pop(0)
                                else:
                                    line_time.pop(0)


    return round(time, 5)

print(Total_time(0))

def Total_Gates(i):
    gates = 0
    circuits = ReadFile()
    for j in range(len(circuits[i])):
        if j==0:
            All_gates=circuits[i][0].split(' ----|')
            gates += len(All_gates)-1
        else:
            endbracket=len(circuits[i][j])-circuits[i][j][-1::-1].index(")")
            All_gates=circuits[i][j][:endbracket].split(' ----|')
            gates += len(All_gates)

    return gates
