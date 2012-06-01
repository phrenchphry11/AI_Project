'''
This will generate a table file for unclassified haiku
please add whatever interesting stuff you want!
'''

def parseHaiku(fileName):
	'''
	Should, given a haikuDB file, return a dictionary with ids as keys and the poems as values.
	Felt like it might be easier to deal with in this format.
	'''
	haikuFile = open(fileName)
	haikuDict = {}
	haiku = ""
	curId = 0
	for line in haikuFile:
		line = line.strip()
		if not line[0].isalpha():
			#we're at the first line of the haiku
			line = line.split("\t")
			ID = int(line[0])
			curId = ID
			haiku = line[1]
			assert ID not in haikuDict
			haikuDict[ID] = haiku
		else:
			haiku += "\n" + line
			haikuDict[curId] = haiku
	return haikuDict

def makeDictionary(dictFilename):
	wordFile = open(dictFilename)
	dictionaryDict = {}
	for line in wordFile:
		line = line.strip()
		line = line.split()
		word = line[0]
		pos = line[1] #this will ne a string will all the pos markers for this word
		syllables = int(line[2])
		dictionaryDict[word] = (pos, syllables)
	return dictionaryDict


def getNumPOS(haiku, POS, dictionaryDict):
	haiku = haiku.split() #split the haiku into words
	posCount = 0
	for word in haiku:
		if POS in dictionaryDict[word][0]:
			posCount +=1
	return posCount

def getAvgSyll(haiku, dictionaryDict):
	haiku = haiku.split() #split the haiku into words
	totalSyll = 0
	for word in haiku:
		totalSyll += dictionaryDict[word][1]
	avg = int(round(totalSyll/float(len(haiku))))
	return avg

def getAvgWordLength(haiku):
	haiku = haiku.split()
	wordLengths = 0
	for word in haiku:
		wordLengths += len(word)
	avg = int(round(float(wordLengths/len(haiku))))
	return avg

def makeTableFile(haikuDict, dictionaryDict):
	tableFile = open("haikuTable.txt", "w")
	line1 = "nouns \t verbs \t adjectives \t av. syllables \t av. word length"
	print >>tableFile, line1
	for ID in haikuDict:
		haiku = haikuDict[ID]
		numNouns = str(getNumPOS(haiku, "N", dictionaryDict))
		numVerbs = str(getNumPOS(haiku, "V", dictionaryDict))
		numAdj = str(getNumPOS(haiku, "A", dictionaryDict))
		numSyll = str(getAvgSyll(haiku, dictionaryDict))
		wordLen = str(getAvgWordLength(haiku))
		newLine = numNouns + "\t" + numVerbs + "\t" + numAdj + "\t" + numSyll + "\t" + wordLen
		print >>tableFile, newLine
	tableFile.close()

def main():
	haikuDict = parseHaiku("haikuDB")
	wordDict = makeDictionary("wordDict.txt")
	makeTableFile(haikuDict, wordDict)

main()



