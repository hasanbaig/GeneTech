/*
 @author Hasan Baig
 This class is used to calculate the cost of equation. 
 
 Inputs: 
 Input equation: String 
 Cost of Equation - Number of literals: integer
 
 Output: 
 New Input Equation. 
 
 */

package LogicOptimization; 
public class BCalculateCost 

{
	public String inputEq;
	public String literalsOnly;
	public int Cost;
	public BCalculateCost (String inputEq)
	{
		inputEq = inputEq.replaceAll(" ", "");
		inputEq = inputEq.replaceAll("'", "");
		inputEq = inputEq.replaceAll("\\.", "");
		inputEq = inputEq.replaceAll("\\+", "");
		inputEq = inputEq.replaceAll("\\(", "");
		inputEq = inputEq.replaceAll("\\)", "");
		int cost = inputEq.length();
		this.Cost = cost;
		this.literalsOnly = inputEq;
		
	}
	
	public int getCost()
	{
		return Cost;
	}
	
	public String getLiteralsOnly()
	{
		return literalsOnly;
	}
}
