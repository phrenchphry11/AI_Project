import random

def makeSyllableDict(wordList):
	syllDict = {}
	for wordTup in wordList:
		numSyll = wordTup[1]
		if numSyll in syllDict:
			syllDict[numSyll].append(wordTup[0])
		else:
			syllDict[numSyll] = [wordTup[0]]
	return syllDict

def makePOSDict(fileName):
	wordFile = open(fileName)
	POSDict = {}
	for line in wordFile:
		line = line.strip()
		line = line.split()
		word = line[0]
		POS = line[1]
		numSyll = int(line[-1])
		for part in POS:
			if numSyll <= 7:
				if part in POSDict:
					POSDict[part].append((word, numSyll))
				else:
					POSDict[part] = [(word, numSyll)]
	for POS in POSDict:
		wordList = POSDict[POS]
		syllDict = makeSyllableDict(wordList)
		POSDict[POS] = syllDict
	return POSDict


def getNextWord(POS, POSDict, remainingSyll):
	if POS == "N" or POS == "p" or POS == "r":
		legalPOS = ["V", "t", "i", "v", "C", "!"]
	elif POS == "V" or POS == "t" or POS == "i":
		legalPOS = ["v", "N", "p", "A", "C", "P", "!", "P", "r"]
	elif POS == "A":
		legalPOS = ["N", "r", "!", "C"]
	elif POS == "v":
		legalPOS = ["r", "V", "t", "i", "!"]
	elif POS == "C":
		legalPOS = ["N", "p", "r", "A", "v", "V", "t", "i", "!"]
	elif POS == "o":
		legalPOS = ["V"]
	elif POS == "P":
		legalPOS = ["N", "p", "r","A", "!"]
	else:
		legalPOS = ["N", "p", "V", "t", "i", "A", "v", "C", "P", "!", "r"]
	newPOS = random.choice(legalPOS)
	numSyll = random.randint(1, remainingSyll)
	try:
		next = random.choice(POSDict[newPOS][numSyll])
	except KeyError:
		numSyll = random.randint(1, remainingSyll)
		while numSyll not in POSDict[newPOS]:
			numSyll = random.randint(1, remainingSyll)
		next = random.choice(POSDict[newPOS][numSyll])

	return next, numSyll, newPOS


def makeRandomLine(numberSyllables, POSDict):
	line = ""
	randKey = random.choice(POSDict.keys())
	randNumSyll = random.choice(POSDict[randKey].keys())
	while randNumSyll > numberSyllables:
		randNumSyll = random.choice(POSDict[randKey].keys())
	startWord = random.choice(POSDict[randKey][randNumSyll])
	line += startWord + " "
	syllablesRemaining = numberSyllables - randNumSyll
	POS = randKey
	while syllablesRemaining > 0:
		next, numSyll, nextPOS = getNextWord(POS, POSDict, syllablesRemaining)
		line += next + " "
		POS = nextPOS
		syllablesRemaining -= numSyll
	return line

def makeRandomHaiku(POSDict):
	line1 = makeRandomLine(5, POSDict)
	line2 = makeRandomLine(7, POSDict)
	line3 = makeRandomLine(5, POSDict)
	haiku = line1 + '\n' + line2 + '\n' + line3
	return haiku

def makeRandomHaikus(POSDict, numHaikus, fileName):
	haikuDB = open(fileName, "w")
	for i in range(numHaikus):
		haiku = makeRandomHaiku(POSDict)
		haikuDB.write(str(i) + "\t" + haiku + "\n")
	haikuDB.close()
			

def main():
	POS = makePOSDict('wordDict.txt')
	makeRandomHaikus(POS, 100, "haikuDB")

main()


