import math

#the abstract class
class Impurity(object):

 @staticmethod
 def factory(choice):
  if choice == 'entropy':
   return Entropy()
  elif choice == 'missclassification':
   return MissClassification()
  else:
    raise ValueError('Unknown choice %c for factory' % choice)

 #Calculates the cost of choice associated to the received probability list
 #If this method is called on the abstract class it will raise an NotImplementedError exception,
 #you need to use the factory method to obtain a concrete subclass for the chosen algorithm
 def calculateCost(self, probList):

    raise NotImplementedError("Class Impurity doesn't implement calculateCost()")




#Implementation of the Impurity calculation by using the Entropy method
class Entropy(Impurity):

 def calculateCost(self, probList):
  entropyVal = 0
  for i in range(len(probList)):
   entropyVal += -(probList[i]*math.log(probList[i]))
  return entropyVal

#Implementation of the Impurity calculation by using the MissClassification method
class MissClassification(Impurity):


 def calculateCost(self, probList):
  classification = []
  for i in range(len(probList)):
   classification.append(1 - probList[i])
  return max(classification)

