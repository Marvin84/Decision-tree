# decision-tree
Tina Raissi
24/01/2016

---------------------------
Project Structure

1.trainTree.py
2.impFactory.py
3.5fold.py
4.Readme.txt


-----------------------------
Launching information

My project is compatible with Python 2.7.
All the files (also datasets) must be in one directory.
For using one of the datasets it is necessary to fill out the relative field in the read_file() function in trainTree.py.
By launching trainTree.py it will be created automatically a file named program.py which will support the execution of 5fold.py. Program.py will contain also the printed tree in nested dictionary verison. The TrainTree.py prints also the simple tree version of the decision tree.
The impFactory.py contains the Factory pattern used for the choice of Impurity Function.
