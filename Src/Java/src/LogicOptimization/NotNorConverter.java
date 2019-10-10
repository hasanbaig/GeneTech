package LogicOptimization;

import java.util.ArrayList;
import java.util.Arrays;

public class NotNorConverter 
{
	public String reducedExpression;
	private EMinTermsProcessor processNorNotExp;
	
	public NotNorConverter ()
	{
		processNorNotExp = new EMinTermsProcessor("",0.0,"");
	}
	
	
	// most high level method for converting expression into NOR/NOT form
	public String convertIntoNotNorExp(String inputExpression)
	{
		String [] minTermsInsideBraces = null;
		String [] beforeBraces = null;
		String expInsideBraces = "";
		String nandToOr = "";
		//String inputExpression = "";
		ArrayList<Integer> braceIndices = new ArrayList<>();
		String outputString = inputExpression;
		
		// if expression contains braces
		if(searchBraceTerm(inputExpression))
		{
			//break minterms around + sign
			
			//First convert braces into SOP tags. 
			//expWithBraces = processNorNotExp.replaceBracesWithTags(inputExpression);
			
			//Count and catch SOP1 (high level braces) terms are in the expression
			braceIndices = countBraceIndices (inputExpression);
			
			
			String intermString = "";
			String insideBraces = "";
			
			
			
			for(int i = 0; i < braceIndices.size(); i++)
			{
				intermString = inputExpression.substring(braceIndices.get(i) + 1);
				insideBraces = intermString.substring(0, intermString.indexOf(")"));
				
				minTermsInsideBraces = splitAroundPlus (insideBraces);
				
				//search and process ANDed minterms inside braces
				minTermsInsideBraces = searchThenProcessANDTerms(minTermsInsideBraces);
				//System.out.println("Minterms inside braces: " + Arrays.toString(minTermsInsideBraces));
				
				//Convert OR terms to NAND
				if (minTermsInsideBraces.length > 1)
				{
					expInsideBraces = processORTerm(minTermsInsideBraces);
					outputString = outputString.replace(insideBraces, expInsideBraces);
				}
				else
				{
					expInsideBraces = processNorNotExp.minTermsToExpression(minTermsInsideBraces);
					outputString = outputString.replace(insideBraces, expInsideBraces);
				}
				
				
				// Check if the terms inside braces contains NANDed terms (without having + sign in it)
				if(!expInsideBraces.contains("+"))
				{
					if (expInsideBraces.substring(expInsideBraces.indexOf("]")+1).equals("'"))
						nandToOr = processNandTerm (expInsideBraces);
					//
					outputString = outputString.replace(expInsideBraces, nandToOr);
				} 
				else // if it contains multiple terms
				{
					intermString = expInsideBraces;
					expInsideBraces = expInsideBraces.substring(expInsideBraces.indexOf("[")+1, expInsideBraces.indexOf("]"));
					minTermsInsideBraces = splitAroundPlus (expInsideBraces);
					minTermsInsideBraces = searchThenProcessANDTerms(minTermsInsideBraces);
					
					String newExpInsideBraces = processNorNotExp.minTermsToExpression(minTermsInsideBraces);
					
					//newExpInsideBraces = newExpInsideBraces.replaceAll("\\[", "(");
					//newExpInsideBraces = newExpInsideBraces.replaceAll("\\]", ")");
					
					outputString = outputString.replace("(["+expInsideBraces+"]')", "("+newExpInsideBraces+")'");
					
				}
			}
			
		}
		else
		{
			String [] minterms;
			//if there are no braces, then proceed further here.
			if(inputExpression.contains("+"))
			{
				minterms = splitAroundPlus (inputExpression);
				
				minterms = searchThenProcessANDTerms(minterms);
				
				outputString = processNorNotExp.minTermsToExpression (minterms);
			}
			else
			{
				outputString = processANDTerm(outputString);
			}	
		}
		
		//outputString = "";
		//processing terms outside braces
		outputString = outputString.replaceAll("\\[", "(");
		outputString = outputString.replaceAll("\\]", ")");
		String resultString = processNorNotExp.replaceBracesWithTags(outputString); 
		String [] currentMinTerms = processNorNotExp.generateMinTermsArray (resultString, processNorNotExp.cntMinTermsInExpression(resultString));
		
		for(int i = 0; i < currentMinTerms.length; i++)
		{
			currentMinTerms[i] = processNorNotExp.replaceTagsWithBraces(currentMinTerms[i]);
			braceIndices = countBraceIndices (currentMinTerms[i]);
			String intermString = currentMinTerms[i];
			if (braceIndices.size() == 1)		// if brace term is present
			{ 
				intermString = processNorNotExp.replaceBracesWithTags(intermString);
				String multiplier = intermString.replace(intermString.substring(intermString.indexOf("SOP1"), intermString.indexOf("EOP1")+4), "");
				
				String multiplicand = intermString.substring(intermString.indexOf("SOP1"));
				if(!multiplier.isEmpty() && !multiplier.contentEquals("'"))
				{
					intermString = multiplier.replaceAll("\\'", "");
					if(intermString.length() == 1)
					{
						if(multiplier.contains("'"))
							multiplier = multiplier.replace("'", "");
						else
							multiplier = multiplier + "'";
					}
					else
						System.out.println("\nThe multiplier contains more than 1 literals");
					
					intermString = multiplicand.substring(multiplicand.indexOf("EOP1")+4);
					if(intermString.equals("'"))
						multiplicand = multiplicand.substring(0, multiplicand.indexOf("EOP1")+4);
					else
						multiplicand = multiplicand + "'";	
					
//					outputString = "("+ multiplier + "+" + multiplicand + ")'"; 
					multiplicand = processNorNotExp.replaceTagsWithBraces(multiplicand);
					
					currentMinTerms [i] = "("+ multiplier + "+" + multiplicand + ")'";
				}
			}
			else			// if minterm do not contain braces
			{
				if(currentMinTerms[i].length()>2)
					currentMinTerms[i] = processANDTerm(currentMinTerms[i]);
				else
					currentMinTerms[i] = processANDTerm(currentMinTerms[i]);
			}
		}
		
		if(currentMinTerms.length > 1)
			outputString = processNorNotExp.minTermsToExpression(currentMinTerms);
		else
			outputString = Arrays.toString(currentMinTerms).replaceAll("\\[", "").replaceAll("\\]", "");
		//System.out.println("process OR Terms: "+orToNand);
//		adsa
		outputString = outputString.replaceAll("\\[", "(");
		outputString = outputString.replaceAll("\\]", ")");
		return outputString;
	}


