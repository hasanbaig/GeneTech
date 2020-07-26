from sbol2 import *
from functions import *
import pandas as pd

class SBOL_File:
    def __init__(self, total_gates, total_time, option, num):
        DeleteExistingFiles()
        circuits = ReadFile()
        Component_strings = self.ListOfLines(circuits)
        self.geneticPartsDf = None #dataframe containing information of genetic parts such as DNA sequence
        self.gateRBS = {} #gets rbs corresponding to the gate
        self.readGeneticParts()
        self.gateRBSMapping()
        self.CreateFile(Component_strings, len(Component_strings), total_gates, total_time, option, num)
    
    def readGeneticParts(self):
        """
        This function loads the csv file genetic_parts.csv into a 
        pandas dataframe for better access when adding sequences
        """
        self.geneticPartsDf = pd.read_csv("genetic_parts.csv")


    def gateRBSMapping(self):
        """
        This function creates a mapping between a gate and it's corresponding 
        RBS (AmeR is mappedd to A1, PhlF mapped to P1, and so on) as given in the
        genetic_parts.csv file
        """ 
        listGates = self.geneticPartsDf.loc[self.geneticPartsDf.type == "CDS"].part
        for i in listGates:
            if i != "YFP":
                rbs = self.geneticPartsDf.loc[self.geneticPartsDf.gate == i].part.values[0]
                self.gateRBS[i] = rbs

    def ListOfLines(self, circuits):
        #This function filters out the unwanted characters from every line of each circuit
        chac = '->|^'
        Component_strings = []
        for i in circuits:
            line = []
            for j in i:
                str = ''
                for k in j:
                    if k not in chac:
                        str += k
                line.append(str)
            Component_strings.append(line)

        return Component_strings

    def CreateFile(self, input_list, circuits, total_gates, total_time, option, num):
        for i in range(circuits): #iter for each circuit
            file_num = SortNum(i, option) + 1
            if Total_Gates(i) <= total_gates and Total_time(i) <= total_time and file_num <= num:   #If Total Delay and number of gates are less than the input
                setHomespace('http://sbols.org/Output_Circuit'+str(i)) #sets the default URI prefix for every object
                #To avoid collision in objects, as we don't want to use the same Id in different type of objects
                Config.setOption('sbol_typed_uris', False)
                version = '1.0.0' #There will only be one version of every object
                doc=Document()
                component_defs = [] #A list to contain objects themselves
                componentDef_string = [] #A list to contain name of the objects
                count=1 #A variable to assign number to terminators

                #Create ModuleDefinition of the device, which will contain the FunctionalComponent of the device connected to its ComponentDefinition
                Circuit = ModuleDefinition('Output_Circuit_' + str(i+1))
                Circuit.name = 'Output Circuit Module'
                doc.addModuleDefinition(Circuit)

                #Create ComponentDefinition for the whole Device which will contain the Components of each part and the SequenceConstraints
                Device = ComponentDefinition('Output_Device_' + str(i+1))
                Device.name = 'Output_Device ' + str(i+1) + ' Component'
                doc.addComponentDefinition(Device)

                
                Circuit_fc = Circuit.functionalComponents.create('Device')
                Circuit_fc.name = 'Device'
                #This Functional Component needs a unique ID of the part it belongs to, in this case it belongs to the Device itself
                Circuit_fc.definition = Device.identity
                Circuit_fc.access = SBOL_ACCESS_PUBLIC
                Circuit_fc.direction = SBOL_DIRECTION_NONE
                
                ### Terminator ###
                terminator = self.geneticPartsDf.loc[self.geneticPartsDf.type == "Terminator"]
                terminatorName = terminator.part.values[0]
                terminatorSeq = terminator.sequence.values[0]
                terminatorSeqObj = Sequence(terminatorName+"_sequence", terminatorSeq)
                
                sequences = [terminatorSeqObj] #these will be added later to the doc
                finalSequenceList = []
                Terminator = ComponentDefinition(terminatorName, BIOPAX_DNA)
                Terminator.roles = SO_TERMINATOR
                Terminator.sequence = terminatorSeqObj
                doc.addComponentDefinition(Terminator)
                
                for j in range(len(input_list[i])): #iter for each line of the circuit
                    splitted_components = input_list[i][j].split()      #each part in a line
                    name_line = []      #List to contain names of each part
                    def_line = []       #List to contain Component Definitions of each part
                    for k in range(len(splitted_components)):       #Loop to get the individual names of promotors and coding sequences in the list
                        if splitted_components[k][0] == '(':        #if the part is a coding sequence
                            name = splitted_components[k][1:-1]
                            Comp = ComponentDefinition(name, BIOPAX_DNA)
                            Comp.roles = SO_CDS
                            seqCDS = self.geneticPartsDf.loc[self.geneticPartsDf.part == name]   
                            #print(name, seqCDS)                             
                            seqName = seqCDS.part.values[0] 
                            seqValue = seqCDS.sequence.values[0]
                            seqObj = Sequence(seqName+"_sequence", seqValue)      
                            sequences.append(seqObj)
                            Comp.sequence = seqObj  
                            
                            if name != "YFP":
                                rbs = self.gateRBS[name]
                                seqCDS = self.geneticPartsDf.loc[self.geneticPartsDf.part == rbs]
                                seqName = seqCDS.part.values[0] 
                                seqValue = seqCDS.sequence.values[0]
                                seqObj = Sequence(seqName+"_sequence", seqValue)
                                sequences.append(seqObj)
                                RBS = ComponentDefinition(rbs, BIOPAX_DNA)
                                RBS.roles = SO_RBS
                                RBS.sequence = seqObj
                                
                                doc.addComponentDefinition(RBS)
                                
                                def_line.append(RBS)
                                name_line.append(rbs)
                                
                            def_line.append(Comp)
                            name_line.append(splitted_components[k])
                            
                            Terminator = ComponentDefinition(terminatorName+"__"+str(count), BIOPAX_DNA)
                            Terminator.roles = SO_TERMINATOR
                            Terminator.sequence = terminatorSeqObj
                            def_line.append(Terminator)
                            name_line.append(terminatorName+"__"+str(count))
                            
                            #Terminator = ComponentDefinition('Terminator' + str(count), BIOPAX_DNA)
                            #Terminator.roles = SO_TERMINATOR
                            #doc.addComponentDefinition(Terminator)
                            #def_line.append(Terminator)
                            #name_line.append('Terminator' + str(count))
                            count+=1
                        else:
                            Comp = ComponentDefinition(splitted_components[k], BIOPAX_DNA)
                            Comp.roles = SO_PROMOTER
                            seqCDS = self.geneticPartsDf.loc[self.geneticPartsDf.part == splitted_components[k]]   
                            #print(name, seqCDS)                             
                            seqName = seqCDS.part.values[0] 
                            seqValue = seqCDS.sequence.values[0]
                            seqObj = Sequence(seqName+"_sequence", seqValue)      
                            sequences.append(seqObj)
                            Comp.sequence = seqObj  

                            def_line.append(Comp)
                            name_line.append(splitted_components[k])

                        doc.addComponentDefinition(Comp)

                    component_defs.append(def_line)
                    componentDef_string.append(name_line)

                #if circuit has 2 lines, add the 2nd line to the start of the first to match sbol visaul
                if len(component_defs) > 1:
                    finalComp = component_defs[1][:] 
                    finalCompString = componentDef_string[1][:]
                    finalComp.extend(component_defs[0][:])
                    finalCompString.extend(componentDef_string[0][:])
                else:
                    finalComp = component_defs[0][:]
                    finalCompString = componentDef_string[0][:]
                #print(finalComp)
                #print(componentDef_string)
                #print(finalCompString)
                Device.assemblePrimaryStructure(finalComp)
                print("DNA : ", Device.compile())
                #For the Flourescent Protein, which is the last element of the first line of the circuit
                FP_protein = ComponentDefinition(componentDef_string[0][-2][1:-1]+'_Protein', BIOPAX_PROTEIN)
                doc.addComponentDefinition(FP_protein)

                FP_protein_c = Device.components.create(componentDef_string[0][-2][1:-1]+'_Protein')
                FP_protein_c.definition = FP_protein.identity
                FP_protein_c.access = SBOL_ACCESS_PUBLIC

                Components = []     #List to store all the Components class of each part
                for j in range(len(componentDef_string)):       #This loop creates those Components
                    Components_line = []
                    for k in range(len(componentDef_string[j])):
                        name = componentDef_string[j][k] + "_component"
                        
                        if componentDef_string[j][k][0] == '(':
                            name = componentDef_string[j][k][1:-1] + "_component"

                        name_c = Device.components.create(name)
                        name_c.definition = component_defs[j][k].identity
                        name_c.access = SBOL_ACCESS_PUBLIC
                        Components_line.append(name_c)
                        
                    Components.append(Components_line)

                s_contraint_list = []
                for j in range(len(componentDef_string)):       #This loop is to create the SequenceConstraints class to defines the Orientation of the device
                    for k in range(len(componentDef_string[j])-1):
                        
                        if componentDef_string[j][k+1][0] == '(':
                            name = componentDef_string[j][k] + '_precedes_' + componentDef_string[j][k+1][1:-1]
                            #S_constraint = Device.sequenceConstraints.create(componentDef_string[j][k] + '_precedes_' + componentDef_string[j][k+1][1:-1])

                        elif componentDef_string[j][k][0] == '(':
                            name = componentDef_string[j][k][1:-1] + '_precedes_' + componentDef_string[j][k+1]
                            #S_constraint = Device.sequenceConstraints.create(componentDef_string[j][k][1:-1] + '_precedes_' + componentDef_string[j][k+1])

                        else:
                            name = componentDef_string[j][k] + '_precedes_' + componentDef_string[j][k+1]
                            #S_constraint = Device.sequenceConstraints.create(componentDef_string[j][k] + '_precedes_' + componentDef_string[j][k+1])

                        if name not in s_contraint_list:
                            s_contraint_list.append(name)
                            S_constraint = Device.sequenceConstraints.create(name)
                            S_constraint.subject = Components[j][k].identity        #Subject is the part that comes first
                            S_constraint.object = Components[j][k+1].identity       #Object is the part that comes later
                            S_constraint.restriction = SBOL_RESTRICTION_PRECEDES    #This describes the order we have defined for this Constraint

                        if j == 0 and componentDef_string[j][k][0] == '(':      #for the coding sequences in the first line of the circuit
                            #For the Module Definition, we only need the coding sequence and the output promotor
                            cds_fc = Circuit.functionalComponents.create(componentDef_string[j][k][1:-1])
                            cds_fc.definition = component_defs[j][k].identity       #Connected to its ComponentDefinition class
                            cds_fc.access = SBOL_ACCESS_PUBLIC
                            cds_fc.direction = SBOL_DIRECTION_NONE

                            if componentDef_string[j][k] != componentDef_string[0][-2]:     #If the component is not the flourescent protein
                                #Create Functional Component of the output promotor
                                P_fc = Circuit.functionalComponents.create(componentDef_string[j][k+2])
                                P_fc.definition = component_defs[j][k+2].identity
                                P_fc.access = SBOL_ACCESS_PUBLIC
                                P_fc.direction = SBOL_DIRECTION_NONE

                                #Define the Interaction between those two Functional Components
                                Repression= Circuit.interactions.create(componentDef_string[j][k][1:-1] + '_represses_' + componentDef_string[j][k+2])
                                Repression.types = SBO_INHIBITION

                                cds_participation = Repression.participations.create(componentDef_string[j][k][1:-1])
                                cds_participation.roles = SBO_INHIBITOR
                                cds_participation.participant = cds_fc.identity

                                P_participation = Repression.participations.create(componentDef_string[j][k+2])
                                P_participation.roles = SBO_INHIBITED
                                P_participation.participant = P_fc.identity

                                #Map the participants from ModuleDefinition to their Component
                                cds_map = Circuit_fc.mapsTos.create(componentDef_string[j][k][1:-1] + '_map')
                                cds_map.refinement = SBOL_REFINEMENT_USE_REMOTE
                                cds_map.local = cds_fc.identity
                                cds_map.remote = Components[j][k].identity

                                P_map = Circuit_fc.mapsTos.create(componentDef_string[j][k+2] + '_map')
                                P_map.refinement = SBOL_REFINEMENT_USE_REMOTE
                                P_map.local = P_fc.identity
                                P_map.remote = Components[j][k+2].identity

                            else:       #If its Flourescent Protein
                                FP_fc = Circuit.functionalComponents.create(componentDef_string[0][-2][1:-1]+'_Protein')
                                FP_fc.definition = FP_protein.identity
                                FP_fc.access = SBOL_ACCESS_PUBLIC
                                FP_fc.direction = SBOL_DIRECTION_NONE

                                Production= Circuit.interactions.create(componentDef_string[0][-2][1:-1]+'_produces_'+componentDef_string[0][-2][1:-1]+'_Protein')
                                Production.types = SBO_GENETIC_PRODUCTION

                                cds_participation = Production.participations.create(componentDef_string[j][k][1:-1])
                                cds_participation.roles = SBO + '0000645'       #The role for the coding sequence of the flourescent protein is not defined
                                cds_participation.participant = cds_fc.identity

                                FP_participation = Production.participations.create(componentDef_string[0][-2][1:-1]+'_Protein')
                                FP_participation.roles = SBO_PRODUCT
                                FP_participation.participant = FP_fc.identity

                                cds_map = Circuit_fc.mapsTos.create(componentDef_string[j][k][1:-1] + '_map')
                                cds_map.refinement = SBOL_REFINEMENT_USE_REMOTE
                                cds_map.local = cds_fc.identity
                                cds_map.remote = Components[j][k].identity

                                FP_map = Circuit_fc.mapsTos.create(componentDef_string[0][-2][1:-1]+'_Protein_map')
                                FP_map.refinement = SBOL_REFINEMENT_USE_REMOTE
                                FP_map.local = FP_fc.identity
                                FP_map.remote = FP_protein_c.identity

                    if j!=0:        #For the remaining lines of the circuit
                        if j == len(componentDef_string)-1:     #To avoid intersection of Repression Lines
                            #The sequnece was already made for the lines but we have to connect this part to the circuit as well, so it gets connected to the first part in first line of the circuit
                            S_constraint = Device.sequenceConstraints.create(componentDef_string[j][-1] + '_precedes_' + componentDef_string[0][0])
                            S_constraint.subject = Components[j][-1].identity
                            S_constraint.object = Components[0][0].identity
                            S_constraint.restriction = SBOL_RESTRICTION_PRECEDES
                        else:
                            S_constraint = Device.sequenceConstraints.create(componentDef_string[j][-1] + '_precedes_' + componentDef_string[j+1][0])
                            S_constraint.subject = Components[j][-1].identity
                            S_constraint.object = Components[j+1][0].identity
                            S_constraint.restriction = SBOL_RESTRICTION_PRECEDES

                        if componentDef_string[j][k][0] == '(':
                            print("BUG HERE") # componentDef_string[j][1] instead of componentDef_string[j][k] 
                            cds_fc = Circuit.functionalComponents.create(componentDef_string[j][k][1:-1])
                            cds_fc.definition = component_defs[j][k].identity
                            cds_fc.access = SBOL_ACCESS_PUBLIC
                            cds_fc.direction = SBOL_DIRECTION_NONE

                            if ('P' + componentDef_string[j][k][1:-1]) in componentDef_string[0]:       #To find the inhibitant Promotor for this coding sequence in the circuit
                                index_of_myP = componentDef_string[0].index('P' + componentDef_string[j][k][1:-1])

                                P_fc = Circuit.functionalComponents.create(componentDef_string[0][index_of_myP])
                                P_fc.definition = component_defs[0][index_of_myP].identity
                                P_fc.access = SBOL_ACCESS_PUBLIC
                                P_fc.direction = SBOL_DIRECTION_NONE

                                Repression= Circuit.interactions.create(componentDef_string[j][k][1:-1] + '_represses_' + componentDef_string[0][index_of_myP])
                                Repression.types = SBO_INHIBITION

                                cds_participation = Repression.participations.create(componentDef_string[j][k][1:-1])
                                cds_participation.roles = SBO_INHIBITOR
                                cds_participation.participant = cds_fc.identity

                                P_participation = Repression.participations.create(componentDef_string[0][index_of_myP])
                                P_participation.roles = SBO_INHIBITED
                                P_participation.participant = P_fc.identity

                                cds_map = Circuit_fc.mapsTos.create(componentDef_string[j][k][1:-1] + '_map')
                                cds_map.refinement = SBOL_REFINEMENT_USE_REMOTE
                                cds_map.local = cds_fc.identity
                                cds_map.remote = Components[j][k].identity

                                P_map = Circuit_fc.mapsTos.create(componentDef_string[0][index_of_myP] + '_map')
                                P_map.refinement = SBOL_REFINEMENT_USE_REMOTE
                                P_map.local = P_fc.identity
                                P_map.remote = Components[0][index_of_myP].identity

                            else:       #If the inhabitant is not in first line
                                index_of_myP = componentDef_string[1].index('P' + componentDef_string[j][k][1:-1])

                                P_fc = Circuit.functionalComponents.create(componentDef_string[1][index_of_myP])
                                P_fc.definition = component_defs[1][index_of_myP].identity
                                P_fc.access = SBOL_ACCESS_PUBLIC
                                P_fc.direction = SBOL_DIRECTION_NONE

                                Repression= Circuit.interactions.create(componentDef_string[j][k][1:-1] + '_represses_' + componentDef_string[1][index_of_myP])
                                Repression.types = SBO_INHIBITION

                                cds_participation = Repression.participations.create(componentDef_string[j][k][1:-1])
                                cds_participation.roles = SBO_INHIBITOR
                                cds_participation.participant = cds_fc.identity

                                P_participation = Repression.participations.create(componentDef_string[1][index_of_myP])
                                P_participation.roles = SBO_INHIBITED
                                P_participation.participant = P_fc.identity

                                cds_map = Circuit_fc.mapsTos.create(componentDef_string[j][k][1:-1] + '_map')
                                cds_map.refinement = SBOL_REFINEMENT_USE_REMOTE
                                cds_map.local = cds_fc.identity
                                cds_map.remote = Components[j][k].identity

                                P_map = Circuit_fc.mapsTos.create(componentDef_string[1][index_of_myP] + '_map')
                                P_map.refinement = SBOL_REFINEMENT_USE_REMOTE
                                P_map.local = P_fc.identity
                                P_map.remote = Components[1][index_of_myP].identity
                print("here")
                result = doc.write("user_files/"+"SBOL File " + str(file_num) +".xml")        #To save the SBOL File
                print("here ", result)

if __name__ == '__main__':
    #inputExp = "IPTG'.aTc'.Arabinose'+IPTG'.aTc.Arabinose'+IPTG.aTc'.Arabinose'"
    f = SBOL_File(1000, 1000)
