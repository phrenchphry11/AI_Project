'''
Holly French and Alexandra Price
Functions to make and display decision trees, and compute accuracy.

The titanic dataset takes a long time due to calculating accuracy with loocv.
Also this requires having Graphviz installed. Also, not sure this works on Windows.
'''
import sys, math, heapq, os
from scipy.stats import chi2
from treeClass import *


def parseFile(fileName):
    '''
    Reads in the tab-delimited dataset into a list of lists.
    '''
    dataFile = open(fileName)
    data = []
    for line in dataFile:
        line = line.strip()
        line = line.split('\t')
        data.append(line)
    dataFile.close()
    return data

def splitData(data):
    '''
    Takes a list of lists, representing a portion of the data.
    Assumes the first item in the data is the names of all the attributes.

    Creates a dictionary of the following form:
    {attr1:[[value1, numYes, numNo][value2, numYes, numNo]],
    attr2: [[value2, numYes, numNo][value4, numYes, numNo]],
    etc}
    '''
    categoryDict = {}
    firstLine = data[0]
    rest = data[1:]
    for row in rest:
        for i in range(len(row) - 1):
            category = firstLine[i]
            attributeFound = False
            if category not in categoryDict:
                categoryDict[category] = []
            for attribute in categoryDict[category]:
                if row[i] == attribute[0]:
                    if row[-1] == 'yes':
                        attribute[1] += 1
                    if row[-1] == 'no':
                        attribute[2] += 1
                    attributeFound = True
                    break
            if not attributeFound:
                if row[-1] == 'yes':
                    categoryDict[category].append([row[i], 1, 0])
                if row[-1] == 'no':
                    categoryDict[category].append([row[i], 0, 1])
    return categoryDict

def chiSquare(categoryDict):
    entropyHeap = []
    totalYes = 0
    totalNo = 0
    delta = 0
    someCategory = categoryDict.keys()[0]
    for attribute in categoryDict[someCategory]:
        totalYes += attribute[1]
        totalNo += attribute[2] 

    for category in categoryDict:
        remainder = 0
        curCategory = categoryDict[category]
        for attribute in curCategory:
            numYes = attribute[1]
            numNo = attribute[2]
            probYes = numYes/float(numYes + numNo)
            probNo = numNo/float(numYes + numNo)
            numYes_hat = totalYes*(numYes + numNo)/(totalYes + totalNo)
            numNo_hat = totalNo*(numYes + numNo)/(totalYes + totalNo)
            if numNo_hat == 0:
                numNo_hat = 0.00000000000000001
            if numYes_hat == 0:
                numYes_hat = 0.0000000000000001
            delta += ((numNo - numNo_hat)**2/numNo_hat) + ((numYes-numYes_hat)**2/numYes_hat)

        df = totalYes + totalNo - 1
        pval = 1 - chi2.cdf(delta, df)
        heapq.heappush(entropyHeap, [pval, category]) #we do 1-gain because heapq makes a min heap
    return entropyHeap

def entropy(q):
    '''
    Calculates entropy for a given boolean event occuring with probability q.
    '''
    if q == 1 or q == 0:
        return 0
    else:
        e = -1 * (q * math.log(q, 2) + (1-q) * math.log((1 - q), 2))
        return e

def calculateEntropy(categoryDict):
    '''
    Takes a dictionary of the form produced by splitData.
    Creates a heap orderded by information gain 
    (popping gives you the item with highest gain).
    Calls the entropy(q) function.
    '''
    entropyHeap = []

    totalYes = 0
    totalNo = 0
    someCategory = categoryDict.keys()[0]
    for attribute in categoryDict[someCategory]:
        totalYes += attribute[1]
        totalNo += attribute[2] 

    for category in categoryDict:
        remainder = 0
        curCategory = categoryDict[category]
        for attribute in curCategory:
            numYes = attribute[1]
            numNo = attribute[2]
            probYes = numYes/float(numYes + numNo)
            probNo = numNo/float(numYes + numNo)
            e = entropy(probYes)
            remainder += e * (numYes + numNo)/float(totalYes + totalNo)

        gain = entropy(totalYes/float(totalYes+totalNo)) - remainder
        heapq.heappush(entropyHeap, [1 - gain, category]) #we do 1-gain because heapq makes a min heap
    return entropyHeap


