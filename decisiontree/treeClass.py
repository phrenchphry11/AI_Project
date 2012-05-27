'''
Holly French and Alexandra Price

This file contains the class for the decisionTree, 
as well as a class for the nodes that comprise it.
'''


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
                edgeName = '[label="'+child.getValue()+'"]'
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
                    if child.getValue() == curValue:
                        curNode = child
                        childfound = True
                        break

                if not childfound:
                    return None

            return curNode.getOutcome()






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

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value