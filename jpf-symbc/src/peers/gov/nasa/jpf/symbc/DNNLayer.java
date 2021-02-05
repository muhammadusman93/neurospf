package gov.nasa.jpf.symbc;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
public abstract class DNNLayer {
	public abstract void printData();
	public abstract void readData(String path,String name);	
	public abstract Object getData();
	public abstract ArrayList<Integer> getSubDimension();
}
