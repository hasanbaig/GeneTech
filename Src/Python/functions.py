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



