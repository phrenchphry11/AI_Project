'''
Holly French and Alexandra Price

This file contains the class for the decisionTree, 
as well as a class for the nodes that comprise it.
'''
from scipy import stats
import math, heapq
class DecisionTree:
    '''
    This class is essentially there in order to keep track
    of the root node of the tree and display the tree.
    '''
    def __init__(self):
        self.root = None

    def getRoot(self):
        return self.root
    
    def setRoot(self, root):
        self.root = root

    def getLeafNodes(self):
        nodeQueue = []
        nodeQueue.append(self.root)
        numCurLevel = 1
        numNextLevel = 0
        leaves = []
        while nodeQueue != []:
            tempNode = nodeQueue[0]
            numCurLevel -=1
            nodeQueue = nodeQueue[1:]
            if tempNode.getOutcome() == "yes" or tempNode.getOutcome() == "no":
                leaves.append(tempNode)
            tempNodeChildren = tempNode.getChildren()
            nodeQueue.extend(tempNodeChildren)
            numNextLevel +=len(tempNodeChildren)
            if numCurLevel == 0:
                numCurLevel = numNextLevel
                numNextLevel = 0
        return leaves


    def printTree(self):
        '''
        Prints the the tree out layer by layer, using BFS.
        mostly used for debugging.
        '''
        nodeQueue = []
        nodeQueue.append(self.root)
        numCurLevel = 1
        numNextLevel = 0
        while nodeQueue != []:
            tempNode = nodeQueue[0]
            numCurLevel -=1
            nodeQueue = nodeQueue[1:]
            print tempNode.getName(), tempNode.getValue(), tempNode.getOutcome(), '\t',
            tempNodeChildren = tempNode.getChildren()
            nodeQueue.extend(tempNodeChildren)
            numNextLevel +=len(tempNodeChildren)
            if numCurLevel == 0:
                print
                numCurLevel = numNextLevel
                numNextLevel = 0

    def contract(self):
        leaves = self.getLeafNodes()
        contracted = False
        while not contracted:
            contracted = True
            leafParents = []
            for leaf in leaves:
                parent = leaf.getParent()
                if parent not in leafParents:
                    leafParents.append(parent)
            for node in leafParents:
                children = node.getChildren()
                if len(children) == 2 and children[0].getOutcome() == children[1].getOutcome():
                    node.setName("Outcome")
                    node.setOutcome(children[0].getOutcome())
                    node.pruneChildren()
                    contracted = False

    def makeGraphViz(self, accuracy):
        '''
        Writes to a graphViz file, tree.dot
        In order to view the tree,
        run the following in the terminal:
        dot -Tpdf tree.dot -o tree.pdf
        This will create a pdf containing the tree,
        along with a label of its accuracy.
        '''
        s = "digraph G {"
        nodeQueue = []
        nodeQueue.append(self.root)
        while nodeQueue != []: #this is basically BFS
            tempNode = nodeQueue[0]
            if tempNode.getOutcome():
                tempLabel = str(tempNode)+' [label="'+ tempNode.getOutcome() + '"]; '
            else:
                tempLabel = str(tempNode)+' [label="'+ tempNode.getName() + '"]; '
            s+=tempLabel
            nodeQueue = nodeQueue[1:]
            for child in tempNode.getChildren():
                edgeName = '[label="'+str(child.getValue())+'"]'
                if child.getName() == "Outcome":
                    label  = str(child)+' [label="'+ child.getOutcome() + '"]; '
                    s+=label
                    s+= str(tempNode) + " -> " + str(child) + edgeName+"; "
                else:
                    label  = str(child)+' [label="'+ child.getName() + '"]; '
                    s+=label
                    s+= str(tempNode) + " -> " + str(child) + edgeName+ "; "

            tempNodeChildren = tempNode.getChildren()
            nodeQueue.extend(tempNodeChildren)
        s+='accuracy [penwidth="0",label="Accuracy is '+str(round(accuracy, 3))+'"];'
        s+="}"
        dotFile = open("tree.dot", "w")
        dotFile.write(s)
        dotFile.close()

    def search(self, itemDict):
        '''
        Searches for an outcome in the decisionTree, given a dictionary of attributes
        for a specific case in the following form:
        {attr1: value, attr2:value, etc}
        an example from the tennis dataset would be:
        {"outlook":"sunny", "temperature":"hot", etc}

        Returns the outcome ("YES" or "NO") of the case if there is a match,
        otherwise returns None.
        '''
        curNode = self.root
        if self.root.getOutcome():
            return self.root.getOutcome()
        else:
            while not curNode.getOutcome():
                curAttribute = curNode.getName()
                curValue = itemDict[curAttribute]
                children = curNode.getChildren()

                childfound = False
                for child in children:
                    if ">" in child.getValue():
                        val = child.getValue().split()[-1]
                        if int(curValue) > int(val):
                            curNode = child
                            childfound = True
                            break
                    elif "<" in child.getValue():
                        val = child.getValue().split()[-1]

                        if int(curValue) <= int(val):
                            curNode = child
                            childFound = True
                            break

            if not childfound:
                return None

            return curNode.getOutcome()

    def createConfidenceHeap(self, haikuDict):
        '''
        Prints the the tree out layer by layer, using BFS.
        mostly used for debugging.
        '''

        confidenceHeap = []
        nodeQueue = []
        nodeQueue.append(self.root)
        numCurLevel = 1
        numNextLevel = 0
        while nodeQueue != []:
            tempNode = nodeQueue[0]

            tempNode.setConfidence(haikuDict, self)
            upper, lower = tempNode.getConfidence()

            heapq.heappush(confidenceHeap, [lower, tempNode])

            numCurLevel -=1
            nodeQueue = nodeQueue[1:]
            print tempNode.getName(), tempNode.getValue(), tempNode.getOutcome(), '\t',
            tempNodeChildren = tempNode.getChildren()
            nodeQueue.extend(tempNodeChildren)
            numNextLevel +=len(tempNodeChildren)
            if numCurLevel == 0:
                print
                numCurLevel = numNextLevel
                numNextLevel = 0

        return confidenceHeap

    def isItemInNode(self, itemDict, node):
        '''
        Searches for an outcome in the decisionTree, given a dictionary of attributes
        for a specific case in the following form:
        {attr1: value, attr2:value, etc}
        an example from the tennis dataset would be:
        {"outlook":"sunny", "temperature":"hot", etc}

        Returns the outcome ("YES" or "NO") of the case if there is a match,
        otherwise returns None.
        '''
        curNode = self.root
        if curNode == node:
            return True
        else:
            while not curNode.getOutcome():
                curAttribute = curNode.getName()
                curValue = itemDict[curAttribute]
                children = curNode.getChildren()

                #childfound = False
                for child in children:
                    if ">" in child.getValue():
                        val = child.getValue().split()[-1]
                        if int(curValue) > int(val):
                            curNode = child
                            return True
                            break
                    elif "<" in child.getValue():
                        val = child.getValue().split()[-1]

                        if int(curValue) <= int(val):
                            curNode = child
                            return True
                            break
                    if curNode == node:
                        return True
            return False






