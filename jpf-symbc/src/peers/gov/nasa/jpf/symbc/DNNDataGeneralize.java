package gov.nasa.jpf.symbc;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
public class DNNDataGeneralize {
	public static Map< String,Object> dataMap = new HashMap(); 
	public static Map< String,Integer> mainDimensionMap = new HashMap(); 
	public static Map< String, ArrayList<Integer>> subDimensionMap = new HashMap(); 
	public static void readDataFromFiles(String path,String jsonpath) throws FileNotFoundException, Exception {
		DNNArchitectureFactory.parseJSON(jsonpath);
		DNNLayer layerObject;
		for (String key : DNNArchitectureFactory.mapDimension.keySet()) {
			if(DNNArchitectureFactory.mapDimension.get(key).size()==1)
			{

				layerObject=new DNNBias();
				layerObject.readData(path, key);		
				mainDimensionMap.put(key,1);
				subDimensionMap.put(key,layerObject.getSubDimension());
				dataMap.put(key,layerObject.getData());				
			}
			else if(DNNArchitectureFactory.mapDimension.get(key).size()==2)
			{
				layerObject=new DNNDenseLayer();
				layerObject.readData(path, key);		
				mainDimensionMap.put(key,2);
				subDimensionMap.put(key,layerObject.getSubDimension());
				dataMap.put(key,layerObject.getData());
			}

			else if(DNNArchitectureFactory.mapDimension.get(key).size()==4)
			{
				layerObject	=new DNNConvolutionLayer();
				layerObject.readData(path, key);		
				mainDimensionMap.put(key,4);
				subDimensionMap.put(key,layerObject.getSubDimension());
				dataMap.put(key,layerObject.getData());
			}
		}
	}
}