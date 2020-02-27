![GeneTech Logo](https://github.com/hasanbaig/GeneTech/blob/master/GT-Logo.png)

### About GeneTech
GeneTech (extracted from **Gene**tic **Tech**nology mapping) is a tool which allows a user to generate genetic logic circuits only by specifying the logical function desired to be achieved in a living cell. It does not require a user (either biologist or a computer scientist) to learn any programming language. All what it requires a user to specify a desired logical function in the form of simple Boolean Algebra. 

The tool first performs logic optimization, followed by synthesis and technology mapping using a library of genetic logic gates. In the end, GeneTech performs technology mapping to generate all the feasible circuits, with different genetic gates, to achieve the desired logical behavior.  

GeneTech generates the circuits in the form of [SBOL data](https://sbolstandard.org/data/), [SBOL visual](https://sbolstandard.org/visual/) and Logic circuit schematic. 


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
