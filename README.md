# Multidimensional knapsack problem using Linear Programing
### A simple CPLEX python code for solving the Multidimensional knapsack problem
the problem is described below:
http://people.brunel.ac.uk/~mastjjb/jeb/orlib/mknapinfo.html
_____________________________________________________
## Tests
the tests are at: 
http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/
and they are the files below: 
mknap1.txt, mknap2.txt, mknapcb1.txt ate mknapcb9.txt

*this code only supports the files mknapcb1,mknapcb2,...,mknapcb9

## Pre-requisites & Installing
- make sure you have IBM ILOG installed in your machine and the python interface for CPLEX.
https://www.ibm.com/products/ilog-cplex-optimization-studio
https://www.ibm.com/support/knowledgecenter/SSSA5P_12.8.0/ilog.odms.cplex.help/CPLEX/GettingStarted/topics/set_up/Python_setup.html

- Python3
- clone this repo
## Running
```python solver.py [test_name]```


- It will generate a file called test_name_sol.txt in the same directory of the test file.



 
