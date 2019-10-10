package TechMap;
import java.io.FileWriter;  

import LogicOptimization.EMinTermsProcessor;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.commons.lang3.StringUtils;

public class TechMapper 
{
	private EMinTermsProcessor techMap;
	public String inpExpressionWithBraces;
	private FileReader gatesLibFileName;
	public ArrayList<ArrayList<String>> externalInvertersList = new ArrayList<ArrayList<String>>();
	public ArrayList<ArrayList<String>> internalInvertersList = new ArrayList<ArrayList<String>>();
	public ArrayList<ArrayList<String>> externalNorGatesList = new ArrayList<ArrayList<String>>();
	public ArrayList<ArrayList<String>> semiExternalNorGatesList = new ArrayList<ArrayList<String>>();
	public ArrayList<ArrayList<String>> internalNorGatesList = new ArrayList<ArrayList<String>>();
	public ArrayList<ArrayList<String>> minTermsGatesListAInv = new ArrayList<ArrayList<String>>();
	public ArrayList<ArrayList<String>> minTermsGatesListBInv = new ArrayList<ArrayList<String>>();
	public ArrayList<ArrayList<String>> minTermsGatesListCInv = new ArrayList<ArrayList<String>>();
	public ArrayList<ArrayList<String>> minTermsGatesListBInvOPGlobal = new ArrayList<ArrayList<String>>();
	public ArrayList<ArrayList<String>> norGate1 = new ArrayList<ArrayList<String>>();
	public ArrayList<ArrayList<String>>  sequenceOfGatesList = new ArrayList<ArrayList<String>> (); 
	public ArrayList<ArrayList<String>>  sequenceOfAllGatesList = new ArrayList<ArrayList<String>> (); 
	public ArrayList<ArrayList<String>> intermNorGatesListInExp = new ArrayList<ArrayList<String>>();
	public int sizeOfListWithInv;
	public int sizeOfListWithOuterInput;		//(c+(b'+a)')' => c
	public int sizeOfListWithLeftInput;			//(c+(b'+a)')' => b
	public int sizeOfListWithRightInput;		//(c+(b'+a)')' => a
	public int sizeOfListWithInvAndGates;
	private int circuitCount = 1;
	public FileWriter fw; 
	
	public TechMapper(String inpExpression)
	{
		try{fw = new FileWriter("../circuits.txt");}
		catch(Exception e){System.out.println(e);}   
		techMap = new EMinTermsProcessor (null, 0, null);
		inpExpressionWithBraces = techMap.replaceBracesWithTags(inpExpression);
		// System.out.println("Minterms: "+ techMap.cntMinTermsInExpression(inpExpressionWithBraces)); 
		
	}
	
	public void finalize()
	{
		try{fw.close();}
		catch(Exception e){System.out.println(e);}
	}
	
	/**
	 * @return Full file without being parsed to different categories of genetic gates
	 * @throws IOException
	 *
	 */
	public String readGatesLibFile () throws IOException
	{
		String fullFile = "";
		gatesLibFileName = new FileReader("./GatesLib.txt");
		BufferedReader gatesLibraryFile = new BufferedReader(gatesLibFileName);
		String read = "";
		String line = gatesLibraryFile.readLine();
		//ArrayList<String> gates =  new ArrayList<String>();
		while (line != null)
		{
			read += line;
			//gates.add(line);
			line = gatesLibraryFile.readLine();
		}
		
		//System.out.println(gates);
		
		return fullFile = read;
	}
	
	
	
	/**
	 * @param inputGatesLib 
	 * 
	 * Take the input gates library file in the form of String. 
	 * It calls out intermediate method (private to TechMapper class)
	 * and generate separate lists of genetic logic gates. 
	 */
	public void parseGateLibComp(String inputGatesLib)
	{
		String extInv = inputGatesLib.substring(inputGatesLib.indexOf("<Ext-Inverters>") + 15, inputGatesLib.indexOf("</Ext-Inverters>"));
		extInv = extInv.substring(extInv.indexOf("Out") + 3);
		String intInv = inputGatesLib.substring(inputGatesLib.indexOf("<Int-Inverters>") + 15, inputGatesLib.indexOf("</Int-Inverters>"));
		String extNorGates = inputGatesLib.substring(inputGatesLib.indexOf("<Ext-NorGates>") + 14, inputGatesLib.indexOf("</Ext-NorGates>"));
		extNorGates = extNorGates.substring(extNorGates.indexOf("Out")+3);
		String semiExtNorGates = inputGatesLib.substring(inputGatesLib.indexOf("<Semi-Ext-NorGates>") + 19, inputGatesLib.indexOf("</Semi-Ext-NorGates>"));
		String intNorGates = inputGatesLib.substring(inputGatesLib.indexOf("<Int-NorGates>") + 14, inputGatesLib.indexOf("</Int-NorGates>"));
		
		externalInvertersList = generateListOfGates(extInv);
		internalInvertersList = generateListOfGates(intInv);
		externalNorGatesList = generateListOfGates(extNorGates);
		semiExternalNorGatesList = generateListOfGates(semiExtNorGates);
		internalNorGatesList = generateListOfGates(intNorGates);
			
	}

	
	
