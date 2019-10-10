package LogicOptimization;

import java.io.File;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.apache.commons.lang3.ArrayUtils;


public class DReduceExp 
{
	public String inputExpression;
	public int loopCnt;
	public int varCnt;
	private EMinTermsProcessor processExpressionReduce;
	private FScanCommonLiterals processRandElements;
	public String newExpression;
	private String expressionToProcess;
	public String outputExpression;
	private int totalMinTerms;
	public int costOfCurrentExpression;
	public int costOfNewExpression;
	
	
	//************************* Control Switches for testing ************************* 
	private boolean expand = false;
	private boolean forceExpand = false;
	private double expandProb = 0.6; // reduce this value to increase the chances of expansion
	
	
	//manual combination selector
	private boolean manualSelComb = false;
	private String manualComb = "M2M3";
	
	private boolean createNewFile = true;
	
	// *******************************************************************************   
	
	public static File file;
	 
	
	public DReduceExp (File file) throws IOException
	{
		//this.inpExp = inpExp;
		//this.loopCnt = loopCnt;
		//this.varCnt = varCnt;
		
		this.file = new File ("../DebugLog.xls");
		if(createNewFile == true)
			file.delete();
		
		String fileHeadings = ("Iteration Count\t" + "Input Expression\t" + "Current Cost\t" + "Expand ?\t"+ 
				"Expression to Process\t" + "selectedRandComb\t" + "Rand El 1\t" + "Rand El 2\t" + "Matched Variable\t" + 
				"Loop Reduced Expression\t" + "lawReplace\t" + "New Expression\t" + "New Cost\r");
		writeText(fileHeadings);
		//System.out.println("\nI am in REDUCE Constructor Class");
		
	}

	
	
	
	
	
	
	
	// Main method to run the REDUCE procedure.
	
