package LogicOptimization;

import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.*;

public class EMinTermsProcessor 

{
	public String inpExp;
	public double selRandomIdx;
	public String outExp;
	
	//Constructor
	public EMinTermsProcessor (String inExp, double selRandomIdx, String outExp) // remove all of them
	{
		this.selRandomIdx = selRandomIdx;
		this.outExp = outExp;
		
		//System.out.println("\nI am in EMinTermsProcessor Constructor Class");
		
	}
	
	// ************ Shared variables among Methods ************** //
	public String multiplier;
	public String resultString;
	public String multiplicand;
	public boolean ruleMatched;

	// ********************************************************** //
	
	
	
	// ************************ Methods  ************************ //
	
	
	// This method executes the whole minterms expansion process
	public String expandMinTerms (String inpExp)
	{
		//System.out.println("\nExpanding SOP Term");
		resultString = replaceBracesWithTags(inpExp);
		
		int selRandIdx = findSopIndices(resultString);
		
		if(selRandIdx != -1)
		{
			expandSOPTag (resultString, selRandIdx);
		 
			int CntMinTerms = cntMinTermsInExpression (multiplicand);
			
			String [] currentMinTerms = new String [CntMinTerms];
			currentMinTerms = generateMinTermsArray (multiplicand, CntMinTerms);
			
			outExp = expandMinTermsArray (currentMinTerms);
		}
		else
			outExp = inpExp;
		
		//System.out.println("\n*** Expression to be Processed: "+outExp);
		return outExp;
	}
	
	
	
	
	// This method takes the input expression and replace the braces with Tags
	// Input: expression with braces - String
	// Output: expression with tags - String
	public String replaceBracesWithTags (String inpExp)
	{
		resultString = inpExp;
		//char var;
		String var;
		int braceCnt = 0;
		String braceTag = "";
		
		resultString = resultString.replaceAll(" ", "");
		
		for (int i = 0; i < resultString.length(); i++)
		{
			//var = resultString.charAt(i);
			var = resultString.substring(i, i+1);
			switch (var)
			{
				case "(":
				{
					braceCnt += 1;
					braceTag = "SOP" + braceCnt;
					resultString = resultString.replaceFirst("\\(" , braceTag);
					break;
				}
					
				case ")":
				{
					braceTag = "EOP" + braceCnt;
					braceCnt -= 1;
					resultString = resultString.replaceFirst("\\)" , braceTag);
					break;
				}
			}
			//resultString = resultString.replaceFirst(var, braceTag);
		}
		//outExp = resultString;
		
		return resultString;		
	}

	
	
	//---------- This method finds the indexes of SOP1 -----------//
	// It takes the manipulated expression from method,ReplaceBracesWithTags,
	// and generate the array of indices of SOP1 tags. Then it 
	// randomly selects any index of SOP1 to expand it in the next method. 
	// Input: expression with tags - String
	// Output: Randomly selected index of SOP - int
	private int findSopIndices (String resultString)
	{
		int sopIdx = 0; 
		int RandIdx=0;
		int selIdx = -1;
		ArrayList<Integer> sopIndices = new ArrayList<Integer>();
		sopIdx = resultString.indexOf("SOP1");
		//System.out.println(sopIdx);
		
		while (sopIdx != -1)
		{
			if(sopIdx != -1)
				sopIndices.add(sopIdx);
				
			sopIdx = resultString.indexOf("SOP1", sopIdx + 4);
			
		}
		//System.out.println("SOP Indices Array: "+sopIndices);
		
		if(!sopIndices.isEmpty() && !sopIndices.equals("-1"))
		{
			RandIdx = (int) Math.floor(Math.random()*sopIndices.size());
			selIdx = sopIndices.get(RandIdx);
		}
		
		//System.out.println("Selected random IDx of SOP1 is: "+selIdx);
		
		return selIdx;
	}
	
	
	
	//---------- This method expand the randomly chosen SOP tags -----------//
	// It takes the resultString and randomly chosen SOP1 Idx and then
	// split it into its multiplier and multiplicands. 
	// Input: SOP tagged resultString - String
	// Input: Randomly chosen index of SOP for its expansion - int
	// Output: Separate multiplicand expression (with tags) - String
	// Output: Separate multiplier - String
	private void expandSOPTag (String resultString, int selIdx)
	{
		multiplier = resultString.substring(0, selIdx);
		//System.out.println("\nMethod ExpandSOPTag \n ");
		//System.out.println("Initial Multplier String: " + multiplier);
		
		multiplicand = resultString.substring(selIdx);
		multiplicand = multiplicand.substring(4, multiplicand.indexOf("EOP1"));
		//System.out.println("Initial Multplicand String: " + multiplicand);
		
		multiplier = multiplier.substring(multiplier.lastIndexOf("+") + 1);
		//System.out.println("Final Multplier String: " + multiplier);
		
		//return multiplicand;
	}
	
	
	
