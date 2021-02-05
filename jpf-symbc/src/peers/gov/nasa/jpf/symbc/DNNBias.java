package gov.nasa.jpf.symbc;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
public class DNNBias extends DNNLayer{
	public double[] data1;
	public int mainDimension=1;
	public String name="";
	public int subDimension1=0;
	public void printData()
	{
		for (int i=0; i<subDimension1; i++) {
			System.out.println(data1[i]);
		}
		System.out.println("");
	}
	public void readData(String path,String name)
	{	
		this.name=name;
		File file = new File(path + "/"+name+".txt");
		subDimension1=DNNArchitectureFactory.mapDimension.get(name).get(0);
		data1 = new double[subDimension1];
		try (BufferedReader br = new BufferedReader(new FileReader(file))) {
			String line;
			for (int i=0; i<subDimension1; i++) {
				line = br.readLine();
				data1[i] = Double.valueOf(line.trim());
			}
		} catch (IOException e) {
			throw new RuntimeException(e);
		}
	}
	public Object getData()
	{	
		return data1;
	}
	public ArrayList<Integer> getSubDimension()
	{
		return DNNArchitectureFactory.mapDimension.get(name);	
	}
}