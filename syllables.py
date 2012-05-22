from BeautifulSoup import BeautifulSoup

import urllib

def makePoetrySet(fileName):
	wordFile = open(filename)
	poetrySet = []
	for line in wordFile:
		line = line.strip()
		poetrySet.append(line)
	poetrySet = set([])
	return poetrySet


def makeSyllableFile(fileName, poetrySet):
	wordFile = open(fileName)
	newFile = open('wordDict.txt', 'w')
	for line in wordFile:
		line = line.strip()
		line = line.split("\\")
		pos = line[-1]
		word = line[:-1]
		if word in poetrySet:
			sCount = get_syllables(word)
			wStr = ''
			for w in word:
				wStr += w + " "
			newLine = str(word[0]) + '\t' + pos + '\t' + str(sCount) + '\n'
			print >>newFile, newLine
	wordFile.close()
	newFile.close()

def make_syllables(fileName):
	wordFile = open(fileName)
	newFile = open('verbDict.txt', 'w')

	for line in wordFile:
		line = line.strip()
		line = line.split()
		word = line[0]
		sCount = get_syllables(word)
		newLine = str(word) + '\t' + str(sCount) + '\n'
		print >> newFile, newLine

	wordFile.close()
	newFile.close()


def get_syllables(word):
	url = 'http://www.wordcalc.com/index.php'

	post_data = urllib.urlencode(
	   {'text': word})
	post_data = '%s&optionSyllableCount&optionWordCount' % post_data


	cnxn = urllib.urlopen(url, post_data)
	response = cnxn.read()
	cnxn.close()

	soup = BeautifulSoup(response)
	h3_matches = [h3 for h3 in soup.findAll('h3') if h3.text == 'Statistics']
	if len(h3_matches) != 1:
	 raise Exception('Wrong number of <h3>Statistics</h3>')
	h3_match = h3_matches[0]
	table = h3_match.findNextSibling('table')

	td_matches = [td for td in table.findAll('td')
	             if td.text == 'Syllable Count']
	if len(td_matches) != 1:
	 raise Exception('Wrong number of <td>Syllable Count</td>')
	td_match = td_matches[0]

	td_value = td_match.findNextSibling('td')
	syllable_count = int(td_value.text)
	return syllable_count

def main():
	poetrySet = makePoetrySet('poeticWords.txt')
	make_syllables('verbs_parsed', poetrySet)

main()
