#  Created by Tina Raissi on 13/01/16.
# Copyright (c) 2016 Tina Raissi. All rights reserved.

from __future__ import division
from collections import Counter
from collections import defaultdict
from impFactory import Impurity
from impFactory import Entropy
from impFactory import MissClassification
import os
import csv
import math
import itertools
import operator
import cProfile
import pstats



'''
  -------> FILE PARSING & WRITING <--------
  
'''
def read_file():
 #create a set of tuples which contain the raws
 with open(os.path.dirname(os.path.abspath(__file__)) + '/grubdamage.csv') as file:
  datatuple=[tuple(line) for line in csv.reader(file)]
  attDataset = datatuple[0]
  datatupleNoAtt =[]
  #created the tuples without the first raw which contains the attributes
  for t in datatuple:
   datatupleNoAtt.append(t)
  del datatupleNoAtt[0]

 #creates a dictionary with 'key:values' where key is the attribute and value its relatives values
 with open(os.path.dirname(os.path.abspath(__file__)) + '/grubdamage.csv', 'r') as csvin:
  reader=csv.DictReader(csvin)
  datacoloumn={k:[v] for k,v in reader.next().items()}
  datadomain={k:[v] for k,v in reader.next().items()}
  for line in reader:
   for k,v in line.items():
    datacoloumn[k].append(v)
    if v not in datadomain[k]:
     datadomain[k].append(v)
 return (attDataset, datatupleNoAtt, datacoloumn )

#print the tree in form of nested dictionary in program.py and includes other informations
#for 5fold cross validation to be done in 5fold.py

def write_file(decisionTree, dataAtt, dataR, attributeV):
 file = open('program.py', 'w+')
 file.write('dTree='+repr(dTree))
 file.write('\n\n'+'impurityChoice='+repr(impurityChoice))
 file.write('\n\n'+'dataAttributes='+repr(dataAtt))
 file.write('\n\n'+'dataRaws='+repr(dataR))
 file.write('\n\n'+'attributeValues='+repr(attributeV))
 file.write('\n\n'+'def get_tree():')
 file.write('\n'+'\t'+'return dTree')
 file.write('\n\n'+'def get_choice():')
 file.write('\n'+'\t'+'return impurityChoice')


'''
  ------> GENERAL FUNCTIONS <--------
'''


#Eliminate the repeated values in a list
def unrepeated_val_list (list):
    unique = []
    for item in list:
     if item not in unique:
      unique.append(item)
    return unique

#take subset class and returns true if 80% of its elements is related to one class
def pre_prune (actualList):
 maxInfo = count_elements(actualList)
 maxList = maxInfo[0]
 maxInd = maxInfo[1]
 max = maxList[maxInd]
 percent = (max/len(actualList))*100
 if percent >= 100:
  return True



#take subset class and returns true if it is pure
def is_pure (list):
    
 if len(list)>len(set(list)):
  return False
 return True


#creates a new list without the given attributes
def create_removed_att_list (oldList, attribute):
 new = []
 for i in range(len(oldList)):
  if oldList[i] != attribute:
   new.append(oldList[i])
 return new


#update the new dic taking only the values of remained attributes
def create_removed_att_dic(attribute):
 new = datacoloumn.copy()
 del new[attribute]
 return new



#takes the attribute on which split the dataset and gives back a list of tuple extracted
#from a subset that contains only the attribute and the class
def get_subset(dataset, attList, index):
 actualAttList = attList[index]
 subsetValue = dataset.get(actualAttList)
 classList = dataset.get('classes')
 subset = zip(subsetValue,classList)
 return subset

#it sorts a list by the i-th value
def get_sorted (list,i):
    return sorted(list, key=lambda x: x[i])

#returns the best attribute using the gain information
def best(gainDictionay):
 return max(gainDictionay.iteritems(), key=operator.itemgetter(1))[0]



#creates a new dictionary with attributes like key and an empty list as value
def create_dic (attList):
 new = {}
 new.fromkeys(att_list, [])
 return new


#takes a list of values of an attribute and returns a new list with the number of counted elements
#and the index of the list given to unrepreated_val_list function
def count_elements(attList):
 i=0
 uniqueAtt = unrepeated_val_list(attList)
 counted =[0 for values in range(len(uniqueAtt))]
 for value in attList:
  counted[uniqueAtt.index(value)]+=1
 i=counted.index(max(counted))
 return (counted,i)


#gives the most common attribute
def most_common(l):
 uniqueList = unrepeated_val_list(l)
 index = count_elements(l)[1]
 return uniqueList[index]



#creates a new tuple without the ind-th element
def new_tuple(t, ind):
 l = []
 for i in range(len(t)):
  if i != ind:
   l.append(t[i])
 return tuple(l)



