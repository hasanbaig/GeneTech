![GeneTech Logo](https://github.com/hasanbaig/GeneTech/blob/master/GT-Logo.png)

### About GeneTech
GeneTech (extracted from **Gene**tic **Tech**nology mapping) is a tool which allows a user to generate genetic logic circuits only by specifying the logical function desired to be achieved in a living cell. It does not require a user (either biologist or a computer scientist) to learn any programming language. All what it requires a user to specify a desired logical function in the form of simple Boolean Algebra. 

The tool first performs logic optimization, followed by synthesis and technology mapping using a library of genetic logic gates. In the end, GeneTech performs technology mapping to generate all the feasible circuits, with different genetic gates, to achieve the desired logical behavior.  

GeneTech generates the circuits in the form of [SBOL data](https://sbolstandard.org/data/), [SBOL visual](https://sbolstandard.org/visual/) and Logic circuit schematic. 


### Platform
GeneTech is written in python 3.

Clone the up-to-date built from https://github.com/hasanbaig/GeneTech.git.

### Dependencies
You need to install the libraries in [requirements.txt](https://github.com/hasanbaig/GeneTech/blob/master/src/requirements.txt) to successfully run GeneTech. You can do it using the following command

``` pip3 install -r src/requirements.txt ```

Once installed, run the Genetech.py as follows:


``` python src/Genetech.py ```


### Current Contributors
1. Mudasir Hanif
2. Hasan Baig

### Past Contributors
1. Hasan Baig
2. Jan Madsen
3. Muhammad Ali Bhutto
4. Mukesh Kumar
5. Abdullah Siddiqui
6. Adil Ali Khan
