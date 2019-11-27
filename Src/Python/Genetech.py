import os
import sys
import time
from PIL import Image
import Gateway as g
import SBOL_File as sbol
import Logical_Representation as logic
import SBOL_visual as visual
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtCore import pyqtSlot, QCoreApplication, QBasicTimer, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QLabel, QLineEdit, QMessageBox, QFileDialog, QTabWidget, QWidget, QListWidget, QProgressBar
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QFont, QPixmap
from itertools import product
from functions import *
from time import sleep
import random

font = QFont("Times", 11)


# The main class which operates the entire widnow
class MainPage(QtWidgets.QMainWindow):
    def __init__(self):
        
        # Lists which are being used in the code later
        self.result=[]
        self.tablist=[]
        self.checkList=[]
        self.checkxmlList=[]
        super(MainPage, self).__init__()

        #Loading the UI file which have been created for the main window
        loadUi('Genetech.ui', self)

        #Setting the logos for the window
        self.setWindowIcon(QtGui.QIcon('SmallLogo.png'))
        self.setWindowTitle("GeneTech - v2.0")
        pixmap = QPixmap('BigLogo.png')
        self.MainLogo.setPixmap(pixmap)
        
        #Intial Label in the status bar
        self.statusBar().showMessage('Ready')

        # Button Entries which have been coded and these are called when button are clicked
        self.SaveButton.clicked.connect(self.SaveLabel)
        self.ViewButton.clicked.connect(self.viewCircuit)
        self.ImportNotesButton.clicked.connect(self.FileOpenDialog)
        self.SaveNotesButton.clicked.connect(self.SaveNotes)
        self.EnterButton.clicked.connect(self.EnterExp)
        self.ExitButton.clicked.connect(self.ResetAll)    

        self.CircuitList.doubleClicked.connect(self.saveImageDialog)        
        self.xmlList.clicked.connect(self.ReadXMLFile)
        self.bexppp = self.InsertExpressionEdit.text()
        self.LabelforList = QLabel(self.tab)
        self.doubleSpinBox.setSuffix(" s")
        self.actionExit.triggered.connect(self.CloseApp)
        self.actionAbout.triggered.connect(self.About)

        #Keyboard Shortcuts for some funtionalities
        self.EnterButton.setShortcut("Return")
        #self.actionSave.setShortcut("Ctrl+S")
        self.actionExit.setShortcut("Ctrl+Q")
        self.actionAbout.setShortcut("Ctrl+O")
        self.ExitButton.setShortcut("Ctrl+R")

        # Messages on the status bar when mouse is hovered on different windows parts
        self.actionAbout.setStatusTip("Know more about GeneTech by clicking this button")  
        self.actionExit.setStatusTip("Reset")
        self.EnterButton.setStatusTip("Press the button for result")
        self.ExitButton.setStatusTip("Exit the window")
        self.InsertExpressionEdit.setStatusTip("Insert a Boolean expression here")
    

    # This funtion reads the txt which of circuits and returns a list
    #with the number of generated circuits by the inserted boolean expression
    def ReadCircuitsFile(self):
        f = open("circuits.txt")
        circuits = []
        for i in f:
            #print(i.replace('\n',''))            
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


    def viewCircuit(self):
        if self.CircuitList.currentItem():
            img = Image.open(str(self.CircuitList.currentItem().text())+".png")
            img.show()


    def SaveLabel(self):
        item = self.CircuitList.currentItem()
        self.saveImageDialog()



    # When the ciruits are developed using the boolean expression
    #This function creates the list of the circuts by reading the
    # txt file of the circuits. It first reads the the number of
    #circuits int the txt and then creates that much entries in the
    #Circuit list available on the main window
    def CreateCircuitList(self):
        circuits = self.ReadCircuitsFile()
        if len(self.checkList) > 0:
            self.CircuitList.clear()
            self.checkList.clear()
            for CircuitIndex in range(CountFiles()):
                self.CircuitList.addItem("Circuit "+str(CircuitIndex+1)+" Logic")
                self.CircuitList.addItem("Circuit "+str(CircuitIndex+1)+" SBOL Visual")
                self.checkList.append("Check")            
        else:
            for CircuitIndex in range(CountFiles()):
                self.CircuitList.addItem("Circuit "+str(CircuitIndex+1)+" Logic")
                self.CircuitList.addItem("Circuit "+str(CircuitIndex+1)+" SBOL Visual")
                self.checkList.append("Check")         
 
   
    #Code for importing a file in Notes
    def FileOpenDialog(self):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            UserfileName, _ = QFileDialog.getOpenFileName(self,"Import File to Notes", "","All Files (*);;TxtFiles (*.txt)", options=options)
            if UserfileName:
                print(UserfileName)
                f = open(UserfileName,"r")
                data = f.read()
                self.Notes.setText(data)
                

    # When the ciruits are developed using the boolean expression
    #This function creates the list of XML files of the
    #generated circuts by reading the
    # txt file of the circuits. It first reads the the number of
    #circuits int the txt and then creates that much entries in the
    #SBOL file list available on the main window. User can click on the
    #file and save it for later use
    def CreateXMLList(self):
        circuits = self.ReadCircuitsFile()
        if len(self.checkxmlList) > 0:
            self.xmlList.clear()
            self.checkxmlList.clear()
            print(self.checkxmlList)
            for CircuitIndex in range(CountFiles()):
                self.xmlList.addItem("SBOL File "+str(CircuitIndex+1))
                self.checkxmlList.append("Check")            
        else:
            for CircuitIndex in range(CountFiles()):
                self.xmlList.addItem("SBOL File "+str(CircuitIndex+1))
                self.checkxmlList.append("Check")




    #This funtoin is created to save the xml file for the generated circuits.
    #Upon clicking this function open a saving browser and ask user to enter a
    #UserfileName (the name with the user wants to save the file). It checks if
    #a file with same name already exists. If yes, then it asks for replacement.
    #If not, then it create a file with the given name. Hereafter, it opens a file
    #with the same name as the name clicked on the list. It reads it and copies
    #whole data to the newly created file.
    def FileSaveDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        UserfileName, _ = QFileDialog.getSaveFileName(self,"Save SBOL File","","All Files (*);;XML Files (*.xml)", options=options)
        if UserfileName:
            fileName = UserfileName.split("/")[-1]
            if (":" in fileName) or ("?" in fileName) or ("/" in fileName) or ("*" in fileName) or ("<" in fileName) or (">" in fileName) or ("|" in fileName) or ('"' in fileName):
                QMessageBox.about(self, "Alert", "A file name can't contain any of the following \n \ / : * ? < > |")
            else:
                print(UserfileName)
                f= open(UserfileName,"w+")
                item = self.xmlList.currentItem()
                fo = open(str(item.text())+".xml")
                for i in fo:
                    f.write(i)



    def ReadXMLFile(self):
        item = self.xmlList.currentItem()
        file = item.text()
        f = open(str(file)+".xml","r")
        data = f.read()
        self.Notes.setText(data)


    #THis functions save the text from the Notes Tab on Main window
    def SaveNotes(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        InputFile, _ = QFileDialog.getSaveFileName(self,"Save Notes","","All Files (*);;Txt Files (*.txt)", options=options)
        Text = self.Notes.toPlainText()
        if InputFile:
            f= open(InputFile+".xml","w+") 
            f.write(Text)



    #This funtoin is created to save an image file for the generated circuits.
    #Upon clicking this function open a saving browser ans ask user to enter a
    #UserfileName (the name with the user wants to save the file). It checks if
    #a file with same name already exists. If yes, then it asks for replacement.
    #If not, then it create a file with the given name. Hereafter, it opens a file
    #with the same name as the name clicked on the list. It reads it and saves that
    #image as a newly created file.
    def saveImageDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        UserfileName, _ = QFileDialog.getSaveFileName(self,"Save Image File","","All Files (*);;Image Files (*.png)", options=options)
        if UserfileName:
            fileName = UserfileName.split("/")[-1]
            if (":" in fileName) or ("?" in fileName) or ("/" in fileName) or ("*" in fileName) or ("<" in fileName) or (">" in fileName) or ("|" in fileName) or ('"' in fileName):
                QMessageBox.about(self, "Alert", "A file name can't contain any of the following \n \ / : * ? < > |")
            else:
                print(UserfileName)
                item = self.CircuitList.currentItem() #the selected item
                saveimg  = Image.open(str(item.text())+".png") #use this image to save
                saveimg.save(str(UserfileName)+".png") #save image as

#or "?" in UserfileName or "/" in UserfileName or "*" in UserfileName or "<" in UserfileName or ">" in UserfileName or "|" in UserfileName or '"' in UserfileName:



    #This function, upon clicking the reset button on main window,
    #clears all the generated/entered values on the main wondow
    def ResetAll(self):
        print("comes here")
        mBox = QMessageBox.question(self, "Warning!!", "Are you sure you want to clear?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if mBox == QMessageBox.Yes:
            #sys.exit()
            self.InsertExpressionEdit.clear()
            self.spinBox.setValue(10)
            self.doubleSpinBox.setValue(100)
            self.CircuitSpinBox.value(10)
            self.xmlList.clear()
            self.CircuitList.clear()
            self.TruthList.clear()
            self.ProgressBar.setValue(0)
            self.Notes.clear()


    def ResetBeforeNew(self):
        self.xmlList.clear()
        self.CircuitList.clear()
        self.TruthList.clear()
        self.ProgressBar.setValue(0)
        self.Notes.clear()


    #This function is dedicated to the close the main wondow
    # upon cliking the Close button it gives the warnign and
    #upon approval it closes the system. By default, No is
    #selected in case the user mistakenly clicks the close butotn
    #and presses the enter button.
    def CloseApp(self):
        print("CloseApp")
        mBox = QMessageBox.question(self, "Warning!!", "Are you sure you want exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if mBox == QMessageBox.Yes:
            sys.exit()

    def About(self):
        print("It's About GeneTech")
        os.startfile('AboutGenetech.txt')

    #This is the most important function of this code.
    #First of all it takes the boolean, using that it generates
    #the circuits using the function g.Gateway(bexp). It also
    #replaces the notations in inserted expression. For example,
    #'and' operation in pyton is either expresssed as "and" or "&",
    #but user inserts it as a dot(.) which is the  how generally
    #'and' is written in an expression. Therfore all the notations are
    #changed accordingly. Then this function uses the expression to
    #generate the truth table
    ttList=[]
    List_TruthTable_Input =[]
    def EnterExp(self):
        if self.DelayRadioButton.isChecked():
            option = 0
        elif self.GatesRadioButton.isChecked():
            option = 1
        a=0
        bexp = self.InsertExpressionEdit.text() #User expression
        print(bexp)
        if bexp == "":
            mBox1 = QMessageBox.about(self, "Alert", "Please insert the expression") # warning in case of empty expression
        elif " " in bexp:
            mBox1 = QMessageBox.about(self, "Alert", "Please remove the spaces from the input expression")
        elif not bexp:
            bexp = 'a'  
        else:
            self.ProgressBar.setVisible(True)
            #self.Progress()
            self.ProgressBar.setValue(0)
            self.result.append("a")
            print(bexp,"################")
            g.Gateway(bexp)
            self.ProgressBar.setValue(25)
            sleep(1.5)
            number = random.randint(30,70)
            self.ProgressBar.setValue(number)
            sbol.SBOL_File(self.spinBox.value(), self.doubleSpinBox.value(), option, self.CircuitSpinBox.value()) #create SBOl files
            number = random.randint(75,90)
            self.ProgressBar.setValue(number)
            sleep(2)
            logic.Logical_Representation(self.spinBox.value(), self.doubleSpinBox.value(), option, self.CircuitSpinBox.value()) #Create Logical Representation images
            visual.SBOLv(self.spinBox.value(), self.doubleSpinBox.value(), option, self.CircuitSpinBox.value())   #create SBOL visual Representation images
            self.ProgressBar.setValue(100)

            print(bexp)
            bexp = Convert(bexp)
            print(bexp)
            bexp = "".join(bexp.split())
            #bexp = bexp.strip() #Remove spaces in the expression
            finalexp=[]
            exp = bexp.split("+") #change the notations
            for i in range(len(exp)):
                term = exp[i].split(".")
                finalterm=[]
                for j in range(len(term)):
                    if term[j][-1]=="'":
                        finalterm.append("not(" + term[j][:-1] + ")")
                    else:
                        finalterm.append(term[j])
                finalexp.append("("+" and ".join(finalterm)+")")
            bexp = " or ".join(finalexp)
            code = compile(bexp, '', 'eval') #evaluation of expression
            TruthTable_Input = code.co_names # Generates the number of inputs in an expression. In a.b there are 2 inputs 'a' and 'b'
            for values1 in product(range(2), repeat=len(TruthTable_Input)): # generate the values of entrid 
                header_count=2**(len(values1))
                List_TruthTable_Input = [[] for i in range(1, header_count+1)]
            self.TruthList.clear()
            for BexpIndex in range(len(TruthTable_Input)): #make the list for TruthTable_Input to show on main window
                self.ttList.append(TruthTable_Input[BexpIndex])
                self.ttList.append("   ")
            self.ttList.append(":   ")
            self.ttList.append(bexp)
            print(self.ttList)
            s = [str(i) for i in self.ttList]
            res = " ".join(s)
            self.TruthList.addItem(res)
            self.ttList.clear()
            for values in product(range(2), repeat=len(TruthTable_Input)):# put inputs of espression together
                for w in range(len(values)):
                    List_TruthTable_Input[a].append(str(values[w]))
                a+=1
                env = dict(zip(TruthTable_Input, values)) #put the TruthTable_Input and values togather
                pk = int(eval(code, env)) #generate the output of truthtable
                print(' '.join(str(v) for v in values), ':', pk) #join ouput and insput and print
                for v in values: #append the list to show on main window
                   self.ttList.append(v)
                   self.ttList.append("     ")
                self.ttList.append(":       ")
                self.ttList.append(pk)
                s = [str(i) for i in self.ttList]
                res = " ".join(s)
                self.TruthList.addItem(res) 
                self.ttList.clear()
        if len(self.result) > 0: #Call these functions only if there is an expression 
            self.CreateCircuitList()
            self.CreateXMLList()
            self.result.clear()
        
            
            

if __name__ == "__main__":
    app = QCoreApplication.instance()               # Fixes error with kernel crashing on second run of application
    if app is None:                                 # PyQt doesn't like multiple QApplications in the same process, therefore
        app = QtWidgets.QApplication(sys.argv)                # apart from the initial run, the first QApplication instance will run
    widget = MainPage()
    widget.show()
    sys.exit(app.exec_())
