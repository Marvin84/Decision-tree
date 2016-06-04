from __future__ import division
from copy import copy
from trainTree import *
from program import *
from functools import reduce
import collections
import math



#calculates the estimation error in percent
def get_percent_totalError(error, k, m):
 totalError = 0
 for index in range(len(error)):
  totalError += error[index]
 totalError /= k
 percent = (totalError/m)*100
 return percent


#get the number of elements initialized True in a list
def get_True_values (l):
 c = 0
 for item in l:
  if item == True:
   c += 1
 return c


#initialize a dictionary with attributes as keys
def create_dic():
 newDic = {}
 for i in range(len(attList)):
   newDic[attList[i]] = []
 return newDic


#returns a dictionary from a list of tuples
def convert_to_dic (l):
 newDic = create_dic()
 for i in range(len(attList)):
  for t in range(len(l)):
   newDic[attList[i]].append(l[t][i])
 return newDic


#return the range of test index
def get_test_range(k, n, m):
  start = (int)((k+1)*m)
  end = (int)((n+k*m)%n)
  if start < end:
   return range(start,end)
  else:
   return range(end,start)


#creates a dictionary of lists of path to class labels with {label:list of paths}
def create_paths(dictionary):
 pathDic = {}
 path =[]
 result=[]
 def get_keys(d, target):
  for k, v in d.iteritems():
   path.append(k)
   if isinstance(v, dict):
    get_keys(v, target)
   if v == target:
    result.append(copy(path))
   path.pop()
 for i in range(len(classLabel)):
  get_keys(dictionary, classLabel[i])
  pathDic[classLabel[i]] = result
  result = []
 return pathDic

#takes a path and a tuple of the dataset and if find the values of the path in a tuple
#verify if the class is the same. returns 'None' if it dosen't find it, True if the label
#is the same and False otherwise
def verify(aPath, aTestTuple, count,label):
 while count < len(aPath):
  if aTestTuple[attList.index(aPath[count])] != aPath[count+1]:
   return 'None'
  else:
   count+=2
 if aTestTuple[-1] == label:
    return True
 else:
   return False

#calculates the estimated error
def calculate_error(attList, dataTuple, dataSet, k):
 n = len(dataTuple)
 m = n/k
 error = [0 for x in range(k)]
 for i in range(k):
  #
  #the i-th test dataset
  #
  testTuple = []
  testDic = {}
  for j in get_test_range(i, n, m):
   testTuple.append(dataTuple[j])
  testDic = convert_to_dic(testTuple)
  #
  #the i-th train set
  #
  trainTuple = []
  trainDic = {}
  for l in range(n):
   if l not in get_test_range(i, n, m):
    trainTuple.append(dataTuple[l])
  trainDic = convert_to_dic(trainTuple)
  trainDTree = DTLearn(attList, trainDic, trainTuple, None, None, impurityChoice)
  trainPaths = create_paths(trainDTree)
  #verifies the numbers of tuple in test with a different label in train
  #and updates the kth element of error list
  testIndexVerify = [False for x in range(len(testTuple))]
  for item in classLabel:
   subsetTrainPaths = trainPaths[item]
   for p in subsetTrainPaths:
    for t in testTuple:
     ind = testTuple.index(t)
     value = verify(p, t, 0, item)
     if value == False:
      testIndexVerify[ind] = True
  error[i] = get_True_values(testIndexVerify)
  return get_percent_totalError(error, k, m)



if __name__ == '__main__':

 datas = read_file()
 attList = datas[0]
 dataTuple = datas[1]
 dataSet = datas[2]
 classLabel = unrepeated_val_list(dataSet['classes'])
 error = calculate_error(attList, dataTuple, dataSet, k=5)
 print 'The estimated classifier error is ' + repr(error) + ' %'

