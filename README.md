



# NEUROSPF: A Tool For the Symbolic Analysis of Neural Networks

# Section I - Instructions on installing JPF and SPF
SPF needs JPF-Core to work, so it is essential that JPF-Core is installed first. 

## Instructions on installing JPF-Core
JPF-Core is also provided as part of this repository. JPF-Core can be downloaded from [https://github.com/javapathfinder/jpf-core](https://github.com/javapathfinder/jpf-core). 
Detailed instructions are provided at the aforementioned repository. 

## Instructions on installing SPF
The following subsection gives the instructions on installing SPF. These instructions are taken from the original SPF GitHub Repository. [https://github.com/SymbolicPathFinder/jpf-symbc](https://github.com/SymbolicPathFinder/jpf-symbc)

---------------------------------------------
### Symbolic (Java) PathFinder:

This JPF extension provides symbolic execution for Java bytecode. It performs a non-standard interpretation of byte-codes. It allows symbolic execution on methods with arguments of basic types (int, long, double, boolean, etc.). It also supports symbolic strings, arrays, and user-defined data structures.

SPF now has a "symcrete" mode that executes paths triggered by concrete inputs and collects constraints along the paths

A paper describing Symbolic PathFinder appeared at ISSTA'08:

Title: Combining Unit-level Symbolic Execution and System-level Concrete Execution for Testing NASA Software, Authors: C. S. Pasareanu, P. C. Mehlitz, D. H. Bushnell, K. Gundy-Burlet, M. Lowry, S. Person, M. Pape. (DOI: https://dl.acm.org/doi/10.1145/1390630.1390635)

#### [](https://github.com/SymbolicPathFinder/jpf-symbc#getting-started)Getting Started

First of all please use Java 8 (I am afraid our tools do not work with older versions of Java).

Then please download jpf-core from here:  [https://github.com/yannicnoller/jpf-core/tree/0f2f2901cd0ae9833145c38fee57be03da90a64f](https://github.com/yannicnoller/jpf-core/tree/0f2f2901cd0ae9833145c38fee57be03da90a64f)

And jpf-symbc from here:  [https://github.com/SymbolicPathFinder/jpf-symbc](https://github.com/SymbolicPathFinder/jpf-symbc)

Import them in Eclipse as 2 Java projects. Also create a .jpf dir in your home directory and create in it a file called "site.properties" with the following content:

```
jpf-core = <path-to-jpf-core-folder>/jpf-core

jpf-symbc = <path-to-jpf-core-folder>/jpf-symbc

extensions=${jpf-core},${jpf-symbc}
```

You can then try to run some examples by selecting a .jpf file from the "examples" directory and then selecting a run configuration from the "Run" menu in Eclipse. In particular you should select: "run-JPF-symbc" to run Symbolic PathFinder on your example (configuration "run-JPF-symbc-mac" is tailored for Mac).

Good luck!

**Additional Steps:** 
-	json-simple.jar, located in the lib folder https://github.com/muhammadusman93/neurospf/blob/main/jpf-symbc/lib/json_simple.jar, should be added to the build path. 
---------------------------------------------
# Section II: Instructions on running NEUROSPF
Command to run the Keras to Java Translator
```
python translator/java-dnn-gen.py --model kerasmodels/<kerasmodel>.h5 --outputs "<path to jpf-symbc>/jpf-symbc/src/examples/neurospf" -d <image file>
```

Sample Command to run the demo example. 
```
python translator/java-dnn-gen.py --model kerasmodels/mnist-lowquality.h5 --outputs "<path to jpf-symbc>/jpf-symbc/src/examples/neurospf" -d demoimage
```

The above command will generate the required code files inside jpf-symbc/src/examples/neurospf directory. User can run the SPF-DNN.jpf file using jpf-symbc to generate adversarial images

---------------------------------------------

# Section III: Link to Demonstration Video
 https://youtu.be/seal8fG78LI
  
---------------------------------------------
# Section IV: Neural Network Architectures
### MNIST-LowQuality

DNN architecture is as follows. 

        Layer (type)                 Output Shape              Param #   
        =================================================================
        conv2d_1 (Conv2D)            (None, 26, 26, 2)         20        
        _________________________________________________________________
        activation_1 (Activation)    (None, 26, 26, 2)         0         
        _________________________________________________________________
        conv2d_2 (Conv2D)            (None, 24, 24, 4)         76        
        _________________________________________________________________
        activation_2 (Activation)    (None, 24, 24, 4)         0         
        _________________________________________________________________
        max_pooling2d_1 (MaxPooling2 (None, 12, 12, 4)         0         
        _________________________________________________________________
        flatten_1 (Flatten)          (None, 576)               0         
        _________________________________________________________________
        dense_1 (Dense)              (None, 128)               73856     
        _________________________________________________________________
        activation_3 (Activation)    (None, 128)               0         
        _________________________________________________________________
        dense_2 (Dense)              (None, 10)                1290      
        _________________________________________________________________
        activation_4 (Activation)    (None, 10)                0         
        =================================================================
        Total params: 75,242
        Trainable params: 75,242
        Non-trainable params: 0

### MNIST-HighQuality

DNN architecture is as follows. 

        Layer (type)                 Output Shape              Param #
        =================================================================
        conv2d_1 (Conv2D)            (None, 26, 26, 8)         80
        _________________________________________________________________
        max_pooling2d_1 (MaxPooling2 (None, 13, 13, 8)         0
        _________________________________________________________________
        conv2d_2 (Conv2D)            (None, 11, 11, 16)        1168
        _________________________________________________________________
        max_pooling2d_2 (MaxPooling2 (None, 5, 5, 16)          0
        _________________________________________________________________
        flatten_1 (Flatten)          (None, 400)               0
        _________________________________________________________________
        dense_1 (Dense)              (None, 100)               40100
        _________________________________________________________________
        dense_2 (Dense)              (None, 10)                1010
        =================================================================
        Total params: 42,358
        Trainable params: 42,358
        Non-trainable params: 0

### CIFAR10

DNN architecture is as follows. 

	Layer (type)                 Output Shape              Param #
	=================================================================
	conv2d_1 (Conv2D)            (None, 30, 30, 32)        896
	_________________________________________________________________
	activation_1 (Activation)    (None, 30, 30, 32)        0
	_________________________________________________________________
	conv2d_2 (Conv2D)            (None, 28, 28, 32)        9248
	_________________________________________________________________
	activation_2 (Activation)    (None, 28, 28, 32)        0
	_________________________________________________________________
	max_pooling2d_1 (MaxPooling2 (None, 14, 14, 32)        0
	_________________________________________________________________
	conv2d_3 (Conv2D)            (None, 12, 12, 64)        18496
	_________________________________________________________________
	activation_3 (Activation)    (None, 12, 12, 64)        0
	_________________________________________________________________
	conv2d_4 (Conv2D)            (None, 10, 10, 64)        36928
	_________________________________________________________________
	activation_4 (Activation)    (None, 10, 10, 64)        0
	_________________________________________________________________
	max_pooling2d_2 (MaxPooling2 (None, 5, 5, 64)          0
	_________________________________________________________________
	flatten_1 (Flatten)          (None, 1600)              0
	_________________________________________________________________
	dense_1 (Dense)              (None, 512)               819712
	_________________________________________________________________
	activation_5 (Activation)    (None, 512)               0
	_________________________________________________________________
	dense_2 (Dense)              (None, 10)                5130
	_________________________________________________________________
	activation_6 (Activation)    (None, 10)                0
	=================================================================
	Total params: 890,410
	Trainable params: 890,410
	Non-trainable params: 0

---------------------------------------------

# Maintainers
* Muhammad Usman (muhammadusman@utexas.edu)

---------------------------------------------

# License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/muhammadusman93/neurospf/blob/main/LICENSE) file for details
