from sbol2 import *
#
import sbol2
print(sbol2.__version__)
import glob, os

def baseList():
    f = open("GatesLib.txt")
    lst = []
    for i in f:
        lst.append(i.replace('\n',''))

    lst = list(filter(bool,lst))        #Filter out the empty values form the list
    lst = lst[lst.index('<Ext-Inverters>')+2:lst.index('</Ext-Inverters>')]

    base = []
    for i in lst:
        promotor = i.split('\t')[1]         #The second column has the names of the base promotors
        if promotor not in base:            #If promotor already in list
            base.append(promotor)

    return base

def DeleteExistingImages():
    """Delete all the existing Images in the directory"""
    list = glob.glob('**/*.png', recursive=True)
    for i in range(len(list)):
        if list[i] != 'BigLogo.png' and list[i] != 'SmallLogo.png':
            os.remove(list[i])

def DeleteExistingFiles():
    """Delete all the existing SBOL files in the directory"""
    list = glob.glob('**/*.xml', recursive=True)
    for i in range(len(list)):
        os.remove(list[i])

def CountFiles():
    """Counts all the existing SBOL files in the directory"""
    list = glob.glob('**/*.xml', recursive=True)
    return len(list)

def ReadFile():
    """Read the file and create a list with lines of circuits in it"""
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

        promotor2 is kept None in case if the the function is called to check NOT gate
    """

    Gates = GatherGates()           #Gather gates by reading the file
    Output_P = 'P' + CDS[1:-1]
    baseLst = baseList()
    promoter1_present = promotor1 in baseLst
    if promotor2 == None:                   #The condition for NOT gates
        if promoter1_present:         #If the promotor is one of the basic promotors
            return Check_NOT(promotor1, Output_P, Gates[0])         #Returns the time of the NOT gate with these inputs
        else:
            return Check_NOT(promotor1, Output_P, Gates[1])

    else:       #For NOR Gates
        #Check all possibilties of inputs for internal, external and semi-external gates
        promoter2_present = promotor2 in baseLst
        if promoter1_present and promoter2_present:
            return Check_NOR(promotor1, promotor2, Output_P, Gates[2])
        elif promoter1_present and not promoter2_present:           #e.g. if P1=PTac and P2=PAmtR
            return Check_NOR(promotor1, promotor2, Output_P, Gates[3])
        elif promoter2_present and not promoter1_present:           #e.g. if P1=PAmtR and P2=PTac
            return Check_NOR(promotor1, promotor2, Output_P, Gates[3])
        else:
            return Check_NOR(promotor1, promotor2, Output_P, Gates[4])
    return 0
	
def Check_NOT(promotor, Output_P, Gates):
    """Check the whole list and returns the delay of the gate matching with inputs"""
    for i in Gates:
        if i[0] == promotor and i[1] == Output_P:
            return i[2]
    return 0 

def Check_NOR(promotor1, promotor2, Output_P, Gates):
    """Check the whole list and returns the delay of the gate matching with inputs"""
    #Checks both possiblities of inputs in case if inputs are swapped
    for i in Gates:
        if i[0] == promotor1 and i[1] == promotor2 and i[2] == Output_P:            #e.g if P1=PAmtR and P2=PBetl
            return i[3]
        elif i[0] == promotor2 and i[1] == promotor1 and i[2] == Output_P:          #e.g. if P1=PBetl and P2=PAmtR
            return i[3]
    return 0
	
def GatherGates():
    f = open("GatesLib.txt")
    lst = []
    for i in f:
        lst.append(i.replace('\n',''))
    lst = list(filter(bool,lst))            #Filter out the empty values from the list

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
    """Calculates the total time of the circuit"""
    time = 0
    circuits = ReadFile()
    line_time = []
    for j in range(len(circuits[i])-1, -1, -1):     #First gather time of other lines to compare it with their respective other input
        if j!= 0:               #For other lines
            t = 0
            endbracket=len(circuits[i][j])-circuits[i][j][-1::-1].index(")")
            All_gates=circuits[i][j][:endbracket].split(' ----|')
            for k in range(len(All_gates)):
                gate = All_gates[k].split('-> ')
                if len(gate)==2:
                    t += float(Delay(gate[0], gate[1]))
                elif len(gate)==3:
                    if gate[1] not in baseList():           #If the second input is not a base promotor
                        if gate[1] == 'P'+line_time[0][1]:
                            if t < line_time[0][0]:         #If the other input has greater time
                                t = line_time[0][0]
                                line_time.pop(0)
                            else:
                                line_time.pop(0)
                    t += float(Delay(gate[0], gate[2], gate[1]))
                if k == len(All_gates)-1:
                    line_time.append((t, gate[-1][1:-1]))       #Store it in a list to compare with other inputs

        else:           #For the first line
            All_gates=circuits[i][0].split(' ----|')
            FP = All_gates[-1].split('-> ')[-1]  #YFP for our case right now
            for k in range(len(All_gates)):
                gate = All_gates[k].split('-> ')
                if FP not in gate[-1]:              #Ignore the flourescent protein gate
                    if len(gate) == 2:
                        time += float(Delay(gate[0], gate[1]))
                    elif len(gate)==3:
                        if gate[1] not in baseList():
                            if gate[1] == 'P'+line_time[0][1]:
                                if time < line_time[0][0]:          #If the other input has greater time
                                    time = line_time[0][0]
                                    line_time.pop(0)
                                else:
                                    line_time.pop(0)
                        time += float(Delay(gate[0], gate[2], gate[1]))

                else:                               #if the gate is the one with flourescent protein as its coding sequence
                    if len(gate)==3:
                        if gate[1] not in baseList():
                            if gate[1] == 'P'+line_time[0][1]:
                                if time > line_time[0][0]:          #Now we need the smaller time to determine the minimum time taken for a circuit to produce output
                                    time = line_time[0][0]
                                    line_time.pop(0)
                                else:
                                    line_time.pop(0)

    return round(time, 5)


def Total_Gates(i):
    """Counts number of gates in the circuit"""
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

def SortNum(index, option):
    """Determine the sort index of the circuit after sorting all the circuits according to a constraint"""
    circuits = ReadFile()
    list = []
    for i in range(len(circuits)):
        if option == 0:
            factor = Total_time(i)
        else:
            factor = Total_Gates(i)

        list.append([i, factor])

    list = sorted(list, key = func)

    d={}
    for i in range(len(list)):
        d[list[i][0]] = list[i]
        d[list[i][0]][0] = i

    return d[index][0]

def func(x):
    return x[1]

def count_no_alphabets(POS):
    """Function to calculate no. of variables used in POS expression"""
    i = 0
    no_var = 0
    # As expression is standard so total no.of alphabets will be equal to alphabets before first '.' character
    while (POS[i]!='.'):
        # checking if character is alphabet
        if (POS[i].isalpha()):
            no_var+= 1
        i+= 1
    return no_var

def Cal_Max_terms(POS):
    """Function to calculate the max terms in integers"""
    Max_terms = []
    a = ""
    i = 0
    while (i<len(POS)):
        if (POS[i]=='.'):
            b = int(a, 2)            # converting binary to decimal
            Max_terms.append(b)      # insertion of each min term(integer) into the list
            a =""                    # empty the string
            i+= 1

        elif(POS[i].isalpha()):
            # checking whether variable is complemented or not
            if(i+1 != len(POS) and POS[i+1]=="'"):
                a += '1'        # concatenating the string with '1'. In POS, complement means '1'
                i += 2          # incrementing by 2 because 1 for alphabet and another for "'"
            else:
                a += '0'        # concatenating the string with '0'. In POS, complement means '0'
                i += 1
        else:
            i+= 1

    # insertion of last min term(integer) into the list
    Max_terms.append(int(a, 2))
    return Max_terms

def Cal_Min_terms(Max_terms, no_var):
    """Function to calculate the min terms in binary then calculate SOP form of POS"""
    Min_terms =[]       # declaration of the list
    max = 2**no_var     # calculation of total no. of terms that can be formed by no_var variables (for 3 variables 8 outcomes)
    for i in range(0, max):
        # checking whether the term is not present in the max terms
        if (Max_terms.count(i)== 0):
            # converting integer to binary and then taking the value from 2nd index as 1st two index contains '0b'
            b = bin(i)[2:]
            # loop used for inserting 0's before the binary value so that its length will be
            # equal to no. of variables present in each product term
            while(len(b)!= no_var):
                b ='0'+b

            # appending the max terms(integer) in the list
            Min_terms.append(b)

    SOP = ""

    # loop till there are min terms
    for i in Min_terms:
        value = 'A'         #assigning first variable for the equation
        # loop till there are 0's or 1's in each min term
        for j in range(len(i)):
            # checking for complement variable to be used
            if (i[j] =='0'):
                # concatenating value, ' and + in string POS
                SOP = SOP + value+"'"

            # checking for uncomplement variable to be used
            else:
                # concatenating value and + in string POS
                SOP = SOP + value

            # increment the alphabet by 1
            value = chr(ord(value)+1)
            if j < len(i)-1:
                SOP += "."

        # appending the SOP string by '+" after every product term
        SOP = SOP+ "+"
    # for discarding the extra '+' in the last
    SOP = SOP[:-1]
    return SOP

def Convert(protein_eq):
    """Converts POS to SOP"""
    if '(' in protein_eq:       #The equation is standard form, so only POS expression can have brackets
        POS_expr, dict = replace_P(protein_eq)
        no_var = count_no_alphabets(POS_expr)
        Max_terms = Cal_Max_terms(POS_expr)
        SOP_expr = Cal_Min_terms(Max_terms, no_var)
        SOP_expr = replace_A(SOP_expr, dict)
        return SOP_expr

    else:
        return protein_eq

def replace_P(protein_eq):
    """Replaces proteins with alphabets"""
    sums = protein_eq.split(".")                #Get the sums of terms
    alpha_eq = ""
    alpha = 65                                  #Start by assigning alphabets starting from 'A'
    dict = {}
    for i in range(len(sums)):
        terms = sums[i][1:-1].split("+")        #Chop the brackets and get terms
        alpha_eq += "("
        for j in range(len(terms)):
            if terms[j][-1] == "'":             #Check if the terms in complemented
                if terms[j][:-1] not in dict:           #If the key not already in dictionary
                    dict[terms[j][:-1]] = chr(alpha)    #then add one
                    alpha_eq += chr(alpha)+"'"          #Add to the string as well
                    alpha += 1                          #Get the next alphabet
                else:
                    alpha_eq += dict[terms[j][:-1]]+"'"         #If the key is in dictionary then use its value
            else:
                if terms[j] not in dict:
                    dict[terms[j]] = chr(alpha)
                    alpha_eq += chr(alpha)
                    alpha += 1
                else:
                    alpha_eq += dict[terms[j]]

            if j<len(terms)-1:
                alpha_eq += "+"                         #concatenating '+' after every terms

        alpha_eq += ")"
        if i < len(sums)-1:
            alpha_eq += "."                             #concatenating '.' after every sums

    return alpha_eq, dict       #Return equation with alphabets and the dictionary to be used again while replacing back

def replace_A(alpha_eq, dict):
    """Replaces alphabets with proteins"""
    products = alpha_eq.split("+")          #Get the products
    protein_eq = ""
    for i in range(len(products)):
        terms = products[i].split(".")      #Get the terms
        for j in range(len(terms)):
            if terms[j][-1] == "'":         #If the term is complemented
                p = list(dict.keys())[list(dict.values()).index(terms[j][:-1])]         #Get the key of the value from the dictionary
                protein_eq += p+"'"
            else:
                p = list(dict.keys())[list(dict.values()).index(terms[j])]
                protein_eq += p

            if j < len(terms)-1:
                protein_eq += "."           #concatenating '.' after every term

        if i < len(products)-1:
            protein_eq += "+"               #concatenating '+' after every product

    return protein_eq

def DisplayCircuits():
    """Display circuits"""
    f = open("circuits.txt")
    for i in f:
        print(i, end ="")

def DisplayData():
    """Display Data"""
    f = open("Data.txt")
    l = []
    for i in f:
        l.append(i)

    print("Optimized Expression:", l[0])
    print("New Cost:", l[1])
    print("Synthesized Expression into NOT-NOR Form:", l[2])
    print("New Expression with input proteins:", l[3])



