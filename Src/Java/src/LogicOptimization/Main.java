package LogicOptimization;
import py4j.GatewayServer;
import java.util.*;
import java.util.Scanner;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.math.*;
import java.util.Arrays;
import org.apache.commons.lang3.*;

import TechMap.TechMapper;

import java.io.*;

public class Main 
{
	public static FileWriter fw; 
	public static void main (String [] args) throws Exception
	{
		//Creates a GatewayServer instance with default port (25333), default address (127.0.0.1), and default timeout value (no timeout).
		GatewayServer gatewayServer = new GatewayServer(new Main());
        gatewayServer.start(false); //Starts to accept connections
        System.out.println("Gateway Server Started");
		//function();
	}
		
	//public static void function() throws Exception
	public static void function(String inputBoolExp) throws Exception
	{
		try{fw = new FileWriter("../Data.txt");}
		catch(Exception e){System.out.println(e);}
		//Calling method to check aLVJavaInterface Class
		ALVJavaInterface inputInterface = new ALVJavaInterface ();
		//String inputBoolExp = "IPTG'.aTc.Arabinose'+IPTG'.aTc.Arabinose+IPTG.aTc.Arabinose";
		//String inputBoolExp = "IPTG'.aTc'.Arabinose'+IPTG.aTc'.Arabinose'+IPTG.aTc.Arabinose'";
		String newInputEq = initLVJavaInterface(inputInterface, inputBoolExp);
		
		System.out.println("***************************************************************************\n");
		System.out.println("Input Expression is: " + inputBoolExp);
		System.out.println("\n***************************************************************************");
		
		
		// Calling method to run simulated annealing algorithm
		double initTemp = inputInterface.initTemp; 		//10.0;
		double tempCoeff = inputInterface.tempCoeff; 	//0.90;
		double timeToRun = inputInterface.timeToRun;	//0.030;	//0.5
		String bestSolution = runSaAlgo(newInputEq, initTemp, tempCoeff, timeToRun);
		
		
		
		String outExp="";
		
		// *********************** Test block for NorNot converter ***********************
		String inputExp = bestSolution; //"c'(ab+b')";
		EMinTermsProcessor processExpression = new EMinTermsProcessor ("", 0, "");
		NotNorConverter convertExp = new NotNorConverter ();
		
		String outputString = convertExp.convertIntoNotNorExp(inputExp);
		System.out.println("\nSynthesized Expression into NOT-NOR Form: "+outputString);
		fw.write("\n" + outputString);
		
		// *********************************************************************
		
		
		ALVJavaInterface outputInterface = new ALVJavaInterface ();
		String newOrigEq = outputToLabVIEW(outputInterface, inputInterface, outputString);
		System.out.println("\nNew Expression with input proteins: "+newOrigEq);
		fw.write("\n"+ newOrigEq);
		
		
		// Technology Mapping
		TechMapper mapGatesOnExpression = new TechMapper (outputString);
		String libFile = mapGatesOnExpression.readGatesLibFile();
		mapGatesOnExpression.parseGateLibComp(libFile);
		//printGatesList(mapGatesOnExpression);
		
		mapGatesOnExpression.generateTreeExpression();
		mapGatesOnExpression.finalize();
		try{fw.close();}
		catch(Exception e){System.out.println(e);}
	}





	private static void printGatesList(TechMapper mapGatesOnExpression) {
		System.out.println("\nList of External Inverters");
		System.out.println("----------------------------");
		for(int i=0; i < mapGatesOnExpression.externalInvertersList.size(); i++)
			System.out.println(mapGatesOnExpression.externalInvertersList.get(i));
		
		System.out.println("\nList of Internal Inverters");
		System.out.println("----------------------------");
		for(int i=0; i < mapGatesOnExpression.internalInvertersList.size(); i++)
			System.out.println(mapGatesOnExpression.internalInvertersList.get(i));
		
		System.out.println("\nList of External Nor Gates");
		System.out.println("----------------------------");
		for(int i=0; i < mapGatesOnExpression.externalNorGatesList.size(); i++)
			System.out.println(mapGatesOnExpression.externalNorGatesList.get(i));
		
		System.out.println("\nList of Semi External Nor Gates");
		System.out.println("---------------------------------");
		for(int i=0; i < mapGatesOnExpression.semiExternalNorGatesList.size(); i++)
			System.out.println(mapGatesOnExpression.semiExternalNorGatesList.get(i));
		
		System.out.println("\nList of Internal Nor Gates");
		System.out.println("----------------------------");
		for(int i=0; i < mapGatesOnExpression.internalNorGatesList.size(); i++)
			System.out.println(mapGatesOnExpression.internalNorGatesList.get(i));
	}

	
	
	
	
	private static String outputToLabVIEW(ALVJavaInterface outputInterface,ALVJavaInterface inputInterface, String outputString) 
	{
		//ALVJavaInterface outputInterface = new ALVJavaInterface ();
		
		
		String [] newInputNames = inputInterface.getNewInputNames(); 
		String [] origInputNames = inputInterface.getOrigInputNames();
		
		String newOrigEq = outputInterface.replaceInputEqWithOrigNames(outputString, newInputNames, origInputNames);
		
		return newOrigEq;
	
	}





	// Main methods	
	public static String initLVJavaInterface(ALVJavaInterface inputInterface, String inputExp)
	{
		
		
		//================================== external inputs ==================================
		//String origInputEq = "IPTG'.aTc.Arabinose'+IPTG'.aTc.Arabinose+IPTG.aTc.Arabinose"; // Current Circuit = 0xC4
		String [] inputProt = {"IPTG", "aTc", "Arabinose"};
		//=====================================================================================
		inputInterface.setOrigInputNames(inputProt);
		
		inputInterface.takeInputs(inputExp);
		
		
		//System.out.println("Original Inputs: " +Arrays.toString(inputProt));
		//System.out.println("Original Equation: " + origInputEq);

		
		//inputInterface.setOrigInputEq(origInputEq);
		
		String newInputEq = inputInterface.replaceInputEqWithNewNames(inputInterface.replaceInputNames());
		
		//System.out.println("New Expressions: " + newInputEq);
		
		return newInputEq; 
	}

	
	
	//Method to calculate initial cost
	public static int initCalculateCost(String inputEq)
	{
		
		BCalculateCost initialCost = new BCalculateCost (inputEq); 
		
		int initCost = initialCost.getCost();
		System.out.println("Initial Cost: "+ initCost);
		return initCost;
	}
	
	
	
	
	//Method to run Simulated Annealing Algorithm
	public static String runSaAlgo (String newInputEq, double initTemp, double tempCoeff, double timeToRun) throws Exception
	{
		String filePath = "";
		File writeFile = new File (filePath);
		
		CSaAlgo SimAnneal = new CSaAlgo(tempCoeff, initTemp, timeToRun, newInputEq);
		
		System.out.println("\nOptimized Expression: "+SimAnneal.getBestSolution());
		System.out.println("\nNew Cost: "+SimAnneal.newCost);
		fw.write(SimAnneal.getBestSolution());
		fw.write("\n" + String.valueOf(SimAnneal.newCost));
		
		return SimAnneal.getBestSolution();
	}
	
	//Method to take input from users
	
}