	private String [] searchThenProcessANDTerms(String[] minTermsInsideBraces) 
	{
		for(int j = 0; j < minTermsInsideBraces.length; j++)
		{
			if(minTermsInsideBraces[j].length() > 1) //may be ANDed terms
			{
				if(minTermsInsideBraces[j].substring(1).equals("'")) //Not term e.g a'
				{
					if(minTermsInsideBraces[j].length()>2) // e.g. a'b
						minTermsInsideBraces[j] = processANDTerm (minTermsInsideBraces[j]); //pass the minterm to process AND term
					else
						continue; 
				}
				else
				{
					if(minTermsInsideBraces[j].length() > 2)
						minTermsInsideBraces[j] = processANDTerm (minTermsInsideBraces[j]); //pass the minterm to process AND term
					else	
						minTermsInsideBraces[j] = processANDTerm (minTermsInsideBraces[j]); //pass the minterm to process AND term
					
				}
			}
		}
		return minTermsInsideBraces;
	}
	
	
	//rest of other methods.
	
	private String processNandTerm(String expInsideBraces) 
	{
		ArrayList<String> sepArrOfLitInMts = new ArrayList<>(); 
		expInsideBraces = expInsideBraces.replaceFirst("\\[", "");
		expInsideBraces = expInsideBraces.replaceFirst("\\]'", "");
		sepArrOfLitInMts = processNorNotExp.extractLiteralsFromMinTerms(sepArrOfLitInMts, expInsideBraces);
		//System.out.println("Separate Array of Lit in Nand term"+sepArrOfLitInMts);
		
		String intermString = "";
		String newElement = "";
		for(int i = 0; i< sepArrOfLitInMts.size(); i++)
		{
			if(sepArrOfLitInMts.get(i).contains("'"))
				newElement = sepArrOfLitInMts.get(i).replace("'", "");
			else
				newElement = sepArrOfLitInMts.get(i) + "'";
			
			if (i == 0)
				intermString = newElement;
			else 
				intermString = intermString + "+" + newElement;
		}
		
		//intermString = "[" + intermString + "]'"; 
		
		return intermString;
	}


	//Count number of SOP tags
	private ArrayList<Integer> countBraceIndices(String expWithBraces) 
	{
		int idxOfBrace = 0;
		ArrayList<Integer> braceIndices = new ArrayList<>();
		expWithBraces = processNorNotExp.replaceBracesWithTags(expWithBraces);
		for (int i = 0; i < expWithBraces.length(); i++)
		{
			idxOfBrace = expWithBraces.indexOf("SOP1", i);
			if (idxOfBrace != -1)
			{
				i = idxOfBrace + 4;
				braceIndices.add(idxOfBrace);
			}
			else
				i = expWithBraces.length();
		}	
		return braceIndices;
	}


	
	public boolean searchBraceTerm (String inputExpression)
	{
		boolean containBraceTerm = inputExpression.contains("(");
		return containBraceTerm;
	}
	
	
	