	/**
	 * @param parsedInputString Take the parsed list of gates not arranged in the array lists. 
	 * @return ArrayLists containing the genetic gates
	 */
	private ArrayList<ArrayList<String>> generateListOfGates(String parsedInputString) 
	{
		ArrayList<ArrayList<String>> inputList = new ArrayList<ArrayList<String>>();
		
		String[] array = parsedInputString.split(" END ");
		
		for(int i =0; i< array.length; i++)
		{
			ArrayList<String> intermList = new ArrayList<String>();
			intermList.addAll(Arrays.asList(array[i].split("\t")));
			inputList.add(i, intermList);
			
			//System.out.println(inputList.get(i));
			//intermList.clear();
		}
		
		return inputList;
	}

	
	
	public void generateTreeExpression()
	{
		String inputExpression = inpExpressionWithBraces;
		String intermExp = inputExpression;
		String SOP = "SOP1";
		String EOP = "EOP1";
		ArrayList<String> minTerms = new ArrayList<String>();
		String [] intermArray;
			
		int Cnt = cntSop1Terms(inputExpression, SOP); //search SOP1 terms first
		
		for(int i = 1; i<= Cnt; i++)
		{
			
			extractNestedSOPelements(intermExp, SOP, EOP);
			
			SOP = "SOP1";
			EOP = "EOP1";
			intermExp = inputExpression.substring(inputExpression.indexOf(EOP)+EOP.length());
		}
			
	}

	
	private void extractNestedSOPelements (String intermExp, String SOP, String EOP)
	{
		String [] intermArray;
		ArrayList<String> minTerms = new ArrayList<String>();
		ArrayList<ArrayList<String>> rxList = new ArrayList<ArrayList<String>>();
		ArrayList<ArrayList<String>> inputRXListWOSop = new ArrayList<ArrayList<String>>();
		intermExp = intermExp.substring(intermExp.indexOf(SOP)+4, intermExp.indexOf(EOP));
		Pattern pattern = Pattern.compile("(?m)(.*?)\\+(SOP.*?$)");
		Matcher sopMinTerms = pattern.matcher(intermExp);
		
		if (sopMinTerms.find())
		{
			minTerms.add(0, sopMinTerms.group(1));
			minTerms.add(1, sopMinTerms.group(2));
			SOP = "SOP";
			EOP = "EOP";
			
			for (int i = 0; i < minTerms.size(); i ++)
			{
				if(minTerms.get(i).contains(SOP))
					extractNestedSOPelements(minTerms.get(i), SOP, EOP);
				else
				{
					rxList = gotoList(minTerms.get(i));
					sizeOfListWithOuterInput = sequenceOfAllGatesList.size(); 
				}
			}
		}
		
		else //When none of the minterms contain SOP
		{
			intermArray = intermExp.split("\\+", 2);
			for (int j = 0; j < intermArray.length;j++)
				minTerms.add(j, intermArray[j]);
			
			intermNorGatesListInExp = gateAssignment(minTerms);
		}
		
		if(!rxList.isEmpty())
		{
			
			//finalOutputLevel(rxList);		//for extracting single possible circuit
			finalOutputMultiple(rxList);	//for extracting all possible circuits
			
			//remove inverter elements from sequenceOfGatesList
			ArrayList<ArrayList<String>> checkInvList = new ArrayList<ArrayList<String>>(); 
			ArrayList<ArrayList<String>> invList = new ArrayList<ArrayList<String>>(); 
			checkInvList.addAll(sequenceOfAllGatesList.subList(0, sizeOfListWithInv));
			String opOfOuterGateInput = "";
			String opOfInnerLeftInput = "";
			String opOfInnerRightInput = "";
			String input1ofInnerNorGate = "";
			String input2ofInnerNorGate = "";
			String outputOfInnerNorGate = "";
			String input1ofOuterNorGate = "";
			String input2ofOuterNorGate = "";
			int cnt = 1;
			ArrayList<ArrayList<String>>  doubleCheck = new ArrayList<ArrayList<String>> (); 

			
			loopThroughOuterInput: //Check the outer input i.e. i.e. from  (c+(b'+a)')'=> it checks the gates list of "c"
			for(int h = 0; h < sizeOfListWithOuterInput; h++)
			{
				opOfOuterGateInput = sequenceOfAllGatesList.get(h).get(2);
				
				loopThroughLeftInnerInput: //Check the list of left inner inputs
				for(int i = 0; i < (sizeOfListWithLeftInput-sizeOfListWithOuterInput); i++)
				{
					opOfInnerLeftInput = sequenceOfAllGatesList.get(i+sizeOfListWithOuterInput).get(2);

					loopThroughRightInnerInput://Check the list of right inner inputs
					for(int j = 0; j < (sizeOfListWithRightInput - sizeOfListWithLeftInput); j++)
					{
						opOfInnerRightInput = sequenceOfAllGatesList.get(j+sizeOfListWithLeftInput).get(2);
						
						if(!opOfInnerLeftInput.equals(opOfInnerRightInput))
						{
							loopThroughGatesList: //Check the list of intermediatte NOR gates i.e. from  (c+(b'+a)')'=> it checks for b'+a
								for(int k = 0; k < sizeOfListWithInvAndGates- sizeOfListWithRightInput; k++)
								{
									input1ofInnerNorGate = sequenceOfAllGatesList.get(k+sizeOfListWithRightInput).get(0);
									input2ofInnerNorGate = sequenceOfAllGatesList.get(k+sizeOfListWithRightInput).get(1);
									
									if((opOfInnerLeftInput.equals(input1ofInnerNorGate) || opOfInnerLeftInput.equals(input2ofInnerNorGate)) && 
											(opOfInnerRightInput.equals(input1ofInnerNorGate) || opOfInnerRightInput.equals(input2ofInnerNorGate)))
									{
										outputOfInnerNorGate = sequenceOfAllGatesList.get(k+sizeOfListWithRightInput).get(2);
										
										loopFinalOutput:
											for (int l = 0; l < sequenceOfAllGatesList.size() - sizeOfListWithInvAndGates; l++)
											{
												input1ofOuterNorGate = sequenceOfAllGatesList.get(l+sizeOfListWithInvAndGates).get(0);
												input2ofOuterNorGate = sequenceOfAllGatesList.get(l+sizeOfListWithInvAndGates).get(1);
												
												if((outputOfInnerNorGate.equals(input1ofOuterNorGate) || outputOfInnerNorGate.equals(input2ofOuterNorGate)) && 
														(opOfOuterGateInput.equals(input1ofOuterNorGate) || opOfOuterGateInput.equals(input2ofOuterNorGate)))
												{
													ArrayList<ArrayList<String>>  sequenceOfGates = new ArrayList<ArrayList<String>> (); 
													ArrayList<String> diagram2= new ArrayList<String>();
													
													//Adding circuit component of inner left input if it is not external input
													if(!sequenceOfAllGatesList.get(i+sizeOfListWithOuterInput).get(0).equals(" "))
														sequenceOfGates.add(sequenceOfAllGatesList.get(i+sizeOfListWithOuterInput));
													
													//Adding circuit component of inner Right input if it is not external input
													if(!sequenceOfAllGatesList.get(j+sizeOfListWithLeftInput).get(0).equals(" "))
														sequenceOfGates.add(sequenceOfAllGatesList.get(j+sizeOfListWithLeftInput));
													
													//Adding circuit component of intermediate NOR Gate
													sequenceOfGates.add(sequenceOfAllGatesList.get(sizeOfListWithRightInput + k));
													
													//Adding the circuit component of outer NOR Gate
													sequenceOfGates.add(sequenceOfAllGatesList.get(sizeOfListWithInvAndGates + l));
													
													
													
													//if(!doubleCheck.contains(sequenceOfAllGatesList.get(sizeOfListWithInvAndGates + l)))
													{ //for 0x0B circuit
														//Checking if the input 1 of outer NOR gate is not external input. If not, then add it to include it 
														//in diagram2 of method constructMultipleDiagrams
														if(!sequenceOfAllGatesList.get(h).get(0).equals(" "))
														{
															diagram2 = sequenceOfAllGatesList.get(h);
															constructMultipleDiagram(sequenceOfGates, cnt, diagram2);
															
														}
														else
														{
															//ArrayList<String> dummy = new ArrayList<String>();
															//diagram2.add(0, dummy);
															diagram2.add(0, "null");
															constructMultipleDiagram(sequenceOfGates, cnt, diagram2);
														}
														
														cnt += 1;
														doubleCheck.add(sequenceOfAllGatesList.get(sizeOfListWithInvAndGates + l));
													}
												}
												else
													continue loopFinalOutput;
											}
									}	
									else
										continue loopThroughGatesList;
								} 
						}
					}
				}
			}
		}
	}
	
	
	//this method is used to construct a single circuit similar to SBOL notation.
	private void constructDiagram() 
	{
		String diagram="";
		String protein = "";
		String in1,in2;
		System.out.println("\n************************************** Genetic Circuit **************************************");
		
		for(int i = 0; i < sequenceOfGatesList.size(); i++)
		{
			if(sequenceOfGatesList.get(i).get(0).contains("'"))
			{
				in1 = sequenceOfGatesList.get(i).get(1);
				protein = sequenceOfGatesList.get(i).get(2);
				protein = protein.replace("P", "");
				diagram = diagram + in1+"-> ("+ protein + ") ----|";
			}
			else
			{
				if(sequenceOfGatesList.get(i).get(0).equals("PTac")||sequenceOfGatesList.get(i).get(0).equals("PTet")|| sequenceOfGatesList.get(i).get(0).equals("PBad"))
				{
					in1 = sequenceOfGatesList.get(i).get(1);
					in2 = sequenceOfGatesList.get(i).get(0);
					protein = sequenceOfGatesList.get(i).get(2);
					protein = protein.replace("P", "");
					diagram = diagram + in1 + "-> " + in2 + "-> ("+ protein + ") ----|";	
				}
			}
		}
		diagram = diagram + "P".concat(protein) + "-> " + "(YFP)";
		System.out.println("\n" + diagram);
		
		System.out.println("\n*********************************************************************************************");
	}

	
	//this method is used to construct all possible circuits from the available components of library.
	private void constructMultipleDiagram(ArrayList<ArrayList<String>> sequenceOfGates, int cnt, ArrayList<String> input1ofOuterNorGate) 
	{
		String diagram="";
		String diagram2 = "";
		int idxD2 = 0;
		int lengthD2 = 0;
		String protein = "";
		String in1 = "",in2="";
		//System.out.println("\n************************************** Genetic Circuit "+ cnt +" **************************************");
		
		for(int i = 0; i < sequenceOfGates.size(); i++)
		{
			if(sequenceOfGates.get(i).get(0).contains("'"))
			{
				in1 = sequenceOfGates.get(i).get(1);
				protein = sequenceOfGates.get(i).get(2);
				protein = protein.replaceFirst("P", "");
				diagram = diagram + in1+"-> ("+ protein + ") ----|";
			}
			else
			{
				if(sequenceOfGates.get(i).get(0).equals("PTac")||sequenceOfGates.get(i).get(0).equals("PTet")|| sequenceOfGates.get(i).get(0).equals("PBad"))
				{
					in1 = sequenceOfGates.get(i).get(1);
					in2 = sequenceOfGates.get(i).get(0);
					protein = sequenceOfGates.get(i).get(2);
					protein = protein.replaceFirst("P", "");
					diagram = diagram + in1 + "-> " + in2 + "-> ("+ protein + ") ----|";	
				}
				else
				{
					if(sequenceOfGates.get(i-1).get(2).equals(sequenceOfGates.get(i).get(0)))
					{
						in1 = sequenceOfGates.get(i).get(0);
						in2 = sequenceOfGates.get(i).get(1);
					}
					else if(sequenceOfGates.get(i-1).get(2).equals(sequenceOfGates.get(i).get(1)))
					{
						in1 = sequenceOfGates.get(i).get(1);
						in2 = sequenceOfGates.get(i).get(0);
					}
						
					protein = sequenceOfGates.get(i).get(2);
					protein = protein.replaceFirst("P", "");
					diagram = diagram + in1 + "-> " + in2 + "-> ("+ protein + ") ----|";	
				}
			}
		}
		diagram = diagram + "P".concat(protein) + "-> " + "(YFP)";
		//System.out.println("\n" + diagram);
		
		if(!input1ofOuterNorGate.get(0).equals("null"))
		{
			in1 = input1ofOuterNorGate.get(1);
			protein = input1ofOuterNorGate.get(2);
			protein = protein.replaceFirst("P", "");
			diagram2 = diagram2 + in1+"-> ("+ protein + ")";
			
		}
		
		checkCircuitDiagram (cnt, diagram, diagram2, input1ofOuterNorGate);
		
		//System.out.println("\n***********************************************************************************************");
	}
	
