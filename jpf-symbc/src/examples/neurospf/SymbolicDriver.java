package neurospf;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import gov.nasa.jpf.symbc.Debug;
import gov.nasa.jpf.symbc.DNN;
import gov.nasa.jpf.symbc.DNNDataGeneralize;
import gov.nasa.jpf.symbc.DNNGeneralize;
public class SymbolicDriver {
    public static String path="C:\\Users\\Muhammad Usman\\eclipse-workspace\\jpf-symbc\\src\\examples\\neurospf\\";
    static final int IMG_HEIGHT = 28;
    static final int IMG_WIDTH = 28; 
    public static void main(String[] args) throws  Exception {
        final long startTime = System.currentTimeMillis();
        String inputFile = path+"inputs\\demoimage";
        File file = new File(inputFile); 
        BufferedReader br = new BufferedReader(new FileReader(file)); 
        double[][][] a = new double[IMG_HEIGHT][IMG_WIDTH][1];
        String st;
       while ((st = br.readLine()) != null) {
            String[] values = st.split(",");
            int index = 0;
            while (index < values.length) {
                for (int i = 0; i <  IMG_HEIGHT; i++)
                    for (int j = 0; j < IMG_WIDTH; j++)
                        for (int k = 0; k < 1; k++)
                        {
                            Double val = Double.valueOf(values[index]);
                            index++;
                            a[i][j][k] = (double)(val);
                            if(i==15 && j==15)
                             {
                             System.out.println("original value "+i+j+k+" "+a[i][j][k]);
                             a[i][j][k]=Debug.addSymbolicDouble(a[i][j][k],"sym_"+i+"_"+j+"_"+k);
                             System.out.println("created sym_"+i+"_"+j+"_"+k)
;                             }
                        }
            }
        }
            InternalData internaldata = new InternalData();    
            DNNt model=new DNNt(internaldata);
            DNNGeneralize.readDataFromFiles(path+"params\\",path+"dnn.json");
  internaldata.biases0 = (double[]) DNNGeneralize.get_data("biases0");
  internaldata.biases2 = (double[]) DNNGeneralize.get_data("biases2");
  internaldata.biases6 = (double[]) DNNGeneralize.get_data("biases6");
  internaldata.biases8 = (double[]) DNNGeneralize.get_data("biases8");
  internaldata.weights0 = (double[][][][]) DNNGeneralize.get_data("weights0");
  internaldata.weights2 = (double[][][][]) DNNGeneralize.get_data("weights2");
  internaldata.weights6 = (double[][]) DNNGeneralize.get_data("weights6");
  internaldata.weights8 = (double[][]) DNNGeneralize.get_data("weights8");
            int label = model.run(a);
            System.out.println("MODEL OUTPUT:" + label);
            if(label!=8) {
    	            Debug.getSolvedPC();
    	            System.out.println("solutions "+
    	            Debug.getSymbolicRealValue(a[15][15][0])
    	);
    	final long endTime = System.currentTimeMillis();
	    System.out.println("Total execution time (seconds): "+ (endTime - startTime)/1000);
     }
    }
}
