package gov.nasa.jpf.symbc;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
public class DNNDenseLayer extends DNNLayer{
	public double[][] data2;
	public int mainDimension=2;
	public String name="";
	public int subDimension1=0;
	public int subDimension2=0;
	public void printData()
	{	
		for (int i=0; i<subDimension1; i++) {
			System.out.println();
			for (int j=0; j<subDimension2; j++) {
				System.out.print(data2[i][j]+" ");
			}
		}  
		System.out.println("");
	}
	public void readData(String path,String name)
	{	
		this.name=name;
		File file = new File(path + "/"+name+".txt");
		mainDimension=DNNArchitectureFactory.mapDimension.get(name).size();
		subDimension1=DNNArchitectureFactory.mapDimension.get(name).get(0);
		subDimension2=DNNArchitectureFactory.mapDimension.get(name).get(1);
		data2 = new double[subDimension1][subDimension2];
		try (BufferedReader br = new BufferedReader(new FileReader(file))) {
			String line;
			for (int i=0; i<subDimension1; i++) {
				line = br.readLine();
				String[] items = line.split(",");
				for (int j=0; j<subDimension2; j++) {
					data2[i][j] = Double.valueOf(items[j].trim());
				}
			}
		} catch (IOException e) {
			throw new RuntimeException(e);
		}
	}	
	public Object getData()
	{	
		return data2;
	}
	public ArrayList<Integer> getSubDimension()
	{
		return DNNArchitectureFactory.mapDimension.get(name);	
	}
}