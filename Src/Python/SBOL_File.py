from sbol import *
import os
import glob

class SBOL_File:
    def __init__(self):
        self.DeleteExistingFiles()
        self.circuits = self.ReadFile()
        self.Component_strings = self.ListOfComponents(self.circuits)
        File = self.CreateFile(self.Component_strings, len(self.Component_strings))

    def DeleteExistingFiles(self):
        list = glob.glob('**/*.xml', recursive=True)
        for i in range(len(list)):
            os.remove(list[i])

    def ReadFile(self):
        f = open("circuits.txt")
        circuits = []
        for i in f:
            print(i.replace('\n',''))
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

    def ListOfComponents(self, circuits):
        chac = '->|^'
        Component_strings = []
        for i in circuits:
            cnt = []
            for j in i:
                str = ''
                for k in j:
                    if k not in chac:
                        str += k
                cnt.append(str)
            Component_strings.append(cnt)

        return Component_strings

    def CreateFile(self, input_list, cnt):
        for i in range(cnt):
            setHomespace('http://sbols.org/Output_Circuit'+str(i))
            Config.setOption('sbol_typed_uris', False)
            version = '1.0.0'
            doc=Document()
            component_defs = []
            componentDef_string = []
            count=1

            Device = ComponentDefinition('Output_Device_' + str(i+1))
            Device.name = 'Output_Device ' + str(i+1) + ' Component'
            doc.addComponentDefinition(Device)

            Circuit = ModuleDefinition('Output_Circuit_' + str(i+1))
            Circuit.name = 'Output Circuit Module'
            doc.addModuleDefinition(Circuit)

            Circuit_fc = Circuit.functionalComponents.create('Device')
            Circuit_fc.name = 'Device'
            Circuit_fc.definition = Device.identity
            Circuit_fc.access = SBOL_ACCESS_PUBLIC
            Circuit_fc.direction = SBOL_DIRECTION_NONE

            for j in range(len(input_list[i])):
                splitted_components = input_list[i][j].split()
                name_line = []
                def_line = []
                for k in range(len(splitted_components)):
                    if splitted_components[k][0] == '(':
                        Comp = ComponentDefinition(splitted_components[k][1:-1], BIOPAX_DNA)
                        Comp.roles = SO_CDS
                        def_line.append(Comp)
                        name_line.append(splitted_components[k])

                        Terminator = ComponentDefinition('Terminator' + str(count), BIOPAX_DNA)
                        Terminator.roles = SO_TERMINATOR
                        doc.addComponentDefinition(Terminator)
                        def_line.append(Terminator)
                        name_line.append('Terminator' + str(count))
                        count+=1
                    else:
                        Comp = ComponentDefinition(splitted_components[k], BIOPAX_DNA)
                        Comp.roles = SO_PROMOTER
                        def_line.append(Comp)
                        name_line.append(splitted_components[k])

                    doc.addComponentDefinition(Comp)

                component_defs.append(def_line)
                componentDef_string.append(name_line)

            YFP_protein = ComponentDefinition('YFP_Protein', BIOPAX_PROTEIN)
            doc.addComponentDefinition(YFP_protein)

            YFP_protein_c = Device.components.create('YFP_Protein')
            YFP_protein_c.definition = YFP_protein.identity
            YFP_protein_c.access = SBOL_ACCESS_PUBLIC

            Components = []
            for j in range(len(componentDef_string)):
                Components_line = []
                for k in range(len(componentDef_string[j])):
                    if componentDef_string[j][k][0] == '(':
                        name_c = Device.components.create(componentDef_string[j][k][1:-1])
                    else:
                        name_c = Device.components.create(componentDef_string[j][k])

                    name_c.definition = component_defs[j][k].identity
                    name_c.access = SBOL_ACCESS_PUBLIC
                    Components_line.append(name_c)

                Components.append(Components_line)

            for j in range(len(componentDef_string)):
                for k in range(len(componentDef_string[j])-1):
                    if componentDef_string[j][k+1][0] == '(':
                        S_constraint = Device.sequenceConstraints.create(componentDef_string[j][k] + '_precedes_' + componentDef_string[j][k+1][1:-1])

                    elif componentDef_string[j][k][0] == '(':
                        S_constraint = Device.sequenceConstraints.create(componentDef_string[j][k][1:-1] + '_precedes_' + componentDef_string[j][k+1])

                    else:
                        S_constraint = Device.sequenceConstraints.create(componentDef_string[j][k] + '_precedes_' + componentDef_string[j][k+1])


                    S_constraint.subject = Components[j][k].identity
                    S_constraint.object = Components[j][k+1].identity
                    S_constraint.restriction = SBOL_RESTRICTION_PRECEDES

                    if j == 0 and componentDef_string[j][k][0] == '(':
                        cds_fc = Circuit.functionalComponents.create(componentDef_string[j][k][1:-1])
                        cds_fc.definition = component_defs[j][k].identity
                        cds_fc.access = SBOL_ACCESS_PUBLIC
                        cds_fc.direction = SBOL_DIRECTION_NONE

                        if componentDef_string[j][k] != '(YFP)':

                            P_fc = Circuit.functionalComponents.create(componentDef_string[j][k+2])
                            P_fc.definition = component_defs[j][k+2].identity
                            P_fc.access = SBOL_ACCESS_PUBLIC
                            P_fc.direction = SBOL_DIRECTION_NONE

                            Repression= Circuit.interactions.create(componentDef_string[j][k][1:-1] + '_represses_' + componentDef_string[j][k+2])
                            Repression.types = SBO_INHIBITION

                            cds_participation = Repression.participations.create(componentDef_string[j][k][1:-1])
                            cds_participation.roles = SBO_INHIBITOR
                            cds_participation.participant = cds_fc.identity

                            P_participation = Repression.participations.create(componentDef_string[j][k+2])
                            P_participation.roles = SBO_INHIBITED
                            P_participation.participant = P_fc.identity

                            cds_map = Circuit_fc.mapsTos.create(componentDef_string[j][k][1:-1] + '_map')
                            cds_map.refinement = SBOL_REFINEMENT_USE_REMOTE
                            cds_map.local = cds_fc.identity
                            cds_map.remote = Components[j][k].identity

                            P_map = Circuit_fc.mapsTos.create(componentDef_string[j][k+2] + '_map')
                            P_map.refinement = SBOL_REFINEMENT_USE_REMOTE
                            P_map.local = P_fc.identity
                            P_map.remote = Components[j][k+2].identity

                        else:
                            YFP_fc = Circuit.functionalComponents.create('YFP_Protein')
                            YFP_fc.definition = YFP_protein.identity
                            YFP_fc.access = SBOL_ACCESS_PUBLIC
                            YFP_fc.direction = SBOL_DIRECTION_NONE

                            Production= Circuit.interactions.create('YFP_produces_YFP_Protein')
                            Production.types = SBO_GENETIC_PRODUCTION

                            cds_participation = Production.participations.create(componentDef_string[j][k][1:-1])
                            cds_participation.roles = SBO + '0000645'
                            cds_participation.participant = cds_fc.identity

                            YFP_participation = Production.participations.create('YFP_Protein')
                            YFP_participation.roles = SBO_PRODUCT
                            YFP_participation.participant = YFP_fc.identity

                            cds_map = Circuit_fc.mapsTos.create(componentDef_string[j][k][1:-1] + '_map')
                            cds_map.refinement = SBOL_REFINEMENT_USE_REMOTE
                            cds_map.local = cds_fc.identity
                            cds_map.remote = Components[j][k].identity

                            YFP_map = Circuit_fc.mapsTos.create('YFP_Protein_map')
                            YFP_map.refinement = SBOL_REFINEMENT_USE_REMOTE
                            YFP_map.local = YFP_fc.identity
                            YFP_map.remote = YFP_protein_c.identity

                if j!=0:
                    if j == len(componentDef_string)-1:
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
                        cds_fc = Circuit.functionalComponents.create(componentDef_string[j][1][1:-1])
                        cds_fc.definition = component_defs[j][1].identity
                        cds_fc.access = SBOL_ACCESS_PUBLIC
                        cds_fc.direction = SBOL_DIRECTION_NONE

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


            result = doc.write("Output_Circuit_" + str(i+1) +".xml")
            print(result)

if __name__ == '__main__':
    inputExp = "IPTG'.aTc'.Arabinose'+IPTG'.aTc.Arabinose'+IPTG.aTc'.Arabinose'"
    f = SBOL_File()