class Node:
    '''
    This class is for the nodes within the decisionTree.
    It contains all the data associated with a node, 
    and its main purpose is to keep track of the parent and 
    child pointers.
    '''
    def __init__(self):
        self.outcome = None #if the node is a leaf, this will be "YES" or "NO"
        self.name = None #this is the attribute the node is splitting on
        self.value = None #this is the value of the parent attribute this node represents
        self.parent = None
        self.children = []
        self.numItems = 0
        self.numYes = 0
        self.numNo = 0
        #this represents the mean value of an attribute that appears in a given category
        #ie: if this is an adjective node, then meanFrequencies is valued at the average
        #number of adjectives a haiku contains that is in this node
        self.meanFrequencies = None 
        #95% confidence interval that meanFrequencies is the true mean.  
        #it is a tuple of (upperBound, lowerBound)
        self.confidence_interval = None
        #just keeps track of the total number of occurrences of an attr -> easier to calculate confidence with
        self.totalOverallAttr = 0

    def setMeanFrequencies(self, haikuDict):
        #this requires our dictionary of whatever values we have for our haikus
        #I'm not sure exactly how this is going to turn out, but I'm guessing this will be a table
        # containing the number of each attribute for each poem, and haikuDict will be the param for this

        #here I'm tracking the number of "yes" instances
        totalPosRating = 0
        totalOverallAttr = 0
        totalHaiku = 0
        for entry in haikuDict:
            totalHaiku += 1
            #again, i'm not sure if this is going to be a dictionary of dictionaries
            #though for now it is :p we're just checking if a given haiku has a positive rating
            numAttribute = entry[self.value]
            #then we get the value of the attribute (like there are 5 adjectives!)
            totalOverallAttr += numAttribute
            if entry["rating"] == "YES":
                totalPosRating += numAttribute
        self.meanFrequencies = totalPosRating / totalOverallAttr
        self.totalOverallAttr = totalOverallAttr

    def setNumItems(self, items):
        self.numItems = items

    def setNumYes(self, yess):
        self.numYes = yess

    def setNumNo(self, nos):
        self.numNo = nos

    def getNumItems(self):
        return self.numItems

    def getNumYes(self):
        return self.numYes

    def getNumNo(self):
        return self.numNo
    
    def getMeanFrequencies(self):
        return self.empirical_frequencies

    def getOutcome(self):
        return self.outcome

    def setOutcome(self, outcome):
        self.outcome = outcome

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def setParent(self, parent):
        self.parent = parent

    def getParent(self):
        return self.parent

    def addChild(self, child):
        self.children.append(child)

    def getChildren(self):
        return self.children

    def pruneChildren(self):
        self.children = []

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def setConfidence(self, haikuDict, tree):
        #very similar to the mean stuff.  maybe I could consolidate this into one function
        #but for the time being i'll keep it separate just for debugging
        totalPosRating = 0
        totalPosRatingSquared = 0
        numAttribute = 0
        for entry in haikuDict:
            if entry[-1] == "yes" or entry[-1] == "no":
                entryDict = {}
                for i in range(len(haikuDict[0]) - 1):
                    entryDict[haikuDict[0][i]] = entry[i]
                if tree.isItemInNode(entryDict, self):
                    if entry[-1] == "yes" or entry[-1] == "no":
                        i = haikuDict[0].index(self.name)
                        if entry[i] != "yes" and entry[i] != "no" and entry[i] != "None":
                            numAttribute = int(entry[i])
                        else:
                            numAttribute = 0
                    if entry[-1] == "yes":
                        totalPosRating += numAttribute
                        totalPosRatingSquared += numAttribute**2
                    self.totalOverallAttr += numAttribute
        if self.totalOverallAttr == 0:
            self.totalOverallAttr = 0.0000001
        self.meanFrequencies = totalPosRatingSquared / self.totalOverallAttr
        meanFrequenciesSquared = (totalPosRating / self.totalOverallAttr)**2
        sigma = math.sqrt(abs(self.meanFrequencies - meanFrequenciesSquared))

        #this is just a formula for 95% confidence interval.  1.96 was taking from a random
        #stats table in my stats book :p
        lowerBound = self.meanFrequencies - 1.96*sigma
        upperBound = self.meanFrequencies + 1.96*sigma

        #confidence interval is a tuple of upper and lower bound
        self.confidence_interval = (lowerBound, upperBound)

    def getConfidence(self):
        return self.confidence_interval