	public String performReduction (String inputExpression, int loopCount) throws Exception
	{
		processExpressionReduce = new EMinTermsProcessor (inputExpression, 0, "");
		
		BCalculateCost currentCost = new BCalculateCost (inputExpression);
		BCalculateCost newCost;
		
		costOfCurrentExpression = currentCost.getCost();
		
		
		
		expressionToProcess = inputExpression;
		
		//Decide whether to expand or reduce minterms 
		//and paste it in DReduceExp
		if(forceExpand == true)
			expressionToProcess = processExpressionReduce.expandMinTerms(inputExpression);
		else
		{
			if(Math.random() > expandProb) 
			{
				expressionToProcess = processExpressionReduce.expandMinTerms(inputExpression); //Replace it with the same object of class EExpandMinTerms here.
				expand = true;
			}
			else
			{
				expressionToProcess = inputExpression;
				expand = false;
			}
		}
		
		//sequence 4 of LabVIEW implementation.
		String resultString = processExpressionReduce.replaceBracesWithTags(expressionToProcess);
		//System.out.println("\n ****** Result String: "+resultString);
		
		totalMinTerms = processExpressionReduce.cntMinTermsInExpression(resultString);
		
		String [] currentMinTerms = new String [totalMinTerms];
		String [] currentMinTermsIDs = new String [totalMinTerms];
		String selectedRandComb = "";
		
		currentMinTerms = processExpressionReduce.generateMinTermsArray(resultString, totalMinTerms);
		
		//Generating the list of minterms IDs
		for(int i = 0; i < currentMinTerms.length; i++)
			currentMinTermsIDs [i] = "M"+String.valueOf(i);
		
		//System.out.println("\nMinterms IDs: "+ Arrays.toString(currentMinTermsIDs));
		
		ArrayList<String> possibleCombinations = new ArrayList<String>();
		possibleCombinations = generatePossibleCombs (currentMinTermsIDs);
		
		//System.out.println("Size of Possible combinations: "+possibleCombinations.size());
		
		String [] randElandComb = new String [3];
		String matchedVariable="";
		String loopReducedExpression="";
		String lawReplace="";
		int randCombIdx = 0;
		if(totalMinTerms > 1)
		{
			//Selecting a random combination of minterms to check 
			randCombIdx = selectRandMtCombId (possibleCombinations);
			//System.out.println("\nRandom Combination Idx: "+randCombIdx);
			
			//Extracting random combination and its repective minterms
			//Manual selection of random minterms
				
			if(manualSelComb)
				randCombIdx = possibleCombinations.indexOf(manualComb);
			
			
			randElandComb = obtainRandMt (possibleCombinations, randCombIdx, currentMinTerms);
			selectedRandComb = randElandComb[2];
			//System.out.println("\nRandom Combination: "+randElandComb[2]);
			//System.out.println("\nRandom minterm 1: "+randElandComb[0]);
			//System.out.println("\nRandom minterm 2: "+randElandComb[1]);
			
			
			//sequence 7 of Reduce: Scan common literal
			processRandElements = new FScanCommonLiterals (randElandComb[0], randElandComb[1]);
			processRandElements.executeScanCommonLiterals(randElandComb[0], randElandComb[1]);
			
			matchedVariable = processRandElements.getMatchedVar();
			String redRandElofMt0 = processRandElements.getRandRedEl1();
			String redRandElofMt1 = processRandElements.getRandRedEl2();
			ArrayList <String> separateArrayOfLitInMt0 = processRandElements.separateArrayOfLitInMt0;
			ArrayList <String> separateArrayOfLitInMt1 = processRandElements.separateArrayOfLitInMt1;
			
		
			
			// Sequence 8 of REDUCE: searching single literals in both minterms
			boolean singleLitInMts = searchSingleLitInMt (separateArrayOfLitInMt0) && searchSingleLitInMt (separateArrayOfLitInMt1);
			//System.out.println("\nSingleLitInMt: "+  singleLitInMts);
			
			
			// Sequence 9 of REDUCE: if single minterm is present, then process
			lawReplace = "";
			String manRedRandElofMt0 = "";
			String manRedRandElofMt1 = "";
			if (singleLitInMts)
				lawReplace = processExpressionReduce.scanRules (separateArrayOfLitInMt0.get(0) +"+"+ separateArrayOfLitInMt1.get(0));
			else
			{
				processRandElements.executeScanCommonLiterals(randElandComb[0], randElandComb[1]);
				matchedVariable = processRandElements.getMatchedVar();
				manRedRandElofMt0 = processRandElements.getRandRedEl1();
				manRedRandElofMt1 = processRandElements.getRandRedEl2();
				separateArrayOfLitInMt0 = processRandElements.separateArrayOfLitInMt0;
				separateArrayOfLitInMt1 = processRandElements.separateArrayOfLitInMt1;
			}
			
			//System.out.println("\nLaw replace: "+lawReplace);
			
			// Sequence 10 of REDUCE: find reduced expression before applying replacement rules
			loopReducedExpression = findReducedExpression (matchedVariable,manRedRandElofMt0, manRedRandElofMt1);
			if(!loopReducedExpression.isEmpty())
				lawReplace = loopReducedExpression;
			
			//System.out.println("\nloopReducedExpression: "+loopReducedExpression);
			
			// Sequence 11 of REDUCE: replacement rules implementation 
			if(!loopReducedExpression.isEmpty())
				lawReplace = replacedLaw(loopReducedExpression, matchedVariable);
			
			
			// Sequence 12 of REDUCE: Deleting elements from the array of minterms and inserting new reduced elements
			ArrayList<String> nextMinterms = new ArrayList<String>();
			if(lawReplace.length() != 0)
			{
				nextMinterms = deleteElFromMtArray (currentMinTerms, selectedRandComb);
				nextMinterms.add(lawReplace);
			}
			else
				nextMinterms = new ArrayList<String>(Arrays.asList(currentMinTerms));
			
			
			// Sequence 13 of REDUCE: Constructing new expression
			newExpression = "";
			newExpression = constructNewExpression(nextMinterms, newExpression);
			
			//System.out.println("\nNew Expression: "+newExpression); 
			
			// Sequence 14 of REDUCE: Calculate the cost of new expression
			newCost = new BCalculateCost (newExpression);
			costOfNewExpression = newCost.getCost();
			//System.out.println("\nNew Cost: "+costOfNewExpression);
		}
		else
		{
			newExpression = inputExpression;
			newCost = new BCalculateCost (newExpression);
			costOfNewExpression = newCost.getCost();
		}
		outputExpression = newExpression;
		
		writeDataToFile (loopCount + "\t" + inputExpression + "\t" + costOfCurrentExpression + "\t" + expand + "\t" + 
						expressionToProcess + "\t" + selectedRandComb + "\t" + randElandComb[0] + "\t" + randElandComb[1] 
						+ "\t" + matchedVariable + "\t" + loopReducedExpression + "\t" + lawReplace + "\t" + newExpression 
						+ "\t" + costOfNewExpression);
		
		return outputExpression;
	}
	
	
	
	
	
	
	
	
	// ******************* Methods ********************* //
	