'''
 -------> MATH FUNCTIONS <------------
'''

#calculates the probability for every element in that list
def probability (attList):

 classAtt = count_elements(attList)[0]
 probabilities = [0 for values in range(len(classAtt))]
 for i in range(len(probabilities)):
  probabilities[i] = (classAtt[i])/(len(attList))
 return probabilities



'''
  -------> ALGORITHM FUNCTIONS <--------
'''

#gets in input the impurity measure of the parent node and sets a dictionary key:value
#with actual attributes as key and the gain measure as value for it
def gain (nodeAttList, nodeDataset, choice):
 ImpurityFunction = Impurity.factory(choice)
 parentImpurity = ImpurityFunction.calculateCost(probability(nodeDataset.get('classes')))
 nodeList = list(nodeAttList)
 gainDic= dict(zip(nodeList, '0'*len(nodeList)))
 for index in range(0,len(nodeList)):
  subset = get_sorted(get_subset(nodeDataset,nodeList,index), 0)
  impurityAfterSplit = 0
  for key,group in itertools.groupby(subset,operator.itemgetter(0)):
      attSubset=[]
      classSubset=[]
      groupSubset = list(group)
      for i in groupSubset:
       attSubset.append(i[0])
       classSubset.append(i[1])
      probList = probability(classSubset)
      impurityAfterSplit += (len(attSubset)/len(nodeDataset.get(nodeList[index])))*ImpurityFunction.calculateCost(probList)
  gainDic[nodeList[index]] = parentImpurity - impurityAfterSplit
 return gainDic



#print the tree
def printTree(d, indent=0):
 for key, value in d.iteritems():
  print '\t' * indent+ str(key)
  if isinstance(value, dict):
   printTree(value, indent+1)
  else:
   print '\t' * (indent+1) + str(value)


#creates the decisione tree
def DTLearn (attributes, nodeDataset, nodeDatatuple, parentDataset, parentDatatuple, choice):
 #it initialize the parent datasets of the root at first call
 if parentDataset == None:
  parentDataset = {}
 if parentDatatuple == None:
  parentDatatuple = []
 #
 #if the dataset or the attribute list is empty it returns the most common class of the parent node
 if len(nodeDataset) == 0:
  return most_common(parentDataset['classes'])
 #if the actual node dataset has a pure label returns it
 elif (pre_prune(nodeDataset['classes'])):
  return most_common(nodeDataset['classes'])
 #if empty attributes or with only classes it returns the most common value of the actual node
 elif (len(attributes)-1) <= 0:
  return most_common(nodeDataset['classes'])
 #created the tree
 else:
  #get attribute list without classes and copy the one with classes
  attWithClasses = list(attributes)
  attNoClasses = create_removed_att_list(attributes, 'classes')
  #initialize the best attribute and its index in the list of actual attributes to be tested
  bestAttribute = best(gain(attNoClasses, nodeDataset, choice))
  #print bestAttribute
  #get the values of this attribute in actual dataset
  values = sorted(unrepeated_val_list(nodeDataset[bestAttribute]))
  #print bestAttribute
  bestIndex = attributes.index(bestAttribute)
  #get the attribute list without the best
  updatedAttList = create_removed_att_list(attributes, bestAttribute)
  tree = {bestAttribute:{}}
  for val in values:
   datatupleSubset = []
   datasetSubset = {}
   for item in nodeDatatuple:
    if item[bestIndex] == val:
     datatupleSubset.append(new_tuple(item, bestIndex))
   for i in range(len(updatedAttList)):
    datasetSubset[updatedAttList[i]] = []
    for j in range(len(datatupleSubset)):
     datasetSubset[updatedAttList[i]].append(datatupleSubset[j][i])
   subTree = DTLearn(updatedAttList, datasetSubset, datatupleSubset, nodeDataset, nodeDatatuple, choice)
   tree[bestAttribute][val] = subTree
  return tree



if __name__ == '__main__':

 
 choice = input("enter 1 for missclassification and 2 for entropy\n")
 if (choice == 1 or choice == 2):
  if choice == 1:
   impurityChoice = 'missclassification'
  else:
   impurityChoice = 'entropy'
  datasets = read_file()
  dataAttributes = datasets[0]
  dataRaws = datasets[1]
  attributeValues = datasets[2]
  dTree = DTLearn(dataAttributes, attributeValues, dataRaws, None, None, impurityChoice)
  write_file(dTree, dataAttributes, dataRaws, attributeValues)
  printTree(dTree)
  cProfile.run('dTree = DTLearn(dataAttributes, attributeValues, dataRaws, None, None, impurityChoice)')
 else:
  print "invalid input, please try again..."