	private void checkCircuitDiagram (int cnt, String diagram, String diagram2, ArrayList<String> input1ofOuterNorGate)
	{
		String firstProt = diagram.substring(diagram.indexOf("(") + 1, diagram.indexOf(")"));
		String firstProm = diagram.substring(diagram.indexOf("|") + 2, diagram.indexOf("->", diagram.indexOf("|"))); //+2 is added to exclude "P" in the name of promoters. 
		String desiredProm = "P" + firstProt; 	//Creating the name of desired promoter corresponding to "first Protein i.e. firstProt"
		
		
		String diagram3 = "";
		if(!firstProt.equals(firstProm)) 
		{
			diagram3 = diagram.substring(0, diagram.indexOf(")") + 1);
			diagram = diagram.substring(diagram.indexOf("|") + 1);	//New main diagram
			
			int idx = diagram.indexOf(desiredProm);
			int length = idx - diagram3.length();
			for(int i = 0; i < length; i ++)
				diagram3 = diagram3 + "-";
			
			diagram3 = diagram3.concat("--^");
		}
		if (!diagram2.isEmpty()) 
		{
			int idxD2 = diagram.indexOf(input1ofOuterNorGate.get(2));
			int lengthD2 = idxD2-diagram2.length();
			for(int i = 0; i < lengthD2; i ++)
				diagram2 = diagram2 + "-";

			diagram2 = diagram2.concat("--^");	
		}
		boolean BadSolution = filterBadSolutions (diagram, diagram2, diagram3);
		
		if(!BadSolution)
		{
			System.out.println("\n************************************** Genetic Circuit "+ circuitCount +" **************************************");
			System.out.println("\n" + diagram);
			   
	        try{fw.write("******************* Genetic Circuit "+ circuitCount +" *****************\n");
	        fw.write("\n" + diagram);
	        
	        if (!diagram2.isEmpty()) 
				{System.out.println(diagram2);
				fw.write("\n" + diagram2);}
	        if(!diagram3.isEmpty()) 
				{System.out.println(diagram3);
				fw.write("\n" + diagram3);}
	        	fw.write("\n\n");
	        }catch(Exception e){System.out.println(e);}
		    
			
			
			System.out.println("\n***********************************************************************************************");
			circuitCount += 1;
		}
		
	}
	
	
	private boolean filterBadSolutions (String diagram, String diagram2, String diagram3)
	{
		int protCnt = StringUtils.countMatches(diagram, "(");
		String intermDiagram = diagram;
		String interm;
		ArrayList<String> protInMainDiag = new ArrayList<String>();
		//ArrayList<String> protInDiag2 = new ArrayList<String>();
		String protInDiag2 = "";
		String protInDiag3 = "";
		//ArrayList<String> protInDiag3 = new ArrayList<String>();
		
		boolean badSolution = false;
		for(int i=0; i < protCnt - 1 ; i++)
		{
			interm = intermDiagram.substring(intermDiagram.indexOf("("), intermDiagram.indexOf(")") + 1);
			protInMainDiag.add(i, interm);
			intermDiagram = intermDiagram.substring(intermDiagram.indexOf(")") + 1);
		}
		
		if (!diagram2.isEmpty()) 
			{
				//protInDiag2.add(diagram2.substring(diagram2.indexOf("("), diagram2.indexOf(")") + 1));
				protInDiag2 = diagram2.substring(diagram2.indexOf("("), diagram2.indexOf(")") + 1);
			}
			
		if (!diagram3.isEmpty()) 
		{
			//protInDiag3.add(diagram3.substring(diagram3.indexOf("("), diagram3.indexOf(")") + 1));
			protInDiag3 = diagram3.substring(diagram3.indexOf("("), diagram3.indexOf(")") + 1);
		}
		
		int protInMainDiagSize = protInMainDiag.size();
		int protInDiagSubSize = protInMainDiagSize;
		
		if(protInMainDiag.contains(protInDiag2))
			badSolution = true;
		else if (protInMainDiag.contains(protInDiag3))
			badSolution = true;
		else 
		{
			for (int i=0; i < protInMainDiagSize; i++)
			{
				for (int j=1 ; j < protInDiagSubSize; j++)
				{
					badSolution = protInMainDiag.get(i).equals(protInMainDiag.get(i+j));
					if(badSolution)
					{
						i = protInMainDiagSize;
						break;
					}
					else if (j == protInDiagSubSize - 1)
					{
						protInDiagSubSize = protInDiagSubSize - 1; 
						badSolution = false;
					}	
				}
			}
		}
		
		return badSolution;
	}
	