	private void writeDataToFile(String data)  throws Exception
		{
		//File file = new File("../DebugLog.xls");
		
		
		// if file doesnt exists, then create it
		if (!file.exists()) 
			file.createNewFile();
				

		writeText(data);
		
		

		//System.out.println("File written");
		
		
	}

	
	
	private void writeText(String data) throws IOException {
		FileWriter fw = new FileWriter(file.getAbsoluteFile(), true);
		BufferedWriter bw = new BufferedWriter(fw);
		bw.append(data);
		bw.newLine();
		bw.flush();
		bw.close();
	}

	
	
	private String constructNewExpression(ArrayList<String> nextMinterms, String newExpression) 
	{
		
		for(int i = 0; i< nextMinterms.size(); i++)
		{
			if(nextMinterms.size() - i == 1)
				newExpression = newExpression + nextMinterms.get(i) + "";
			else
				newExpression = newExpression + nextMinterms.get(i) + "+";
		}
		return newExpression;
	}



	// The following method generate the list of possible input combinations of minterms
	// in the expression. 
	private ArrayList <String> generatePossibleCombs (String [] minTermsIDs)
	{
		ArrayList<String> possibleCombinations = new ArrayList<String>();
		
		for(int i = 0; i < minTermsIDs.length ; i++)
		{
			for (int j = 0; j < minTermsIDs.length - (i+1); j++)
			{
				possibleCombinations.add(minTermsIDs[i].concat(minTermsIDs[i+1+j]));
			}
		}
		
		return possibleCombinations;
	}
	
	
	
	// The following method extracts the list of variables used in the input expression
	private ArrayList<String> extractVariable (String inpExp)
	{
		BCalculateCost currentExpCost = new BCalculateCost (inpExp);
		int currentCost = currentExpCost.getCost();
		String literalsOnly = currentExpCost.getLiteralsOnly();
		
		ArrayList<String> variablesInExp = new ArrayList<String>();
		String var;
		
		for(int i = 0; i < currentCost;i++)
		{
			var = literalsOnly.substring(i, i+1);
			
			if(variablesInExp.contains(var)==false)
				variablesInExp.add(var);
			
		}
		
		varCnt = variablesInExp.toArray().length;
		return variablesInExp;
		
	}

	
	
	// The following method randomly select the combination of minterms
	private int selectRandMtCombId (ArrayList<String> possibleCombinations)
	{
		int randCombIdx;
		
		randCombIdx = (int) Math.floor(Math.random()*possibleCombinations.size());
		return randCombIdx;
	}
	
	
	
