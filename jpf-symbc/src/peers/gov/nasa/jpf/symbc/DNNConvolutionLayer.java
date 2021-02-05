package gov.nasa.jpf.symbc;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
public class DNNConvolutionLayer extends DNNLayer {
	public double[][][][] data4;
	public int mainDimension=4;
	public String name="";
	public int subDimension1=0;
	public int subDimension2=0;
	public int subDimension3=0;
	public int subDimension4=0;
	public void printData()
	{	
		for (int i=0; i<subDimension1; i++) {
			for (int j=0; j<subDimension2; j++) {
				for (int k=0; k<subDimension3; k++) {
					System.out.println();
					for (int l=0; l<subDimension4; l++) {
						System.out.print(data4[i][j][k][l]+" ");          	    
					}
				}
			}
		}
		System.out.println("");
	}
	public void readData(String path,String name)
	{	
		this.name=name;
		File file = new File(path + "/"+name+".txt");
		subDimension1=DNNArchitectureFactory.mapDimension.get(name).get(0);
		subDimension2=DNNArchitectureFactory.mapDimension.get(name).get(1);
		subDimension3=DNNArchitectureFactory.mapDimension.get(name).get(2);
		subDimension4=DNNArchitectureFactory.mapDimension.get(name).get(3);		
		data4 = new double[subDimension1][subDimension2][subDimension3][subDimension4];
		try (BufferedReader br = new BufferedReader(new FileReader(file))) {
			String line;
			for (int i=0; i<subDimension1; i++) {
				for (int j=0; j<subDimension2; j++) {
					for (int k=0; k<subDimension3; k++) {
						line = br.readLine();
						String[] items = line.split(",");
						for (int l=0; l<subDimension4; l++) {
							data4[i][j][k][l] = Double.valueOf(items[l].trim());
						}
					}
				}
			}
		} catch (IOException e) {
			throw new RuntimeException(e);
		}    
	}	
	public Object getData()
	{	
		return data4;
	}
	public ArrayList<Integer> getSubDimension()
	{
		return DNNArchitectureFactory.mapDimension.get(name);	
	}
}