	private void finalOutputLevel(ArrayList<ArrayList<String>> norGateInputA) 
	{
		ArrayList<ArrayList<String>> intermList = new ArrayList<ArrayList<String>>();
		if(norGateInputA.get(1).size() == 1)
		{
			if(norGateInputA.get(1).get(0).contains("PTac") || norGateInputA.get(1).get(0).contains("PTet")||norGateInputA.get(1).get(0).contains("PBad"))
			{
				//Call semi external gates lib
				if(norGateInputA.get(1).get(0).contains("PTac"))
					intermList.addAll(semiExternalNorGatesList.subList(0, 5));
				
				else if(norGateInputA.get(1).get(0).contains("PTet"))
					intermList.addAll(semiExternalNorGatesList.subList(5, 12));
				
				else if(norGateInputA.get(1).get(0).contains("PBad"))
					intermList.addAll(semiExternalNorGatesList.subList(12, 16));
				
				outerloop: 
				for(int i = 0; i < intermNorGatesListInExp.size(); i++)
				{
					for(int j = 0; j < intermList.size(); j ++)
					{
						if((intermNorGatesListInExp.get(i).get(2)).equals(intermList.get(j).get(1)))
						{
							//matched
							sequenceOfGatesList.add(intermNorGatesListInExp.get(i));
							sequenceOfGatesList.add(intermList.get(j));
							break outerloop;
						}
					}
				}
			}
		}
		
	}

	
	private void finalOutputMultiple(ArrayList<ArrayList<String>> OuterNorGateInputA) //for all possible combinations
	{
		ArrayList<ArrayList<String>> intermList = new ArrayList<ArrayList<String>>();
		ArrayList<ArrayList<String>> addedGate = new ArrayList<ArrayList<String>>();
		
		if(OuterNorGateInputA.size() == 1) //old: norGateInputA.get(1).size() == 1
		{
			if(OuterNorGateInputA.get(0).get(2).contains("PTac") || OuterNorGateInputA.get(0).get(2).contains("PTet")||OuterNorGateInputA.get(0).get(2).contains("PBad"))
			{
				//Call semi external gates lib
				if(OuterNorGateInputA.get(0).get(2).contains("PTac"))
					intermList.addAll(semiExternalNorGatesList.subList(0, 5));
				
				else if(OuterNorGateInputA.get(0).get(2).contains("PTet"))
					intermList.addAll(semiExternalNorGatesList.subList(5, 12));
				
				else if(OuterNorGateInputA.get(0).get(2).contains("PBad"))
					intermList.addAll(semiExternalNorGatesList.subList(12, 16));
				
				//Adding gates list in the sequence of all possible circuits
				sequenceOfAllGatesList.addAll(intermNorGatesListInExp); 
				sizeOfListWithInvAndGates = sequenceOfAllGatesList.size();
				
				outerloop: 
				for(int i = 0; i < intermNorGatesListInExp.size(); i++)
				{
					innerloop:
					for(int j = 0; j < intermList.size(); j ++)
					{
						if((intermNorGatesListInExp.get(i).get(2)).equals(intermList.get(j).get(1)))
						{
							//matched
							//sequenceOfAllGatesList.add(gatesList.get(i));
							if(!intermList.get(j).get(2).equals(intermNorGatesListInExp.get(i).get(1)))
								sequenceOfAllGatesList.add(intermList.get(j));
							//break outerloop;
						}
					}
				}
			}
		}
		else if (OuterNorGateInputA.size() > 1)
		{
			String opOfOuterInput = "";
			String opOfIntermNorGateInExp = "";
			
			//Adding gates list in the sequence of all possible circuits
			sequenceOfAllGatesList.addAll(intermNorGatesListInExp); 
			sizeOfListWithInvAndGates = sequenceOfAllGatesList.size();
			
			for(int i = 0; i < intermNorGatesListInExp.size(); i++)
			{
				for(int j = 0; j < OuterNorGateInputA.size(); j ++)
				{
					opOfOuterInput = OuterNorGateInputA.get(j).get(2);
					opOfIntermNorGateInExp = intermNorGatesListInExp.get(i).get(2);
					
					if(!opOfOuterInput.equals(opOfIntermNorGateInExp))
					{
						for(int k = 0; k < internalNorGatesList.size(); k++)
						{
							if((opOfOuterInput.equals(internalNorGatesList.get(k).get(0)) || opOfOuterInput.equals(internalNorGatesList.get(k).get(1))) &&
									(opOfIntermNorGateInExp.equals(internalNorGatesList.get(k).get(0)) || opOfIntermNorGateInExp.equals(internalNorGatesList.get(k).get(1))))
							{
								if(!internalNorGatesList.get(k).get(2).equals(intermNorGatesListInExp.get(i).get(0)) &&
										!internalNorGatesList.get(k).get(2).equals(intermNorGatesListInExp.get(i).get(1)))
								{
									if(!opOfOuterInput.equals(intermNorGatesListInExp.get(i).get(0)) && !opOfOuterInput.equals(intermNorGatesListInExp.get(i).get(1)))
									{
										if(!addedGate.contains(internalNorGatesList.get(k)))
										{
											sequenceOfAllGatesList.add(internalNorGatesList.get(k));
											addedGate.add(internalNorGatesList.get(k));
										}
									}
								}
							}
						}
					}
					else
					{
						for(int m = 0; m < internalInvertersList.size(); m++)
						{
							if(opOfOuterInput.equals(internalInvertersList.get(0)))
								sequenceOfAllGatesList.add(internalInvertersList.get(m));
						}
					}
				}
			}
		}
	}
	
	
	
