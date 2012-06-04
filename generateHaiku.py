import random
import re
from syllableCount import *

def makeSyllableDict(wordList):
	"""efficient way to mark syllables"""
	syllDict = {}
	for wordTup in wordList:
		numSyll = wordTup[1]
		if numSyll in syllDict:
			syllDict[numSyll].append(wordTup[0])
		else:
			syllDict[numSyll] = [wordTup[0]]
	return syllDict

def makePOSDict(fileName):
	"""Helps us efficiently parse parts of speech"""
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
	"""get next word based on part of speech"""
	if POS == "N" or POS == "r":
		legalPOS = ["V", "t", "i", "v", "C", "!"]
	elif POS == "V" or POS == "t" or POS == "i":
		legalPOS = ["v", "N", "A", "C", "P", "!", "P", "r"]
	elif POS == "A":
		legalPOS = ["N", "r", "!", "C"]
	elif POS == "v":
		legalPOS = ["r", "V", "t", "i", "!"]
	elif POS == "C":
		legalPOS = ["N", "r", "A", "v", "V", "t", "i", "!"]
	elif POS == "o":
		legalPOS = ["V"]
	elif POS == "P":
		legalPOS = ["N", "r","A", "!"]
	else:
		legalPOS = ["N", "V", "t", "i", "A", "v", "C", "P", "!", "r"]
	random.shuffle(legalPOS)
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
	"""sub method for generating random poems"""
	line = ""
	keys = POSDict.keys()
	random.shuffle(keys)
	randKey = random.choice(keys)
	randNumSyll = random.choice(POSDict[randKey].keys())
	while randNumSyll > numberSyllables:
		randNumSyll = random.choice(POSDict[randKey].keys())
	words = POSDict[randKey][randNumSyll]
	random.shuffle(words)
	startWord = random.choice(words)
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
	"""makes a random haiku from common poetry words"""
	line1 = makeRandomLine(5, POSDict)
	line2 = makeRandomLine(7, POSDict)
	line3 = makeRandomLine(5, POSDict)
	haiku = line1 + '\n' + line2 + '\n' + line3
	return haiku

def makeRandomHaikuFromCorpus(corpus):
	"""generates haikus from Pride and Prejudice"""
	corpus = open(corpus)
	words = []
	for line in corpus:
		line = line.strip()
		line = re.split("\W", line)
		for word in line:
			if word != "":
				words.append(word)
	line1 = ""
	remainingSyllables = 5
	while remainingSyllables > 0:
		randWord = random.choice(words)
		numSyllables = get_syllables(randWord) 
		line1 += randWord + " "
		remainingSyllables -= numSyllables
		if remainingSyllables > 0:
			nextWordIndex = words.index(randWord) + 1
			line1 += words[nextWordIndex] + " "
			remainingSyllables -= get_syllables(words[nextWordIndex])

	line2 = ""
	remainingSyllables = 7
	while remainingSyllables > 0:
		randWord = random.choice(words)
		numSyllables = get_syllables(randWord) 
		line2 += randWord + " "
		remainingSyllables -= numSyllables
		if remainingSyllables > 0:
			nextWordIndex = words.index(randWord) + 1
			line2 += words[nextWordIndex] + " "
			remainingSyllables -= get_syllables(words[nextWordIndex])

	line3 = ""
	remainingSyllables = 5
	while remainingSyllables > 0:
		randWord = random.choice(words)
		numSyllables = get_syllables(randWord) 
		line3 += randWord + " "
		remainingSyllables -= numSyllables
		if remainingSyllables > 0:
			nextWordIndex = words.index(randWord) + 1
			line3 += words[nextWordIndex] + " "
			remainingSyllables -= get_syllables(words[nextWordIndex])

	haiku = line1 + "\n" + line2 + "\n" + line3
	print haiku




def makeRandomHaikus(POSDict, numHaikus, fileName):
	haikuDB = open(fileName, "w")
	for i in range(numHaikus):
		haiku = makeRandomHaiku(POSDict)
		haikuDB.write(str(i) + "\t" + haiku + "\n")
	haikuDB.close()
			

def main():
	POS = makePOSDict('wordDict.txt')
	makeRandomHaiku(POS)
	#makeRandomHaikus(POS, 100, "haikuDB")
	makeRandomHaikuFromCorpus("prideprejudice.txt")

main()


