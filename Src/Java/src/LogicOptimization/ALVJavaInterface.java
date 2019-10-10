/*
 @author Hasan Baig
 This class is used to create LabVIEW-JAVA interface. It takes the unoptimized input equation from
 LabVIEW logic analysis VI and the name of input genetic components. It then replace the names of input
 genetic components with the simple alphabets in the equation. 
 
 Inputs: 
 Original Input Equation from Labview 
 Names of input genetic components
 
 Output: 
 New Input Equation. 
 
 */


package LogicOptimization;

import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ALVJavaInterface 

{
	public static String origInputEq;			//Takes in the Original input equations
	public String [] origInputNames; 		//Takes in the Original input names
	public String newInputEq;
	public String [] newInputNames;
	public static double tempCoeff;
	public static double initTemp;
	public static double timeToRun;
	
	public ALVJavaInterface ()
	{
		this.origInputNames = origInputNames;
		this.tempCoeff = tempCoeff;
		//String [] newInputNames = replaceInputNames(origInputNames);
		//newInputEq = replaceInputEq (origInputEq, origInputNames, newInputNames);
	}
	
	public String getOrigInputEq() {
		return origInputEq;
	}

	public static void setOrigInputEq(String origInputEq) {
		origInputEq = origInputEq;
	}

	public String[] getOrigInputNames() {
		return origInputNames;
	}

	public void setOrigInputNames(String[] origInputNames) {
		this.origInputNames = origInputNames;
	}

	public String getNewInputEq() {
		return newInputEq;
	}

	public void setNewInputEq(String newInputEq) {
		this.newInputEq = newInputEq;
	}

	public String [] replaceInputNames ()
	{
		int size = origInputNames.length; 
		String [] newInputNames ;
		newInputNames = new String [size];			//Initializing the size of array
		char in;
		for (int i = 0; i < size ; i++)
		{
			in = (char) (i+97);
			newInputNames [i] = Character.toString(in); 	
		}
		this.newInputNames = newInputNames;
		return newInputNames;
	}
	
	


	//public String replaceInputEq (String origInputEq, String [] origInputNames, String [] newInputNames)
	public String replaceInputEqWithNewNames (String [] newInputNames)
	{
		
		String newInputEq = "";
		
		newInputEq = origInputEq;
		for (int i = 0; i < origInputNames.length; i++)
		{
			String currentInput = origInputNames [i];
			String newInput = newInputNames [i];
			newInputEq = newInputEq.replaceAll(currentInput, newInput);
		}
		
		// Removing space characters from input expression
		newInputEq = newInputEq.replaceAll(" ", "");
		newInputEq = newInputEq.replaceAll("\\.", "");
		return newInputEq;
		
	}

	public String[] getNewInputNames() {
		return newInputNames;
	}
	
	
	public String replaceInputEqWithOrigNames (String inputEquation, String [] newInputNames, String [] origInputNames)
	{
		
		String newOrigEq = "";
		
		newOrigEq = inputEquation;
		for (int i = 0; i < origInputNames.length; i++)
		{
			String currentInput = origInputNames [i];
			String newInput = newInputNames [i];
			newOrigEq = newOrigEq.replaceAll("\\b"+newInput+"\\b", currentInput);
		}
		
		// Removing space characters from input expression
		newOrigEq = newOrigEq.replaceAll(" ", "");
		newOrigEq = newOrigEq.replaceAll("\\.", "");
		return newOrigEq;
		
	}
	
	public static void takeInputs (String inpBoolExpression)
	{
		
		Scanner userInputs = new Scanner (System.in);
		System.out.println("*********** Please enter the following values ***********");
		
		while(true)
		{
			System.out.print("Temperature Coefficient (e.g. 0.9). => ");
			try{
				tempCoeff = 0.9;//userInputs.nextDouble();
				break;
			}
			catch (Exception e)
			{
				System.out.print("You have entered a wrong value. Please try again. \n\n");
				userInputs.next();
				continue;
			}
		}
		
		while (true)
		{
			System.out.print("Initial Temperature (e.g. 10). => ");
			try{
				initTemp = 10;//userInputs.nextDouble();
				break;
			}
			catch (Exception e)
			{
				System.out.print("You have entered a wrong value. Please try again. \n\n");
				userInputs.next();
				continue;
			}
		}
		
		while(true)
		{
			System.out.print("Time to run in seconds (e.g. 0.5 secs). => ");
			try{
				timeToRun = 0.5;//userInputs.nextDouble();	
				break;
			}
			catch(Exception e)
			{
				System.out.print("You have entered a wrong value. Please try again. \n\n");
				userInputs.next();
				continue;
			}
		}
		
		while (true)
		{
			System.out.print("Enter boolean expression in terms of inputs IPTG, aTc and Arabinose. \n"
					+ "(Use \" ' \" for inverted terms; \" . \" for ANDed terms; and \" + \" for ORed terms, without any spaces.) \n"
					+ "(e.g. IPTG'.aTc.Arabinose'+IPTG'.aTc.Arabinose+IPTG.aTc.Arabinose) \n"
					+ "=> ");
			try {
				//String inpBoolExpression = "IPTG'.aTc.Arabinose'+IPTG'.aTc.Arabinose+IPTG.aTc.Arabinose";//userInputs.next();
				
				if(inpBoolExpression.matches("[a-zA-Z' +.]+")) 
				{					
					if(Pattern.compile("^(\\w).*[\\w']$").matcher(inpBoolExpression).find()) //If expression starts with any non-word character and ends with any non-word character except '. 
					{
						origInputEq = inpBoolExpression;
						break;
					}
					else
						System.out.print("Invalid Expression! Please try again below. \n\n");
				}
				else
				{
					System.out.print("The input expression contains invalid characters. Please try again below. \n\n");
					continue;
				}
			}
			catch (Exception e)
			{
				System.out.print("You have entered a wrong expression. Please try again below. \n\n");
				userInputs.next();
				continue;
			}
		}

		
		System.out.println("");
		
	}
	
}