	private ArrayList<ArrayList<String>> gotoList(String minterm) 
	{
		ArrayList<ArrayList<String>> outputList = new ArrayList<ArrayList<String>>();
		ArrayList<String> type = new ArrayList<String>();
		ArrayList<String> element = new ArrayList<String>();
		
		if(minterm.contains("'")) // if this is inverted term
		{
			if(minterm.contentEquals("a'")) 
			{
				outputList.addAll(0, externalInvertersList.subList(0, 4));
				sequenceOfAllGatesList.addAll(outputList);
				//sizeOfListWithInv = sequenceOfAllGatesList.size();
			}
			
			else if(minterm.contentEquals("b'")) 
			{
				//outputList.get(0).set(0, "b'");
				outputList.addAll(0, externalInvertersList.subList(4, 6));
				sequenceOfAllGatesList.addAll(outputList);
				//sizeOfListWithInv = sequenceOfAllGatesList.size();
			}
			
			else if(minterm.contentEquals("c'")) 
			{
				outputList.addAll(0, externalInvertersList.subList(6, 9));
				sequenceOfAllGatesList.addAll(outputList);
				//sizeOfListWithInv = sequenceOfAllGatesList.size();
			}
		}
		else	// if this is not inverted term
		{
			outputList.add(0, type);
			outputList.get(0).add(0, "null");
			outputList.get(0).add(1, "null");
			outputList.get(0).add(2, "null");
			//outputList.add(1, element);
			//outputList.get(1).add(0, "null");
			
			if(minterm.contains("a"))
			{
				outputList.get(0).set(0, " ");
				outputList.get(0).set(1, "a");
				//outputList.get(1).set(0, "PTac");
				outputList.get(0).set(2, "PTac");
				sequenceOfAllGatesList.addAll(outputList);
			}
			
			else if(minterm.contains("b"))
			{
				outputList.get(0).set(0, " ");
				outputList.get(0).set(1, "b");
				//outputList.get(1).set(0, "PTet");
				outputList.get(0).set(2, "PTet");
				sequenceOfAllGatesList.addAll(outputList);
			}
			
			else if(minterm.contains("c"))
			{
				outputList.get(0).set(0, " ");
				outputList.get(0).set(1, "c");
				//outputList.get(1).set(0, "PBad");
				outputList.get(0).set(2, "PBad");			
				sequenceOfAllGatesList.addAll(outputList);
			}
		}
		
		return outputList;
	}