	// The following method extracts the random combination IDs and then the respective
	// elements to be compared **** Switch to select specific combination is here ****
	private String [] obtainRandMt (ArrayList<String> possibleCombinations, int randCombIdx, String [] currentMinTerms)
	{

//		int localRandIdx = randCombIdx;
		String selectedRandComb = "";
		
//		if(manualSelComb)
//			localRandIdx = possibleCombinations.indexOf(manualComb);
		//System.out.println("\npossibleCombinations: "+possibleCombinations);
		selectedRandComb = possibleCombinations.get(randCombIdx);
		
		String [] randIndices =  selectedRandComb.substring(1).split("M", 2);
		String [] randElandComb =  new String [randIndices.length + 1]; // 1 is added to hold the combination value
		
		for (int i=0; i< randIndices.length ; i++)
			randElandComb [i] = currentMinTerms [Integer.parseInt(randIndices[i])].replaceAll(" ", "");
		
		randElandComb [2] = selectedRandComb;
		
		return randElandComb;
	}
	
	
	
	//The following method test if minterms contain only one literal
	private boolean searchSingleLitInMt (ArrayList<String> separateArrayOfLitInMt)
	{
		boolean SingleLitInMt;
		if(separateArrayOfLitInMt.get(separateArrayOfLitInMt.size() - 1).isEmpty())
			separateArrayOfLitInMt.remove(separateArrayOfLitInMt.size()-1);
		
		if(separateArrayOfLitInMt.size() == 1)
			SingleLitInMt = true;
		else
			SingleLitInMt = false;
		
		return SingleLitInMt;
	}

	
	
