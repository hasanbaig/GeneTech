package LogicOptimization;

import java.util.ArrayList;

public class FScanCommonLiterals {
	
	public String randEl1;
	public String randEl2;
	public String randRedEl1;
	public String randRedEl2;
	public String matchedVar;
	private EMinTermsProcessor processExpression;
	
	
	public FScanCommonLiterals (String randEl1, String randEl2)
	
	{
		this.randRedEl1 = randRedEl1;
		this.randRedEl2 = randRedEl2;
		this.matchedVar = matchedVar;		
	}
	
	public ArrayList <String> separateArrayOfLitInMt0;
	public ArrayList <String> separateArrayOfLitInMt1;

	public void executeScanCommonLiterals (String randEl1, String randEl2)
	{
		processExpression = new EMinTermsProcessor ("", 0, "");
		// Sequence 7 of REDUCE: Scan common literals... Seq 1of6
		separateArrayOfLitInMt0 = splitMinTermsIntoLiterals(randEl1);
		//System.out.println("\n Separate Arrays of Literals in Minterm 0;"+ separateArrayOfLitInMt0);
		
		separateArrayOfLitInMt1 = splitMinTermsIntoLiterals(randEl2);
		//System.out.println("\n Separate Arrays of Literals in Minterm 1;"+ separateArrayOfLitInMt1);
		
		// Sequence 7 of REDUCE: Scan common literals... Seq 2of6
		// received output in the form of matchedVariable, reduced randElofMt0 and reduced randElofMt1
		ArrayList<String> mvRedRandElOfMt = searchCommonLiterals (separateArrayOfLitInMt0, separateArrayOfLitInMt1, randEl1, randEl2);
		String matchedVariable = mvRedRandElOfMt.get(0);
		String redRandElofMt0 = mvRedRandElOfMt.get(1);
		String redRandElofMt1 = mvRedRandElOfMt.get(2);
		
		//System.out.println("\nMatched Variable: "+ matchedVariable);
		
		// Sequence 7 of REDUCE: Scan common literals... Seq 3of6
		redRandElofMt0 = processExpression.replaceBracesWithTags(redRandElofMt0);
		redRandElofMt1 = processExpression.replaceBracesWithTags(redRandElofMt1);
		
		// Sequence 7 of REDUCE: Scan common literals... Seq 4-5 of 6
		//String splittedString0 [] = processExpression.splitStringIntoTwo(redRandElofMt0, "SOP1");
		redRandElofMt0 = procRedRandMtEl (redRandElofMt0);
		redRandElofMt1 = procRedRandMtEl (redRandElofMt1);
		//System.out.println("\nReduced Element0: "+ redRandElofMt0); 
		//System.out.println("\nReduced Element1: "+ redRandElofMt1);
					
		// Sequence 7 of REDUCE: Scan common literals... Seq 6 of 6
		redRandElofMt0 = processEmptyBraces (redRandElofMt0);
		redRandElofMt1 = processEmptyBraces (redRandElofMt1);
		//System.out.println("\nReduced Element0 after processing braces: "+ redRandElofMt0); 
		//System.out.println("\nReduced Element1 after processing braces: "+ redRandElofMt1);
		
		randRedEl1 = redRandElofMt0;
		randRedEl2 = redRandElofMt1;
		matchedVar = matchedVariable;	
	}
	
	
	public String getRandRedEl1() {
		return randRedEl1;
	}
	

	public void setRandRedEl1(String randRedEl1) {
		this.randRedEl1 = randRedEl1;
	}

	public String getRandRedEl2() {
		return randRedEl2;
	}

	public void setRandRedEl2(String randRedEl2) {
		this.randRedEl2 = randRedEl2;
	}

	public String getMatchedVar() {
		return matchedVar;
	}

	public void setMatchedVar(String matchedVar) {
		this.matchedVar = matchedVar;
	}

	
	
	// The following method splits the minterms into an array of literals
	public ArrayList<String> splitMinTermsIntoLiterals (String randElofMt)
	{
		EMinTermsProcessor processMinTerm = new EMinTermsProcessor (randElofMt, 0, "");
		//EMinTermsProcessor ProcessMinTerm1 = new EMinTermsProcessor (randElofMt, 0, "");
		
		//Separate array of literals in minterm 0
		ArrayList <String> separateArrayOfLitInMt = new ArrayList<>();
		
		//Separate array of literals in minterm 1
		//ArrayList <String> separateArrayOfLitInMt1 = new ArrayList<>();
		
		separateArrayOfLitInMt = processMinTerm.arrangeLitInArray(processMinTerm.replaceBracesWithTags(randElofMt)) ;
		
		return separateArrayOfLitInMt;
	}
	
	
	
	// The following method scan for the common literals in the minterms
	public ArrayList<String> searchCommonLiterals (ArrayList<String> separateArrayOfLitInMt0, 
										 ArrayList<String> separateArrayOfLitInMt1,
										 String randElofMt0, String randElofMt1)
	{
		String intString;
		ArrayList<String> outArray = new ArrayList<String>();
		String matchedVariable = "";
		for(int i = 0; i < separateArrayOfLitInMt0.size(); i++)
		{
			for (int j=0; j < separateArrayOfLitInMt1.size(); j ++)
			{
				if(separateArrayOfLitInMt0.get(i).equals(separateArrayOfLitInMt1.get(j)))
				{
					if(separateArrayOfLitInMt0.get(i).contains("+"))
						intString = "("+separateArrayOfLitInMt0.get(i)+")";
					else
						intString = separateArrayOfLitInMt0.get(i);
					
					randElofMt0 = randElofMt0.replaceFirst(intString, "");
					randElofMt1 = randElofMt1.replaceFirst(intString, "");
					
					if(!matchedVariable.isEmpty())
						matchedVariable = matchedVariable + intString;
					else
						matchedVariable = intString;	
				}
			}
		}
			outArray.add(matchedVariable);
			outArray.add(randElofMt0);
			outArray.add(randElofMt1);
			
			return outArray;
	}
	
	
	
	// process reduced minterm elements which were chosen randomly
	public String procRedRandMtEl (String redRandElofMt)
	{
		String splittedString [] = processExpression.splitStringIntoTwo(redRandElofMt, "SOP1");
		String intermediatte = "";
		if(splittedString [0].equals(""))
		{
			if(!splittedString [1].equals(""))
				intermediatte = splittedString[1].substring(0, splittedString[1].indexOf("EOP1"));
		}
		else
			intermediatte = redRandElofMt;
		
		redRandElofMt = processExpression.replaceTagsWithBraces(intermediatte);
		
		if(redRandElofMt.isEmpty())
			redRandElofMt = "1";
				
		return redRandElofMt;
	}

	
	
	// The following method is used to search and remove the empty pair of braces
	public String processEmptyBraces (String redRandElofMt)
	{
		
		String stringAfterLeftBrace [] = processExpression.splitStringIntoTwo(redRandElofMt, "(");
		String stringBeforeRightBrace [];
		
		if(!stringAfterLeftBrace[1].equals("")) //stringAfterLeftBrace[1] != "" means '(' is found
		{
			stringBeforeRightBrace = processExpression.splitStringIntoTwo(stringAfterLeftBrace[1], ")");
			
			if(stringBeforeRightBrace[0].equals(""))
				redRandElofMt = redRandElofMt.replace(redRandElofMt.subSequence(redRandElofMt.indexOf("("), redRandElofMt.indexOf("(") + 2), "");
			else
				redRandElofMt = redRandElofMt;			
		}
		
		return redRandElofMt;
	}	
}


//Make an upper method which calls all of these methods and return the results.