	//---------- This method calculates the number of minterms -----------//
	// It takes the expression (either multiplicand or full expression) and 
	// counts the number of literals in it. 
	// Input: multiplicand expression (with Tags) - String
	// Output: Total number of minterms present in multiplicand - int
	public int cntMinTermsInExpression (String expression)
	{
		String origMultiplicand = expression;
		String [] splitMultiplicand;			//Two-input array to hold minterms around "+". 
		String EOP = "EOP";	
		int Idx = 0;							//Holds index to check if anything exist in multiplicand string
		int CntMinTerms = 0;					//Counter for minterms
		
		//To check the pattern of SOP1,SOP2, SOP3, and so on.
		Pattern pattern = Pattern.compile("(SOP)([0-9]+)");	
		
		while (Idx != -1)
		{
			Idx = expression.indexOf("+");
			//If there is no + sign left in the string.
			if(Idx != -1)
			{
				//Split multiplicand into two halves around "+"
				splitMultiplicand = expression.split("\\+", 2);
				
				//Creating a matcher object and search the "pattern" in the left side of multiplicand
				Matcher matcher = pattern.matcher(splitMultiplicand[0]); 
				
				//System.out.println("\nIdx: "+Idx);
				//System.out.println("\nFirst Multiplicand: " + splitMultiplicand[0] + 
				//				   "\nSecond Multiplicand: " +splitMultiplicand[1]);
				
				//If SOP with any digit is found in the left side of multiplicand, then
				if (matcher.find())
				{
					//Concatenate the digit of SOP with the string EOP
					EOP = EOP.concat(matcher.group(2));
					
					//Find the index of EOP[digit] in right side of multiplicand
					Idx = splitMultiplicand[1].indexOf(EOP);
					
					//If the above EOP is present, then extract rest of the string after EOP[digits] 
					if(Idx != -1)
					{
						expression = splitMultiplicand[1].substring(Idx + EOP.length()); 
						if(expression.contains("+") && !expression.startsWith("+"))
							expression = expression.substring(expression.indexOf("+"));
					}
					
					//Increase Min Terms counter
					CntMinTerms += 1;
				}
				else //If SOP with any digit is not found in the left side of multiplicand, then
				{
					//Check if there is any + sign left in the multiplicand string
					Idx = expression.indexOf("+");
					
					//if neither SOP is present in the left multiplicand nor it is empty, then increase
					//min terms counter
					if(splitMultiplicand[0].isEmpty() == false)
						CntMinTerms += 1;
					
					//Assign only right multiplicand to main multiplicand string 
					expression = splitMultiplicand[1];
				}
				
				EOP = "EOP";
			}
			else // if there is no + signs in the multiplicand string
			{
				if(!expression.isEmpty() && !expression.contentEquals("'"))
					CntMinTerms += 1;
			}
		}
		
		//System.out.println("\nTotal Minterms: "+CntMinTerms);
		return CntMinTerms;
	}

	
	
