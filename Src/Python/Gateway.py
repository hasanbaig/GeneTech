from py4j.java_gateway import *
import os
import subprocess
import SBOL_File as s
import Logical_Representation_final as l

class Gateway:
    def __init__(self, inputString):
        self.run_java()
        gateway = JavaGateway()
        myclass = gateway.entry_point
        Circuit = myclass.function(inputString)
        f=s.SBOL_File()
        os.system("taskkill /im javaw.exe /f")
        l.Logical_Representation()

    def run_java(self):
        current = os.getcwd()
        os.system(r'"'+current+'\exe\GeneTechJava.exe"')

if __name__ == '__main__':
    inputExp = "IPTG'.aTc'.Arabinose'+IPTG'.aTc.Arabinose'+IPTG.aTc'.Arabinose'"
    #inputExp = "IPTG'.aTc.Arabinose'+IPTG'.aTc.Arabinose+IPTG.aTc.Arabinose'"
    #inputExp = "IPTG.aTc.Arabinose'+IPTG'.aTc.Arabinose'+IPTG.aTc'.Arabinose'"
    #inputExp = "IPTG'.aTc'.Arabinose+IPTG'.aTc.Arabinose+IPTG.aTc'.Arabinose"

    c = Gateway(inputExp)
