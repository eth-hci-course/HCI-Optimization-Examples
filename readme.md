This is a collection of optimization techniques used in HCI UI optimization. We mainly focused on discrete problems. 
We have random and exhaustive search for a 1D menu. An evolutionary algorithm for determining which webcam in a video
call should be shown. And a quadratic assignment problem solved through integer programming for keyboard optimization.
Each file has a function called: solve/solver or similar. This usually contains the core part of the algorithm. 

This repo is still a work in progress. Over time perhaps more solvers will be added and code will be improved. 

**This is not directly applicable to your projects. 
It is meant as inspiration and help for your own specific implementations.**

For a lot of these solvers you can probably find libraries who do most of the things for you:
- e.g. an advanced implementation of an evolutionary strategy: https://pypi.org/project/cma/

You can use those for your projects. This repo is more to give you an idea of how this all works. 

Maintainer: Thomas Langerak (first.last@inf.ethz.ch)




# OPTION 1: Installation with PyCharm
- Install Python 3.8
- Install Gurobi: https://www.gurobi.com/downloads/end-user-license-agreement-academic/
- Recommended IDE: https://www.jetbrains.com/pycharm/ (professional edition, this is free for students, https://www.jetbrains.com/community/education/#students)
- ```git clone git@github.com:eth-ait/HCI-Optimization-Examples.git```
- open it as project in pycharm
- create venv
- Install required packages: numpy, scipy, gurobipy, matplotlib
    
    ```pip install numpy```
    ```pip install scipy```
    ```pip install -i https://pypi.gurobi.com gurobipy```
    ```pip install matplotlib```
    
- it probably asks you to install juypter and run it
- In general to run it press any green arrow you see.


# OPTION 2: Installation with Jupyter Lab
- Install Python 3.8
- Open PowerShell in admin mode (or any other shell of your OS)
- Install jupyter lab: ```pip install jupyterlab``` https://jupyter.org/install
- Download the repo or ```git clone``` this repo and navigate in it using ```cd HCI-Optimization-Examples```
- Install required packages: numpy, scipy, gurobipy, matplotlib
    ```pip install numpy```
    ```pip install scipy```
    ```pip install -i https://pypi.gurobi.com gurobipy```
    ```pip install matplotlib```
- run the command ```jupyter-lab``` and, within the left panel, navigate to your cloned HCI-Optimization-Examples folder and open one of the ipynb example files
- then press the play button