	//---------- This method generates the array of minterms -----------//
	// It takes the expression (or multiplicand) and the total number of 
	// multiplicands calculated from previous method, and arranges all of 
	// them in an array. It also assign unique IDs to each minterm.
	// Input: multiplicand expression (with Tags) - String
	// Input: total number of minterms present in multiplicand - int
	// Output: generate minterms array 
	public String [] generateMinTermsArray (String inputExp, int CntMinTerms)
	{
		String [] splitMultiplicand;	//Two-input array to hold minterms around "+". 
		String [] splitMultiplicand2;	//Two-input array to hold minterms around ")". 
		String [] currentMinTerms = new String [CntMinTerms]; 
		String EOP = "EOP";	
		String SOP = "SOP";
		String bar = "";
		int Idx = 0;					//Holds index to check if anything exist in multiplicand string
		
		
		//To check the pattern of SOP1,SOP2, SOP3, and so on.
		Pattern pattern = Pattern.compile("(SOP)([0-9]+)");	
		
		for (int i = 0; i < CntMinTerms ; i++)
		{
			bar = "";
			//Split multiplicand into two halves around "+"
			splitMultiplicand = inputExp.split("\\+", 2);
			
			//Creating a matcher object and search the "pattern" in the left side of multiplicand
			Matcher matcher = pattern.matcher(splitMultiplicand[0]); 
			
			if(matcher.find())
			{
				SOP = "SOP" + matcher.group(2);
				
				//System.out.println ("\nSOP: "+SOP);
				splitMultiplicand[0] = splitMultiplicand[0].replaceFirst(SOP, "(");
				//System.out.println("\n****splitMultiplicand[0]: "+splitMultiplicand[0]);
				splitMultiplicand[0] = splitMultiplicand[0].replaceAll("(SOP)([0-9]+)", "(");
				//System.out.println("\n****splitMultiplicand[0]: "+splitMultiplicand[0]);
				splitMultiplicand[0] = splitMultiplicand[0].replaceAll("(EOP)([0-9]+)", ")");
				//System.out.println("\n****splitMultiplicand[0] replace EOP: "+splitMultiplicand[0]);
				splitMultiplicand[0] = splitMultiplicand[0].replaceAll(" ", "");
				
				
				EOP = "EOP" + matcher.group(2);
				splitMultiplicand[1] = splitMultiplicand[1].replaceFirst(EOP, ")");
				//System.out.println("\n\n****splitMultiplicand[1] : "+splitMultiplicand[1]);
				if(i != CntMinTerms -1)
					bar = splitMultiplicand[1].substring(splitMultiplicand[1].indexOf(")")+1, splitMultiplicand[1].indexOf(")")+2);
				else
					bar = splitMultiplicand[1].substring(splitMultiplicand[1].indexOf(")")+1);
				
				if(bar.contentEquals("'"))
					splitMultiplicand2 = splitMultiplicand[1].split("\\)'", 2);
				else
					splitMultiplicand2 = splitMultiplicand[1].split("\\)", 2);
				
				//System.out.println("\n\n****splitMultiplicand2[0] : "+splitMultiplicand2[0]+"    splitMultiplicand2[1] : "+splitMultiplicand2[1]);
				splitMultiplicand2[0] = splitMultiplicand2[0].replaceAll("(SOP)([0-9]+)", "(");
				//System.out.println("\n****splitMultiplicand2[0] : "+splitMultiplicand2[0]);
				splitMultiplicand2[0] = splitMultiplicand2[0].replaceAll("(EOP)([0-9]+)", ")");
				splitMultiplicand2[0] = splitMultiplicand2[0].replaceAll(" ", "");
				//System.out.println("\n****splitMultiplicand2[0] : "+splitMultiplicand2[0]);
				
				//System.out.println("\nsplitMultiplicand2[1]: "+splitMultiplicand2[1]);
				//System.out.println("\nsplitMultiplicand2[1].substring(0, 1).contentEquals("+"): "+splitMultiplicand2[1].charAt(0));
				
				char check = ' ';
				if(!splitMultiplicand2[1].isEmpty())
					check = splitMultiplicand2[1].charAt(0);
				
				if(check == '+')
				{
					//System.out.println("\nsplitMultiplicand2[1]: "+splitMultiplicand2[1]);
					inputExp = splitMultiplicand2[1].substring(1);
					//System.out.println("\ninputExp IF: "+inputExp);
				}
				else
				{
					inputExp = splitMultiplicand2[1];	
					//System.out.println("\ninpuExp Else: "+inputExp);
				}	
				//System.out.println("\ninpuExp: "+inpExp);
				if(bar.contentEquals("'"))
					currentMinTerms [i] = splitMultiplicand[0].concat("+").concat(splitMultiplicand2[0]).concat(")'");
				else
					currentMinTerms [i] = splitMultiplicand[0].concat("+").concat(splitMultiplicand2[0]).concat(")");
			}
			else
			{
				//System.out.println("Error might be here");
				//System.out.println("splitMultiplicand.length: "+ splitMultiplicand.length);
				if(splitMultiplicand[0].isEmpty())
					currentMinTerms [i] = splitMultiplicand[1];
				else
					currentMinTerms [i] = splitMultiplicand[0];
				
				if(splitMultiplicand.length >1)
					inputExp = splitMultiplicand[1];
			}	
			//System.out.println("\ninputExp: "+inputExp);
		}
		
		//for(int i = 0; i < currentMinTerms.length; i++)
		//	currentMinTermsIDs [i] = "M"+String.valueOf(i);
				
		//System.out.println("\nMinterms Array: "+ Arrays.toString(currentMinTerms) );
		
		
		return currentMinTerms;
	}

	
	
