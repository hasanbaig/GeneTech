![Image of GeneTech](https://github.com/hasanbaig/GeneTech/blob/master/Logo1.png)

# About GeneTech
GeneTech (extracted from **Gene**tic **Tech**nology mapping) is a tool which allows a user to generate genetic logic circuits only by specifying the logical function desired to be achieved in a living cell. It performs Boolean optimization, followed by synthesis and technology mapping using a library of genetic logic gates. The genetic logic gates library used in this work has been developed and tested in the laboratory by MIT and Boston University [1]. GeneTech takes the Boolean expression of a genetic circuit as input, and then first optimize it. Afterwards, it synthesizes the optimized Boolean expression into NOR-NOT form in order to construct the circuit using the real NOR/NOT gates available in the genetic gates library [1]. In the end, GeneTech performs technology mapping to generate all the feasible circuits, with different genetic gates, to achieve the desired logical behavior.  

After performing all the operations to generate the possible circuits, it processes all the circuits one by one to generate their standard SBOL files, Logical Representation and SBOL Visual Representation,. It also allow users to save all the desired circuits and their representations as well, for future references or to be used in any other software.


### Platform
GeneTech is a combination of Java and Python.

Clone the up-to-date built from https://github.com/hasanbaig/GeneTech.git.

### Dependencies
You need to install the following libraries before running the GeneTech on your system.

* py4j
* SchemDraw
* pysbol
* pyqt5
* matplotlib
* Pillow
* dnaplotlib 

Once installed, run the Gateway.py file. 

### References
A. a K. Nielsen, B. S. Der, J. Shin, P. Vaidyanathan, V. Paralanov, E. a Strychalski, D. Ross, D. Densmore, and C. a. Voigt, “Genetic circuit design automation.,” Science, vol. 352, no. 6281, p. aac7341, 2016.