	private ArrayList<ArrayList<String>> gateAssignment(ArrayList<String> minTerms)
	{
		String [] intermMintermArray = {"",""};
		String minTermL = minTerms.get(0);
		String minTermR = minTerms.get(1);
		ArrayList<String> mintermArray = minTerms;
		ArrayList<ArrayList<String>> rxListL = new ArrayList<ArrayList<String>>();
		ArrayList<ArrayList<String>> rxListR = new ArrayList<ArrayList<String>>();
		ArrayList<ArrayList<String>> listOfNorGates = new ArrayList<ArrayList<String>>();
		ArrayList<ArrayList<String>> intermList = new ArrayList<ArrayList<String>>();
		
		String [] norGateType = {"",""};

		
		if(minTermL.contains("'"))
		{
			rxListL = gotoList (minTermL);
			sizeOfListWithLeftInput = sequenceOfAllGatesList.size();
			norGateType[0] = "Int";
		}
		else
		{
			rxListL = gotoList (minTermL);
			sizeOfListWithLeftInput = sequenceOfAllGatesList.size();
			norGateType[0] = "Ext";
		}
		
		if(minTermR.contains("'"))
		{
			rxListR = gotoList (minTermR);
			sizeOfListWithRightInput = sequenceOfAllGatesList.size();
			norGateType[1] = "Int";
		}
		else
		{
			rxListR = gotoList (minTermR);
			sizeOfListWithRightInput = sequenceOfAllGatesList.size();
			norGateType[1] = "Ext";
		}
		

		
		
		//Assigning NOR Gates
		if(norGateType[0] == "Int" && norGateType[1] == "Int")
		{
			// call internal nor gates list
			String gateInput1 = "";
			String gateInput2 = "";
			String leftT = "";
			String rightT = "";
			intermList.addAll(internalNorGatesList);
			
			for(int leftTerm = 0; leftTerm < rxListL.size(); leftTerm++)
			{
				for(int rightTerm = 0; rightTerm < rxListR.size(); rightTerm++)
				{
					leftT = rxListL.get(leftTerm).get(2);
					rightT = rxListR.get(rightTerm).get(2);
					if(!leftT.equals(rightT))
					{
						searchNorGates:
						for(int searchIdx = 0; searchIdx < intermList.size(); searchIdx ++)
						{
							gateInput1 = intermList.get(searchIdx).get(0);
							gateInput2 = intermList.get(searchIdx).get(1);
							
							if((leftT.equals(gateInput1) || leftT.equals(gateInput2))
								&& (rightT.equals(gateInput1) || rightT.equals(gateInput2)))
								{
									listOfNorGates.add(intermList.get(searchIdx));
									intermList.remove(searchIdx);
									//break searchNorGates;
								}
						}
					}
				}
				
			}
			
		}
			
		else if(norGateType[0] == "Ext" && norGateType[1] == "Ext") 
		{
			// call external nor gates list	
			if(minTermL.contentEquals("a"))
			{
				if(minTermR.contentEquals("b"))
					intermList.addAll(externalNorGatesList.subList(0, 5));
				
				else if(minTermR.contentEquals("c"))
				{
					System.out.println("\nError: There are no gates available that can be integrated to implement the desired function.");
					//intermList.addAll(null);
				}
			}
			
			if(minTermL.contentEquals("b"))
			{
				if(minTermR.contentEquals("a"))
					intermList.addAll(externalNorGatesList.subList(0, 5));
				
				else if(minTermR.contentEquals("c"))
					intermList.addAll(externalNorGatesList.subList(5, 8));
			}
				
			if(minTermL.contentEquals("c"))
			{
				if(minTermR.contentEquals("a"))
				{
					System.out.println("\nError: There are no gates available that can be integrated to implement the desired function.");
					//intermList.addAll(null);
				}
				
				else if(minTermR.contentEquals("b"))
					intermList.addAll(externalNorGatesList.subList(5, 8));
			}
			
			if(!intermList.contains(null))
				listOfNorGates.addAll(intermList);
			
		}
		else 
		{
			// call semi external nor gates list
			//(Ptac)

			
			if(minTermL.contains("'"))
			{
				if(rxListR.get(0).get(2).contains("PTac"))
					intermList.addAll(semiExternalNorGatesList.subList(0, 5));

				else if(rxListR.get(0).get(2).contains("PTet"))
					intermList.addAll(semiExternalNorGatesList.subList(5, 12));
				
				else if(rxListR.get(0).get(2).contains("PBad"))
					intermList.addAll(semiExternalNorGatesList.subList(12, 16));					
					
				for(int inv = 0; inv < rxListL.size(); inv ++)
				{
					for(int gates = 0 ; gates < intermList.size(); gates ++)
					{
						String a = rxListL.get(inv).get(2);
						String b = intermList.get(gates).get(1);
						if(a.equals(b))
						{
							listOfNorGates.add(intermList.get(gates));
						}
					}
				}
			}
			else if (minTermR.contains("'"))
			{
				if(rxListL.get(0).get(2).contains("PTac"))
					intermList.addAll(semiExternalNorGatesList.subList(0, 5));

				else if(rxListL.get(0).get(2).contains("PTet"))
					intermList.addAll(semiExternalNorGatesList.subList(5, 12));
				
				else if(rxListL.get(0).get(2).contains("PBad"))
					intermList.addAll(semiExternalNorGatesList.subList(12, 16));					
					
				for(int inv = 0; inv < rxListR.size(); inv ++)
				{
					for(int gates = 0 ; gates < intermList.size(); gates ++)
					{
						String a = rxListR.get(inv).get(2);
						String b = intermList.get(gates).get(1);
						if(a.equals(b))
						{
							listOfNorGates.add(intermList.get(gates));
						}
					}
				}
			}
			
			
		}
		return listOfNorGates;
	}
	
	
	private int cntSop1Terms(String inputExpression, String searchSOP) 
	{
		String [] array;
		int Cnt = 1;
		//Count number of SOP1 terms
		array = inputExpression.split("\\+", 2);
		while(array[1].contains(searchSOP))
		{
			inputExpression = array[1].substring(array[1].indexOf(searchSOP)+4);
			array = inputExpression.split("\\+", 2);
			Cnt += 1;
		}
		return Cnt;
	}
}