	// This method multiplies the multiplier with all minterms of multiplicand
	// and expand it in the form of expression.
	// Input: array of minterms - string array
	// Output: global output outExp 
	public String expandMinTermsArray (String [] currentMinTerms)
	{
		String [] outputMinTerms = new String[currentMinTerms.length];
		for(int i=0; i< currentMinTerms.length; i++)
		{
			if(currentMinTerms[i].contains("1"))
				currentMinTerms[i] = "";
			
			outputMinTerms[i] = scanRules(multiplier.concat(currentMinTerms[i]));				
		}
		
		//System.out.println(Arrays.toString(outputMinTerms));
		
		String expandedMinTerms = minTermsToExpression (outputMinTerms);
		
		String searchExpression = multiplier.concat("SOP1").concat(multiplicand).concat("EOP1");
		//System.out.println("\nSearch Expression: "+searchExpression);
		
		String expandedExpression = resultString;
		expandedExpression = expandedExpression.replace(searchExpression, expandedMinTerms); //replaceFirst(searchExpression, expandedMinTerms);
		
		//System.out.println("\nexpandedExpression "+expandedExpression);
		expandedExpression = replaceTagsWithBraces (expandedExpression);
		
		return expandedExpression;
	}

	

	
	
	// This method takes the minterms array and transformed it into expression
	//  E.g. a(b+c) => ab + ac
	// Input: Array of minterms - String array
	// Output: expanded expression - String
	public String minTermsToExpression (String [] inputMinTerms)
	{
		String expandedMinterms = "";
		
		for(int i = 0; i <inputMinTerms.length; i++)
		{
			if(inputMinTerms.length - i != 1)
				expandedMinterms = expandedMinterms.concat(inputMinTerms[i]).concat("+");
			else
				expandedMinterms = expandedMinterms.concat(inputMinTerms[i]).concat("");
		}
		
		//System.out.println("\nExpanded Minterms: "+expandedMinterms);
		
		return expandedMinterms;
	}
	
		
	
	// This method replace the SOP/EOP tags present in the expression
	// with braces. 
	// Input: takes the input expression with tags - String
	// Output: throws the expression without tags - String
	public String replaceTagsWithBraces (String inputExpression)
	{
		//System.out.println("\nExpression with Tags: "+inputExpression);
		String expandedExpression = inputExpression;
		if(expandedExpression != null)
		{
			expandedExpression = expandedExpression.replaceAll("(SOP)([0-9]+)", "(");
			expandedExpression = expandedExpression.replaceAll("(EOP)([0-9]+)", ")");
		}
		//System.out.println("\nExpression without Tags: "+expandedExpression);
		return expandedExpression;
	}
		
	
	
	// ***************** Public Methods ***************** //	
	
	// This method scans for rules
	// Input: takes the input multiplicand to scanl for boolean laws - String
	// Output: output the replaced expression - String
	public String scanRules (String inpExp)
	{
		String localInpExp = inpExp;
		String ruleVariable = localInpExp;
		String replacedRule = "";
		String [] breakAroundOne;
		boolean ones = false;
		ruleMatched = false;
		
		ruleVariable = ruleVariable.replaceAll("1|\\+|0", "");
		if(!ruleVariable.isEmpty())
			ruleVariable = ruleVariable.substring(0, 1);
		
		if(localInpExp.contains("1"))
		{
			breakAroundOne = localInpExp.split("1", 2);
			//System.out.println("\nbreakAroundOne: "+Arrays.toString(breakAroundOne));
			breakAroundOne[0] = breakAroundOne[0].replaceAll(" ", "");
			//System.out.println("\nbreakAroundOne length: "+breakAroundOne[0].length());
			
			if(breakAroundOne[0].length() != 0)
				breakAroundOne[0] = breakAroundOne[0].substring(breakAroundOne[0].length() - 1, breakAroundOne[0].length());
			
			breakAroundOne[1] = breakAroundOne[1].replaceAll(" ", "");
			
			if(breakAroundOne[1].length() != 0)
				breakAroundOne[1] = breakAroundOne[1].substring(0, 1);
			
			if((breakAroundOne[0].equals("+") || breakAroundOne[1].equals("+")) || (breakAroundOne[0].equals("") && breakAroundOne[1].equals("")))
				ones = true;
			else
				ones = false;
		}
		
		//Replacing rules (defined in x) with the variable present in the current expression
		String [][] rulesForVariables = generateRulesforVariable(ruleVariable);
		
		if(ones)
		{
			replacedRule = "1";
			ruleMatched = true;
		}
		else
		{
			for(int row = 0; row < 17; row ++)
			{
				for(int col = 0; col < 2; col++)
				{
					if(col == 0)
					{
						if(localInpExp.equals(rulesForVariables[row][col]))
						{
							replacedRule = rulesForVariables[row][col+1];
							ruleMatched = true;
							row = 18;
							col = 3;
							break;
						}
						else
						{
							replacedRule = localInpExp;
							ruleMatched = false;
						}
					}	
				}
			}
		}
		//System.out.println("\nReplaced Rule: "+replacedRule);
		
		return replacedRule;
	}
	
	
	
