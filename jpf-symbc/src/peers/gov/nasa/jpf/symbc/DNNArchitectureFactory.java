package gov.nasa.jpf.symbc;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.HashMap;

import java.util.TreeMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
public class DNNArchitectureFactory {
	public static Map<String,ArrayList<Integer>> mapDimension = new TreeMap();
	public static void parseJSON(String path) throws FileNotFoundException, Exception {
		JSONParser jsonParserObj = new JSONParser();		
		/////////////////////////////////////////Read Biases////////////////////////////////////////////////////////////////////
		String fileName="";
		Object obj = jsonParserObj.parse(new FileReader(path));
		JSONObject jsonObject = (JSONObject) obj; 
		Set<?> setKey =  jsonObject.keySet();
		Iterator<?> iteratorObject = setKey.iterator();
		do{
			String tempString = iteratorObject.next().toString();
			if(tempString.matches(".*\\d.*"))
			{    
				fileName=tempString;
				Map jsonArray = ((Map)jsonObject.get(tempString)); 
				Iterator<Map.Entry> itreator = jsonArray.entrySet().iterator(); 
				while (itreator.hasNext()) { 
					Map.Entry pair = itreator.next(); 
					if(pair.getKey().equals("b_sp"))
					{
						String tempString2=pair.getValue().toString();
						Matcher matcher = Pattern.compile("\\d+").matcher(tempString2);
						ArrayList<Integer> numbers = new ArrayList<>();
						while (matcher.find()) {
							numbers.add(Integer.valueOf(matcher.group()));
						}
						mapDimension.put("biases"+tempString, numbers);
					}
				} 
			}
		}while(iteratorObject.hasNext());
		/////////////////////////////////////////////Read Weights////////////////////////////////////////////////////////////////////////
		obj = jsonParserObj.parse(new FileReader(path));
		jsonObject = (JSONObject) obj; 
		setKey =  jsonObject.keySet();
		iteratorObject = setKey.iterator();
		do{
			String tempString = iteratorObject.next().toString();
			if(tempString.matches(".*\\d.*"))
			{ 
				fileName=tempString;
				Map jsonArray = ((Map)jsonObject.get(tempString)); 
				Iterator<Map.Entry> itr1 = jsonArray.entrySet().iterator(); 
				while (itr1.hasNext()) { 
					Map.Entry pair = itr1.next(); 
					if(pair.getKey().equals("w_sp"))
					{
						String temp=pair.getValue().toString();
						Matcher matcher = Pattern.compile("\\d+").matcher(temp);
						ArrayList<Integer> numbers = new ArrayList<>();
						while (matcher.find()) {
							numbers.add(Integer.valueOf(matcher.group()));
						}
						mapDimension.put("weights"+tempString, numbers);
					}
				} 
			}
		}while(iteratorObject.hasNext());
	}

}