	// The following method find reduce expression before applying replacement rules
	private String findReducedExpression (String matchedVariable, String redRandElofMt0, String redRandElofMt1)
	{
		String initialReducedExpression = "";
		
		if(!matchedVariable.isEmpty())
		{
			if((matchedVariable == redRandElofMt0) && (redRandElofMt0 == redRandElofMt1))
				initialReducedExpression = "";
			else
			{
				initialReducedExpression = matchedVariable + "(" + redRandElofMt0 + "+" + redRandElofMt1 + ")";
				initialReducedExpression = initialReducedExpression.replaceAll(" ", "");
			}
		}
		return initialReducedExpression;
	}


	
	// This method extracts subminterms from reduced expression and give the law after replacement
	private String replacedLaw (String loopReducedExpression, String matchedVariable)
	{
		String intermediatte;
		intermediatte = loopReducedExpression.substring(matchedVariable.length());
		intermediatte = processExpressionReduce.replaceBracesWithTags(intermediatte);
		
		String [] afterSOPTag;
		String [] beforeEOPTag;
		
		afterSOPTag = processExpressionReduce.splitStringIntoTwo(intermediatte, "SOP1");
		if(intermediatte.contains("SOP1"))
			intermediatte = afterSOPTag [1];
		else
			intermediatte = afterSOPTag [0];
		
		beforeEOPTag = processExpressionReduce.splitStringIntoTwo(intermediatte, "EOP1");
		
		intermediatte = beforeEOPTag [0];
		
		int cntSubMinTerms = processExpressionReduce.cntMinTermsInExpression(intermediatte);
		
		String [] subMintermsArray = processExpressionReduce.generateMinTermsArray(intermediatte, cntSubMinTerms);
		
		String [] subMintermsIDs = new String [cntSubMinTerms];
		
		//generating minterm Ids
		subMintermsIDs = genMintermIDs (subMintermsArray.length);
		
		ArrayList<String> subPossibleComb = generatePossibleCombs (subMintermsIDs);
		
		
		for(int i = 0; i < subMintermsArray.length ; i ++)
		{
			intermediatte = processExpressionReduce.scanRules(subMintermsArray[i]);
			
			if(processExpressionReduce.ruleMatched)
				loopReducedExpression = loopReducedExpression.replaceFirst(subMintermsArray[i], intermediatte);
			else 
				loopReducedExpression = loopReducedExpression;
			
			subMintermsArray[i] = intermediatte;
		}
		
		
		// finding if any minterm contain braces
		boolean subElHasBrace = false;
		ArrayList<Integer> idxOfBrace = new ArrayList<Integer>();
		//Find if any minterm contains braces
		for (int i = 0; i < subMintermsArray.length; i ++)
		{
			if(subMintermsArray[i].contains("("))
			{
				subElHasBrace = true;
				idxOfBrace.add(i);
			}
		}
		
		String toReplace;
		String subMinTermEl;
		String replacedRule;
		String replacedLaw;
		
		if (subElHasBrace)
		{
			for (int i =0; i < idxOfBrace.size(); i ++)
			{
				//implement Seq 11 of Reduce. 11TT2.T.0.0.
				subMinTermEl = subMintermsArray[idxOfBrace.get(i)];
				intermediatte = subMinTermEl.substring(subMinTermEl.indexOf("(") + 1);
				//System.out.println("\nIntermediate: "+intermediatte);
				toReplace = intermediatte.substring(0, intermediatte.indexOf(")")); // changed here
				
				//implement Seq 11 of Reduce. 11TT2.T.0.1
				replacedRule = processExpressionReduce.scanRules(toReplace);
				
				if(processExpressionReduce.ruleMatched == false)
					replacedLaw = subMinTermEl;
				else
					replacedLaw = rulesReplacer(subMinTermEl, toReplace, replacedRule);
				
				subMintermsArray[idxOfBrace.get(i)] = replacedLaw;
			}	
			loopReducedExpression = subExpressionReducer (subMintermsArray, matchedVariable, subPossibleComb);
		}
		else
			loopReducedExpression = subExpressionReducer (subMintermsArray, matchedVariable, subPossibleComb);
		
		
		//Seq Reduce 11.T.T.3
		String [] beforeBrace;
		String [] afterBrace;
		String lawReplace = "";
		if(loopReducedExpression.contains("("))
		{
			beforeBrace = processExpressionReduce.splitStringIntoTwo(loopReducedExpression, "(");
			
			if(beforeBrace[1].contains(")"))
			{
				afterBrace = processExpressionReduce.splitStringIntoTwo(loopReducedExpression, "(");
				
				if(afterBrace[0] == "1" || afterBrace[0] == "0" || afterBrace[0] == "")
					lawReplace = loopReducedExpression.replace("("+afterBrace[0]+")", "");
				else
					lawReplace = loopReducedExpression;
			}
			lawReplace = loopReducedExpression;
		}
		lawReplace = loopReducedExpression;
		return lawReplace;
	}

	
	
	
	// The following method is used to generate minterms IDS
	private String [] genMintermIDs (int numberOfMts)
	{
		String [] subMintermIDs = new String [numberOfMts] ;
		for(int i = 0; i < numberOfMts; i++)
			subMintermIDs [i] = "M"+String.valueOf(i);
		
		return subMintermIDs; 
	}
	
	
	
	
	// The following method is used to reduce subexpression. REDUCE 11of15, Seq T2T1
	private String subExpressionReducer (String [] subMintermsArray, String matchedVariable, ArrayList<String> subPossibleComb)
	{
		int idx = 0;
		String newExpression = "";
		ArrayList<String> nextMinTermsArray = new ArrayList<String>();
		String [] randElandComb = {"","",""};
		String randComb;
		String intermString;
		String randRedEl1;
		String randRedEl2;
		String matchedVar = "";
		
		do
		{
			if(!subPossibleComb.isEmpty() && idx < subPossibleComb.size())
				randElandComb = obtainRandMt (subPossibleComb, idx, subMintermsArray);
			randComb = randElandComb[2];
			
			String randEl1 = processExpressionReduce.scanRules(randElandComb[0]);
			String randEl2 = processExpressionReduce.scanRules(randElandComb[1]);
			
			processRandElements.executeScanCommonLiterals(randElandComb[0], randElandComb[1]);
			
			randRedEl1 = processRandElements.randRedEl1;
			randRedEl2 = processRandElements.randRedEl2;
			matchedVar = processRandElements.matchedVar;
			
			newExpression = "";
			if(!matchedVar.isEmpty())
			{
				newExpression = "";
				intermString = randRedEl1 + "+" + randRedEl2;
				intermString = processExpressionReduce.scanRules(intermString);
				if(intermString.length()>2)
					intermString = "("+"intermString"+")";
				else
				{
					if(intermString.equals("1"))
						intermString = "";
				}
				
				if(!intermString.isEmpty())
					intermString = matchedVar + intermString;
				else
					intermString = matchedVar;
				intermString = processExpressionReduce.scanRules(intermString);
				
				nextMinTermsArray = deleteElFromMtArray(subMintermsArray, randComb);
				 
				nextMinTermsArray.add(intermString);
				idx = 0;
				// jugad
				newExpression = createNewExp(newExpression, nextMinTermsArray);
				
				subMintermsArray = nextMinTermsArray.toArray(new String [nextMinTermsArray.size()]); 
				subPossibleComb = generatePossibleCombs (genMintermIDs (nextMinTermsArray.size()));
					
			}
			else
			{
				//newExpression = "";
				intermString = processExpressionReduce.scanRules(randEl1 + "+" +randEl2);
				
				if(processExpressionReduce.ruleMatched)
				{
					nextMinTermsArray = deleteElFromMtArray(subMintermsArray, randComb);
					//System.out.println(nextMinTermsArray);
					nextMinTermsArray.add(intermString);
					idx = 0;
					
					newExpression = createNewExp(newExpression, nextMinTermsArray);
					subMintermsArray = nextMinTermsArray.toArray(new String [nextMinTermsArray.size()]); 
					subPossibleComb = generatePossibleCombs (genMintermIDs (nextMinTermsArray.size()));
				}
				else
				{
					newExpression = "";
					nextMinTermsArray = new ArrayList<String> (Arrays.asList(subMintermsArray));
					newExpression = createNewExp(newExpression, nextMinTermsArray);
					idx = 0;	//idx += 1;
				}
			}
		}while ((subPossibleComb.size() - 1 != idx)&& (!subPossibleComb.isEmpty())); //(subPossibleComb.size() -1 != idx);
		
		if(!newExpression.equals("1"))
			newExpression = matchedVariable + "(" + newExpression + ")";
		else
			newExpression = matchedVariable;
		
		return newExpression; 
	}


	

