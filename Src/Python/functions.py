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




print(Delay('PTet', '(AmeR)', 'PTac'))

