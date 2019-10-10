/*
 @author Hasan Baig
 This class is used to implement simulated annealing algorithm. Everything is run inside this algo.
 
 Inputs: 
 Temperature Co-efficient: Float 
 Initial Temperature: Float
 Time to run: Int
 Output: 
 New Input Equation. 
 
*/
package LogicOptimization;

import java.io.File;

public class CSaAlgo 
{
	private double tempCoeff;
	private double initTemp;
	private int timeToRun;
	private String inputExp;
	public String bestSolution;
	public int newCost = 0;
	



	public CSaAlgo (double tempCoeff, double initTemp, double timeToRun, String inputExpression) throws Exception
	{

		double currentTemp = 0;
		String currentSt = inputExpression;
		String nextSt = "";
		int prevCost = 0;
		//int newCost = 0;
		double acceptanceProb;
		int Cnt = 0;
		boolean forceExpand = false;
		String exprToProcess;
		
		//Creating a file object
		File file = new File("../DebugLog.xls");
		
		// Removing space characters from input expression
		//inputExpression = inputExpression.replaceAll(" ", "");
		//inputExpression = inputExpression.replaceAll(".", "");
		
		
		
		//Creating an object to reduce expression. Have to put it inside while loop 
		DReduceExp REDUCE = new DReduceExp(file); // Creating a reduce object only once.
		
		
		//nextState = REDUCE.performReduction(currentState);
		
		//System.out.println(REDUCE.extractVariable(inputExp));
		//System.out.println(REDUCE.varCnt);
		
		long tStart = System.currentTimeMillis();
		double currentTime = 0.0 ;
		
		int loopCount = 0;
		while (currentTime<=timeToRun)
		{
			currentTemp = tempCoeff * initTemp;
			initTemp = currentTemp;

			
			//--------Here DReduceExp will be executed.
			
			//if(loopCount == 0)						//remove this... added for testing only ************************
			nextSt = REDUCE.performReduction(currentSt, loopCount);
			prevCost = REDUCE.costOfCurrentExpression;
			newCost = REDUCE.costOfNewExpression;
			
			
			//--------------------------------------------------//
			
			//Calculate the acceptance probability based on the new cost of reduced expression. 
			if(newCost >= prevCost)
			{
				acceptanceProb = Math.exp(-(newCost - prevCost)/currentTemp);
				Cnt += 1;
			}
			else
				acceptanceProb = 1;
		
			if(acceptanceProb > Math.random())
				currentSt = nextSt;
			else
				currentSt = currentSt;
			
			
			currentTime = getTime (tStart);
			
			
			
			loopCount += 1;
			
		}
		//System.out.println("\n*******Out of CSaAlgo While loop*******");
		
		//System.out.println("\nCurrent Time: "+currentTime+" s");
		//System.out.println("\nCurrent Temp: "+currentTemp);
		
		//System.out.println("\nBest Solution: "+currentSt);
		bestSolution = currentSt;
		//System.out.println("\nNew Cost: "+newCost);
	}
	

	private double getTime (long tStart)
	{
		long tEnd = System.currentTimeMillis();
		long tDelta = tEnd - tStart;
		double elapsedSeconds = tDelta / 1000.0;
		return elapsedSeconds;
	}
	
	public String getBestSolution() {
		return bestSolution;
	}

}

