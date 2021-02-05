package gov.nasa.jpf.symbc;

import java.io.FileNotFoundException;

import gov.nasa.jpf.annotation.MJI;
import gov.nasa.jpf.symbc.numeric.PathCondition;
import gov.nasa.jpf.vm.MJIEnv;
import gov.nasa.jpf.vm.NativePeer;

public class JPF_gov_nasa_jpf_symbc_DNNGeneralize extends NativePeer {
	@MJI
	public static int get_data_dimension_value(MJIEnv env, int objRef, int stringRef,int index) {
		String name = env.getStringObject(stringRef);
		return DNNDataGeneralize.subDimensionMap.get(name).get(index);
	}
	@MJI
	public static int get_data_dimensions(MJIEnv env, int objRef, int stringRef) {
		String name = env.getStringObject(stringRef);
		return DNNDataGeneralize.mainDimensionMap.get(name);
	}
	@MJI
	public static double get_data_value1(MJIEnv env, int objRef, int stringRef,int index0) {
		String name = env.getStringObject(stringRef);
		return ((double[])DNNDataGeneralize.dataMap.get(name))[index0];
	}
	@MJI
	public static double get_data_value2(MJIEnv env, int objRef, int stringRef,int index0, int index1) {
		String name = env.getStringObject(stringRef);
		return ((double[][])DNNDataGeneralize.dataMap.get(name))[index0][index1];
	}
	@MJI
	public static double get_data_value4(MJIEnv env, int objRef, int stringRef,int index0,int index1,int index2,int index3) {
		String name = env.getStringObject(stringRef);
		return ((double[][][][])DNNDataGeneralize.dataMap.get(name))[index0][index1][index2][index3];
	}
	@MJI
	public static void readDataFromFiles(MJIEnv env, int objRef, int pathRef,int jsonRef) throws FileNotFoundException, Exception {

		String path = env.getStringObject(pathRef);
		String jsonpath = env.getStringObject(jsonRef);
		System.out.println("Reading from ..."+path);
		DNNDataGeneralize.readDataFromFiles(path,jsonpath);
	}
}