	private ArrayList<String> deleteElFromMtArray(String[] subMintermsArray, String randComb) {
		ArrayList<String> nextMinTermsArray = new ArrayList<String>(Arrays.asList(subMintermsArray));
		
		//nextMinTermsArray = (ArrayList<String>)(Arrays.asList(subMintermsArray));
		//System.out.println("\nNextMinTermsArray: "+nextMinTermsArray);
		//System.out.println("\nrandComb: "+randComb);
		//Remove x of combination MxMy 
		//if(nextMinTermsArray.size()>1)
			nextMinTermsArray.remove(Integer.parseInt(randComb.substring(3)));
		
		//Remove y of combination MxMy 
		nextMinTermsArray.remove(Integer.parseInt(randComb.substring(1, randComb.length()-2)));
		return nextMinTermsArray; 
	}



	private String createNewExp(String newExpression, ArrayList<String> nextMinTermsArray) {
		for (int i = 0; i < nextMinTermsArray.size(); i++)
		{
			if(nextMinTermsArray.size() - i == 1)
				newExpression = newExpression + nextMinTermsArray.get(i);
			else
				newExpression = newExpression + nextMinTermsArray.get(i) + "+";
		}
		return newExpression;
	}



	//Rule replacer 
	private String rulesReplacer(String lawToReplace, String toReplace, String replacedRule)
	{
		String intermString;
		String replacedLaw;
		int idx;
		intermString = lawToReplace.replaceFirst(toReplace, replacedRule);
		idx = intermString.indexOf(replacedRule);
		intermString = intermString.replace(intermString.charAt(idx-1), ' ');
		idx = intermString.indexOf(replacedRule);
		intermString = intermString.replace(intermString.charAt(idx+replacedRule.length()), ' ');
		
		if(replacedRule == "0" || replacedRule == "1")
			replacedLaw = intermString.replaceFirst(replacedRule, " ");
		else
			replacedLaw = intermString;
		
		return replacedLaw;
		
	}
}























