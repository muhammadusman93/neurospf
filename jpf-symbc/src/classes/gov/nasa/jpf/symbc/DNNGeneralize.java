package gov.nasa.jpf.symbc;

//Methods to read the internal values of the DNN on the SPF side.
//needs to be generalized

public class DNNGeneralize {
	native public static int get_data_dimension_value(String name, int index);
	native public static int get_data_dimensions(String name);
	native public static double get_data_value1(String name,int index0);
	native public static double get_data_value2(String name,int index0,int index1);
	native public static double get_data_value4(String name,int index0,int index1,int index2,int index3);
	native public static void readDataFromFiles(String path,String jsonpath);
	public static Object get_data(String name) {
		// TODO Auto-generated method stub
		int dimension=get_data_dimensions(name);
		if(dimension==1)
		{
			int dim1=get_data_dimension_value(name,0);
			double []data=new double[dim1];
			for(int i=0;i<dim1;i++)
			{
				data[i]=get_data_value1(name,i);
			}
			return data;
		}
		else if (dimension==2)
		{
			int dim1=get_data_dimension_value(name,0);
			int dim2=get_data_dimension_value(name,1);
			double [][]data=new double[dim1][dim2];
			for(int i=0;i<dim1;i++)
			{
				for(int j=0;j<dim2;j++)
				{
					data[i][j]=get_data_value2(name,i,j);
				}
			}
			return data;
		}
		else if (dimension==4)
		{
			int dim1=get_data_dimension_value(name,0);
			int dim2=get_data_dimension_value(name,1);
			int dim3=get_data_dimension_value(name,2);
			int dim4=get_data_dimension_value(name,3);
			double [][][][]data=new double[dim1][dim2][dim3][dim4];
			for(int i=0;i<dim1;i++)
			{
				for(int j=0;j<dim2;j++)
				{
					for(int k=0;k<dim3;k++)
					{
						for(int l=0;l<dim4;l++)
						{
							data[i][j][k][l]=get_data_value4(name,i,j,k,l);		
						}
					}
				}
			}
			return data;
		}
		return null;
	}
}