	//Arrange minterms inside braces in a separate array
	public String [] splitAroundPlus (String inputExpression)
	{
		String[] splitAroundPlus ;
		
		splitAroundPlus = inputExpression.split("\\+");
		
		return splitAroundPlus;
	}
	
	
	
	public String processANDTerm (String currentMinTerm)
	{
		ArrayList<String> sepArrOfLitInMts = new ArrayList<>(); 
		sepArrOfLitInMts = processNorNotExp.extractLiteralsFromMinTerms(sepArrOfLitInMts, currentMinTerm);
		
		String intermString = "";
		String newElement = "";
		for(int i = 0; i< sepArrOfLitInMts.size(); i++)
		{
			if(sepArrOfLitInMts.get(i).contains("'"))
				newElement = sepArrOfLitInMts.get(i).replace("'", "");
			else
				newElement = sepArrOfLitInMts.get(i) + "'";
			
			if (i == 0)
				intermString = newElement;
			else 
				intermString = intermString + "+" + newElement;
		}
		
		intermString = "[" + intermString + "]'"; 
		
		return intermString;
	}
	
	
	
	public String processORTerm (String [] mintermsInsideBraces)
	{
		String newElement = "";
		String intermString = "";
		
		if(mintermsInsideBraces.length > 1)
		{
			for (int i = 0; i<mintermsInsideBraces.length; i++)
			{
				if(mintermsInsideBraces[i].substring(mintermsInsideBraces[i].length() - 1).contains("'")) //extracting last character.
					newElement = mintermsInsideBraces[i].substring(0,mintermsInsideBraces[i].length() - 1);
				else
					newElement = mintermsInsideBraces[i] + "'";
				
				if(i == 0)
					intermString = newElement;
				else
					intermString = intermString + newElement;
			}
			
			intermString = intermString.replace("[", "(");
			intermString = intermString.replace("]", ")");
			
			// search for ( and bring the multiplier before (, instead of after ).
			//Extracting multiplier first. searching and replacing brace terms () with "". Can process upto 1 braced term
			// only.
			processNorNotExp.resultString = intermString;
			
			String multiplier = intermString.replace(intermString.substring(intermString.indexOf("("), intermString.indexOf(")")+1), "");
			String multiplicand = intermString.substring(intermString.indexOf("(")+1, intermString.indexOf(")"));
			//System.out.println("\nmultiplier: "+multiplier);
			//System.out.println("\nmultiplicand: "+multiplicand);
			
			int CntMinTerms = processNorNotExp.cntMinTermsInExpression (multiplicand);
			String [] currentMinTerms = new String [CntMinTerms];
			currentMinTerms = processNorNotExp.generateMinTermsArray (multiplicand, CntMinTerms);
			
			
			intermString = expandMinTerms (currentMinTerms, multiplier, multiplicand);
			
			//System.out.println("\nCheck: "+check);
			
			intermString = "[" + intermString + "]'";
		}
		
		
		return intermString;
	}

	
	//This method is used by a class NotNorConverter
	public String expandMinTerms (String [] currentMinTerms, String multiplier, String multiplicand)
	{
		String [] outputMinTerms = new String[currentMinTerms.length];
		for(int i=0; i< currentMinTerms.length; i++)
		{
			if(currentMinTerms[i].contains("1"))
				currentMinTerms[i] = "";
			else if(multiplier.contains("("))
			{
				String intermString = multiplier;
				String expInsideMultiplier = intermString.substring(intermString.indexOf("(")+1, intermString.indexOf(")"));
				int CntMinTerms = processNorNotExp.cntMinTermsInExpression (expInsideMultiplier);
				String [] minTermsInMultiplier = new String [CntMinTerms];	
				minTermsInMultiplier = processNorNotExp.generateMinTermsArray (expInsideMultiplier, CntMinTerms);
				
				outputMinTerms[i] = expandMinTerms (minTermsInMultiplier, currentMinTerms[i], expInsideMultiplier);
				
			}
			else
				outputMinTerms[i] = processNorNotExp.scanRules(multiplier.concat(currentMinTerms[i]));				
		}
		
		//System.out.println(Arrays.toString(outputMinTerms));
		
		String expandedMinTerms = processNorNotExp.minTermsToExpression (outputMinTerms);
		
		//String searchExpression = multiplier.concat("(").concat(multiplicand).concat(")");
		//System.out.println("\nSearch Expression: "+searchExpression);
		
		//String expandedExpression = resultString;
		//expandedExpression = expandedExpression.replace(searchExpression, expandedMinTerms); //replaceFirst(searchExpression, expandedMinTerms);
		
		if(expandedMinTerms.contains("0"))
			expandedMinTerms = expandedMinTerms.replaceAll(".?{0,1}(0).?{0,1}", "");
		
		return expandedMinTerms;
	}

}
