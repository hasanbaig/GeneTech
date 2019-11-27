from py4j.java_gateway import *
import os
import subprocess
from functions import *

class Gateway:
    def __init__(self, inputString):
        inputString = Convert(inputString)
        self.run_java()
        gateway = JavaGateway() #A JavaGateway instance is connected to a Gateway instance on the Java side
        myclass = gateway.entry_point #JavaGateway instance is connected to the Gateway.entryPoint instance on the Java side.
        Circuit = myclass.function(inputString) #Call a function from the instance on Java side
        os.system("taskkill /im javaw.exe /f") #close the JavaGateway instance so it would be ready to connect next time


    def run_java(self):
        current = os.getcwd() #get current path
        os.system(r'"'+current+'\exe\GeneTechJava.exe"') #run .exe file

if __name__ == '__main__':
    #inputExp = "IPTG.aTc.Arabinose'+IPTG'.aTc.Arabinose'+IPTG.aTc'.Arabinose'"
    #inputExp = "(IPTG+aTc+Arabinose').(IPTG'+aTc'+Arabinose').(IPTG+aTc'+Arabinose).(IPTG+aTc'+Arabinose')"
    inputExp = "(IPTG+aTc+Arabinose').(IPTG'+aTc'+Arabinose').(IPTG+aTc'+Arabinose).(IPTG+aTc'+Arabinose')"
    #inputExp = "IPTG'.aTc'.Arabinose'+IPTG.aTc'.Arabinose'+IPTG.aTc'.Arabinose+IPTG.aTc.Arabinose'"
    #inputExp = "a.b.c'+a'.b.c'+a.b'.c'"
    #inputExp = "IPTG'.aTc.Arabinose'+IPTG'.aTc.Arabinose+IPTG.aTc.Arabinose'"
    #inputExp = "IPTG'.aTc'.Arabinose+IPTG.aTc'.Arabinose'+IPTG.aTc'.Arabinose"
    #Gateway(inputExp, 1000, 1000, 0, 10)
    os.system("taskkill /im javaw.exe /f")