	// This method replaces the standard variable x with the variable being used in
	// the current expression, and returns the list of rules in that variable.
	// Input: Takes the variable of expression to replaced the standard laws with 
	// that variable - String
	// Output: 2D array of boolean rules in the form of input varibale.  
	public String [][] generateRulesforVariable (String ruleVariable)
	{
		String [][] standardRules = {
										{"x+x", "x"},
										{"x'+x'", "x'"},
										{"x+1", "1"},
										{"1+x", "1"},
										{"x'+1", "1"},
										{"1+x'", "1"},
										{"x1", "x"},
										{"1x", "x"},
										{"x0", "0"},
										{"0x", "0"},
										{"x+0", "x"},
										{"0+x", "x"},
										{"x+x'", "1"},
										{"x'+x", "1"},
										{"xx'", "0"},
										{"x'x", "0"},
										{"xx","x"}
									};
		
		String [][] rulesForVariables = new String [17][2]; 
		
		if(ruleVariable.equals(""))
			rulesForVariables = rulesForVariables;
		else
		{
			for (int row = 0; row < 16; row ++)
			{
				for (int col = 0; col < 2; col ++)
				{
					rulesForVariables [row][col] = standardRules [row][col].replaceAll("x", ruleVariable); 
					//System.out.println("New Rules "+rulesForVariables[row][col]);
				}
			}
		}
			
		
		return rulesForVariables;
	}

	
	
	
	// This method arranges literals of minterms in an array
	// Input: Minterm string with SOP tags
	// Output: list of literals arranged in ArrayList.
	public ArrayList<String> arrangeLitInArray (String minTerm)
	{
		ArrayList<String> separateArrayOfLitInMt = new ArrayList<>();
		String MtWithSopTag = ""; //to hold the SOP1-EOP1 expression
		String tempString = "";
		
		//System.out.println("Original Minterm: "+minTerm);
		if(minTerm.contains("SOP1"))
		{
			MtWithSopTag = minTerm.substring(minTerm.indexOf("SOP1"), minTerm.indexOf("EOP1") + 4); // expression along with SOP-EOP tags
			tempString = minTerm.substring(minTerm.indexOf("SOP1") + 4, minTerm.indexOf("EOP1"));   // expression within SOP-EOP tags
			tempString = replaceTagsWithBraces(tempString);
			
			separateArrayOfLitInMt.add(tempString);
		}
		else
			tempString = "";
		
		String restOfMt = minTerm.replace(MtWithSopTag, ""); 
		//System.out.println("\nRest of Minterm: "+restOfMt);
		
		separateArrayOfLitInMt = extractLiteralsFromMinTerms(separateArrayOfLitInMt, restOfMt);
		return separateArrayOfLitInMt;
	}


	public ArrayList<String> extractLiteralsFromMinTerms(ArrayList<String> separateArrayOfLitInMt, String restOfMt) 
	{
		
		for(int i = 0; i< restOfMt.length(); i++)
		{
			if((i + 1) != restOfMt.length())
			{
				if(restOfMt.charAt(i+1) == '\'')
				{
					if(i+2 == restOfMt.length())
						separateArrayOfLitInMt.add(restOfMt.substring(i));
					else
						separateArrayOfLitInMt.add(restOfMt.substring(i, i+2));
				}
				else
				{
					if(restOfMt.charAt(i) != '\'')
						separateArrayOfLitInMt.add(restOfMt.substring(i, i+1));
				} 
			}
			else
			{
				if(restOfMt.charAt(i) != '\'')
					separateArrayOfLitInMt.add(restOfMt.substring(i));
			}

		}
		return separateArrayOfLitInMt;
	}

	
	public String [] splitStringIntoTwo (String inputString, String splitAroundString)
	{
		String [] splittedString = {"",""};
		
		if(inputString.contains(splitAroundString))
		{
			try {
				splittedString = inputString.split(splitAroundString, 2);
			} catch (Exception e) {
				splittedString = inputString.split("\\"+splitAroundString, 2);
				//e.printStackTrace();
			}
		}
		else
		{
			splittedString[0] = inputString;
			splittedString[1] = "";
		}
		return splittedString;
		
	}
	
}




