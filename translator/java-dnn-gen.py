
import argparse
import sys
import codecs
import re
from pathlib import Path
import keras
from keras.models import *
from keras.layers import *
from keras import *
from utils import *
import os
import numpy
import json
from keras.applications.vgg16 import VGG16
def unescaped_str(arg_str):
    return codecs.decode(str(arg_str), 'unicode_escape')
jmodel = {} # json

##  DNN ==> JAVA
def java_convert(model, path='',pathtospf='',img='',demo=''):

  ## to store weights amd bias parameters
  if not os.path.exists(path+'params'):
    os.makedirs(path+'params')
  
  consts=''
  prog=''

  ##  input, we assume that channel is in behind
  input_shape=model.layers[0].input.shape
  print ('####', input_shape)
  ###  uint8_t 'input[channel][row][column]'
  fc = False
  try:
    channel=input_shape[3].value
    row=input_shape[1].value
    column=input_shape[2].value
  except: 
      fc = True

  if not fc:
    prog+='  // the DNN input is of shap {0}x{1}x{2}\n'.format(row, column, channel)
    prog+='  int run(double[][][] input)\n'.format(row, column, channel)
  else:
    prog+='  int run(double[] input)\n'.format(input_shape[1].value)
  prog+='  {\n'

  iw=0 ## index of weights layer

  ##  Assumption: kernel is a box shape and stride is 1
  ##  Assumption: convolutional layer is of type '2d'
  ##  Assumption: channel is put behind
  for l in range(0, len(model.layers)):
    jlayer = {} # json
    layer=model.layers[l]
    name=layer.name
    jlayer['name'] = name # json
    _inp=layer.input
    _out=layer.output
    jlayer['inp_sp'] = _inp.shape.as_list() # json
    jlayer['out_sp'] = _out.shape.as_list() # json
    is_conv=is_conv_layer(layer)
    jlayer['is_conv'] = is_conv # json
    if is_conv:
      is_padding = (layer.padding == 'same')
      jlayer['is_padding'] = is_padding # json
    is_dense=is_dense_layer(layer)
    jlayer['is_dense'] = is_dense # json
    is_activation=is_activation_layer(layer)
    jlayer['is_activation'] = is_activation # json
    is_maxpooling=is_maxpooling_layer(layer)
    jlayer['is_maxpooling'] = is_maxpooling # json
    is_flatten=is_flatten_layer(layer)
    jlayer['is_flatten'] = is_flatten # json
    #is_dropout=False ##   we do not allow dropout
    #activation=''
    is_relu=False
    if is_conv or is_dense or is_activation: #activation=layer.activation
      is_relu=((get_activation(layer)).find('relu')>=0) ##  (not is_relu) ==> is_linear
    jlayer['is_relu'] = is_relu # json


    prog+='\n    //  layer {0}: {1}\n'.format(l, name)


    weights=[]
    biases=[]
    if is_dense or is_conv:
      params=layer.get_weights()
      weights= params[0]
      biases= params[1]

      print (l, weights)
      sp=weights.shape
      jlayer['w_sp'] = sp # json
      jlayer['b_sp'] = biases.shape # json
      if is_conv:
        consts+='  // weights{0}: shape is {1}x{2}x{3}x{4}\n'.format(l, sp[0], sp[1], sp[2], sp[3])
        #fw = open('./data/weights{0}.txt'.format(l), 'a')
        weights_rs=weights.reshape((sp[0]*sp[1]*sp[2], sp[3]))
        numpy.savetxt(path+'params/weights{0}.txt'.format(l), weights_rs, fmt='%.18f', delimiter=',')
      else:
        consts+='  // weights{0}: shape is {1}\n'.format(l, sp[0])
        numpy.savetxt(path+'params/weights{0}.txt'.format(l), weights, fmt='%.18f', delimiter=',')

      ## biases
      consts+='  // biases{0}: shape is {1}\n'.format(l, len(biases))
      numpy.savetxt(path+'params/biases{0}.txt'.format(l), biases, fmt='%.18f')

    if is_conv:
      prog+='    double[][][] layer{3}=new double[{0}][{1}][{2}];\n'.format(_out.shape[1].value, _out.shape[2].value, _out.shape[3].value, l)
      kernel_size=layer.kernel_size ##  Assumption: kernels are of box shape with stride 1
      jlayer['kernel_size'] = kernel_size # json
      if is_padding:
        prog+='    for(int i=0; i<{0}; i++)\n'.format(_out.shape[1].value-kernel_size[0]+1)
        prog+='      for(int j=0; j<{0}; j++)\n'.format(_out.shape[2].value-kernel_size[1]+1)
      else:
        prog+='    for(int i=0; i<{0}; i++)\n'.format(_out.shape[1].value)
        prog+='      for(int j=0; j<{0}; j++)\n'.format(_out.shape[2].value)
      prog+='        for(int k=0; k<{0}; k++)\n'.format(_out.shape[3].value)
      prog+='        {\n'
      prog+='          layer{0}[i][j][k]=internal.biases{0}[k];\n'.format(l)
      prog+='          for(int I=0; I<{0}; I++)\n'.format(kernel_size[0])
      prog+='            for(int J=0; J<{0}; J++)\n'.format(kernel_size[1])
      prog+='              for(int K=0; K<{0}; K++)\n'.format(weights.shape[2])
      if l==0:
        prog+='                layer{0}[i][j][k]+=internal.weights{0}[I][J][K][k]*input[i+I][j+J][K];\n'.format(l)
      else:
        prog+='                layer{0}[i][j][k]+=internal.weights{0}[I][J][K][k]*layer{1}[i+I][j+J][K];\n'.format(l,l-1)
    
      if is_relu:
        prog+='          if (layer{0}[i][j][k]<0) layer{0}[i][j][k] = 0; // relu\n'.format(l)

      prog+='        }\n'
    elif is_dense:
      prog+='    double[] layer{1}=new double[{0}];\n'.format(_out.shape[1].value, l)
      prog+='    for(int i=0; i<{0}; i++)\n'.format(weights.shape[1])
      prog+='    {\n'
      prog+='      layer{0}[i]=internal.biases{0}[i];\n'.format(l)
      prog+='      for(int I=0; I<{0}; I++)\n'.format(weights.shape[0])
      if l==0:
        prog+='        layer{0}[i]+=internal.weights{0}[I][i]*input[I];\n'.format(l)
      else:
        prog+='        layer{0}[i]+=internal.weights{0}[I][i]*layer{1}[I];\n'.format(l,l-1)

      if is_relu:
        prog+='      if (layer{0}[i]<0) layer{0}[i] = 0; // relu\n'.format(l)

      prog+='    }\n'
    elif is_flatten:
      s=_inp.shape[1].value * _inp.shape[2].value * _inp.shape[3].value
      prog+='    double[] layer{1}=new double[{0}];\n'.format(s, l)
      prog+='    for(int i=0; i<{0}; i++)\n'.format(s)
      prog+='    {\n'
      prog+='      int d0=i/{0};\n'.format(_inp.shape[2].value * _inp.shape[3].value)
      prog+='      int d1=(i%{0})/{1};\n'.format(_inp.shape[2].value * _inp.shape[3].value, _inp.shape[3].value)
      prog+='      int d2=i-d0*{0}-d1*{1};\n'.format((_inp.shape[2].value * _inp.shape[3].value), _inp.shape[3].value)
      if l>0:
        prog+='      layer{0}[i]=layer{1}[d0][d1][d2];\n'.format(l,l-1)
      else:
        prog+='      layer{0}[i]=input[d0][d1][d2];\n'.format(l,l-1)
      prog+='    }\n'
    elif is_maxpooling:
      pool_size=layer.pool_size ##  Assumption: maxpooling is of box shape with stride 1
      jlayer['pool_size'] = pool_size # json
      prog+='    double[][][] layer{3}=new double[{0}][{1}][{2}];\n'.format(_out.shape[1].value, _out.shape[2].value, _out.shape[3].value, l)
      prog+='    for(int i=0; i<{0}; i++)\n'.format(_out.shape[1].value)
      prog+='      for(int j=0; j<{0}; j++)\n'.format(_out.shape[2].value)
      prog+='        for(int k=0; k<{0}; k++)\n'.format(_out.shape[3].value)
      prog+='        {\n'
      prog+='          layer{0}[i][j][k]=0;\n'.format(l)
      prog+='          for(int I=i*{0}; I<(i+1)*{0}; I++)\n'.format(pool_size[0])
      prog+='            for(int J=j*{0}; J<(j+1)*{0}; J++)\n'.format(pool_size[1])
      prog+='              if(layer{0}[I][J][k]>layer{1}[i][j][k]) layer{1}[i][j][k]=layer{0}[I][J][k];\n'.format(l-1,l)
      prog+='        }\n'

    elif is_activation:
       if is_relu:
         if len(_out.shape.as_list())>2: ## conv
           prog+='    double[][][] layer{3}=new double[{0}][{1}][{2}];\n'.format(_out.shape[1].value, _out.shape[2].value, _out.shape[3].value, l)
           prog+='    for(int i=0; i<{0}; i++)\n'.format(_out.shape[1].value)
           prog+='      for(int j=0; j<{0}; j++)\n'.format(_out.shape[2].value)
           prog+='        for(int k=0; k<{0}; k++)\n'.format(_out.shape[3].value)
           prog+='          if(layer{0}[i][j][k]>0) layer{1}[i][j][k]=layer{0}[i][j][k];\n'.format(l-1,l)
           prog+='          else layer{1}[i][j][k]=0;\n'.format(l-1,l)
         else:
           prog+='    double[] layer{0}=new double[{1}];\n'.format(l, _out.shape[1].value)
           prog+='    for(int i=0; i<{0}; i++)\n'.format(_out.shape[1].value)
           prog+='          if(layer{0}[i]>0) layer{1}[i]=layer{0}[i];\n'.format(l-1,l)
           prog+='          else layer{0}[i]=0;\n'.format(l)
       else:
           if not l==len(model.layers)-1:
             print ('Unrecpgnizable DNN structure...layer {0}'.format(l))
             print (model.layers[l])
             sys.exit(0)
           else:
             prog+='    double[] layer{0}=new double[{1}];\n'.format(l, _out.shape[1].value)
             prog+='    for(int i=0; i<{0}; i++)\n'.format(_out.shape[1].value)
             prog+='          layer{1}[i]=layer{0}[i]; // alala\n'.format(l-1,l)

    jmodel[l] = jlayer
    if l==len(model.layers)-1: ## TODO
      prog+='    int ret=0;\n'
      prog+='    double res=-100000;\n'
      prog+='    for(int i=0; i<{0};i++)\n'.format(_out.shape[1].value)
      prog+='    {\n'
      #prog+='      if(layer{0}[i]>res)\n'.format(l-1)
      prog+='      if(layer{0}[i]>res)\n'.format(l)
      prog+='      {\n'
      #prog+='        res=layer{0}[i];\n'.format(l)
      prog+='        res=layer{0}[i];\n'.format(l)
      prog+='        ret=i;\n'
      prog+='      }\n'
      prog+='    }\n'
      prog+='    return ret;\n'
      prog+='  }\n'

  dnn_class='package neurospf;\n'
  dnn_class+='public class DNNt\n'
  dnn_class+='{\n'
  dnn_class+='\n'
  dnn_class+='  private InternalData internal;\n'
  dnn_class+='\n'
  dnn_class+=consts
  dnn_class+='\n'
  dnn_class+='  public DNNt(InternalData internal) {\n'
  dnn_class+='    this.internal = internal;\n'
  dnn_class+='  }\n'
  dnn_class+='\n'
  dnn_class+=prog
  dnn_class+='\n'
  dnn_class+='\n'
  dnn_class+='}\n'


  dnn_file = open(path+'DNNt.java', 'w')
  dnn_file.write(dnn_class)
  dnn_file.close()


  ## To generate internal data
  idata = "package neurospf;\n"
  idata += "import java.io.*;\n"
  idata += "public class InternalData {\n"
  convs = []
  denses = []
  union = []
  for l in range(0, len(model.layers)):
    layer=model.layers[l]
    name=layer.name
    _inp=layer.input
    _out=layer.output
    is_conv=is_conv_layer(layer)
    is_dense=is_dense_layer(layer)
    if is_conv: 
        convs.append(l)
        union.append(l)
    if is_dense: 
        denses.append(l)
        union.append(l)

  parameters = ""

  jmodel["union"] = union
  jmodel["nlayers"] = len(model.layers)
  for i in union:
    if i in convs:
        idata += "  public double[][][][] weights{0};\n".format(i)
        if not (parameters == ""):
          parameters += ','
        parameters += "String weights{0}file".format(i)
    if i in denses:
        idata += "  public double[][] weights{0};\n".format(i)
        if not (parameters == ""):
          parameters += ','
        parameters += "String weights{0}file".format(i)
  for i in union:
    if i in convs:
        idata += "  public double[] biases{0};\n".format(i)
        parameters += ','
        parameters += "String bias{0}file".format(i)
    if i in denses:
        idata += "  public double[] biases{0};\n".format(i)
        parameters += ','
        parameters += "String bias{0}file".format(i)

  #for i in convs:
  #    idata += "  public double[][][][] weights{0};\n".format(i)
  #    if not (parameters == ""):
  #      parameters += ','
  #    parameters += "String weights{0}file".format(i)
  #for i in denses:
  #    idata += "  public double[][] weights{0};\n".format(i)
  #    if not (parameters == ""):
  #      parameters += ','
  #    parameters += "String weights{0}file".format(i)
  #for i in convs:
  #    idata += "  public double[] biases{0};\n".format(i)
  #    parameters += ','
  #    parameters += "String bias{0}file".format(i)
  #for i in denses:
  #    idata += "  public double[] biases{0};\n".format(i)
  #    parameters += ','
  #    parameters += "String bias{0}file".format(i)

  idata += "\n"
  idata += "  public InternalData("+ parameters + ") throws NumberFormatException, IOException {\n"

  idata += "\n"
  idata += "    String path = \"./params/\";"
  idata += "\n"
  idata += "    int index = 0;\n"
  idata += "    double[] Wvalues = null;\n"
  idata += "    double[] Bvalues = null;\n"
  idata += "    File file = null;\n"
  idata += "    BufferedReader br = null;\n"
  idata += "    String st = null;\n"

  for i in union:
      idata += "\n"
      idata += "    file = new File(path + weights{0}file);\n".format(i)
      idata += "    br = new BufferedReader(new FileReader(file));\n"
      #idata += "    st;\n"
      params = model.layers[i].get_weights()
      weights = params[0]
      biases = params[1]
      if i in convs:
          sp = weights.shape
          print (i, sp, model.layers[i])
          idata += "    Wvalues = new double[{0}];\n".format(sp[0]*sp[1]*sp[2]*sp[3])
      elif i in denses:
          sp = weights.shape
          print (i, sp, model.layers[i])
          idata += "    Wvalues = new double[{0}];\n".format(sp[0]*sp[1])
      idata += "    index = 0;\n"
      idata += "    while ((st = br.readLine()) != null) {\n"
      idata += "      if (st.isEmpty()) continue;\n"
      idata += "      String[] vals = st.split(\",\");\n"
      if i in convs:
        for j in range(0, sp[3]):
          idata += "        Wvalues[index] = Double.valueOf(vals[{0}]);\n".format(j)
          idata += "        index++;\n"
      elif i in denses:
          idata += "        for (int i = 0; i < {0}; i++) ".format(sp[1])
          idata += "{\n"
          idata += "          Wvalues[index] = Double.valueOf(vals[i]);\n"
          idata += "          index ++;\n"
          idata += "        }\n"
      idata += "    }\n"
      idata += "    br.close();\n"
      idata += "    file = new File(path + bias{0}file);\n".format(i)
      idata += "    br = new BufferedReader(new FileReader(file));\n"
      if i in convs:
        idata += "    Bvalues = new double[{0}];\n".format(sp[3])
      elif i in denses:
        idata += "    Bvalues = new double[{0}];\n".format(sp[1])
      idata += "    index = 0;\n"
      idata += "    while ((st = br.readLine()) != null) {\n"
      idata += "      if (st.isEmpty()) continue;\n"
      idata += "      Bvalues[index] = Double.valueOf(st);\n"
      idata += "      index++;\n"
      idata += "    }\n"

      if i in convs:
        idata += "    biases{0} = new double[{1}];\n".format(i, sp[3])
        idata += "    index = 0;\n"
        idata += "    for (int k = 0; k < {0}; k++) ".format(sp[3])
        idata += "{\n"
        idata += "      biases{0}[k] = Bvalues[index];\n".format(i)
        idata += "      index++;\n"
        idata += "    }\n"

        idata += "    weights{0} = new double[{1}][{2}][{3}][{4}];\n".format(i, sp[0], sp[1], sp[2], sp[3])
        idata += "    index = 0;\n"
        idata += "    for (int I = 0; I < {0}; I++)\n".format(sp[0])
        idata += "      for (int J = 0; J < {0}; J++)\n".format(sp[1])
        idata += "        for (int K = 0; K < {0}; K++)\n".format(sp[2])
        idata += "          for (int k = 0; k < {0}; k++)\n".format(sp[3])
        idata += "          {\n"
        idata += "            weights{0}[I][J][K][k] = Wvalues[index];\n".format(i)
        idata += "            index++;\n".format(i)
        idata += "          }\n"
        idata += "    br.close();\n"
      elif i in denses:
        idata += "    biases{0} = new double[{1}];\n".format(i, sp[1])
        idata += "    index = 0;\n"
        idata += "    for (int k = 0; k < {0}; k++) ".format(sp[1])
        idata += "{\n"
        idata += "      biases{0}[k] = Bvalues[index];\n".format(i)
        idata += "      index++;\n"
        idata += "    }\n"

        idata += "    weights{0} = new double[{1}][{2}];\n".format(i, sp[0], sp[1])
        idata += "    index = 0;\n"
        idata += "    for (int I = 0; I < {0}; I++)\n".format(sp[0])
        idata += "      for (int J = 0; J < {0}; J++)\n".format(sp[1])
        idata += "          {\n"
        idata += "            weights{0}[I][J] = Wvalues[index];\n".format(i)
        idata += "            index++;\n"
        idata += "          }\n"
        idata += "    br.close();\n"



      idata += "\n"



  idata += "  }\n"
  idata +="public InternalData() {}\n"
  # The end of internal data
  idata += "}"

  test_file = open(path+'InternalData.java', 'w')
  test_file.write(idata)
  test_file.close()
  configdata=""
  configdata += "target=neurospf.SymbolicDriver\n"
  configdata += "classpath=${jpf-symbc}/build/examples/\n"
  configdata += "sourcepath=${jpf-symbc}/src/examples/\n"
  configdata += "symbolic.min_double=0.0\n"
  configdata += "symbolic.max_double=255.0\n"
  configdata += "symbolic.dp=z3\n"
 
  test_file = open(path+'SPF-DNN.jpf', 'w')
  test_file.write(configdata)
  test_file.close()

  symbolicdata=""
  symbolicdata += "package neurospf;\n"
  symbolicdata += "import java.io.BufferedReader;\n"
  symbolicdata += "import java.io.File;\n"
  symbolicdata += "import java.io.FileReader;\n"
  symbolicdata += "import gov.nasa.jpf.symbc.Debug;\n"
  symbolicdata += "import gov.nasa.jpf.symbc.DNN;\n"
  symbolicdata += "import gov.nasa.jpf.symbc.DNNDataGeneralize;\n"
  symbolicdata += "import gov.nasa.jpf.symbc.DNNGeneralize;\n"
  symbolicdata += "public class SymbolicDriver {\n"
  symbolicdata += "    public static String path="+"\""+str(pathtospf)+"\";\n"
  symbolicdata += "    static final int IMG_HEIGHT = 28;\n"
  symbolicdata += "    static final int IMG_WIDTH = 28; \n"
  symbolicdata += "    public static void main(String[] args) throws  Exception {\n"
  symbolicdata += "        final long startTime = System.currentTimeMillis();\n"
  symbolicdata += "        String inputFile = path+\"inputs\\"+"\\"+img+"\";\n"
  symbolicdata += "        File file = new File(inputFile); \n"
  symbolicdata += "        BufferedReader br = new BufferedReader(new FileReader(file)); \n"
  symbolicdata += "        double[][][] a = new double[IMG_HEIGHT][IMG_WIDTH][1];\n"
  symbolicdata += "        String st;\n"
  symbolicdata += "       while ((st = br.readLine()) != null) {\n"
  symbolicdata += "            String[] values = st.split(\",\");\n"
  symbolicdata += "            int index = 0;\n"
  symbolicdata += "            while (index < values.length) {\n"
  symbolicdata += "                for (int i = 0; i <  IMG_HEIGHT; i++)\n"
  symbolicdata += "                    for (int j = 0; j < IMG_WIDTH; j++)\n"
  symbolicdata += "                        for (int k = 0; k < 1; k++)\n"
  symbolicdata += "                        {\n"
  symbolicdata += "                            Double val = Double.valueOf(values[index]);\n"
  symbolicdata += "                            index++;\n"
  symbolicdata += "                            a[i][j][k] = (double)(val);\n"
  if(demo=="1"):
      symbolicdata += "                            if(i==15 && j==15)\n"
      symbolicdata += "                             {\n"
      symbolicdata += "                             System.out.println(\"original value \"+i+j+k+\" \"+a[i][j][k]);\n"
      symbolicdata += "                             a[i][j][k]=Debug.addSymbolicDouble(a[i][j][k],\"sym_\"+i+\"_\"+j+\"_\"+k);\n"
      symbolicdata += "                             System.out.println(\""+"created sym_\"+i+\"_\"+j+\"_\"+k)\n;"
      symbolicdata += "                             }\n"
      symbolicdata += "                        }\n"
  symbolicdata += "            }\n"
  symbolicdata += "        }\n"
  symbolicdata += "            InternalData internaldata = new InternalData();    \n"
  symbolicdata += "            DNNt model=new DNNt(internaldata);\n"
  symbolicdata += "            DNNGeneralize.readDataFromFiles(path+\"params"+"\\"+"\\"+"\""+",path+\"dnn.json\");\n"
  for i in union:
    if i in convs:
        symbolicdata += "  internaldata.biases{0} = (double[]) DNNGeneralize.get_data(\"biases{0}\");\n".format(i)
        parameters += ','
        parameters += "String bias{0}file".format(i)
    if i in denses:
        symbolicdata += "  internaldata.biases{0} = (double[]) DNNGeneralize.get_data(\"biases{0}\");\n".format(i)
        parameters += ','
        parameters += "String bias{0}file".format(i)
  for i in union:
    if i in convs:
        symbolicdata += "  internaldata.weights{0} = (double[][][][]) DNNGeneralize.get_data(\"weights{0}\");\n".format(i)
        if not (parameters == ""):
          parameters += ','
        parameters += "String weights{0}file".format(i)
    if i in denses:
        symbolicdata += "  internaldata.weights{0} = (double[][]) DNNGeneralize.get_data(\"weights{0}\");\n".format(i)
        if not (parameters == ""):
          parameters += ','
        parameters += "String weights{0}file".format(i)
  
  symbolicdata += "            int label = model.run(a);\n"
  symbolicdata += "            System.out.println(\""+"MODEL OUTPUT:\""+" + label);\n"
  if(demo=="1"):
      symbolicdata += "            if(label!=8) {\n"
      symbolicdata += "    	            Debug.getSolvedPC();\n"
      symbolicdata += "    	            System.out.println(\""+"solutions \"+\n"
    #  symbolicdata += "    	            Debug.getSymbolicRealValue(a[10][10][0])+\n"
      symbolicdata += "    	            Debug.getSymbolicRealValue(a[15][15][0])\n"
    #  symbolicdata += "    	            Debug.getSymbolicRealValue(a[20][20][0])\n"
      symbolicdata += "    	);\n"
      symbolicdata += "    	final long endTime = System.currentTimeMillis();\n"
      symbolicdata += "	    System.out.println(\""+"Total execution time (seconds): \"" +"+ (endTime - startTime)/1000);\n"
  symbolicdata += "     }\n"
  symbolicdata += "    }\n"
  symbolicdata += "}\n"

  test_file = open(path+'SymbolicDriver.java', 'w')
  test_file.write(symbolicdata)
  test_file.close()

  test_file = open(path+'SymbolicDriver.java', 'w')
  test_file.write(symbolicdata)
  test_file.close()
#  print("Hello"+path)
def main():
  parser=argparse.ArgumentParser(
          description='To convert a DNN model to JAVA program' )

  parser.add_argument('--model', action='store', nargs='+', default = 'None', help='The input neural network model (.h5)')
  parser.add_argument("--vgg16-model", dest='vgg16', help="vgg16 model", action="store_true")
  parser.add_argument("--outputs", dest="outs", default="outs",
                    help="the output directory", metavar="DIR")
  parser.add_argument("-d", "--img", help="test")
  
  args=parser.parse_args()
  if args.vgg16:
      model = VGG16()
  else:
      model = load_model(args.model[0])
  model.summary()
  path = args.outs
  if not path[-1] == '/': path += '/'
  if not os.path.exists(path):
    os.system('mkdir -p {0}'.format(path))
  if args.img:
    java_convert(model, path,str(path).replace('/','\\\\'),args.img,"1")
  else:
    java_convert(model, path,str(path).replace('/','\\\\'),args.img,"0")
  
  with open(path+'dnn.json', 'w') as outfile:
    json.dump(jmodel, outfile)

  #isl=model.layers[0].input.shape.as_list() ## input shape list
  #write_harness(isl)
  #print(args.img)
if __name__=="__main__":
  main()
