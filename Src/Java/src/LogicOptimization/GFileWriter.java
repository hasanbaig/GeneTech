package LogicOptimization;



public class GFileWriter 
{
	public String inputFilePath; 
	public String inputData;
	public GFileWriter (String inputFilePath, String inputData)
	{
		this.inputFilePath = inputFilePath;
		this.inputData = inputData;
	}
	public String getInputFilePath() {
		return inputFilePath;
	}
	public void setInputFilePath(String inputFilePath) {
		this.inputFilePath = inputFilePath;
	}
	public String getInputData() {
		return inputData;
	}
	public void setInputData(String inputData) {
		this.inputData = inputData;
	}
}