def makeTree(fullData):
    '''
    Given a training set (fullData) this makes a DecisionTree object.
    Follows the ID3 algorithm.
    Calls the recursive makeTreeHelper.
    '''
    dataDict = splitData(fullData)
    entropyHeap = calculateEntropy(dataDict)
    tree = DecisionTree()
    splitVal = heapq.heappop(entropyHeap) #contains the attribute to split on

    #get the root node
    rootNode = Node()
    rootNode.setName(splitVal[1])
    tree.setRoot(rootNode)
    numYes = 0
    numNo = 0
    for j in dataDict[splitVal[1]]:
        numYes += j[1]
        numNo += j[2]

    if numYes == 0:
        rootNode.setOutcome("NO")
        return tree
    if numNo == 0:
        rootNode.setOutcome("YES")
        return tree

    makeTreeHelper(tree.getRoot(), fullData, dataDict[rootNode.getName()])
    return tree


def makeTreeHelper(rootNode, examples, parentExamples):
    '''
    Recursive helper function for makeTree.
    Closely follows the algorithm as laid out in the textbook.
    '''
    if len(examples) == 1: #we are out of examples
        parentNumYes = 0
        parentNumNo = 0
        childNode = Node()
        childNode.setParent(rootNode)
        rootNode.addChild(childNode)
        childNode.setValue(rootNode.getValue())
        for row in parentExamples:
            parentNumYes += row[1]
            parentNumNo += row[2]
        if parentNumYes > parentNumNo: #pick most common
            childNode.setOutcome("YES")
        else:
            childNode.setOutcome("NO")
    else:
        dataDict = splitData(examples)
        entropyHeap = calculateEntropy(dataDict)
        splitVal = heapq.heappop(entropyHeap) #attribute to split on
        rootNode.setName(splitVal[1])

        for value in dataDict[splitVal[1]]:
            childNode = Node()
            childNode.setParent(rootNode)
            rootNode.addChild(childNode)
            childNode.setValue(value[0])
            childNode.setName("Outcome") #will be reset by children if not a leaf node

            numYes = value[1]
            numNo = value[2]
            if numYes == 0:
                childNode.setOutcome("NO")
            elif numNo == 0:
                childNode.setOutcome("YES")

            elif entropyHeap == []: #we are out of attributes to split on
                if numYes > numNo: #pick most common outcome
                    childNode.setOutcome("YES")
                else:
                    childNode.setOutcome("NO")

            else:
                #now we remove the attribute we split on from the data
                categoryIndex = examples[0].index(splitVal[1])
                newExamples = [examples[0][:categoryIndex]+examples[0][(categoryIndex+1)%len(examples[0]):]]
                for e in examples:
                    if e[categoryIndex] == childNode.getValue():
                        newE = e[:categoryIndex]+e[categoryIndex+1 % len(e):]
                        newExamples.append(newE)
                parentExamples = dataDict[splitVal[1]]
                makeTreeHelper(childNode, newExamples, parentExamples)
    return
                
def looCV(dataSet):
    '''
    Leave one out cross validation.
    Takes a data set, returns the accuracy of the 
    decisionTree, made using ID3.
    '''
    numCorrect = 0
    numItems = len(dataSet) - 1
    for i in range(1,len(dataSet)):
        testItem = dataSet.pop(i) #the data point we will try to classify
        testTree = makeTree(dataSet)

        #make a dictionary in order to pair the categories and values for the data point
        itemDict = {}
        categories = dataSet[0]
        for i in range(len(categories) - 1):
            itemDict[categories[i]] = testItem[i]

        outcome = testTree.search(itemDict)
        if not outcome: #there was no branch in the decision tree for the specified data point
            numItems -= 1

        elif outcome.lower() == testItem[-1]:
            numCorrect += 1
        dataSet.insert(i, testItem)
    accuracy = numCorrect/float(numItems)
    return accuracy
                    
                
def main():
    fileName = sys.argv[1]
    parsedFile = parseFile(fileName)
    treeTimes = makeTree(parsedFile)
    treeTimes.makeGraphViz(looCV(parsedFile))
    os.system("dot -Tpdf tree.dot -o tree.pdf")
    os.system("open tree.pdf")
    
main()
    
    
